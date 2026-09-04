"""
Shared plumbing for the experiments: load the refined panel, key it by company, and reshape it
into the matrices every strategy rule is written against.

Only the *mechanical* steps live here -- reading files, stitching ticker changes into one
position, pivoting to `dates x companies`.  Each experiment's **selection and weighting rule stays
in its own notebook**, because that is the part that differs between experiments and the part a
reader needs to see spelled out.  For the same reason **no strategy column is named in this
module**: the columns a rule reads are declared in the experiment's configuration cell and passed
in through `columns`.  A signal column that leaks into shared code becomes every later
experiment's default without anyone deciding it.

`Experiments/Experiment_1/experiment_1.ipynb` deliberately writes these same steps inline rather
than importing them: it is the benchmark, and a benchmark that cannot be read top to bottom
without following an import is a worse benchmark.  Later experiments import from here so their
notebooks show only what they change relative to that baseline.

Sharing the loader is what guarantees the comparison is fair -- every experiment sees an identical
panel, over an identical window, keyed identically.
"""

__all__ = [
    "BASE_PANEL_COLUMNS",
    "CLASSIFICATION_COLUMNS",
    "DATE_COLUMN",
    "MARK_PRICE_COLUMN",
    "TRADE_PRICE_COLUMN",
    "CompanyPanel",
    "build_matrices",
    "load_company_panel",
]

import dataclasses
import pathlib

import pandas

DATE_COLUMN = "m_date"
MARK_PRICE_COLUMN = "m_close_dividend_and_split_adjusted"
TRADE_PRICE_COLUMN = "c_vwap_dividend_and_split_adjusted"

# The columns every experiment needs regardless of its rule.  An experiment adds its own signal
# and sizing columns on top:
#     load_company_panel(..., columns=(*BASE_PANEL_COLUMNS, "r_regime_bull"))
BASE_PANEL_COLUMNS = (
    DATE_COLUMN,
    MARK_PRICE_COLUMN,
    TRADE_PRICE_COLUMN,
)

# Classification columns joined onto the panel by `Data/refinery.py`, carried into the metadata
# frame so a book can be grouped for reporting.  They are named here rather than in
# `BASE_PANEL_COLUMNS` because they are optional: a security master that classifies securities by
# something else, or not at all, changes this tuple and nothing else.  A column absent from the
# refined files is skipped rather than raising -- the panel is still a panel without it.
CLASSIFICATION_COLUMNS = (
    "asset_class_current",
    "asset_group_current",
)


@dataclasses.dataclass(frozen=True)
class CompanyPanel:
    """The refined panel keyed by company, with the metadata needed to read a book."""

    frame: pandas.DataFrame
    metadata: pandas.DataFrame
    ticker_count: int
    multi_leg_count: int
    overlapping_rows: int


def build_matrices(
    company_panel: "CompanyPanel",
    columns: tuple[str, ...],
) -> dict[str, pandas.DataFrame]:
    """
    One `dates x companies` matrix per name in `columns`, plus a `ticker` matrix.

    Pivoting once here is what lets a strategy rule be written as a few whole-matrix operations
    rather than a loop over dates.
    """
    matrices = {
        column: company_panel.frame.pivot(
            index=DATE_COLUMN,
            columns="company",
            values=column,
        ).sort_index()
        for column in (*columns, "ticker")
    }

    return matrices


def load_company_panel(
    refinery_directory: pathlib.Path,
    universe_path: pathlib.Path,
    columns: tuple[str, ...] = BASE_PANEL_COLUMNS,
) -> "CompanyPanel":
    """
    Read every refined file, then collapse ticker changes into one position per company.

    The universe is point-in-time, so it carries ticker changes -- two legs sharing an ISIN, each
    holding only part of the history.  Positions are keyed by ISIN (falling back to the ticker
    where the universe file has none), and where two legs report on the same date the one still
    reporting later wins, because that is the surviving listing.  Left unstitched, the book would
    hold both legs and double the bet on one company.
    """
    paths = sorted(refinery_directory.glob("*.csv"))
    if len(paths) == 0:
        msg = f"no refined files in {refinery_directory}; run: uv run python Data/refinery.py"

        raise FileNotFoundError(msg)

    available = set(pandas.read_csv(paths[0], nrows=0).columns)
    missing = [column for column in columns if column not in available]
    if len(missing) > 0:
        msg = " ".join(
            (
                f"the refined files do not carry {missing}.",
                "Either the Refinery has not produced them yet (rerun Data/refinery.py) or the",
                "experiment's setup cell names a column that no longer exists.",
            )
        )

        raise KeyError(msg)

    # Classification is optional: an experiment that reports by group gets it, one whose security
    # master carries no classification simply has no group column in its metadata.
    classification = [column for column in CLASSIFICATION_COLUMNS if column in available]

    frames = []
    for path in paths:
        frame = pandas.read_csv(
            path,
            usecols=[*columns, *classification],
            parse_dates=[DATE_COLUMN],
        )
        frame.insert(0, "ticker", path.stem)
        frames.append(frame)

    panel = pandas.concat(
        frames,
        ignore_index=True,
    )

    universe = pandas.read_csv(
        universe_path,
        encoding="utf-8-sig",
        dtype=str,
    )
    universe["ticker"] = universe["ticker"].str.strip()
    company_by_ticker = {
        row.ticker: (row.isin if isinstance(row.isin, str) and row.isin else row.ticker)
        for row in universe.itertuples()
    }
    panel["company"] = panel["ticker"].map(company_by_ticker).fillna(panel["ticker"])

    tickers_by_company: dict[str, list[str]] = {}
    for ticker, company in company_by_ticker.items():
        tickers_by_company.setdefault(company, []).append(ticker)
    multi_leg_companies = {
        company
        for company, ticker_list in tickers_by_company.items()
        if len(ticker_list) > 1
    }

    last_date_by_ticker = panel.groupby("ticker")[DATE_COLUMN].max()
    panel["leg_rank"] = panel["ticker"].map(last_date_by_ticker)
    overlapping_rows = int(
        panel[panel["company"].isin(multi_leg_companies)]
        .duplicated(
            subset=[
                "company",
                DATE_COLUMN,
            ],
            keep=False,
        )
        .sum()
    )

    stitched = (
        panel.sort_values(
            [
                "company",
                DATE_COLUMN,
                "leg_rank",
            ]
        )
        .drop_duplicates(
            subset=[
                "company",
                DATE_COLUMN,
            ],
            keep="last",
        )
        .drop(columns="leg_rank")
    )

    metadata = (
        stitched.sort_values(DATE_COLUMN)
        .groupby("company")
        .agg(
            ticker=("ticker", "last"),
            **{
                column.removesuffix("_current"): (column, "last")
                for column in classification
            },
        )
    )
    name_by_isin = dict(
        zip(
            universe["isin"],
            universe["name"],
        )
    )
    metadata["name"] = pandas.Series(
        metadata.index.map(name_by_isin),
        index=metadata.index,
    ).fillna(metadata["ticker"])

    return CompanyPanel(
        frame=stitched,
        metadata=metadata,
        ticker_count=int(panel["ticker"].nunique()),
        multi_leg_count=len(multi_leg_companies),
        overlapping_rows=overlapping_rows,
    )
