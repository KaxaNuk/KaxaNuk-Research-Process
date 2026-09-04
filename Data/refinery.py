"""
Data Refinery stage: the cross-sectional (N x N) layer over the curated data.

**Run order: step 4 of 6** (see README.md).  After `Universe/universe.ipynb`, because it
joins the security master that notebook writes; before `Data/analyzer.ipynb`, which reads
what this writes.  Run it too early and it says which columns it is dropping and carries
on.

Block 2 of 3 in the Data stage, and the seam the KaxaNuk Data Refinery library will replace: this
module is hand-rolled today.  Keep its contract stable -- read Curator files, resolve `r_*`
functions by parameter name, write Refinery files with the same rows -- so the swap is a one-file
change.

The Curator works one security at a time, so every `c_*` column is a function of that security's
own history.  A rank or a breadth reading compares securities against each other on a date, which
no per-security calculation can express.  This module stacks every Curator file into one panel,
computes the `r_*` columns across it, and writes per-security files back out carrying the original
columns plus the new ones:

    Data/Curator/Time_Series/IVV.csv     m_* + c_*                (per security, time series)
            |
            v   read every security, compute per date across the cross-section
    Data/Refinery/Time_Series/IVV.csv    m_* + c_* + r_* (+ join) (same rows, more columns)

Run it directly:

    uv run python Data/refinery.py                  # refine everything on disk
    uv run python Data/refinery.py --limit 50       # first 50 securities, for a quick pass
    uv run python Data/refinery.py --dry-run        # compute and report, write nothing

`Data/Refinery/custom_calculations.py` owns the calculations; this module owns loading, ordering
and writing.  Functions are resolved by parameter name against the columns already built, the same
convention the Data Curator uses, so a new `r_*` column needs no registration beyond being defined
-- add it to `REFINERY_COLUMNS` there and it lands in the output.

Enrichment that comes from *outside* the panel is attached here rather than in the calculations
module, because it is a join and not a calculation.  Today that means the classification columns
of `Universe/Security_Master.csv`.

    WARNING: a joined column is what a security is classified as **today**.  The provider keeps no
    history, so on a universe whose members get reclassified -- an equity moving between GICS
    sectors, a token changing category -- every period before the move is attributed wrongly, and
    nothing raises an error.  Joined columns are suffixed `_current` so no downstream reader can
    mistake one for a point-in-time value.
"""

__all__ = [
    "attach_security_master",
    "build_curator_panel",
    "load_custom_calculation_functions",
    "main",
    "read_investable_tickers",
    "refine_panel",
    "write_refinery_files",
]

import argparse
import csv
import importlib.util
import inspect
import pathlib
import sys
import time
import types

import pandas

# --- Paths ---------------------------------------------------------------------------------
REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent
CURATOR_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Time_Series"
CUSTOM_CALCULATIONS_PATH = REPOSITORY_ROOT / "Data" / "Refinery" / "custom_calculations.py"
INVESTABLE_UNIVERSE_PATH = REPOSITORY_ROOT / "Universe" / "Investable_Universe.csv"
REFINERY_DIRECTORY = REPOSITORY_ROOT / "Data" / "Refinery" / "Time_Series"
SECURITY_MASTER_PATH = REPOSITORY_ROOT / "Universe" / "Security_Master.csv"

# --- Panel conventions -----------------------------------------------------------------------
DATE_COLUMN = "m_date"
TICKER_COLUMN = "ticker"
UNIVERSE_TICKER_COLUMN = "ticker"

# Columns joined in from the security master, as {master column: panel column}.  Every one is
# suffixed `_current` on purpose -- see the module docstring.  Edit this mapping to carry whatever
# your security master classifies securities by; a column the master does not have is reported and
# skipped rather than joined in as nulls.
SECURITY_MASTER_COLUMNS = {
    "asset_class": "asset_class_current",
    "asset_group": "asset_group_current",
}


def attach_security_master(
    panel: pandas.DataFrame,
) -> pandas.DataFrame:
    """
    Join the security master's classification columns onto the panel, or warn and skip.

    Missing security master is not fatal: everything computed from the panel itself still works,
    and the universe notebook is what produces the master in the first place.
    """
    if not SECURITY_MASTER_PATH.is_file():
        print(
            " ".join(
                (
                    f"  WARNING: {SECURITY_MASTER_PATH.name} not found, so",
                    f"{', '.join(SECURITY_MASTER_COLUMNS.values())} are omitted.",
                    "Run Universe/universe.ipynb to produce it.",
                )
            )
        )

        return panel

    with SECURITY_MASTER_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        available = set(reader.fieldnames or ())
        classification = {
            row["ticker"]: row
            for row in reader
        }

    enriched = panel.copy()
    for source_column, output_column in SECURITY_MASTER_COLUMNS.items():
        if source_column not in available:
            print(
                f"  WARNING: {SECURITY_MASTER_PATH.name} has no '{source_column}' column,"
                f" so {output_column} is omitted rather than joined in as nulls."
            )

            continue

        enriched[output_column] = enriched[TICKER_COLUMN].map(
            {
                ticker: (row.get(source_column) or None)
                for ticker, row in classification.items()
            }
        )

    return enriched


def build_curator_panel(
    directory: pathlib.Path,
    limit: int | None = None,
) -> pandas.DataFrame:
    """
    Every column of every Curator file, stacked into one long panel sorted by date then ticker.

    Membership is an **allowlist** taken from the investable universe, not a list of things to
    skip.  The Curator directory also holds the cash proxy and the benchmarks, because the engine
    prices every ticker from one place, and none of them belongs in a cross-section: a benchmark
    ranked against its own constituents is meaningless, and a cash proxy would sit at the bottom of
    every risk rank and the top of every calm one.  Reading membership back from the same file the
    Curator downloaded from means adding a benchmark can never silently pollute a rank -- there is
    no second list to forget to update.
    """
    investable_tickers = read_investable_tickers()
    paths = sorted(
        path
        for path in directory.glob("*.csv")
        if path.stem in investable_tickers
    )
    if limit is not None:
        paths = paths[:limit]

    frames = []
    for path in paths:
        frame = pandas.read_csv(
            path,
            parse_dates=[DATE_COLUMN],
        )
        frame.insert(0, TICKER_COLUMN, path.stem)
        frames.append(frame)

    if len(frames) == 0:
        msg = f"no Curator CSVs found in {directory}"

        raise FileNotFoundError(msg)

    panel = pandas.concat(
        frames,
        ignore_index=True,
    )

    return panel.sort_values(
        [
            DATE_COLUMN,
            TICKER_COLUMN,
        ]
    ).reset_index(drop=True)


def load_custom_calculation_functions(
    skip_classified_columns: bool = False,
) -> dict[str, types.FunctionType]:
    """
    The `r_*` functions from `Data/Refinery/custom_calculations.py`, keyed by column name.

    Loaded by path rather than by import statement because `Data/` is a plain directory rather
    than a package.  `skip_classified_columns` drops the columns that need the security master's
    classification join, so the refinery stays runnable before the universe notebook has run.
    """
    module = _load_module(CUSTOM_CALCULATIONS_PATH)
    requested = [
        column
        for column in module.REFINERY_COLUMNS
        if not (skip_classified_columns and column in module.CLASSIFICATION_DEPENDENT_COLUMNS)
    ]

    functions = {}
    for column in requested:
        if not hasattr(module, column):
            msg = f"{CUSTOM_CALCULATIONS_PATH.name} lists {column} but defines no such function"

            raise AttributeError(msg)

        functions[column] = getattr(module, column)

    return functions


def main() -> int:
    """Parse the command line, refine the panel, write the files.  Returns a process exit code."""
    parser = argparse.ArgumentParser(
        description="Compute the cross-sectional r_* columns over the curated data.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="only refine the first N tickers, for a quick pass",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="compute and report, but write no files",
    )
    arguments = parser.parse_args()

    print(f"Repository root : {REPOSITORY_ROOT}")
    print(f"Reading         : {CURATOR_DIRECTORY.relative_to(REPOSITORY_ROOT)}")
    print(f"Writing         : {REFINERY_DIRECTORY.relative_to(REPOSITORY_ROOT)}")

    started_at = time.monotonic()
    panel = build_curator_panel(CURATOR_DIRECTORY, arguments.limit)
    print(
        " ".join(
            (
                f"Panel           : {panel[TICKER_COLUMN].nunique()} tickers x",
                f"{panel[DATE_COLUMN].nunique()} dates = {len(panel):,} rows",
                f"({time.monotonic() - started_at:.0f}s)",
            )
        )
    )

    curator_columns = list(panel.columns)
    enriched = attach_security_master(panel)
    skip_classified_columns = not SECURITY_MASTER_PATH.is_file()
    functions = load_custom_calculation_functions(skip_classified_columns)
    print(f"Calculations    : {len(functions)} r_* column(s)")
    if skip_classified_columns:
        print("  classification-dependent columns skipped (no Security_Master.csv yet)")

    refined = refine_panel(enriched, functions)
    print(
        f"Refined         : {len(refined.columns)} columns"
        f" ({time.monotonic() - started_at:.0f}s)"
    )
    _report_coverage(refined, functions)

    if arguments.dry_run:
        print("\n--dry-run: no files written.")

        return 0

    written = write_refinery_files(
        refined,
        REFINERY_DIRECTORY,
        curator_columns,
        list(functions),
    )
    print(f"\nWrote {written} file(s) in {time.monotonic() - started_at:.0f}s total.")

    return 0


def read_investable_tickers() -> frozenset[str]:
    """
    Every ticker the universe declares investable -- the panel's membership list.

    This is the same seed file `Data/curator.py` downloads from, which is the point: the Curator
    directory holds those tickers plus the cash proxy and the benchmarks, and reading membership
    back from the seed keeps the extras out without naming them anywhere.
    """
    if not INVESTABLE_UNIVERSE_PATH.is_file():
        msg = " ".join(
            (
                f"{INVESTABLE_UNIVERSE_PATH} is missing, so the panel has no membership list.",
                "It is committed with the repository; restore it from version control.",
            )
        )

        raise FileNotFoundError(msg)

    with INVESTABLE_UNIVERSE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)

        return frozenset(
            row[UNIVERSE_TICKER_COLUMN].strip()
            for row in rows
            if len(row.get(UNIVERSE_TICKER_COLUMN, "").strip()) > 0
        )


def refine_panel(
    panel: pandas.DataFrame,
    functions: dict[str, types.FunctionType],
) -> pandas.DataFrame:
    """
    Build every requested `r_*` column, in dependency order derived from the signatures.

    Each pass computes whatever functions have all their inputs available, so declaration order
    in the calculations module is irrelevant.  A function whose parameters are never satisfied is
    a hard error rather than a silently missing column -- an absent input almost always means a
    typo in a parameter name, and a quietly dropped column would surface much later as a
    confusing failure downstream.

    `panel` is extended in place and returned.  The full universe stacks to roughly 2.3 million
    rows across 28 columns, and a defensive copy of that costs about half a gigabyte for no
    benefit: `attach_security_master` already hands over a frame nobody else holds.
    """
    refined = panel
    pending = dict(functions)

    while len(pending) > 0:
        resolved = [
            column
            for column, function in pending.items()
            if _parameter_names(function) <= set(refined.columns)
        ]
        if len(resolved) == 0:
            msg = _unresolved_message(pending, set(refined.columns))

            raise ValueError(msg)

        for column in resolved:
            arguments = {
                name: refined[name]
                for name in _parameter_names(pending[column])
            }
            started_at = time.monotonic()
            refined[column] = pending[column](**arguments)
            print(f"  {column:34s} {time.monotonic() - started_at:6.1f}s")
            del pending[column]

    return refined


def write_refinery_files(
    refined: pandas.DataFrame,
    directory: pathlib.Path,
    curator_columns: list[str],
    refinery_columns: list[str],
) -> int:
    """
    One CSV per ticker: the same rows as the Curator file, the same columns plus the new ones.

    The helper column the panel is keyed by is dropped again on the way out, so a refined file is
    a drop-in replacement for the Curator file it came from.  Returns the number of files written.
    """
    directory.mkdir(parents=True, exist_ok=True)
    enrichment_columns = [
        column
        for column in SECURITY_MASTER_COLUMNS.values()
        if column in refined.columns
    ]
    output_columns = [
        column
        for column in curator_columns + enrichment_columns + refinery_columns
        if column != TICKER_COLUMN
    ]

    written = 0
    for ticker, group in refined.groupby(TICKER_COLUMN):
        output = group.sort_values(DATE_COLUMN)[output_columns]
        output.to_csv(
            directory / f"{ticker}.csv",
            index=False,
        )
        written += 1

    return written


def _load_module(
    path: pathlib.Path,
) -> types.ModuleType:
    """
    Import `path` as a standalone module object.

    Its directory goes on the import path first, so the calculations module can import a sibling
    -- `jump_model` -- by name.  `Data/Refinery/` is a plain directory rather than a package, so
    without this the only way a calculations file could reach a helper beside it would be another
    path-loading incantation at the top of every one.
    """
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))

    specification = importlib.util.spec_from_file_location(
        f"{path.parent.name.lower()}_calculations",
        path,
    )
    if specification is None or specification.loader is None:
        msg = f"could not load custom calculations from {path}"

        raise ImportError(msg)

    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def _parameter_names(
    function: types.FunctionType,
) -> set[str]:
    """The panel columns `function` consumes, taken from its signature."""

    return set(
        inspect.signature(function).parameters
    )


def _report_coverage(
    refined: pandas.DataFrame,
    functions: dict[str, types.FunctionType],
) -> None:
    """Print how much of each new column is populated, so an all-null column cannot slip past."""
    print("\nColumn coverage:")
    for column in functions:
        populated = int(refined[column].notna().sum())
        share = populated / len(refined) if len(refined) > 0 else 0.0
        print(f"  {column:28s} {populated:>10,} / {len(refined):,} ({share:.1%})")


def _unresolved_message(
    pending: dict[str, types.FunctionType],
    available: set[str],
) -> str:
    """Explain which columns could not be built and exactly which inputs were missing."""
    details = [
        f"{column} needs {sorted(_parameter_names(function) - available)}"
        for column, function in sorted(pending.items())
    ]

    return "; ".join(
        (
            f"could not resolve {len(pending)} refinery column(s)",
            *details,
        )
    )


if __name__ == "__main__":
    sys.exit(main())
