"""
A statistical jump model, small enough to read in one sitting.

This is the model behind the example strategy.  It answers one question per asset per day: **is
this asset in its good regime or its bad one?**  It is unsupervised -- nobody labels the days --
and it is deliberately reluctant to change its mind, which is the whole idea.

## What it optimises

Given a matrix of features `x` and `K` regimes, pick a label for every day so as to minimise

    sum over days of  0.5 * ||x_t - centre[label_t]||^2   +   penalty * (number of label changes)

The first term is ordinary clustering: put each day with the regime whose average day it most
resembles.  The second term is what makes it a *jump* model.  With `penalty = 0` this is k-means
and the labels flicker day to day; raise it and the model will only switch when the features have
moved far enough, for long enough, to pay the fee.  **The penalty is the one knob that matters**,
and it is a direct expression of how much turnover you are willing to buy regime accuracy with.

## Two ways to read the same model, and only one of them is tradable

    _smoothed_labels    the best label sequence for a *finished* stretch of history.  Every day's
                        label is allowed to depend on what happened afterwards, so this is what
                        training uses and what a chart of "where the regimes were" should show.

    _advance_values     the label for today given only today and everything before it.  This is
                        the same recursion stopped one step early -- no looking back from the
                        future -- and it is the only version a strategy may trade on.

Reporting the smoothed labels as if they were tradable is one of the easiest look-ahead mistakes
to make with a regime model, because the two series look almost identical on a chart and differ
exactly at the turning points, which is where all the money is.  `rolling_regime_labels` returns
the causal one.

## The rolling scheme

The model is refitted as it walks forward, so no day is ever labelled by a model that was trained
on it:

    |<---- training_days ---->|<- refit_every_days ->|<- refit_every_days ->|
    [ fit centres here .......][ label these days ...]
                              [ fit again ..........][ label these days ...]

Each fit uses the `training_days` most recent usable observations *strictly before* the first day
it will label.  Everything the fit produces -- the clipping bounds, the standardisation, the
centres -- comes from that window alone.

## What it does not do

It does not *forecast* the regime; it identifies the one in force.  The paper this repository
works through adds a supervised layer on top that predicts tomorrow's regime from today's
features plus macro data.  That layer is a strategy decision, not a data one, so it belongs in an
experiment rather than here.
"""

__all__ = [
    "RegimeModel",
    "fit_regime_model",
    "rolling_regime_labels",
]

import dataclasses

import numpy
import pandas

# Regime 0 is always the one with the highest average training return, because `fit_regime_model`
# sorts the centres that way before returning them.  Without that step the label numbers would be
# arbitrary and would flip between refits, which would turn every refit into a fake regime change.
REGIME_BULL = 0

MAX_FIT_ITERATIONS = 30


@dataclasses.dataclass(frozen=True)
class RegimeModel:
    """
    One fitted model: how to trim an observation, how to scale it, and where the regimes sit.

    All five arrays come from a single training window, and inference applies them unchanged.
    Refitting produces a new instance rather than mutating this one, so a model can always be
    traced back to the window that made it.
    """

    lower_bound: numpy.ndarray
    upper_bound: numpy.ndarray
    location: numpy.ndarray
    scale: numpy.ndarray
    centers: numpy.ndarray


def fit_regime_model(
    training_features: numpy.ndarray,
    training_returns: numpy.ndarray,
    *,
    regimes_count: int,
    jump_penalty: float,
    clipping_deviations: float,
) -> RegimeModel:
    """
    Fit regime centres on one training window, by alternating labels and centres until settled.

    The loop is coordinate descent on the objective in the module docstring: hold the centres and
    solve exactly for the best label sequence, then hold the labels and set each centre to the
    mean of its days.  Both halves can only lower the objective, so it converges, and in practice
    it settles in well under ten passes.

    Labels start from the *returns*, not from a random draw: the best days go into regime 0 and
    the worst into the last one.  That makes the fit deterministic -- the same window always gives
    the same model, which is what lets a result be reproduced -- and it starts the search from an
    arrangement that already means something.
    """
    lower_bound = numpy.nanmean(training_features, axis=0) - clipping_deviations * numpy.nanstd(
        training_features,
        axis=0,
    )
    upper_bound = numpy.nanmean(training_features, axis=0) + clipping_deviations * numpy.nanstd(
        training_features,
        axis=0,
    )
    clipped = numpy.clip(training_features, lower_bound, upper_bound)

    location = clipped.mean(axis=0)
    scale = clipped.std(axis=0)
    # A feature that never moves inside the window would divide by zero and blow up every
    # distance; leaving it at 1.0 makes it a constant offset instead, which the centres absorb.
    scale = numpy.where(scale > 0.0, scale, 1.0)
    scaled = (clipped - location) / scale

    labels = _initial_labels(training_returns, regimes_count)
    centers = _regime_centers(scaled, labels, regimes_count)
    for _ in range(MAX_FIT_ITERATIONS):
        updated_labels = _smoothed_labels(_regime_losses(scaled, centers), jump_penalty)
        if numpy.array_equal(updated_labels, labels):

            break

        labels = updated_labels
        centers = _regime_centers(scaled, labels, regimes_count)

    ordering = _order_by_mean_return(training_returns, labels, regimes_count)

    return RegimeModel(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        location=location,
        scale=scale,
        centers=centers[ordering],
    )


def rolling_regime_labels(
    features: pandas.DataFrame,
    returns: pandas.Series,
    *,
    training_days: int,
    refit_every_days: int,
    regimes_count: int,
    jump_penalty: float,
    clipping_deviations: float,
) -> pandas.Series:
    """
    Walk one asset's history forward, refitting periodically, and label each day causally.

    The result is aligned to `features.index` and is null everywhere the model could not speak:
    rows with an incomplete feature vector, and the whole warm-up stretch before the first
    training window has filled.  A null is the honest answer there, and the experiment stage is
    expected to treat it as "not investable yet" rather than to fill it.

    The running value vector is carried across refit boundaries rather than reset.  That is what
    stops a refit reading as a regime change on its own: the penalty keeps applying across the
    seam, so a new model has to actually disagree with the old one to move the label.
    """
    labels = pandas.Series(numpy.nan, index=features.index, dtype="float64")
    feature_values = features.to_numpy(dtype="float64")
    return_values = returns.to_numpy(dtype="float64")

    usable_positions = numpy.flatnonzero(
        numpy.isfinite(feature_values).all(axis=1)
        & numpy.isfinite(return_values)
    )
    if len(usable_positions) <= training_days:

        return labels

    model = None
    values = None
    days_since_fit = 0
    for offset, position in enumerate(usable_positions):
        if offset < training_days:

            continue

        if model is None or days_since_fit >= refit_every_days:
            # The window ends at `offset`, exclusive: the model never sees the day it labels.
            training_positions = usable_positions[offset - training_days:offset]
            model = fit_regime_model(
                feature_values[training_positions],
                return_values[training_positions],
                regimes_count=regimes_count,
                jump_penalty=jump_penalty,
                clipping_deviations=clipping_deviations,
            )
            days_since_fit = 0

        observation = numpy.clip(
            feature_values[position],
            model.lower_bound,
            model.upper_bound,
        )
        scaled = (observation - model.location) / model.scale
        losses = _regime_losses(scaled.reshape(1, -1), model.centers)[0]
        values = _advance_values(values, losses, jump_penalty)
        labels.iloc[position] = float(values.argmin())
        days_since_fit += 1

    return labels


def _advance_values(
    values: numpy.ndarray | None,
    losses: numpy.ndarray,
    jump_penalty: float,
) -> numpy.ndarray:
    """
    Carry the running cost of ending in each regime forward by one day.

    The cost of arriving in regime k today is today's loss for k, plus the cheapest way of having
    been anywhere yesterday.  Because every switch costs the same, that cheapest way is one of
    only two things -- stay in k, or come from whichever regime was cheapest and pay the penalty
    -- which is why this is two lines rather than a matrix.

    `argmin` over the result is today's label using only today and everything before it.  The
    running minimum is subtracted each step so the numbers stay small over a long history;
    subtracting the same amount from every regime cannot change which one wins.
    """
    if values is None:

        return losses - losses.min()

    cheapest_arrival = numpy.minimum(values, values.min() + jump_penalty)
    advanced = losses + cheapest_arrival

    return advanced - advanced.min()


def _initial_labels(
    training_returns: numpy.ndarray,
    regimes_count: int,
) -> numpy.ndarray:
    """
    Seed the fit by splitting the training days into equal buckets, best return first.

    Day-by-day returns are a noisy label, and deliberately so: the point is only to give the
    centres a starting arrangement that is deterministic and already ordered good-to-bad.  The
    smoothing step takes over from there.
    """
    ranks = pandas.Series(training_returns).rank(pct=True).to_numpy()

    return numpy.clip(
        ((1.0 - ranks) * regimes_count).astype("int64"),
        0,
        regimes_count - 1,
    )


def _order_by_mean_return(
    training_returns: numpy.ndarray,
    labels: numpy.ndarray,
    regimes_count: int,
) -> numpy.ndarray:
    """
    The permutation that puts the highest-earning regime first, so regime 0 always means bull.

    A regime the fit left empty sorts last, because a centre nothing was assigned to cannot be
    the good one.
    """
    mean_returns = numpy.full(regimes_count, -numpy.inf)
    for regime in range(regimes_count):
        members = labels == regime
        if members.any():
            mean_returns[regime] = training_returns[members].mean()

    return numpy.argsort(-mean_returns, kind="stable")


def _regime_centers(
    scaled: numpy.ndarray,
    labels: numpy.ndarray,
    regimes_count: int,
) -> numpy.ndarray:
    """
    The average scaled observation in each regime.

    A regime with no days keeps the overall mean, which leaves it a live candidate for the next
    pass instead of silently collapsing the model to fewer regimes.
    """
    overall_mean = scaled.mean(axis=0)
    centers = numpy.tile(overall_mean, (regimes_count, 1))
    for regime in range(regimes_count):
        members = labels == regime
        if members.any():
            centers[regime] = scaled[members].mean(axis=0)

    return centers


def _regime_losses(
    scaled: numpy.ndarray,
    centers: numpy.ndarray,
) -> numpy.ndarray:
    """Half the squared distance from every observation to every centre, shaped (days, regimes)."""
    differences = scaled[:, numpy.newaxis, :] - centers[numpy.newaxis, :, :]

    return 0.5 * (differences ** 2).sum(axis=2)


def _smoothed_labels(
    losses: numpy.ndarray,
    jump_penalty: float,
) -> numpy.ndarray:
    """
    The exact best label sequence for a finished stretch of history.

    Forward pass accumulates the cheapest cost of ending each day in each regime and remembers
    where that came from; the backward pass reads the winning path off those pointers.  This is
    the standard dynamic program, and it is exact rather than approximate because the penalty
    depends only on whether the label changed, never on which regime it changed to.

    **Training only.**  Every label here can depend on days that came after it, which is exactly
    what makes it unusable as a signal -- see the module docstring.
    """
    day_count, regimes_count = losses.shape
    values = losses[0].copy()
    predecessors = numpy.zeros((day_count, regimes_count), dtype="int64")

    for day in range(1, day_count):
        cheapest_regime = int(values.argmin())
        switch_cost = values[cheapest_regime] + jump_penalty
        staying = values <= switch_cost
        predecessors[day] = numpy.where(staying, numpy.arange(regimes_count), cheapest_regime)
        values = losses[day] + numpy.where(staying, values, switch_cost)

    labels = numpy.zeros(day_count, dtype="int64")
    labels[-1] = int(values.argmin())
    for day in range(day_count - 1, 0, -1):
        labels[day - 1] = predecessors[day][labels[day]]

    return labels
