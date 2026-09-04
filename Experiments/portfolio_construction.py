"""
Step 4: turn an eligible set into a book of weights.

The third shared module, and the seam the KaxaNuk **Portfolio Construction** library will replace.
It is hand-rolled today, and the point of the design is that replacing it is a one-line change in an
experiment notebook rather than a rewrite: everything here is reached through a single function
signature.

## The contract

A **weigher** is any function with this shape:

    weigher(
        eligible_securities: pandas.Index,      # what may be held on this rebalance date
        returns_history: pandas.DataFrame,      # daily returns, ending STRICTLY BEFORE that date
        settings: ConstructionSettings,
    ) -> pandas.Series                          # weights, non-negative, summing to at most 1.0

Two of them ship here: `equal_weight` and `inverse_volatility`.  A minimum-variance optimiser, a
hierarchical risk parity allocator, or a call into the Portfolio Construction library are all the
same shape, and `build_target_weights` neither knows nor cares which it was handed.

**A weigher never sees a date.**  It is given a history that has already been cut off before the
day it is weighting, which is what makes look-ahead impossible to introduce by accident inside one:
there is no future available to reach for.  The cut is made in one place, `build_target_weights`,
and it is a single line -- `returns.index < rebalance_date` -- so it can be checked by reading.

## Weights sum to at most one, not to exactly one

A defensive strategy is a strategy that is sometimes not fully invested, so a book that must sum to
1.0 cannot express one.  Every function here returns weights summing to **at most** 1.0, and the
residual becomes cash: `backtest_engine.to_engine_frame` parks it in a real, priced,
transaction-costed instrument, because the engine's weight file has no cash row of its own.

Nothing eligible means an empty book, which means 100% cash.  That is a position, and a deliberate
one.
"""

__all__ = [
    "ConstructionSettings",
    "build_target_weights",
    "equal_weight",
    "inverse_volatility",
    "lag_eligibility",
    "rebalance_dates_on_change",
]

import dataclasses
import typing

import numpy
import pandas


@dataclasses.dataclass(frozen=True)
class ConstructionSettings:
    """
    The constraints every weigher respects, kept apart from the weigher itself.

    Separating them is what lets two weighting schemes be compared without also changing the
    constraints, which is the only way to tell which of the two changes mattered.

    The defaults switch every constraint **off** -- one security may hold the whole book, one
    security is enough to be invested -- because a constraint is a lever, and this repository adds
    levers one at a time so each has to earn its place against the simpler baseline.
    """

    maximum_weight: float = 1.0
    minimum_holdings: int = 1
    risk_lookback_days: int = 63


def build_target_weights(
    buyable: pandas.DataFrame,
    rebalance_dates: pandas.DatetimeIndex,
    returns: pandas.DataFrame,
    weigher: typing.Callable[
        [
            pandas.Index,
            pandas.DataFrame,
            ConstructionSettings,
        ],
        pandas.Series,
    ],
    settings: ConstructionSettings,
) -> pandas.DataFrame:
    """
    Strike the book on every rebalance date, using only what was knowable before each one.

    `buyable` is a `dates x securities` boolean of what may be held, already lagged by the caller
    (see `lag_eligibility`) and already intersected with what can actually be traded that day.

    The returned frame is `rebalance_dates x securities`; a date on which nothing was eligible is
    kept as an all-zero row rather than dropped, because "the book went to cash on this date" is an
    instruction the engine needs to receive, and a missing row would instead mean "carry on holding
    whatever you had".
    """
    rows = {}
    for rebalance_date in rebalance_dates:
        eligible_today = buyable.loc[rebalance_date]
        eligible_securities = eligible_today.index[eligible_today.to_numpy()]
        # The one line that makes the whole module causal: strictly before, never up to and
        # including.  `.loc[:date]` would include the rebalance date itself.
        history = returns.loc[returns.index < rebalance_date].tail(settings.risk_lookback_days)
        rows[rebalance_date] = weigher(eligible_securities, history, settings)

    weights = pandas.DataFrame(
        rows,
        index=buyable.columns,
    ).T.reindex(
        columns=buyable.columns,
    )
    weights.index = pandas.DatetimeIndex(rebalance_dates)

    return weights.fillna(0.0)


def equal_weight(
    eligible_securities: pandas.Index,
    returns_history: pandas.DataFrame,
    settings: ConstructionSettings,
) -> pandas.Series:
    """
    One over N across the eligible securities.  The control every other scheme has to beat.

    It ignores `returns_history` entirely, which is its whole appeal: there is no parameter to
    estimate, so there is nothing to estimate wrongly.  On a small universe that is a real
    advantage rather than a handicap -- an estimated covariance over twelve assets is mostly noise,
    and a scheme built on it can lose to this one on out-of-sample data alone.
    """
    if len(eligible_securities) < settings.minimum_holdings:

        return pandas.Series(dtype="float64")

    raw = pandas.Series(
        1.0 / len(eligible_securities),
        index=eligible_securities,
    )

    return _apply_constraints(raw, settings)


def inverse_volatility(
    eligible_securities: pandas.Index,
    returns_history: pandas.DataFrame,
    settings: ConstructionSettings,
) -> pandas.Series:
    """
    Weight each eligible security by the reciprocal of its recent volatility.

    The economically coherent partner to a signal that identifies *calm*: if the model's finding is
    about risk rather than return, then sizing by risk is spending the signal on what it actually
    measured.  Equal weight, by contrast, gives a calm bond ETF and a calm small-cap ETF the same
    weight and therefore very different risk.

    A security with no usable volatility -- too little history, or a window in which it never moved
    -- is dropped rather than guessed at.  If that leaves nothing, the book is cash: silently
    falling back to equal weight would hide a data problem behind a plausible number.
    """
    if len(eligible_securities) < settings.minimum_holdings:

        return pandas.Series(dtype="float64")

    volatility = returns_history.reindex(columns=eligible_securities).std()
    usable = volatility[numpy.isfinite(volatility) & (volatility > 0.0)]
    if len(usable) == 0:

        return pandas.Series(dtype="float64")

    inverse = 1.0 / usable

    return _apply_constraints(inverse / inverse.sum(), settings)


def lag_eligibility(
    eligible: pandas.DataFrame,
    lag_days: int,
) -> pandas.DataFrame:
    """
    The eligible set as it was known `lag_days` trading days earlier.

    This is the point-in-time discipline made into one call rather than a `shift` scattered through
    a notebook: the decision struck on day t may only use information from day `t - lag_days`.  The
    fill is False, so the warm-up at the start of the sample holds nothing rather than everything.

    **Apply this to the signal, then intersect with today's tradability** -- in that order.  A
    security has to have been *authorised* yesterday and be *sellable* today, and those are two
    different days on purpose.
    """

    return eligible.shift(
        lag_days,
        fill_value=False,
    ).astype(bool)


def rebalance_dates_on_change(
    buyable: pandas.DataFrame,
) -> pandas.DatetimeIndex:
    """
    The days the eligible set changed, which for an event-driven rule are the days it trades.

    The first day anything is eligible counts as a change, because going from holding nothing to
    holding something is a trade.  Between changes the book drifts and nothing is done: a signal
    that has not moved is not a reason to pay commission, and a calendar rebalance on an unchanged
    set is pure cost.
    """
    changed = buyable.ne(buyable.shift(1, fill_value=False)).any(axis=1)

    return buyable.index[changed.to_numpy()]


def _apply_constraints(
    raw_weights: pandas.Series,
    settings: ConstructionSettings,
) -> pandas.Series:
    """
    Cap each weight, and let whatever the cap frees up become cash rather than be redistributed.

    Redistributing would keep the book fully invested at the cost of quietly breaking the cap on
    the securities that were already at it, which is the wrong trade: a cap exists to bound a single
    position, and the honest response to "there are too few things to hold" is to hold less.
    """
    capped = raw_weights.clip(upper=settings.maximum_weight)

    return capped[capped > 0.0]
