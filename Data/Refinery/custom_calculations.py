"""
Custom `r_*` calculation functions for the Data Refinery stage.

The Curator works one security at a time, so every `c_*` column is a function of that security's
own history.  Two kinds of thing cannot be expressed that way, and both live here:

1.  **Anything that compares securities against each other on a date** -- a rank, a breadth
    reading, a share of the cross-section.  This is what the stage is named for.
2.  **Anything with a fitted parameter**, even when it is per-security.  A model has knobs an
    experiment will sweep, and widening the Curator's schema forces a refetch of every identifier.
    **A sweep must never cost a download.**  Put the model's *inputs* in the Curator, where they
    are frozen arithmetic, and the model itself here.

`Data/refinery.py` resolves each function's parameter names against the columns already built --
the same convention the Curator uses -- so a parameter named `c_daily_traded_value_63d` receives
that Curator column and a parameter named `r_universe_size` receives the output of the function of
the same name.  Every parameter is a `pandas.Series` aligned to the panel's index, and `m_date`,
`ticker` and any `*_current` column joined from the security master are ordinary panel columns a
function may group by.

One correctness requirement this module exists to enforce: **causality**.  Every cross-sectional
column on date t uses only the cross-section as of t, and every rolling window looks strictly
backward.  A rank taken over the pooled sample, or a mean taken over the whole history, would leak
the future distribution into every row and would not raise a single error doing it.

Rank convention: every `*_rank` column is `rank(pct=True)` per date, ascending, so **1.0 is the
highest raw value in that day's cross-section**.  A percentile stays comparable across dates even
as the number of securities with data changes -- and note that it averages to `(n + 1) / 2n`, not
to 0.5, which matters on a narrow universe.

**Your cross-sectional features go here.**  Three columns ship: two that every strategy needs, and
one worked example of per-date normalisation.
"""

__all__ = [
    "CLASSIFICATION_DEPENDENT_COLUMNS",
    "REFINERY_COLUMNS",
    "r_liquidity_rank",
    "r_liquidity_zscore",
    "r_universe_size",
]

import pandas

# Output order of the columns this module contributes, appended after the Curator's columns.
# Add an `r_*` function to this tuple and it lands in the output; nothing else registers it.
REFINERY_COLUMNS = (
    "r_liquidity_rank",
    "r_liquidity_zscore",
    "r_universe_size",
)

# Columns that read a `*_current` column joined from the security master.  `Data/refinery.py`
# skips them with a warning when `Universe/Security_Master.csv` has not been produced yet, so the
# refinery stays runnable before the universe notebook has ever been run.
CLASSIFICATION_DEPENDENT_COLUMNS: tuple[str, ...] = ()


def r_liquidity_rank(
    m_date: pandas.Series,
    c_daily_traded_value_63d: pandas.Series,
) -> pandas.Series:
    """
    Per-date percentile rank of average daily traded value -- the capacity ordering.

    A percentile stays comparable across dates even as the number of securities with data changes;
    a raw rank of 20 means something different in a 300-name and a 780-name cross-section.
    """

    return c_daily_traded_value_63d.groupby(m_date).rank(pct=True)


def r_liquidity_zscore(
    m_date: pandas.Series,
    c_daily_traded_value_63d: pandas.Series,
) -> pandas.Series:
    """
    Per-date z-score of average daily traded value -- the worked example of normalisation.

    Kept beside the rank because the two answer different questions: the rank says where a security
    sits in the order, the z-score says how far it is from the crowd.  Note the grouping by date on
    every statistic: a mean or a deviation taken over the pooled panel would leak the future
    distribution into every row, and nothing would raise an error.
    """
    grouped = c_daily_traded_value_63d.groupby(m_date)
    cross_sectional_mean = grouped.transform("mean")
    cross_sectional_deviation = grouped.transform("std")

    return (
        (c_daily_traded_value_63d - cross_sectional_mean)
        / cross_sectional_deviation.where(cross_sectional_deviation > 0)
    )


def r_universe_size(
    m_date: pandas.Series,
    ticker: pandas.Series,
) -> pandas.Series:
    """
    How many securities carry a row on this date.

    The denominator behind every rank in this module.  It rises as securities list and falls as
    they delist, so a rank is only comparable across dates once this is known.
    """

    return ticker.groupby(m_date).transform("size")
