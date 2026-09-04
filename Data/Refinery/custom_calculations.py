"""
Custom `r_*` calculation functions for the Data Refinery stage.

The Curator works one security at a time, so every `c_*` column is a function of that security's
own history.  Two kinds of thing cannot be expressed that way, and both live here:

1.  **Anything that compares securities against each other on a date** -- a rank, a breadth
    reading, a share of the cross-section.  This is what the stage is named for.
2.  **Anything with a fitted parameter.**  The regime label below is per-security, so by the
    naming rule alone it would be a `c_*` column.  It is here instead because it comes out of a
    *model*, and a model has knobs an experiment will sweep -- the jump penalty, the training
    window, the number of regimes.  Widening the Curator's schema forces a refetch of every
    identifier, so putting the model there would mean a network round trip every time somebody
    changed a number.  **A sweep must never cost a download.**  The features the model eats stay
    in the Curator precisely because they carry no knobs: they are frozen at the paper's values.

`Data/refinery.py` resolves each function's parameter names against the columns already built --
the same convention the Curator uses -- so a parameter named `c_sortino_hl21` receives that
Curator column and a parameter named `r_regime` receives the output of the function of the same
name.  Every parameter is a `pandas.Series` aligned to the panel's index, and `m_date`, `ticker`
and any `*_current` column joined from the security master are ordinary panel columns a function
may group by.

One correctness requirement this module exists to enforce: **causality**.  Every cross-sectional
column on date t uses only the cross-section as of t, and every rolling window looks strictly
backward.  A rank taken over the pooled sample, or a mean taken over the whole history, would
leak the future distribution into every row and would not raise a single error doing it.

Rank convention: every `*_rank` column is `rank(pct=True)` per date, ascending, so **1.0 is the
highest raw value in that day's cross-section**.  For return and Sortino that means 1.0 is the
attractive end; for downside deviation it is the risky end.  A percentile stays comparable across
dates even as the number of names with data changes.
"""

__all__ = [
    "CLASSIFICATION_DEPENDENT_COLUMNS",
    "CLIPPING_DEVIATIONS",
    "FEATURE_COLUMNS",
    "JUMP_PENALTY",
    "REFINERY_COLUMNS",
    "REFIT_EVERY_DAYS",
    "REGIMES_COUNT",
    "TRAINING_DAYS",
    "r_downside_deviation_hl21_rank",
    "r_liquidity_rank",
    "r_regime",
    "r_regime_bull",
    "r_regime_bull_breadth",
    "r_return_ewm_hl21_rank",
    "r_sortino_hl21_rank",
    "r_universe_size",
]

import numpy
import pandas

import jump_model

# Output order of the columns this module contributes, appended after the Curator's columns.
# Add an `r_*` function to this tuple and it lands in the output; nothing else registers it.
REFINERY_COLUMNS = (
    "r_regime",
    "r_regime_bull",
    "r_regime_bull_breadth",
    "r_return_ewm_hl21_rank",
    "r_sortino_hl21_rank",
    "r_downside_deviation_hl21_rank",
    "r_liquidity_rank",
    "r_universe_size",
)

# Columns that read a `*_current` column joined from the security master.  `Data/refinery.py`
# skips them with a warning when `Universe/Security_Master.csv` has not been produced yet, so the
# refinery stays runnable before the universe notebook has ever been run.  Empty here: nothing
# below groups by classification, because a classification with no history is a diagnostic rather
# than a selection input.
CLASSIFICATION_DEPENDENT_COLUMNS: tuple[str, ...] = ()

# --- The regime model's configuration --------------------------------------------------------
# These five numbers are the whole model.  They are the first thing an experiment sweeps, and the
# reason the model lives in this stage rather than in the Curator: changing one costs a rerun of
# `Data/refinery.py` and nothing else.
#
# The features are Shu, Yu & Mulvey (2024), Table 2, at the paper's half-lives.  The order is the
# order the model sees them in and has no other meaning.
FEATURE_COLUMNS = (
    "c_return_ewm_hl5",
    "c_return_ewm_hl10",
    "c_return_ewm_hl21",
    "c_downside_deviation_log_hl5",
    "c_downside_deviation_log_hl21",
    "c_sortino_hl5",
    "c_sortino_hl10",
    "c_sortino_hl21",
)
# Outliers are trimmed at three standard deviations of the training window before scaling, so one
# crisis week cannot set the scale for the whole model.
CLIPPING_DEVIATIONS = 3.0
# How reluctant the model is to change its mind.  Zero is k-means and flickers daily; large values
# never switch at all.  Chosen for regime *persistence* -- spells long enough to be tradable --
# and deliberately not for return, because tuning it on P&L is the data-snooping this repository
# is built to avoid.  See `Data/analyzer.ipynb`, which measures what this setting produces.
JUMP_PENALTY = 50.0
# Refit about twice a year, on five years of daily history.
REFIT_EVERY_DAYS = 126
REGIMES_COUNT = 2
TRAINING_DAYS = 1260


def r_downside_deviation_hl21_rank(
    m_date: pandas.Series,
    c_downside_deviation_log_hl21: pandas.Series,
) -> pandas.Series:
    """
    Per-date rank of one-month downside deviation across the assets that have data.

    Note the direction: 1.0 is the **riskiest** asset that day, not the safest, because the rank
    convention is uniform across this module and a column that quietly inverted it would be a trap
    the first time somebody combined two ranks.
    """

    return c_downside_deviation_log_hl21.groupby(m_date).rank(pct=True)


def r_liquidity_rank(
    m_date: pandas.Series,
    c_daily_traded_value_63d: pandas.Series,
) -> pandas.Series:
    """
    Per-date percentile rank of average daily traded value -- the capacity ordering.

    A percentile stays comparable across dates even as the number of names with data changes; a
    raw rank of 3 means something different in a 5-name and a 12-name cross-section.
    """

    return c_daily_traded_value_63d.groupby(m_date).rank(pct=True)


def r_regime(
    ticker: pandas.Series,
    m_date: pandas.Series,
    c_return_1d: pandas.Series,
    c_return_ewm_hl5: pandas.Series,
    c_return_ewm_hl10: pandas.Series,
    c_return_ewm_hl21: pandas.Series,
    c_downside_deviation_log_hl5: pandas.Series,
    c_downside_deviation_log_hl21: pandas.Series,
    c_sortino_hl5: pandas.Series,
    c_sortino_hl10: pandas.Series,
    c_sortino_hl21: pandas.Series,
) -> pandas.Series:
    """
    Which regime each asset is in on each date: 0 is its good state, 1 its bad one.

    One model per asset, each fitted on that asset's own history and refitted as the window rolls
    forward -- see `Data/Refinery/jump_model.py` for what is being minimised and why the label
    returned here is the causal one rather than the smoothed one.

    Null until an asset has `TRAINING_DAYS` of usable history, and null wherever a feature is
    missing.  Downstream that reads as "not investable yet", which is the honest answer; filling
    it forward would invent a regime for a model that had not been fitted.

    The eight features arrive as separate parameters because that is how the refinery wires
    columns to functions.  Listing them out is also the point: this signature is the complete,
    checkable statement of what the model is allowed to see.
    """
    panel = pandas.DataFrame(
        {
            "ticker": ticker,
            "m_date": m_date,
            "c_return_1d": c_return_1d,
            "c_return_ewm_hl5": c_return_ewm_hl5,
            "c_return_ewm_hl10": c_return_ewm_hl10,
            "c_return_ewm_hl21": c_return_ewm_hl21,
            "c_downside_deviation_log_hl5": c_downside_deviation_log_hl5,
            "c_downside_deviation_log_hl21": c_downside_deviation_log_hl21,
            "c_sortino_hl5": c_sortino_hl5,
            "c_sortino_hl10": c_sortino_hl10,
            "c_sortino_hl21": c_sortino_hl21,
        }
    )
    labels = pandas.Series(numpy.nan, index=panel.index, dtype="float64")

    for rows in _grouped_by_ticker(panel):
        # The panel arrives sorted by date then ticker, but sorting again here is what lets this
        # function be read on its own: a rolling model that silently depended on the caller's row
        # order would be correct today and wrong the first time the caller changed.
        ordered = rows.sort_values("m_date")
        labels.loc[ordered.index] = jump_model.rolling_regime_labels(
            ordered[list(FEATURE_COLUMNS)],
            ordered["c_return_1d"],
            training_days=TRAINING_DAYS,
            refit_every_days=REFIT_EVERY_DAYS,
            regimes_count=REGIMES_COUNT,
            jump_penalty=JUMP_PENALTY,
            clipping_deviations=CLIPPING_DEVIATIONS,
        )

    return labels


def r_regime_bull(
    r_regime: pandas.Series,
) -> pandas.Series:
    """
    1.0 when an asset is in its good regime, 0.0 when it is not, null when the model has not run.

    This is the eligibility column the example strategy selects on, kept separate from `r_regime`
    so that raising `REGIMES_COUNT` above two changes what "bull" means in exactly one place.
    """

    return (r_regime == jump_model.REGIME_BULL).astype("float64").where(r_regime.notna())


def r_regime_bull_breadth(
    m_date: pandas.Series,
    r_regime_bull: pandas.Series,
) -> pandas.Series:
    """
    Share of the assets with a regime that day which are in their good one.

    The same value for every asset on a date, so it is a reading about the market rather than
    about a security -- and the most useful one a regime model produces.  It separates "we hold
    six things because six qualified" from "we hold six things because everything qualified", and
    it is what a rule like *go to cash when almost nothing is bullish* would be struck on.
    """

    return r_regime_bull.groupby(m_date).transform("mean")


def r_return_ewm_hl21_rank(
    m_date: pandas.Series,
    c_return_ewm_hl21: pandas.Series,
) -> pandas.Series:
    """
    Per-date rank of one-month exponentially weighted return: cross-sectional momentum.

    The regime model says *whether* an asset is worth holding; this says which of the ones that
    are look strongest against each other today.  Whether that ordering carries any information is
    a question for `Data/analyzer.ipynb`, not for this file.
    """

    return c_return_ewm_hl21.groupby(m_date).rank(pct=True)


def r_sortino_hl21_rank(
    m_date: pandas.Series,
    c_sortino_hl21: pandas.Series,
) -> pandas.Series:
    """
    Per-date rank of the one-month Sortino ratio: cross-sectional return per unit of downside.

    The sibling of the momentum rank, and the more defensible of the two for a multi-asset book,
    because gold and long treasuries are not comparable on raw return but are on return per unit
    of the risk they actually took.
    """

    return c_sortino_hl21.groupby(m_date).rank(pct=True)


def r_universe_size(
    m_date: pandas.Series,
    ticker: pandas.Series,
) -> pandas.Series:
    """
    How many assets carry a row on this date.

    The denominator behind every rank above.  It rises as assets list and falls as they delist, so
    a rank is only comparable across dates once this is known.
    """

    return ticker.groupby(m_date).transform("size")


def _grouped_by_ticker(
    panel: pandas.DataFrame,
) -> list[pandas.DataFrame]:
    """One frame per ticker, in ticker order, so a per-asset model can be run over each."""

    return [
        rows
        for _, rows in panel.groupby("ticker", sort=True)
    ]
