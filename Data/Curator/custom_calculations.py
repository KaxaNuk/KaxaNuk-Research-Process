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
is intended, because it is what stops the directory holding a mix of schemas.  It also means the
Curator is the wrong home for anything you intend to *tune*: a sweep must never cost a download.
Put fitted columns in the Refinery.

**Your signal goes here.**  What ships is the minimum:

1.  **Engine infrastructure -- never remove.**  `c_split_ratio`, `c_dividend_split_ratio`,
    `c_vwap` and `c_vwap_dividend_and_split_adjusted` rebuild the VWAP columns the provider
    returns as null.  `Experiments/backtest_engine.py` charges commission on `c_vwap` and fills at
    `c_vwap_dividend_and_split_adjusted`.
2.  **`c_return_1d`**, because almost every feature is built on it.
3.  **A liquidity measure**, because capacity is a question every strategy has to answer, and
    because it is the worked example of the two patterns a `c_*` column uses: arithmetic between
    provider columns, and a rolling helper over another `c_*` column.

Three adjustment families arrive from the provider and each does a different job:

    unadjusted           recovers the split / dividend ratios; the price commission is charged on
    split-adjusted       traded value, i.e. liquidity in today's share terms
    dividend-and-split   the total-return series a signal and the backtest P&L run on
"""

__all__ = [
    "c_daily_traded_value_1d",
    "c_daily_traded_value_63d",
    "c_dividend_split_ratio",
    "c_return_1d",
    "c_split_ratio",
    "c_vwap",
    "c_vwap_dividend_and_split_adjusted",
]

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


def c_return_1d(
    m_close_dividend_and_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    One-day total return -- the series most features end up being built on.

    Dividend-and-split adjusted, so a dividend shows up as return rather than as a price drop.
    The first row is null: there is no prior close to compare against.
    """
    prices = _to_float_series(m_close_dividend_and_split_adjusted)

    return kaxanuk.data_curator.DataColumn.load(
        prices.pct_change()
    )


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


def _to_float_series(
    column: "kaxanuk.data_curator.DataColumn",
) -> pandas.Series:
    """
    The column as a plain float series, which is what a statistical calculation expects.

    Prices arrive from the provider as fixed-point decimals, and pandas will not compare or clip
    one of those against an ordinary float.  Casting once at the boundary is cheaper than
    scattering `Decimal` literals through arithmetic that is statistical, not monetary.
    """

    return column.to_pandas().astype("float64")
