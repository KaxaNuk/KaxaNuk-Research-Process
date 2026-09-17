---
source: https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1990.tb05110.x
citation: "Jegadeesh, N. (1990). Evidence of Predictable Behavior of Security Returns. The Journal of Finance, 45(3), 881-898. DOI 10.1111/j.1540-6261.1990.tb05110.x. Link last checked 2026-09-10."
local_copy: none
read: "2026-09-10 — published citation and headline result verified against the publisher's record and the abstract; not a full re-read of the paper. Verify any number against the source before quoting it."
---

<!-- example: begin -->

# Jegadeesh (1990) — Evidence of Predictable Behavior of Security Returns

*The abstract only, with the citation checked against the publisher's record — not the full paper.*

## Why it is here

Claim 1 of [`OBJECTIVE.md`](../../OBJECTIVE.md) — *a positive twelve-month return, skipping the
most recent month, selects stocks whose following month beats the universe average*.

**The note that changed the design.** It is the reason the momentum column is `r_momentum_12_1` and
not `r_momentum_12_0`.

## Monthly security returns are negatively serially correlated at the one-month horizon

Individual stock returns show significant negative first-order serial correlation month to month.
Last month's strongest performers tend to underperform in the month that follows, and the effect is
strong enough to build a profitable contrarian rule on.

> **For claim 1:** the most recent month runs the opposite way to the twelve-month effect. A
> formation window ending on the trade date therefore contains a reversal and a continuation pulling
> against each other, and the column measures the difference between two things rather than one
> thing. That is not a small distortion to accept for simplicity: it is a signal built out of two
> signals with opposite signs.
>
> **So the window ends one month before the trade.** The design decision is recorded here rather
> than in the notebook, because the reason is a citation and the notebook is not where citations
> live.

## The predictability is at a horizon distinct from longer-run momentum

The reversal is a one-month phenomenon. It does not contradict continuation measured over longer
formation windows; it sits beside it at a different horizon.

> **For claim 1:** this is why the fix is a skip rather than a sign flip. We are not choosing between
> reversal and momentum, and we are not claiming reversal is absent — we are removing the segment
> where the two disagree so that `r_momentum_12_1` measures continuation alone.
>
> Short-term reversal is a real signal and a legitimate later experiment. It is not this one, and
> mixing them by accident is exactly what this note prevents.

## What it changes

- **The formation window ends one month before the trade:** the column is `r_momentum_12_1`, not
  `r_momentum_12_0`.
- **The fix is a skip, not a sign flip.** Only the segment where reversal and continuation disagree
  is removed, so the column measures continuation alone.
- **Short-term reversal stays out of this experiment** — a real signal, and a legitimate later one.
- **The skip is principled rather than fitted**, which is what [`OBJECTIVE.md`](../../OBJECTIVE.md)
  claims under *what is not claimed*. A two-month skip, or none, are points on a curve a later
  experiment sweeps and publishes.
- **The reversal's size inside the liquid quintile is measured in `Data/analyzer.ipynb`, not
  assumed.** Microstructure effects that drive short-horizon reversal are usually weaker in heavily
  traded names, which would make the skip cheaper for us than for the paper, or unnecessary.
- **Does not settle** whether the one-month skip is optimal, or how large the reversal is in our
  universe — the liquid quintile is not the paper's sample.

<!-- example: end -->
