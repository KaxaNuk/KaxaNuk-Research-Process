"""
Custom `r_*` calculation functions for the Data Refinery stage.

The Data Curator works one ticker at a time: every `c_*` column is a function of that ticker's
own history and nothing else.  A rank or a breadth reading is a statement about names *relative
to each other on a given date*, which no per-ticker calculation can express.  Those live here,
as `r_*` columns.

`Data/refinery.py` resolves each function's parameter names against the columns it has already
built -- the same convention the Data Curator uses -- so a parameter named
`c_daily_traded_value_63d` receives that Curator column and a parameter named `r_liquidity_rank`
receives the output of the function of the same name.  Dependency order comes from the
signatures, not from the order of definition in this file.  Every parameter is a `pandas.Series`
aligned to the panel's index, and `m_date`, `ticker` and `sector_current` are ordinary panel
columns available to any function that needs to group by them.

One correctness requirement this module exists to enforce: **causality**.  Every cross-sectional
column on date t uses only the cross-section as of t, and every rolling window looks strictly
backward.  All ranking and normalisation is per date, over that date's names only; a z-score
computed over the pooled sample would leak the future distribution into every row.

The template ships four columns.  Three are infrastructure every strategy needs --
`r_return_1d`, `r_universe_size`, `r_liquidity_rank` -- and one, `r_liquidity_zscore`, is the
worked example of per-date normalisation.  Your candidate features go here too: a feature earns
its place in `Data/analyzer.ipynb`, where its information coefficient is measured, before any
book is built on it.

Rank convention: every `*_rank` column is `rank(pct=True)` per date, ascending -- 1.0 is the
highest raw value in that day's cross-section.  A percentile is comparable across dates even
though the number of names with data changes.
"""

__all__ = [
    "REFINERY_COLUMNS",
    "SECTOR_DEPENDENT_COLUMNS",
    "r_liquidity_rank",
    "r_liquidity_zscore",
    "r_return_1d",
    "r_universe_size",
]

import pandas

# Output order of the columns this module contributes, appended after the Curator's columns.
# Add a new `r_*` function to this tuple and it lands in the output; nothing else registers it.
REFINERY_COLUMNS = (
    "r_return_1d",
    "r_liquidity_rank",
    "r_liquidity_zscore",
    "r_universe_size",
)

# Columns that need the security master's classification join (`sector_current`).
# `Data/refinery.py` skips them with a warning when `Universe/Security_Master.csv` has not been
# produced yet, so the refinery stays runnable before the universe notebook has ever been run.
# Empty in the template; list any sector-relative feature you add here.
SECTOR_DEPENDENT_COLUMNS: tuple[str, ...] = ()


def r_liquidity_rank(
    m_date: pandas.Series,
    c_daily_traded_value_63d: pandas.Series,
) -> pandas.Series:
    """
    Per-date percentile rank of average daily traded value.

    A percentile is comparable across dates even though the number of names with data changes; a
    raw rank of 20 means something different in a 300-name and a 780-name cross-section.
    """

    return c_daily_traded_value_63d.groupby(m_date).rank(pct=True)


def r_liquidity_zscore(
    m_date: pandas.Series,
    c_daily_traded_value_63d: pandas.Series,
) -> pandas.Series:
    """
    Per-date z-score of average daily traded value -- the worked example of normalisation.

    Kept alongside the rank because the two answer different questions: the rank says where a
    name sits in the order, the z-score says how far it is from the crowd.  Note the grouping by
    date on every statistic: a mean or deviation taken over the pooled panel would leak the
    future distribution into every row.
    """
    grouped = c_daily_traded_value_63d.groupby(m_date)
    cross_sectional_mean = grouped.transform("mean")
    cross_sectional_deviation = grouped.transform("std")

    return (
        (c_daily_traded_value_63d - cross_sectional_mean)
        / cross_sectional_deviation.where(cross_sectional_deviation > 0)
    )


def r_return_1d(
    ticker: pandas.Series,
    m_close_dividend_and_split_adjusted: pandas.Series,
) -> pandas.Series:
    """
    One-day total return, computed within each ticker.

    Grouping by ticker is what stops the first row of one name differencing against the last row
    of the previous one in the stacked panel.
    """

    return m_close_dividend_and_split_adjusted.groupby(ticker).pct_change()


def r_universe_size(
    m_date: pandas.Series,
    ticker: pandas.Series,
) -> pandas.Series:
    """
    How many names carry a row on this date.

    The denominator behind every rank in this module.  It rises as names list and falls as they
    delist, so a rank is only comparable across dates once this is known.
    """

    return ticker.groupby(m_date).transform("size")
