"""
Data Curator stage: download one price file per identifier, with its `c_*` columns computed.

**Run order: steps 1 and 2 of 6** (see README.md).  `--report` is step 1 and touches no
network; the plain run is step 2.  Nothing has to have run before it.  Next is
`Universe/universe.ipynb`, which profiles what this wrote.

Block 1 of 3 in the Data stage, and the only thing in this repository that talks to a data
provider.

    Data/curator.py                     this file -- the download driver
    Data/Curator/custom_calculations.py the `c_*` columns, computed during the pull
    Data/Curator/Time_Series/           one CSV per identifier: universe, cash proxy, benchmarks
    Data/Curator/Benchmarks/            NOT written here -- the drop zone for index files no
                                        provider serves, which attribution reads
    Data/Curator/Factors/               NOT written here -- the same, for factor-model files

Nothing under `Data/` is committed.  Every file there is downloaded here, derived by
`Data/refinery.py`, or dropped in by hand, so a fresh clone starts empty and rebuilds.

The cash proxy and the benchmarks land in `Time_Series/` alongside the universe, and they have
to: the backtest engine resolves every ticker it prices -- holdings and benchmarks alike --
against one market-data directory, so a benchmark filed anywhere else is a benchmark the engine
cannot price.  Nothing leaks into the cross-section as a result, because `Data/refinery.py` takes
its membership from `Universe/Investable_Universe.csv` and those three are not in it.

Run it directly:

    uv run python Data/curator.py --report    # no network at all; say what is on disk
    uv run python Data/curator.py             # download whatever is missing or stale
    uv run python Data/curator.py --mode smoke   # three tickers, for a first run
    uv run python Data/curator.py --force        # refetch everything

The run is **resumable**.  One provider call per identifier means an interrupted run picks up
where it stopped, and one bad ticker costs one ticker rather than the whole batch.  A file already
on disk whose header matches `OUTPUT_COLUMNS` is skipped.
"""

__all__ = [
    "build_configuration",
    "build_market_data_provider",
    "build_output_handlers",
    "download_identifier",
    "download_identifiers",
    "load_custom_calculation_modules",
    "main",
    "read_identifiers",
    "report_on_disk",
    "report_supplied_files",
]

import argparse
import collections
import concurrent.futures
import csv
import dataclasses
import datetime
import http.client
import importlib.util
import logging
import os
import pathlib
import sys
import threading
import time
import types

import dotenv

import kaxanuk.data_curator
import kaxanuk.data_curator.data_providers
import kaxanuk.data_curator.entities
import kaxanuk.data_curator.output_handlers

# --- Paths -----------------------------------------------------------------------------------
REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent
CUSTOM_CALCULATIONS_PATH = REPOSITORY_ROOT / "Data" / "Curator" / "custom_calculations.py"
ENVIRONMENT_PATH = REPOSITORY_ROOT / "Config" / ".env"
INVESTABLE_UNIVERSE_PATH = REPOSITORY_ROOT / "Universe" / "Investable_Universe.csv"
SUPPLIED_BENCHMARK_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Benchmarks"
SUPPLIED_FACTOR_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Factors"
TIME_SERIES_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Time_Series"

# --- Provider and window ---------------------------------------------------------------------
# The window starts before the earliest asset's inception on purpose: the panel is then ragged at
# the left edge, which is what a real universe looks like, and `Universe/universe.ipynb` measures
# exactly how ragged.  The end date is fixed rather than "today" so two people running this a week
# apart still get comparable files.
END_DATE = datetime.date(2026, 9, 1)
FUNDAMENTAL_DATA_PROVIDER = None  # None skips fundamentals; a price-driven strategy needs none.
MARKET_DATA_PROVIDER = "financial_modeling_prep"
PERIOD = "quarterly"  # Only consulted when fundamentals are enabled.
START_DATE = datetime.date(2010, 1, 1)

# --- Identifiers -----------------------------------------------------------------------------
# The investable universe comes from `Universe/Investable_Universe.csv`.  Two other groups ride
# along with every mode, because the engine has to be able to price them:
#
#   - the cash proxy, because the engine's weight file has no cash row, so "go to cash" has to be
#     expressible as a holding in a real, priced, transaction-costed instrument;
#   - the benchmarks, because they are what the strategy is reported against.
#
# To change what a result is measured against, edit `BENCHMARK_IDENTIFIERS` here *and*
# `BENCHMARK_TICKERS` in `Experiments/backtest_engine.py`.  Keeping those apart is deliberate:
# this file
# decides what is *fetched*, that one decides what is *reported against*, and a benchmark can be
# downloaded for reference without being promoted to a headline comparison.
BENCHMARK_IDENTIFIERS = (
    "AOR",  # iShares Core 60/40 Balanced Allocation
    "SPY",  # S&P 500, for the "why not just hold equities?" comparison
)
CASH_TICKER = "BIL"
SMOKE_TICKERS: tuple[str, ...] = (
    # --- example: begin ---
    "IVV",
    "AGG",
    "GLD",
    # --- example: end ---
)

# --- Output columns --------------------------------------------------------------------------
# All three adjustment families are carried in full.  An unused column costs bytes on disk; a
# missing one costs a refetch of every identifier.
BASE_COLUMNS = (
    "m_date",
    "m_open",
    "m_high",
    "m_low",
    "m_close",
    "m_vwap",
    "m_volume",
    "m_open_split_adjusted",
    "m_high_split_adjusted",
    "m_low_split_adjusted",
    "m_close_split_adjusted",
    "m_vwap_split_adjusted",
    "m_volume_split_adjusted",
    "m_open_dividend_and_split_adjusted",
    "m_high_dividend_and_split_adjusted",
    "m_low_dividend_and_split_adjusted",
    "m_close_dividend_and_split_adjusted",
    "m_vwap_dividend_and_split_adjusted",
    "m_volume_dividend_and_split_adjusted",
)
# Every name here is a function in `Data/Curator/custom_calculations.py`.
CUSTOM_COLUMNS = (
    "c_return_1d",
    # --- example: begin ---
    "c_return_ewm_hl5",
    "c_return_ewm_hl10",
    "c_return_ewm_hl21",
    "c_downside_deviation_log_hl5",
    "c_downside_deviation_log_hl21",
    "c_sortino_hl5",
    "c_sortino_hl10",
    "c_sortino_hl21",
    # --- example: end ---
    "c_daily_traded_value_1d",
    "c_daily_traded_value_63d",
    "c_split_ratio",
    "c_vwap",
    "c_dividend_split_ratio",
    "c_vwap_dividend_and_split_adjusted",
)
OUTPUT_COLUMNS = BASE_COLUMNS + CUSTOM_COLUMNS

# --- Run behaviour ---------------------------------------------------------------------------
# Everything attribution needs and no provider serves.  Reported so a clone learns what is missing
# from the first command it runs, rather than from a notebook failing three stages later.
FACTOR_FILE_PATTERN = "f_*.csv"
LOGGER_LEVEL = logging.WARNING
MAX_ATTEMPTS = 3
OUTPUT_FORMATS = ("csv",)  # Any non-empty subset of ("csv", "parquet"); csv is required.
RETRY_BACKOFF_SECONDS = 2
SPARE_CORES = 2  # Left free so the machine stays usable during a full run.
TRANSIENT_ERRORS = (
    http.client.HTTPException,
    OSError,
)

_OUTPUT_HANDLERS_BY_FORMAT = {
    "csv": kaxanuk.data_curator.output_handlers.CsvOutput,
    "parquet": kaxanuk.data_curator.output_handlers.ParquetOutput,
}
_PRINT_LOCK = threading.Lock()
# Providers hold per-instance connection state, so each worker thread gets its own set rather than
# sharing one.  A transient error replaces them, because a dropped connection is exactly what
# leaves that state dirty.
_THREAD_STATE = threading.local()


@dataclasses.dataclass
class OnDiskReport:
    """Which identifiers are already usable in an output directory, and which are not."""

    pending: tuple[str, ...]
    ready: tuple[str, ...]


def build_configuration(
    identifier: str,
) -> "kaxanuk.data_curator.entities.Configuration":
    """Assemble the Configuration entity one download is driven by."""

    return kaxanuk.data_curator.entities.Configuration(
        start_date=START_DATE,
        end_date=END_DATE,
        period=PERIOD,
        identifiers=(identifier,),
        columns=OUTPUT_COLUMNS,
    )


def build_market_data_provider() -> "kaxanuk.data_curator.data_providers.DataProviderInterface":
    """A fresh market-data provider instance."""

    return kaxanuk.data_curator.data_providers.FinancialModelingPrep(
        api_key=_read_api_key(),
    )


def build_output_handlers(
    output_directory: pathlib.Path,
) -> list["kaxanuk.data_curator.output_handlers.OutputHandlerInterface"]:
    """One handler per entry in OUTPUT_FORMATS, all writing into `output_directory`."""

    return [
        _OUTPUT_HANDLERS_BY_FORMAT[output_format](output_base_dir=str(output_directory))
        for output_format in OUTPUT_FORMATS
    ]


def download_identifier(
    identifier: str,
    output_directory: pathlib.Path,
    custom_calculation_modules: list[types.ModuleType],
    force_redownload: bool,
) -> str:
    """
    Download one identifier and return its outcome: skipped, processed, or a failure reason.

    Never raises.  One bad ticker has to cost one ticker, not the batch, so every exception is
    turned into a reason string the caller reports and moves past.
    """
    output_path = output_directory / f"{identifier}.csv"
    if _stale_reason(output_path, force_redownload) is None:

        return "skipped"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            kaxanuk.data_curator.main(
                configuration=build_configuration(identifier),
                market_data_provider=_thread_market_data_provider(),
                fundamental_data_provider=_thread_fundamental_data_provider(),
                output_handlers=_thread_output_handlers(output_directory),
                custom_calculation_modules=custom_calculation_modules,
                logger_level=LOGGER_LEVEL,
            )
            if output_path.is_file():

                return "processed"

            return "failed: no output produced (unknown identifier, or no data in the window)"

        except TRANSIENT_ERRORS as error:
            if attempt >= MAX_ATTEMPTS:

                return f"failed: {type(error).__name__}: {error} (after {attempt} attempts)"

            time.sleep(RETRY_BACKOFF_SECONDS * attempt)
            _reset_thread_providers()
        except Exception as error:  # noqa: BLE001 - one bad ticker must not stop the batch.

            return f"failed: {type(error).__name__}: {error}"

    return "failed: retries exhausted"


def download_identifiers(
    identifiers: tuple[str, ...],
    output_directory: pathlib.Path,
    custom_calculation_modules: list[types.ModuleType],
    label: str,
    force_redownload: bool = False,
    max_threads: int | None = None,
) -> collections.Counter:
    """
    Download every identifier into `output_directory`, in parallel, and tally the outcomes.

    Downloads are network-bound, so threads rather than processes are the right tool.  Work is
    handed out one identifier at a time instead of in fixed blocks, so a slow ticker delays only
    itself.
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    worker_count = _thread_count(len(identifiers), max_threads)
    print(
        f"--- {label}: {len(identifiers)} identifier(s)"
        f" -> {output_directory.name}/ on {worker_count} thread(s) ---"
    )

    started_at = time.monotonic()
    outcomes = collections.Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(
                download_identifier,
                identifier,
                output_directory,
                custom_calculation_modules,
                force_redownload,
            ): identifier
            for identifier in identifiers
        }
        for future in concurrent.futures.as_completed(futures):
            identifier = futures[future]
            outcome = future.result()
            outcomes[outcome.split(":")[0]] += 1
            _report_progress(identifier, outcome, sum(outcomes.values()), len(identifiers))

    print(
        f"{label} done in {time.monotonic() - started_at:,.0f}s -"
        f" {dict(outcomes)}"
    )

    return outcomes


def load_custom_calculation_modules() -> list[types.ModuleType]:
    """
    Import `Data/Curator/custom_calculations.py` as a module object.

    Loaded by path rather than by import statement because `Data/` is a plain directory rather
    than a package, and the Curator wants a module object either way.
    """
    specification = importlib.util.spec_from_file_location(
        "curator_calculations",
        CUSTOM_CALCULATIONS_PATH,
    )
    if specification is None or specification.loader is None:
        msg = f"could not load custom calculations from {CUSTOM_CALCULATIONS_PATH}"

        raise ImportError(msg)

    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return [module]


def main() -> int:
    """Parse the command line, then download or report.  Returns a process exit code."""
    parser = argparse.ArgumentParser(
        description="Download the universe's market data via the KaxaNuk Data Curator.",
    )
    parser.add_argument(
        "--mode",
        choices=(
            "full",
            "smoke",
        ),
        default="full",
        help="which slice of the universe to download (default: full)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="refetch every identifier, even files that are already up to date",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="make no network calls; report what is already on disk",
    )
    parser.add_argument(
        "--no-benchmarks",
        action="store_true",
        help="skip the benchmark download",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=None,
        help="worker threads (default: one per core, less a couple of spares)",
    )
    arguments = parser.parse_args()

    logging.getLogger().setLevel(LOGGER_LEVEL)
    _validate_output_formats()

    try:
        identifiers = read_identifiers(arguments.mode)
    except (FileNotFoundError, ValueError) as error:
        # The universe is the one input a person has to supply, so getting it wrong is the most
        # likely first failure. A traceback would say the same thing and read like a bug.
        print(f"Cannot read the universe: {error}")

        return 1

    print(f"Repository root : {REPOSITORY_ROOT}")
    print(f"Mode            : {arguments.mode} -> {len(identifiers)} identifier(s)")
    print(f"Output          : {TIME_SERIES_DIRECTORY.relative_to(REPOSITORY_ROOT)}")
    print(f"Window          : {START_DATE} -> {END_DATE}")
    print(f"Columns         : {len(OUTPUT_COLUMNS)} ({len(CUSTOM_COLUMNS)} of them c_*)")
    print()

    if arguments.report:
        report_on_disk(identifiers, TIME_SERIES_DIRECTORY, f"Universe ({arguments.mode})")
        report_on_disk(BENCHMARK_IDENTIFIERS, TIME_SERIES_DIRECTORY, "Benchmarks")
        report_supplied_files()

        return 0

    custom_calculation_modules = load_custom_calculation_modules()
    universe_outcomes = download_identifiers(
        identifiers,
        TIME_SERIES_DIRECTORY,
        custom_calculation_modules,
        f"Universe ({arguments.mode})",
        arguments.force,
        arguments.threads,
    )
    benchmark_outcomes = collections.Counter()
    if not arguments.no_benchmarks:
        print()
        benchmark_outcomes = download_identifiers(
            BENCHMARK_IDENTIFIERS,
            TIME_SERIES_DIRECTORY,
            custom_calculation_modules,
            "Benchmarks",
            arguments.force,
            arguments.threads,
        )

    print()
    report_supplied_files()
    failures = universe_outcomes["failed"] + benchmark_outcomes["failed"]

    return 1 if failures > 0 else 0


def read_identifiers(
    mode: str,
) -> tuple[str, ...]:
    """
    The identifiers to download for `mode`, always including the cash proxy.

    `Investable_Universe.csv` is the authority on what exists, so it -- not the enriched security
    master -- drives the download.  That keeps the Curator runnable before the universe notebook
    has ever been run, which matters because the notebook needs downloaded files to profile.
    """
    selected = SMOKE_TICKERS if mode == "smoke" else _read_universe_tickers()

    return tuple(
        dict.fromkeys(selected + (CASH_TICKER,))
    )


def report_on_disk(
    identifiers: tuple[str, ...],
    output_directory: pathlib.Path,
    label: str,
) -> OnDiskReport:
    """Which of `identifiers` are already usable in `output_directory`.  Makes no network calls."""
    reasons = {
        identifier: _stale_reason(output_directory / f"{identifier}.csv", False)
        for identifier in identifiers
    }
    ready = tuple(
        identifier
        for identifier, reason in reasons.items()
        if reason is None
    )
    pending = tuple(
        identifier
        for identifier, reason in reasons.items()
        if reason is not None
    )

    print(f"{label}: {len(ready)}/{len(identifiers)} ready in {output_directory.name}/")
    if len(pending) > 0:
        print(f"  needs download: {', '.join(pending)}")

    return OnDiskReport(pending=pending, ready=ready)


def report_supplied_files() -> bool:
    """
    Report whether the attribution inputs are present, and say what breaks without them.

    Nothing downloads these: an index's daily holdings and a factor model are not products a price
    provider sells.  Stages 1 to 5 run without them; step 6 does not.  Returns whether any were
    found.
    """
    benchmark_files = _existing_files(SUPPLIED_BENCHMARK_DIRECTORY, "*.csv")
    factor_files = _existing_files(SUPPLIED_FACTOR_DIRECTORY, FACTOR_FILE_PATTERN)

    print(
        f"Attribution inputs: {len(benchmark_files)} file(s) in Benchmarks/,"
        f" {len(factor_files)} in Factors/"
    )
    if len(benchmark_files) == 0 or len(factor_files) == 0:
        print("  -> step 6 reports what is missing and skips; steps 1-5 are unaffected")

    return len(benchmark_files) > 0 and len(factor_files) > 0


def _existing_files(
    directory: pathlib.Path,
    pattern: str,
) -> list[pathlib.Path]:
    """Files matching `pattern` in `directory`, or an empty list when the directory is absent."""
    if not directory.is_dir():

        return []

    return sorted(directory.glob(pattern))


def _read_api_key() -> str:
    """The market-data provider's API key, loaded from the gitignored Config/.env."""
    dotenv.load_dotenv(ENVIRONMENT_PATH)
    api_key = os.getenv("KNDC_API_KEY_FMP")
    if not api_key:
        msg = f"KNDC_API_KEY_FMP not found; expected it in {ENVIRONMENT_PATH}"

        raise RuntimeError(msg)

    return api_key


def _read_universe_tickers() -> tuple[str, ...]:
    """Every ticker in the investable universe, in file order."""
    if not INVESTABLE_UNIVERSE_PATH.is_file():
        msg = " ".join(
            (
                f"{INVESTABLE_UNIVERSE_PATH} is missing, so there is nothing to download.",
                "It is committed with the repository; restore it from version control, or point",
                "INVESTABLE_UNIVERSE_PATH at whichever seed you want to download.",
            )
        )

        raise FileNotFoundError(msg)

    with INVESTABLE_UNIVERSE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        tickers = [
            row["ticker"].strip()
            for row in csv.DictReader(handle)
            if row.get("ticker", "").strip()
        ]

    if len(tickers) == 0:
        msg = " ".join(
            (
                f"{INVESTABLE_UNIVERSE_PATH.name} has a header but no rows, so there is nothing to",
                "download.  Add one line per security you want -- `ticker` and `name` are the only",
                "required columns, and every other column in that file is yours to choose.",
            )
        )

        raise ValueError(msg)

    return tuple(dict.fromkeys(tickers))


def _report_progress(
    identifier: str,
    outcome: str,
    done: int,
    total: int,
) -> None:
    """
    One line per identifier, printed under a lock so worker output cannot interleave.

    A dozen identifiers is small enough to name every one; that is more useful than a percentage,
    because the interesting case is always "which ticker was it".
    """
    marker = "FAILED " if outcome.startswith("failed") else ""
    with _PRINT_LOCK:
        print(f"  [{done:>3}/{total}] {marker}{identifier}: {outcome}")


def _reset_thread_providers() -> None:
    """Discard this thread's providers so the next attempt builds clean connection state."""
    _THREAD_STATE.market_data_provider = None
    _THREAD_STATE.fundamental_data_provider = None


def _stale_reason(
    output_path: pathlib.Path,
    force_redownload: bool,
) -> str | None:
    """
    Why `output_path` needs downloading again, or None when it is usable as it stands.

    Checking the header rather than only the file's existence is what stops a change to
    `OUTPUT_COLUMNS` leaving a directory of mixed-schema files behind.
    """
    if force_redownload:

        return "forced"

    if not output_path.is_file():

        return "missing"

    with output_path.open(encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle), [])
    if tuple(header) != OUTPUT_COLUMNS:

        return f"schema mismatch ({len(header)} columns on disk vs {len(OUTPUT_COLUMNS)} expected)"

    return None


def _thread_count(
    work_item_count: int,
    max_threads: int | None,
) -> int:
    """How many workers to run, honouring an explicit override."""
    if max_threads is not None:

        return max(1, min(max_threads, work_item_count))

    available_cores = (os.cpu_count() or 1) - SPARE_CORES

    return max(1, min(work_item_count, available_cores))


def _thread_fundamental_data_provider() -> (
    "kaxanuk.data_curator.data_providers.DataProviderInterface | None"
):
    """This thread's fundamental-data provider, or None while fundamentals are disabled."""
    if FUNDAMENTAL_DATA_PROVIDER is None:

        return None

    if getattr(_THREAD_STATE, "fundamental_data_provider", None) is None:
        _THREAD_STATE.fundamental_data_provider = build_market_data_provider()

    return _THREAD_STATE.fundamental_data_provider


def _thread_market_data_provider() -> (
    "kaxanuk.data_curator.data_providers.DataProviderInterface"
):
    """This thread's market-data provider, built on first use and reused afterwards."""
    if getattr(_THREAD_STATE, "market_data_provider", None) is None:
        _THREAD_STATE.market_data_provider = build_market_data_provider()

    return _THREAD_STATE.market_data_provider


def _thread_output_handlers(
    output_directory: pathlib.Path,
) -> list["kaxanuk.data_curator.output_handlers.OutputHandlerInterface"]:
    """This thread's output handlers, so no two threads ever share a writer."""
    if getattr(_THREAD_STATE, "output_handlers", None) is None:
        _THREAD_STATE.output_handlers = build_output_handlers(output_directory)

    return _THREAD_STATE.output_handlers


def _validate_output_formats() -> None:
    """Fail early on an OUTPUT_FORMATS value the rest of the module cannot honour."""
    if len(OUTPUT_FORMATS) == 0 or not set(OUTPUT_FORMATS) <= set(_OUTPUT_HANDLERS_BY_FORMAT):
        msg = f"OUTPUT_FORMATS must be a non-empty subset of {tuple(_OUTPUT_HANDLERS_BY_FORMAT)}"

        raise ValueError(msg)

    # The staleness check reads the CSV header, so CSV has to be one of the formats.
    if "csv" not in OUTPUT_FORMATS:
        msg = "keep 'csv' in OUTPUT_FORMATS: the resume and staleness check depends on it"

        raise ValueError(msg)


if __name__ == "__main__":
    sys.exit(main())
