"""
The one path from a book of weights to a performance number: the KaxaNuk Backtest Engine.

Every experiment in this repository ranks its variants and reports its results through this
module and nothing else.  There is deliberately no second, simpler simulator: a lightweight
backtest that disagrees with the engine is worse than no backtest at all, because it invites the
reader to pick whichever number they prefer.  The engine models integer share counts, per-share
commission on the unadjusted price and a cash reserve, and it is what the results are quoted on.

Three things this module owns, so the three experiment notebooks share one code path:

- **Shaping** a `dates x companies` weight frame into the `Ticker x dates` CSV the engine loads.
- **Running** the engine over that file, including the gross/net exposure limits a long/short
  book needs.
- **Reading back** the two sheets anything downstream wants: `benchmark_comparison` (the summary
  metrics) and `portfolio_bench_total_value` (the daily value series every chart is drawn from).

Fair variant ranking.  Variants of one experiment start on different dates -- a rule that needs
twelve months of history simply cannot trade in its first year -- and comparing books measured
over different windows is meaningless.  `align_to_common_start` gives every variant the same
first day by carrying forward the book that was already prevailing on that day.  That lookup is
strictly backward-looking, so it introduces no information the strategy did not already have.
"""

__all__ = [
    "ATTRIBUTION_HOLDINGS_FILE",
    "ATTRIBUTION_RETURNS_DAY_FIRST",
    "ATTRIBUTION_RETURNS_FILE",
    "ATTRIBUTION_RETURNS_SERIES_NAME",
    "BENCHMARK_TICKERS",
    "CASH_TICKER",
    "FACTOR_FILE_PATTERN",
    "EngineRun",
    "EngineSettings",
    "align_to_common_start",
    "available_benchmarks",
    "read_benchmark_comparison",
    "read_daily_values",
    "run_variant",
    "to_engine_frame",
]

import dataclasses
import datetime
import logging
import pathlib
import re

import pandas

# What every experiment is scored against, in the order results report them; the first is
# primary.  `Data/curator.py` decides what gets *fetched* -- SPY and QQQ are downloaded, KN600 is
# supplied by hand -- and this decides what gets *reported*.  A ticker named here without a price
# file in the market-data directory is dropped by the engine, so `available_benchmarks` checks
# for the files before a run rather than letting a benchmark vanish from a results table.
BENCHMARK_TICKERS = (
    "SPY",
    "QQQ",
    "KN600",
)
CASH_TICKER = "BIL"

# The inputs the attribution stage reads, all supplied by hand into `Data/Curator/`.
ATTRIBUTION_HOLDINGS_FILE = "index_daily_holdings_2017.csv"
ATTRIBUTION_RETURNS_DAY_FIRST = True
ATTRIBUTION_RETURNS_FILE = "kn600_returns.csv"
ATTRIBUTION_RETURNS_SERIES_NAME = "KN600"
FACTOR_FILE_PATTERN = "f_*.csv"

# The three price columns, each doing a different job.  Getting them out of step is silent: the
# P&L and the attribution would quietly run on different bases and the disagreement would surface
# as an unexplained residual rather than as an error.
COMMISSION_PRICE_COLUMN = "c_vwap"
DATE_COLUMN = "m_date"
MARK_PRICE_COLUMN = "m_close_dividend_and_split_adjusted"
TRADE_PRICE_COLUMN = "c_vwap_dividend_and_split_adjusted"

# Both result sheets carry a title row and a blank row before their real header.
SHEET_HEADER_ROW = 2
SUMMARY_SHEET = "benchmark_comparison"
VALUE_SHEET = "portfolio_bench_total_value"


@dataclasses.dataclass(frozen=True)
class EngineSettings:
    """Everything a run needs that does not change between the variants of one experiment."""

    market_data_directory: pathlib.Path
    portfolio_directory: pathlib.Path
    output_directory: pathlib.Path
    start_date: datetime.date
    end_date: datetime.date
    benchmark_tickers: tuple[str, ...] = BENCHMARK_TICKERS
    cash_reserve_percentage: float = 0.01
    commission_cents: float = 0.05
    dashboard_port: int = 8090
    initial_capital: int = 1_000_000


@dataclasses.dataclass(frozen=True)
class EngineRun:
    """One completed engine run: where it landed, what it scored, and its daily series."""

    variant_name: str
    workbook_path: pathlib.Path
    summary: pandas.DataFrame
    daily_values: pandas.DataFrame
    invalid_reason: str | None = None

    @property
    def is_valid(self) -> bool:
        """
        Whether this run's numbers can be believed.

        The engine can produce a *workbook* for a book it could not fully simulate: the daily
        value series simply stops and every later day is null.  Every summary metric is then
        computed over the truncated part and looks entirely plausible -- a low volatility, a
        shallow drawdown, a Sharpe that invites a conclusion.  Nothing about the file says so,
        which is exactly why this is checked rather than assumed.
        """

        return self.invalid_reason is None


def align_to_common_start(
    weights: pandas.DataFrame,
    common_start: pandas.Timestamp,
) -> pandas.DataFrame:
    """
    Restate a book so it begins on `common_start`, carrying forward whatever it already held.

    Variants of one experiment first trade on different days, and a Sharpe measured over a
    different window is not comparable.  The row dated `common_start` is the book struck on the
    last rebalance at or before that date -- a backward-looking lookup, so nothing the strategy
    could not already have known enters the file.  Rebalances after the common start are kept as
    they are; anything before it is dropped, since it is already represented by that first row.
    """
    prior_strikes = weights.index[weights.index <= common_start]
    later_strikes = weights.index[weights.index > common_start]
    if len(prior_strikes) == 0:
        msg = f"no book exists on or before {common_start.date()}; cannot start there"

        raise ValueError(msg)

    opening_book = weights.loc[prior_strikes[-1]].rename(common_start)

    return pandas.concat(
        [
            opening_book.to_frame().T,
            weights.loc[later_strikes],
        ]
    )


def available_benchmarks(
    market_data_directory: pathlib.Path,
    tickers: tuple[str, ...],
) -> tuple[str, ...]:
    """
    Which of `tickers` actually have a price file, reporting the ones that do not.

    A fresh clone has no `KN600.csv` -- that index is supplied by hand, not downloaded (see
    README.md) -- and the engine raises if it is told to measure against a benchmark it cannot
    price.  Measuring against two benchmarks instead of three is a much better outcome than a
    crash, so the missing ones are named and dropped rather than allowed to stop the run.
    """
    present = tuple(
        ticker
        for ticker in tickers
        if (market_data_directory / f"{ticker}.csv").is_file()
    )
    missing = tuple(
        ticker
        for ticker in tickers
        if ticker not in present
    )
    if len(missing) > 0:
        print(
            " ".join(
                (
                    f"  benchmark price file missing for {', '.join(missing)}",
                    f"in {market_data_directory.name}/ - measuring against",
                    f"{', '.join(present) if present else 'nothing'} instead.",
                )
            )
        )
        print("  See README.md: the KaxaNuk index files are supplied by hand, not downloaded.")

    if len(present) == 0:
        msg = f"no benchmark price files at all in {market_data_directory}; cannot run a backtest"

        raise FileNotFoundError(msg)

    return present


def read_benchmark_comparison(
    workbook_path: pathlib.Path,
) -> pandas.DataFrame:
    """The summary metrics sheet, indexed by metric name with one column per series."""
    raw = pandas.read_excel(
        workbook_path,
        sheet_name=SUMMARY_SHEET,
        header=SHEET_HEADER_ROW,
    )
    named = raw.rename(columns={raw.columns[0]: "metric"})

    return named.dropna(subset=["metric"]).set_index("metric")


def read_daily_values(
    workbook_path: pathlib.Path,
) -> pandas.DataFrame:
    """
    The daily value series for the portfolio and every benchmark, indexed by date.

    Only the `*_Value` columns are returned.  The engine also writes `*_Returns` columns, but
    those are rounded to two decimals -- fine for a spreadsheet, useless for compounding -- so
    anything wanting returns should difference the values here instead.
    """
    raw = pandas.read_excel(
        workbook_path,
        sheet_name=VALUE_SHEET,
        header=SHEET_HEADER_ROW,
    )
    dated = raw.rename(columns={raw.columns[0]: DATE_COLUMN})
    dated[DATE_COLUMN] = pandas.to_datetime(dated[DATE_COLUMN])
    value_columns = [
        column
        for column in dated.columns
        if str(column).endswith("_Value")
    ]

    return dated.dropna(subset=[DATE_COLUMN]).set_index(DATE_COLUMN)[value_columns]


def run_variant(
    variant_name: str,
    engine_frame: pandas.DataFrame,
    settings: "EngineSettings",
    max_gross_exposure: float = 1.0,
    max_net_exposure: float | None = None,
    logger_level: int = logging.WARNING,
) -> "EngineRun":
    """
    Write one variant's weight file, run the engine over it, and read the results back.

    `max_gross_exposure` and `max_net_exposure` are what make a long/short book expressible: a
    long-only book leaves them at 1.0 and None, while a 130/30 passes 1.6 and 1.0.  The engine
    rejects a book that breaches them, which is the point -- an exposure limit that is not
    enforced is a comment.
    """
    # Imported here rather than at module scope so the notebooks can import this module, and
    # report a clean message, in an environment where the licensed engine is not installed.
    import kaxanuk.backtest_engine.backtest_engine
    import kaxanuk.backtest_engine.entities.configuration
    import kaxanuk.backtest_engine.input_handlers.csv_input
    import kaxanuk.backtest_engine.input_handlers.csv_portfolio_input_handler

    portfolio_name = _slugify(variant_name)
    settings.portfolio_directory.mkdir(parents=True, exist_ok=True)
    settings.output_directory.mkdir(parents=True, exist_ok=True)
    engine_frame.to_csv(settings.portfolio_directory / f"{portfolio_name}.csv")

    configuration = kaxanuk.backtest_engine.entities.configuration.Configuration(
        initial_capital=settings.initial_capital,
        start_date=settings.start_date,
        end_date=settings.end_date,
        cash_reserve_percentage=settings.cash_reserve_percentage,
        commission_cents=settings.commission_cents,
        market_data_input_format="csv",
        portfolio_name=portfolio_name,
        portfolio_input_format="csv",
        benchmark_file_name=",".join(settings.benchmark_tickers),
        input_market_data_directory=str(settings.market_data_directory),
        input_portfolio_directory=str(settings.portfolio_directory),
        backtest_results_output_directory=str(settings.output_directory),
        user_column_commission_price=COMMISSION_PRICE_COLUMN,
        user_column_trade_execution_price=TRADE_PRICE_COLUMN,
        user_column_mark_to_market_price=MARK_PRICE_COLUMN,
        user_column_date=DATE_COLUMN,
        max_gross_exposure=max_gross_exposure,
        max_net_exposure=max_net_exposure,
    )

    kaxanuk.backtest_engine.backtest_engine.main(
        configuration=configuration,
        input_handlers=[
            kaxanuk.backtest_engine.input_handlers.csv_input.CsvInput(
                input_dir=str(settings.market_data_directory),
            )
        ],
        portfolio_handlers=[
            kaxanuk.backtest_engine.input_handlers.csv_portfolio_input_handler
            .CsvPortfolioInputHandler(str(settings.portfolio_directory))
        ],
        logger_level=logger_level,
        logger_file=None,
        launch_dashboard=False,
        dashboard_port=settings.dashboard_port,
    )

    # A book the engine refuses -- an exposure limit breached, an input it cannot price -- leaves
    # no workbook behind.  That is one variant failing, not a reason to abandon the sweep, so it
    # comes back as an invalid run for the caller to report and exclude.
    candidates = sorted(
        settings.output_directory.glob(f"{portfolio_name}_*_backtest_results.xlsx"),
        key=lambda path: path.stat().st_mtime,
    )
    if len(candidates) == 0:

        return EngineRun(
            variant_name=variant_name,
            workbook_path=settings.output_directory / f"{portfolio_name}.csv",
            summary=pandas.DataFrame(),
            daily_values=pandas.DataFrame(),
            invalid_reason=(
                "the engine produced no results workbook, so it rejected this book outright"
                " -- most often an exposure limit breached on at least one date"
            ),
        )

    workbook_path = candidates[-1]
    daily_values = read_daily_values(workbook_path)

    return EngineRun(
        variant_name=variant_name,
        workbook_path=workbook_path,
        summary=read_benchmark_comparison(workbook_path),
        daily_values=daily_values,
        invalid_reason=_truncation_reason(daily_values),
    )


def to_engine_frame(
    weights: pandas.DataFrame,
    ticker_matrix: pandas.DataFrame,
    cash_ticker: str | None = None,
) -> pandas.DataFrame:
    """
    Reshape a `dates x companies` book into the `Ticker x dates` table the engine loads.

    The engine resolves every row against `<Ticker>.csv` in its market-data directory, so the
    file has to speak in tickers rather than in the ISIN-stitched companies the research view
    uses.  A company that changed ticker mid-history therefore occupies two rows, each non-zero
    only while that listing was the live one -- which is right, because they are two files with
    two price histories.

    When `cash_ticker` is given, any residual left over from a book that does not reach 1.0 is
    parked in it, since the engine's weight file has no cash row of its own.
    """
    held = weights.stack()
    held = held[held.abs() > 0]
    tickers = ticker_matrix.reindex(weights.index).stack().reindex(held.index)

    engine_frame = (
        pandas.DataFrame(
            {
                "weight": held,
                "ticker": tickers,
            }
        )
        .rename_axis(
            [
                "rebalance_date",
                "company",
            ]
        )
        .reset_index()
        .pivot_table(
            index="ticker",
            columns="rebalance_date",
            values="weight",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reindex(columns=weights.index, fill_value=0.0)
    )

    if cash_ticker is not None:
        residual = 1.0 - engine_frame.sum(axis=0)
        if float(residual.abs().max()) > 1e-9:
            engine_frame.loc[cash_ticker] = residual.clip(lower=0.0).to_numpy()

    ordered = engine_frame.sort_index().round(9)
    ordered.columns = [
        date.strftime("%Y-%m-%d")
        for date in ordered.columns
    ]
    ordered.index.name = "Ticker"

    return ordered


def _truncation_reason(
    daily_values: pandas.DataFrame,
) -> str | None:
    """
    Why this run's value series cannot be trusted, or None when it is complete.

    A run the engine could not finish leaves the portfolio's value null from the day it gave up
    onward, while the benchmark columns carry on as normal.  The summary sheet is then computed
    over the surviving stub and reads as a real result: unusually low volatility, an unusually
    shallow drawdown, and a Sharpe somebody will otherwise put in a table.
    """
    column = "Total_Portfolio_Value"
    if column not in daily_values.columns:

        return f"the results workbook has no {column} column"

    series = daily_values[column]
    missing = int(series.isna().sum())
    if missing == 0:

        return None

    first_missing = series[series.isna()].index[0]

    return " ".join(
        (
            f"the engine stopped valuing this book on {first_missing.date()};",
            f"{missing} of {len(series)} days are null, so every metric is computed",
            "over a truncated window and must not be compared against a complete run",
        )
    )


def _slugify(
    variant_name: str,
) -> str:
    """A filesystem- and engine-safe name, since the variant label becomes a file name."""
    lowered = variant_name.strip().lower()
    collapsed = re.sub(r"[^a-z0-9]+", "_", lowered)

    return collapsed.strip("_")
