---
source: https://www.nber.org/papers/w20439
citation: "Daniel, K., & Moskowitz, T. J. (2016). Momentum crashes. Journal of Financial Economics, 122(2), 221-247. Circulated as NBER Working Paper No. 20439. Link last checked 2026-09-10."
local_copy: none
read: "2026-09-10 — published citation and headline result verified against the publisher's record, the NBER working-paper record and the abstract; not a full re-read of the paper. Verify any number against the source before quoting it."
---

<!-- example: begin -->

# Daniel & Moskowitz (2016) — Momentum Crashes

*The abstract only, with the citation checked against the publisher's and the NBER working-paper
records — not the full paper.*

## Why it is here

*What is not claimed* in [`OBJECTIVE.md`](../../OBJECTIVE.md) — not that momentum is safe — which
qualifies claim 1: *a positive twelve-month return, skipping the most recent month, selects stocks
whose following month beats the universe average*.

What the drawdown is expected to look like, so that when it arrives nobody mistakes it for a broken
pipeline.

## Momentum suffers infrequent but severe crashes

The strategy's long-run record is punctuated by rare episodes of very large losses. They are not
spread through the sample; they are concentrated in a small number of periods, and they are large
enough to dominate the return distribution's left tail.

> **For claim 1:** the shape of this book's worst period is a known shape, and it is written down
> before the backtest so that it cannot later be explained away. A deep, fast drawdown in this
> strategy is evidence of momentum behaving as documented — not, on its own, evidence of a bug. The
> reverse also holds and matters more: **a backtest of a momentum book that shows no such episode is
> a backtest to distrust**, and that is a check `FINDINGS_1.md` should run rather than a reassurance
> to take.

## The crashes come in panic states — high volatility following market declines — when the market rebounds

The losses concentrate when the market has fallen and volatility is high, and they are realised as
the market turns back up. Momentum's market beta is time-varying, turning sharply negative after
bear markets, so the strategy is short the market precisely into the rebound. The paper reports the
losses are partly forecastable from those conditions.

> **For claim 1:** the mechanism is the short leg meeting a rebound, and our book has no short leg.
> That is the most important line in this note for us, and it cuts both ways.
>
> Long-only with a cash residual, the failure mode is different in kind: after a market fall almost
> nothing has positive twelve-month momentum, the eligible set empties, the book sits in cash, and
> it **misses the rebound** rather than being run over by it. Missing a rebound is a smaller loss
> than the paper's and a real one.
>
> **So this is a prediction, not an inherited result:** the strategy's worst episodes should be
> periods of *underperformance while holding cash after a decline*, not sudden losses. If instead
> the drawdowns look like the paper's, something about our construction is not what we think it is.

## What it changes

- **The drawdown shape is predicted before the backtest:** underperformance while holding cash after
  a decline, not sudden losses. Drawdowns that look like the paper's mean the construction is not
  what we think it is.
- **A backtest of this book with no crash-like episode is one to distrust**, and `FINDINGS_1.md`
  runs that check rather than taking the reassurance.
- **The forecastability it offers is not used here.** The paper's dynamic, volatility-aware
  weighting is a real lever, and taking it now would break the one-lever-at-a-time constraint in
  [`OBJECTIVE.md`](../../OBJECTIVE.md). It is a later experiment, and it has to beat this one.
- **How often the eligible set empties is measured in `Data/analyzer.ipynb` before any book is
  run.** It is a property of our universe and our screen, and worth knowing early: a rule that is
  fully in cash for long stretches is a different product from the one described.
- **Does not settle** the size of our crashes: its magnitudes describe a long-short, broad-universe
  construction, and borrowing them for a long-only liquid book that was never tested is the kind of
  thing [`AGENTS.md`](../../AGENTS.md) exists to stop.

<!-- example: end -->
