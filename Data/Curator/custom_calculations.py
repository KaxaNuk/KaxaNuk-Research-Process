"""
Custom `c_*` calculation functions for the Data Curator stage.

The Data Curator resolves each function's parameter names against the columns it has already
built, so a parameter named `m_close_split_adjusted` receives that market-data column and a
parameter named `c_split_ratio` receives the output of the function of the same name.  Dependency
order is therefore derived from the signatures, not from the order of definition in this file.

Every function here returns a `DataColumn`.  Arithmetic between `DataColumn` objects yields a
`DataColumn`, so most calculations are one-liners; drop into pandas only when an operation has to
compare columns element-wise or keep warm-up rows null.

Two kinds of function live here, and the template ships both:

- **Infrastructure the backtest engine needs.**  `c_split_ratio`, `c_dividend_split_ratio`,
  `c_vwap` and `c_vwap_dividend_and_split_adjusted` rebuild the VWAP columns the provider returns
  as null.  `Experiments/engine.py` names `c_vwap` as the commission price and
  `c_vwap_dividend_and_split_adjusted` as the fill price.  **Do not remove them.**
- **A worked example of a strategy column.**  `c_daily_traded_value_1d` and
  `c_daily_traded_value_63d` show the two patterns every `c_*` column uses -- arithmetic between
  columns, and a rolling helper over another `c_*` column.  Dollar volume is kept because nearly
  every strategy needs a liquidity measure for capacity; replace or extend it with your own.

Adding a column: define the function here, then list it in `CUSTOM_COLUMNS` in `Data/curator.py`.
Widening that tuple changes the output header, so the staleness check refetches every identifier
on the next run -- intended, so the directory never holds a mix of schemas.

Three adjustment families arrive from the provider and each does a different job:

- unadjusted            -- recovers the split / dividend ratios, and is the price commission is
                           charged on
- split-adjusted        -- traded value / ADTV, i.e. liquidity in today's share terms
- dividend-and-split    -- the total-return series a signal and the backtest P&L run on
"""

__all__ = [
    "c_daily_traded_value_1d",
    "c_daily_traded_value_63d",
    "c_dividend_split_ratio",
    "c_split_ratio",
    "c_vwap",
    "c_vwap_dividend_and_split_adjusted",
]

import kaxanuk.data_curator
import kaxanuk.data_curator.features.helpers

ADTV_WINDOW_DAYS = 63


def c_daily_traded_value_1d(
    m_volume_split_adjusted: "kaxanuk.data_curator.DataColumn",
    m_close_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    Single-day dollar volume: split-adjusted close times split-adjusted volume.

    The worked example of arithmetic between two provider columns.  Both legs are split-adjusted
    so the series is expressed in today's share terms and is comparable across a split.
    """

    return m_close_split_adjusted * m_volume_split_adjusted


def c_daily_traded_value_63d(
    c_daily_traded_value_1d: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    Average daily traded value over roughly one quarter: the ADTV liquidity measure.

    The worked example of a rolling helper over another `c_*` column.  The parameter name is what
    wires it to `c_daily_traded_value_1d` above; the Curator computes that one first.
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

    The provider does not return a raw VWAP column, so it is divided back out of the adjusted one
    using the split ratio derived above.  This is the price the engine charges commission on.
    """

    return m_vwap_split_adjusted / c_split_ratio


def c_vwap_dividend_and_split_adjusted(
    c_dividend_split_ratio: "kaxanuk.data_curator.DataColumn",
    c_vwap: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """VWAP on the same total-return basis as the adjusted close.  The engine's fill price."""

    return c_dividend_split_ratio * c_vwap
