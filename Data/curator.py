"""
Data Curator stage: download market data for the universe and the benchmarks.

Block 1 of 3 in the Data stage.  This module owns everything that touches a data provider:

    Data/curator.py            -- this file, the download driver
    Data/Curator/
        custom_calculations.py -- the `c_*` functions the curator computes during the pull
        Time_Series/           -- one file per identifier: the universe, the cash proxy, and the
                                  tradable benchmarks
        Benchmarks/            -- NOT written here.  The drop zone for index data no provider
                                  serves (the KaxaNuk KN600 family), supplied by hand today and
                                  downloaded by this script once that fabric exists
        Factors/               -- NOT written here.  The same, for the factor-model files the
                                  attribution stage reads

Nothing under `Data/` is committed to version control except code: every file is downloaded
here, derived by `Data/refinery.py`, or dropped in by the user.  A fresh clone therefore starts
empty and rebuilds.

The tradable benchmarks land in `Time_Series/` alongside the universe rather than in a directory
of their own.  They have to: the backtest engine resolves every ticker -- holdings and benchmarks
alike -- against one market-data directory, so a benchmark filed anywhere else is a benchmark the
engine cannot price.  Keeping them apart would be tidier on disk and broken in use.  Nothing
leaks into the cross-section as a result, because `Data/refinery.py` excludes them by name.

Run it directly:

    uv run python Data/curator.py                 # download whatever is missing or stale
    uv run python Data/curator.py --mode smoke    # a handful of liquid names
    uv run python Data/curator.py --report        # no network at all; report what is on disk
    uv run python Data/curator.py --force         # refetch everything

The run is **resumable**: one `main()` call per identifier means an interrupted run picks up
where it stopped, and a single bad ticker costs one ticker rather than the whole batch.  Files
already on disk with the expected header are skipped.
"""

__all__ = [
    "build_configuration",
    "build_fundamental_data_provider",
    "build_market_data_provider",
    "build_output_handlers",
    "download_identifiers",
    "load_custom_calculation_modules",
    "main",
    "read_identifiers",
    "report_on_disk",
    "report_supplied_files",
    "stage_supplied_price_series",
]

import argparse
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
import numpy
import pandas

import kaxanuk.data_curator
import kaxanuk.data_curator.data_providers
import kaxanuk.data_curator.entities
import kaxanuk.data_curator.output_handlers

# --- Paths ---------------------------------------------------------------------------------
REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent
# Where the user drops the index and factor files no provider serves.  This script never writes
# to either; it only reports on what it finds, so a missing file is visible before a notebook
# fails on it.
SUPPLIED_BENCHMARK_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Benchmarks"
SUPPLIED_FACTOR_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Factors"
CUSTOM_CALCULATIONS_PATH = REPOSITORY_ROOT / "Data" / "Curator" / "custom_calculations.py"
ENVIRONMENT_PATH = REPOSITORY_ROOT / "Config" / ".env"
RAW_UNIVERSE_PATH = REPOSITORY_ROOT / "Universe" / "Investable_Universe.csv"
SECURITY_MASTER_PATH = REPOSITORY_ROOT / "Universe" / "Security_Master.csv"
TIME_SERIES_OUTPUT_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Time_Series"

# --- Providers and window ------------------------------------------------------------------
END_DATE = datetime.date(2026, 7, 1)
FUNDAMENTAL_DATA_PROVIDER = None  # None skips fundamentals entirely; this strategy needs none.
MARKET_DATA_PROVIDER = "financial_modeling_prep"
PERIOD = "quarterly"  # Only consulted when fundamentals are enabled.
START_DATE = datetime.date(2015, 1, 1)

# --- Identifiers ---------------------------------------------------------------------------
# Three things ride along with every mode, all for the same reason: the backtest engine resolves
# every ticker it is given against one market-data directory, so anything it has to price needs a
# file there.
#
#   - the cash proxy, because the engine's weight file has no cash row, so "go to cash" has to be
#     expressible as a holding in a real, priced, transaction-costed instrument;
#   - the tradable benchmarks, because they are what the strategy is measured against.
#
# KN600, the KaxaNuk US equity index, is deliberately absent from the downloads: no provider
# serves it, so it is supplied by hand into Benchmarks/.  See `report_supplied_files`.
#
# To swap in a different benchmark, edit the constants below and the matching ones in
# `Experiments/engine.py`, which decides what results are *reported* against.  This file decides
# what gets *fetched*; keeping the two apart is why a benchmark can be downloaded for the panel
# without being promoted to a headline comparison.
BENCHMARK_IDENTIFIERS = (
    "SPY",
    "QQQ",
)
CASH_TICKER = "BIL"
FACTOR_FILE_PATTERN = "f_*.csv"
# Price series that have to reach the market-data directory, because the engine prices every
# ticker it is given from there and a benchmark it cannot price is a benchmark it silently drops.
SUPPLIED_PRICE_SERIES = ("KN600.csv",)
# Everything a fresh clone must be handed by a person: the supplied price series plus the two
# tables the attribution stage reads.  Named so a clone is told what is missing rather than
# discovering it three notebooks later.
SUPPLIED_BENCHMARK_FILES = SUPPLIED_PRICE_SERIES + (
    "index_daily_holdings_2017.csv",
    "kn600_returns.csv",
)
# Columns the engine asks for by name, each paired with the `m_*` twin to fall back on.  An index
# level series carries no reconstructed VWAP -- our ticker files only have one because the
# custom calculations rebuild it from the provider's nulls -- but for an already-adjusted level
# the twin *is* the same series, and a benchmark is never traded, so the column only has to
# satisfy the loader.
ENGINE_COLUMN_FALLBACKS = {
    "c_vwap": "m_vwap",
    "c_vwap_dividend_and_split_adjusted": "m_vwap_dividend_and_split_adjusted",
}
SMOKE_TICKERS = (
    "AAPL",
    "MSFT",
    "JPM",
    "XOM",
    "JNJ",
    "PG",
    "NEE",
    "AMT",
)

# --- Output columns ------------------------------------------------------------------------
# Market data only.  All three adjustment families are carried in full (OHLC + vwap + volume):
# the cost of an unused column is bytes on disk, while the cost of a missing one is a full
# refetch of every identifier.  Widening this tuple changes the header, so the staleness check
# below refetches everything on the next run -- intended, because the directory can then never
# end up holding a mix of schemas.
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
CUSTOM_COLUMNS = (
    "c_daily_traded_value_1d",
    "c_daily_traded_value_63d",
    "c_split_ratio",
    "c_vwap",
    "c_dividend_split_ratio",
    "c_vwap_dividend_and_split_adjusted",
)
OUTPUT_COLUMNS = BASE_COLUMNS + CUSTOM_COLUMNS

# --- Run behaviour -------------------------------------------------------------------------
LOGGER_LEVEL = logging.WARNING
MAX_ATTEMPTS = 3
OUTPUT_FORMATS = ("csv",)  # Any non-empty subset of ("csv", "parquet"); csv is required.
PROGRESS_EVERY = 25
RETRY_BACKOFF_SECONDS = 2
SPARE_CORES = 2  # Left free so the machine stays responsive during a full run.
TRANSIENT_ERRORS = (
    http.client.HTTPException,
    OSError,
)

_OUTPUT_HANDLERS_BY_FORMAT = {
    "csv": kaxanuk.data_curator.output_handlers.CsvOutput,
    "parquet": kaxanuk.data_curator.output_handlers.ParquetOutput,
}
_PRINT_LOCK = threading.Lock()


@dataclasses.dataclass
class DownloadState:
    """Running tally of one `download_identifiers` call, shared across its worker threads."""

    total: int
    failed: int = 0
    processed: int = 0
    skipped: int = 0
    failures: dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class OnDiskReport:
    """Which identifiers are already usable in an output directory, and which are not."""

    pending: tuple[str, ...]
    ready: tuple[str, ...]


def build_configuration(
    identifiers: tuple[str, ...],
) -> "kaxanuk.data_curator.entities.Configuration":
    """Assemble the Configuration entity the curator is driven by."""

    return kaxanuk.data_curator.entities.Configuration(
        start_date=START_DATE,
        end_date=END_DATE,
        period=PERIOD,
        identifiers=identifiers,
        columns=OUTPUT_COLUMNS,
    )


def build_fundamental_data_provider() -> (
    "kaxanuk.data_curator.data_providers.DataProviderInterface | None"
):
    """Fresh fundamental-data provider, or None while fundamentals are disabled."""
    if FUNDAMENTAL_DATA_PROVIDER is None:

        return None

    return kaxanuk.data_curator.data_providers.FinancialModelingPrep(
        api_key=_read_api_key(),
    )


def build_market_data_provider() -> "kaxanuk.data_curator.data_providers.DataProviderInterface":
    """
    Fresh market-data provider instance.

    Providers keep per-instance state after `initialize()`, so every worker thread builds its own
    rather than sharing one.
    """

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


def download_identifiers(
    identifiers: tuple[str, ...],
    output_directory: pathlib.Path,
    custom_calculation_modules: list[types.ModuleType],
    label: str,
    force_redownload: bool = False,
    max_threads: int | None = None,
) -> DownloadState:
    """
    Resumable, multithreaded per-identifier download into `output_directory`.

    Downloads are network-bound, so threads rather than processes are the right tool.  Identifiers
    are split into one contiguous chunk per worker and each worker builds its own providers and
    output handlers, so no two threads share a writer or a connection.
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    state = DownloadState(total=len(identifiers))
    worker_count = _thread_count(len(identifiers), max_threads)
    print(
        " ".join(
            (
                f"--- {label}: {len(identifiers)} identifier(s) ->",
                f"{output_directory.name}/ on {worker_count} thread(s) ---",
            )
        )
    )

    started_at = time.monotonic()
    chunks = _chunk_identifiers(identifiers, worker_count)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunks)) as executor:
        futures = [
            executor.submit(
                _download_chunk,
                chunk,
                output_directory,
                custom_calculation_modules,
                state,
                force_redownload,
            )
            for chunk in chunks
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Re-raise anything a worker could not handle itself.
    elapsed_seconds = time.monotonic() - started_at

    print(
        " ".join(
            (
                f"{label} done in {elapsed_seconds:,.0f}s -",
                f"processed={state.processed} skipped={state.skipped} failed={state.failed}",
            )
        )
    )
    for identifier, detail in sorted(state.failures.items()):
        print(f"  {identifier}: {detail}")

    return state


def load_custom_calculation_modules() -> list[types.ModuleType]:
    """
    Import `Data/Curator/custom_calculations.py` as a module object.

    It is loaded by path rather than by import statement because `Data/` is a plain directory
    rather than a package, and the curator wants a module object either way.
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
            "sector_sample",
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
    parser.add_argument(
        "--sector-sample-size",
        type=int,
        default=3,
        help="industries sampled per sector when --mode sector_sample (default: 3)",
    )
    arguments = parser.parse_args()

    logging.getLogger().setLevel(LOGGER_LEVEL)
    _validate_output_formats()

    identifiers = read_identifiers(arguments.mode, arguments.sector_sample_size)
    print(f"Repository root : {REPOSITORY_ROOT}")
    print(f"Mode            : {arguments.mode} -> {len(identifiers)} identifier(s)")
    print(f"Output          : {TIME_SERIES_OUTPUT_DIRECTORY.relative_to(REPOSITORY_ROOT)}")
    print(f"Window          : {START_DATE} -> {END_DATE}")
    print(f"Columns         : {len(OUTPUT_COLUMNS)}")

    if arguments.report:
        print()
        report_on_disk(identifiers, TIME_SERIES_OUTPUT_DIRECTORY, f"Universe ({arguments.mode})")
        report_on_disk(BENCHMARK_IDENTIFIERS, TIME_SERIES_OUTPUT_DIRECTORY, "Benchmarks")
        staged = stage_supplied_price_series()
        print(f"Staged index price series: {staged} into {TIME_SERIES_OUTPUT_DIRECTORY.name}/")
        report_supplied_files()

        return 0

    custom_calculation_modules = load_custom_calculation_modules()
    print(f"Custom calcs    : {CUSTOM_CALCULATIONS_PATH.name}")
    print()

    universe_state = download_identifiers(
        identifiers,
        TIME_SERIES_OUTPUT_DIRECTORY,
        custom_calculation_modules,
        f"Universe ({arguments.mode})",
        arguments.force,
        arguments.threads,
    )
    benchmark_state = DownloadState(total=0)
    if not arguments.no_benchmarks:
        print()
        benchmark_state = download_identifiers(
            BENCHMARK_IDENTIFIERS,
            TIME_SERIES_OUTPUT_DIRECTORY,
            custom_calculation_modules,
            "Benchmarks",
            arguments.force,
            arguments.threads,
        )

    print()
    staged = stage_supplied_price_series()
    print(f"Staged index price series: {staged} into {TIME_SERIES_OUTPUT_DIRECTORY.name}/")
    report_supplied_files()

    return 1 if (universe_state.failed + benchmark_state.failed) > 0 else 0


def read_identifiers(
    mode: str,
    sector_sample_size: int = 3,
) -> tuple[str, ...]:
    """
    The identifiers to download for `mode`, always including the cash proxy.

    `Investable_Universe.csv` is the authority on *what exists*, so it -- not the enriched
    security master -- drives the download.  That keeps the curator runnable before the universe
    notebook has ever been run.  Only `sector_sample` needs classification data, and it says so
    if the master is missing.
    """
    if mode == "smoke":
        selected = SMOKE_TICKERS
    elif mode == "sector_sample":
        selected = _read_sector_sample(sector_sample_size)
    else:
        selected = _read_universe_tickers()

    return tuple(
        dict.fromkeys(
            selected + (CASH_TICKER,)
        )
    )


def stage_supplied_price_series() -> int:
    """
    Copy hand-supplied index price series into the market-data directory, and report how many.

    The engine resolves every ticker it prices -- holdings and benchmarks alike -- against one
    directory.  These files arrive in `Benchmarks/` because a person put them there, so without
    this step `KN600` is a benchmark the engine cannot find, and the run quietly measures against
    SPY and QQQ alone.  Copying is cheap and idempotent, so it happens on every run rather than
    being something to remember.

    Columns the engine asks for but an index level series does not carry are filled from their
    `m_*` twins on the way across.  Returns the number of files staged.
    """
    staged = 0
    for file_name in SUPPLIED_PRICE_SERIES:
        source = SUPPLIED_BENCHMARK_DIRECTORY / file_name
        destination = TIME_SERIES_OUTPUT_DIRECTORY / file_name
        if not source.is_file():

            continue

        if (
            destination.is_file()
            and destination.stat().st_mtime >= source.stat().st_mtime
        ):
            staged += 1

            continue

        frame = pandas.read_csv(source)
        for engine_column, fallback_column in ENGINE_COLUMN_FALLBACKS.items():
            if engine_column in frame.columns and frame[engine_column].notna().any():

                continue

            if fallback_column not in frame.columns or not frame[fallback_column].notna().any():
                msg = " ".join(
                    (
                        f"{file_name} carries neither {engine_column} nor a usable",
                        f"{fallback_column} to derive it from; the engine cannot price it",
                    )
                )

                raise ValueError(msg)

            frame[engine_column] = frame[fallback_column]

        TIME_SERIES_OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        frame.to_csv(destination, index=False)
        staged += 1

    return staged


def report_supplied_files() -> bool:
    """
    Report which hand-supplied inputs are present, and say what breaks without them.

    These are the files no data provider serves: the KaxaNuk index family and the factor models.
    Reporting them here means a fresh clone learns what is missing from the first command it runs,
    rather than from a notebook failing three stages later.  Returns whether everything is present.
    """
    missing_benchmarks = [
        name
        for name in SUPPLIED_BENCHMARK_FILES
        if not (SUPPLIED_BENCHMARK_DIRECTORY / name).is_file()
    ]
    factor_files = (
        sorted(SUPPLIED_FACTOR_DIRECTORY.glob(FACTOR_FILE_PATTERN))
        if SUPPLIED_FACTOR_DIRECTORY.is_dir()
        else []
    )

    print(
        " ".join(
            (
                "Supplied index files:",
                f"{len(SUPPLIED_BENCHMARK_FILES) - len(missing_benchmarks)}",
                f"/ {len(SUPPLIED_BENCHMARK_FILES)} in",
                f"{SUPPLIED_BENCHMARK_DIRECTORY.name}/",
            )
        )
    )
    if len(missing_benchmarks) > 0:
        print(f"  missing: {', '.join(missing_benchmarks)}")
        print("  -> the backtest runs against SPY and QQQ only; attribution cannot run at all")

    print(f"Supplied factor files: {len(factor_files)} in {SUPPLIED_FACTOR_DIRECTORY.name}/")
    if len(factor_files) == 0:
        print("  -> attribution cannot run; see README.md for what to drop in here")

    return len(missing_benchmarks) == 0 and len(factor_files) > 0


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
        listed = ", ".join(pending[:15])
        suffix = " ..." if len(pending) > 15 else ""
        print(f"  needs download: {listed}{suffix}")

    return OnDiskReport(pending=pending, ready=ready)


def _chunk_identifiers(
    identifiers: tuple[str, ...],
    chunk_count: int,
) -> list[tuple[str, ...]]:
    """Split `identifiers` into `chunk_count` roughly equal contiguous tuples."""
    # dtype=object keeps the identifiers plain `str`, so they still format into a file path.
    parts = numpy.array_split(
        numpy.asarray(identifiers, dtype=object),
        chunk_count,
    )

    return [
        tuple(part)
        for part in parts
        if len(part) > 0
    ]


def _download_chunk(
    identifiers: tuple[str, ...],
    output_directory: pathlib.Path,
    custom_calculation_modules: list[types.ModuleType],
    state: DownloadState,
    force_redownload: bool,
) -> None:
    """
    Download every identifier in `identifiers` through one set of providers.

    Providers are built once per chunk rather than once per identifier to keep the per-instance
    setup off the hot path.  A transient error swaps in fresh ones, because a dropped connection
    is exactly what leaves the provider's connection state dirty.
    """
    market_data_provider = build_market_data_provider()
    fundamental_data_provider = build_fundamental_data_provider()
    output_handlers = build_output_handlers(output_directory)

    for identifier in identifiers:
        output_path = output_directory / f"{identifier}.csv"
        reason = _stale_reason(output_path, force_redownload)
        if reason is None:
            _record_outcome(state, identifier, "skipped")

            continue

        configuration = build_configuration((identifier,))
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                kaxanuk.data_curator.main(
                    configuration=configuration,
                    market_data_provider=market_data_provider,
                    fundamental_data_provider=fundamental_data_provider,
                    output_handlers=output_handlers,
                    custom_calculation_modules=custom_calculation_modules,
                    logger_level=LOGGER_LEVEL,
                )
                if output_path.is_file():
                    _record_outcome(state, identifier, "processed")
                else:
                    _record_outcome(
                        state,
                        identifier,
                        "failed",
                        "no output produced (identifier error / no data)",
                    )

                break
            except TRANSIENT_ERRORS as error:
                if attempt >= MAX_ATTEMPTS:
                    _record_outcome(
                        state,
                        identifier,
                        "failed",
                        f"{type(error).__name__}: {error} (after {attempt} attempts)",
                    )
                else:
                    time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                    market_data_provider = build_market_data_provider()
                    fundamental_data_provider = build_fundamental_data_provider()
            except Exception as error:  # noqa: BLE001 - one bad ticker must not stop the batch.
                _record_outcome(
                    state,
                    identifier,
                    "failed",
                    f"{type(error).__name__}: {error}",
                )

                break


def _read_api_key() -> str:
    """The market-data provider's API key, loaded from the gitignored Config/.env."""
    dotenv.load_dotenv(ENVIRONMENT_PATH)
    api_key = os.getenv("KNDC_API_KEY_FMP")
    if not api_key:
        msg = f"KNDC_API_KEY_FMP not found; expected it in {ENVIRONMENT_PATH}"

        raise RuntimeError(msg)

    return api_key


def _read_sector_sample(
    sector_sample_size: int,
) -> tuple[str, ...]:
    """
    One ticker from each of the largest `sector_sample_size` industries in every sector.

    Spreading across industries, rather than taking the first few tickers of a sector, keeps the
    sample from being all banks or all REITs.  Selection is alphabetical within an industry, so
    the sample is identical on every run.
    """
    if not SECURITY_MASTER_PATH.is_file():
        msg = " ".join(
            (
                f"--mode sector_sample needs {SECURITY_MASTER_PATH.name}, which does not exist.",
                "Run Universe/universe.ipynb first: sector and industry are not in",
                "Investable_Universe.csv, they come from the data provider.",
            )
        )

        raise FileNotFoundError(msg)

    with SECURITY_MASTER_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row.get("sector") and row.get("industry")
        ]

    industries_by_sector: dict[str, dict[str, list[str]]] = {}
    for row in rows:
        sector_industries = industries_by_sector.setdefault(row["sector"], {})
        sector_industries.setdefault(row["industry"], []).append(row["ticker"])

    selected = []
    for sector in sorted(industries_by_sector):
        sector_industries = industries_by_sector[sector]
        # Negating the count sorts the largest industries first while keeping the tie-break on
        # the industry name ascending, so the sample is stable across runs.
        ranked_industries = sorted(
            (-len(tickers), industry)
            for industry, tickers in sector_industries.items()
        )
        for negative_count, industry in ranked_industries[:sector_sample_size]:
            selected.append(
                sorted(sector_industries[industry])[0]
            )

    return tuple(selected)


def _read_universe_tickers() -> tuple[str, ...]:
    """Every ticker in the raw investable universe, in file order."""
    with RAW_UNIVERSE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        tickers = [
            row["ticker"].strip()
            for row in csv.DictReader(handle)
            if row.get("ticker", "").strip()
        ]

    return tuple(dict.fromkeys(tickers))


def _record_outcome(
    state: DownloadState,
    identifier: str,
    outcome: str,
    detail: str | None = None,
) -> None:
    """
    Thread-safe tally plus a milestone progress line.  Failures are always reported immediately.

    Printing inside the lock is the point: it is what keeps the workers' lines from interleaving.
    """
    with _PRINT_LOCK:
        setattr(state, outcome, getattr(state, outcome) + 1)
        if detail is not None:
            state.failures[identifier] = detail
        done = state.processed + state.skipped + state.failed

        if outcome == "failed":
            print(f"  [FAILED] {identifier}: {detail}")
        if done % PROGRESS_EVERY == 0 or done == state.total:
            print(
                " ".join(
                    (
                        f"  [{done:>4}/{state.total}] processed={state.processed}",
                        f"skipped={state.skipped} failed={state.failed}",
                    )
                )
            )


def _stale_reason(
    output_path: pathlib.Path,
    force_redownload: bool,
) -> str | None:
    """
    Why `output_path` needs downloading again, or None when it is usable as-is.

    Checking the header rather than just the file's existence is what keeps a change to
    OUTPUT_COLUMNS from silently leaving a directory of mixed-schema files behind.
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


def _validate_output_formats() -> None:
    """Fail early on an OUTPUT_FORMATS value the rest of the module cannot honour."""
    if len(OUTPUT_FORMATS) == 0 or not set(OUTPUT_FORMATS) <= set(_OUTPUT_HANDLERS_BY_FORMAT):
        msg = f"OUTPUT_FORMATS must be a non-empty subset of {tuple(_OUTPUT_HANDLERS_BY_FORMAT)}"

        raise ValueError(msg)

    # The staleness check reads the CSV header, so CSV has to be one of the formats.
    if "csv" not in OUTPUT_FORMATS:
        msg = "keep 'csv' in OUTPUT_FORMATS: the resume/staleness check depends on it"

        raise ValueError(msg)


if __name__ == "__main__":
    sys.exit(main())
