"""
Custom `c_*` calculation functions for the Data Curator stage.

`c_*` means **one security's own history and nothing else**.  The Curator works one identifier at
a time, so anything that has to compare securities against each other belongs one stage later, in
`Data/Refinery/custom_calculations.py`, as an `r_*` column.

Functions are resolved by parameter name against the columns already built, so a parameter named
`m_close_dividend_and_split_adjusted` receives that market-data column and a parameter named
`c_return_1d` receives the output of the function of the same name.  Dependency order comes from
the signatures, not from the order of definition here.

**Adding a column:** define the function, then list it in `CUSTOM_COLUMNS` in `Data/curator.py`.
Widening that tuple changes the output header, so the next run refetches every identifier -- which
is intended, because it is what stops the directory holding a mix of schemas.

Three groups of function live here.

1.  **Engine infrastructure -- never remove.**  `c_split_ratio`, `c_dividend_split_ratio`,
    `c_vwap` and `c_vwap_dividend_and_split_adjusted` rebuild the VWAP columns the provider
    returns as null.  `Experiments/backtest_engine.py` charges commission on `c_vwap` and fills at
    `c_vwap_dividend_and_split_adjusted`.
2.  **The example strategy's features.**  `c_return_1d` and the eight exponentially weighted
    columns below are the feature set of Shu, Yu & Mulvey (2024), the regime paper this repository
    works through.  They are deliberately *arithmetic only*: they carry no fitted parameter, so
    nothing here changes when the jump model in the Refinery is retuned.  That is the whole reason
    they can live in the Curator at all -- see the Refinery module's docstring.
3.  **A liquidity measure**, because capacity is a question every strategy has to answer.

Two suffixes, and they mean different things:

    _63d   a **window**: the last 63 observations, equally weighted
    _hl5   a **half-life**: exponential weights that halve every 5 observations, no cut-off

Three adjustment families arrive from the provider and each does a different job:

    unadjusted           recovers the split / dividend ratios; the price commission is charged on
    split-adjusted       traded value, i.e. liquidity in today's share terms
    dividend-and-split   the total-return series a signal and the backtest P&L run on
"""

__all__ = [
    "c_daily_traded_value_1d",
    "c_daily_traded_value_63d",
    "c_dividend_split_ratio",
    "c_downside_deviation_log_hl5",
    "c_downside_deviation_log_hl21",
    "c_return_1d",
    "c_return_ewm_hl5",
    "c_return_ewm_hl10",
    "c_return_ewm_hl21",
    "c_sortino_hl5",
    "c_sortino_hl10",
    "c_sortino_hl21",
    "c_split_ratio",
    "c_vwap",
    "c_vwap_dividend_and_split_adjusted",
]

import numpy
import pandas

import kaxanuk.data_curator
import kaxanuk.data_curator.features.helpers

ADTV_WINDOW_DAYS = 63


def c_daily_traded_value_1d(
    m_volume_split_adjusted: "kaxanuk.data_curator.DataColumn",
    m_close_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    Single-day dollar volume: split-adjusted close times split-adjusted volume.

    Both legs are split-adjusted so the series is expressed in today's share terms and stays
    comparable across a split.
    """

    return m_close_split_adjusted * m_volume_split_adjusted


def c_daily_traded_value_63d(
    c_daily_traded_value_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    Average daily traded value over roughly one quarter -- the capacity measure.

    The parameter name is what wires this to `c_daily_traded_value_1d`; the Curator reads the
    dependency out of the signature and computes that column first.
    """

    return kaxanuk.data_curator.features.helpers.simple_moving_average(
        column=c_daily_traded_value_1d,
        days=ADTV_WINDOW_DAYS,
    )


def c_dividend_split_ratio(
    m_close_dividend_and_split_adjusted: "kaxanuk.data_curator.DataColumn",
    m_close: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Combined dividend-and-split adjustment ratio, recovered from the two close columns."""

    return m_close_dividend_and_split_adjusted / m_close


def c_downside_deviation_log_hl5(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Log downside deviation, half-life 5 days: the fast reading of how bad the bad days are."""

    return _log_downside_deviation(c_return_1d, 5)


def c_downside_deviation_log_hl21(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Log downside deviation, half-life 21 days: the same reading over about a month."""

    return _log_downside_deviation(c_return_1d, 21)


def c_return_1d(
    m_close_dividend_and_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    One-day total return -- the series every feature below is built on.

    Dividend-and-split adjusted, so a dividend shows up as return rather than as a price drop.
    The first row is null: there is no prior close to compare against.
    """
    prices = _to_float_series(m_close_dividend_and_split_adjusted)

    return kaxanuk.data_curator.DataColumn.load(
        prices.pct_change()
    )


def c_return_ewm_hl5(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Exponentially weighted mean return, half-life 5 days: short-horizon direction."""

    return _exponentially_weighted_mean(c_return_1d, 5)


def c_return_ewm_hl10(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Exponentially weighted mean return, half-life 10 days."""

    return _exponentially_weighted_mean(c_return_1d, 10)


def c_return_ewm_hl21(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Exponentially weighted mean return, half-life 21 days: about a month of direction."""

    return _exponentially_weighted_mean(c_return_1d, 21)


def c_sortino_hl5(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Return per unit of downside deviation, half-life 5 days."""

    return _sortino(c_return_1d, 5)


def c_sortino_hl10(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Return per unit of downside deviation, half-life 10 days."""

    return _sortino(c_return_1d, 10)


def c_sortino_hl21(
    c_return_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Return per unit of downside deviation, half-life 21 days."""

    return _sortino(c_return_1d, 21)


def c_split_ratio(
    m_close_split_adjusted: "kaxanuk.data_curator.DataColumn",
    m_close: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """Cumulative split ratio, recovered from the adjusted and unadjusted close columns."""

    return m_close_split_adjusted / m_close


def c_vwap(
    c_split_ratio: "kaxanuk.data_curator.DataColumn",
    m_vwap_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    Unadjusted VWAP, recovered from the split-adjusted VWAP.

    The provider returns no raw VWAP column, so it is divided back out of the adjusted one using
    the split ratio above.  This is the price the engine charges commission on.
    """

    return m_vwap_split_adjusted / c_split_ratio


def c_vwap_dividend_and_split_adjusted(
    c_dividend_split_ratio: "kaxanuk.data_curator.DataColumn",
    c_vwap: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """VWAP on the same total-return basis as the adjusted close.  The engine's fill price."""

    return c_dividend_split_ratio * c_vwap


def _downside_deviation(
    returns: pandas.Series,
    half_life_days: int,
) -> pandas.Series:
    """
    Root mean square of the losing days only, exponentially weighted.

    Winning days enter as zero rather than being dropped, so a calm stretch pulls the reading down
    instead of leaving it undefined.  A reading of exactly zero -- a stretch with no losing day at
    all -- becomes null, because the two features built on it would otherwise take the log of zero
    or divide by it.
    """
    losses = returns.clip(upper=0.0)
    mean_squared_loss = (
        losses.pow(2)
        .ewm(halflife=half_life_days)
        .mean()
    )

    return (
        mean_squared_loss.pow(0.5)
        .replace(0.0, numpy.nan)
    )


def _exponentially_weighted_mean(
    column: "kaxanuk.data_curator.DataColumn",
    half_life_days: int,
) -> "kaxanuk.data_curator.DataColumn":
    """
    Exponentially weighted mean with the given half-life, in trading-day units.

    The Curator's own `exponential_moving_average` helper is parameterised by span rather than by
    half-life, and the two do not line up on whole numbers, so this drops into pandas to keep the
    half-lives at exactly the values the paper specifies.
    """
    values = _to_float_series(column)

    return kaxanuk.data_curator.DataColumn.load(
        values.ewm(halflife=half_life_days).mean()
    )


def _log_downside_deviation(
    column: "kaxanuk.data_curator.DataColumn",
    half_life_days: int,
) -> "kaxanuk.data_curator.DataColumn":
    """
    Downside deviation on a log scale, which is what the jump model is fed.

    Volatility is roughly lognormal, so the log makes the feature closer to symmetric and stops a
    single crisis stretch dominating the standardisation the model applies later.
    """
    returns = _to_float_series(column)

    return kaxanuk.data_curator.DataColumn.load(
        numpy.log(
            _downside_deviation(returns, half_life_days)
        )
    )


def _sortino(
    column: "kaxanuk.data_curator.DataColumn",
    half_life_days: int,
) -> "kaxanuk.data_curator.DataColumn":
    """
    Exponentially weighted return divided by exponentially weighted downside deviation.

    The risk-free rate is taken as zero, so this is a ratio of two quantities the other six
    features already carry separately.  It earns its place anyway because the model sees their
    *interaction* only if something states it: a small positive return means one thing in a calm
    market and another in a falling one.
    """
    returns = _to_float_series(column)

    return kaxanuk.data_curator.DataColumn.load(
        returns.ewm(halflife=half_life_days).mean()
        / _downside_deviation(returns, half_life_days)
    )


def _to_float_series(
    column: "kaxanuk.data_curator.DataColumn",
) -> pandas.Series:
    """
    The column as a plain float series, which is what every calculation below expects.

    Prices arrive from the provider as fixed-point decimals, and pandas will not compare or clip
    one of those against an ordinary float.  Casting once at the boundary is cheaper than
    scattering `Decimal` literals through arithmetic that is statistical, not monetary.
    """

    return column.to_pandas().astype("float64")
