# Journal — Experiment 1

> **Append-only, dated, oldest first.** Every iteration of this experiment, in the order it
> happened. Maintained by the AI as work proceeds.
>
> **Earlier entries are never edited.** The one exception is correcting an error, and the correction
> is written as a new entry saying what was wrong — not by rewriting the original.
>
> The hypothesis is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md); what to try next is in
> [`BRAINSTORMING_1.md`](BRAINSTORMING_1.md); the results that survive are in
> [`FINDINGS_1.md`](FINDINGS_1.md).
>
> **Paths and figures inside entries are as they were written.** Where a path has since moved the
> entry is left alone — it was correct on its date. Repository-level history — choosing the
> benchmark, the data step, the architecture — belongs in this journal, Experiment 1 being the
> declared benchmark and therefore the shared context; later experiments' journals point here
> rather than copying it.
>
> **Entry format:**
>
> ```
> ## YYYY-MM-DD — <short topic>
>
> - Idea / question:
> - What we tried / considered:
> - Outcome / decision:
> - Open threads:
> ```

---

## 2026-09-03 — Universe, data and the regime model

- **Idea / question:** can a statistical jump model, fitted per asset on its own history, say
  usefully which asset classes are worth holding today?
- **What we tried / considered:** replaced the 787-name US-equity seed with the twelve asset-class
  ETFs of Shu, Yu & Mulvey (2024). Put the paper's eight features in the Curator as `c_*` (pure
  arithmetic, no fitted parameter) and the model itself in the Refinery as `r_*`, so a penalty sweep
  costs a `refinery.py` run and never a download. Wrote the model by hand in
  `Data/Refinery/jump_model.py` rather than taking the `jumpmodels` dependency, so the algorithm is
  readable in one file.
- **Outcome / decision:** the signal separates **risk, not return** — lower forward volatility on 11
  of 12 assets, higher forward return on only 5, at every jump penalty from 5 to 100. Reading the
  same fitted model smoothed instead of causally is worth **44 annualised points**, which is now the
  repository's own evidence for the look-ahead control. Jump penalty fixed at 50 on *persistence*
  (median spell 43 trading days), deliberately not on return.
- **Open threads:** the source paper adds a supervised layer that forecasts tomorrow's regime; we
  have implemented only the identification half, and that is the stated remedy for the return
  result.

## 2026-09-03 — Experiment 1's blueprint, written before the rule

- **Idea / question:** what should the simplest possible book built on this signal do?
- **What we tried / considered:** fixed four predictions in `BLUEPRINT_1.md` from the analyzer's
  measurements, before writing the rule cell — volatility falls, return does not rise, Sharpe
  improves through the denominator, and cash is a large time-varying part of the book.
- **Outcome / decision:** benchmark rule frozen as equal weight over the eligible set, cash
  otherwise, event-driven, one day of lag. Three levers declined on purpose: a weight cap, a
  minimum holding count, and inverse-volatility sizing.
- **Open threads:** costs. Nothing in the analyzer licensed a prediction about turnover, so it was
  written down as the one genuinely open question.

## 2026-09-03 — Step 4 built, and prediction 4 falsified

- **Idea / question:** does the benchmark book behave the way the blueprint expected?
- **What we tried / considered:** built `Experiments/portfolio_construction.py` as a single swappable
  signature — eligible securities plus a returns history already cut off before the date, returning
  weights that sum to **at most** one. Shipped `equal_weight` and `inverse_volatility` behind it.
  Relaxed the notebook's sum-to-1.0 invariant, which a strategy that can go to cash cannot satisfy.
- **Outcome / decision:** the book is 461 rebalances, 40 a year, ~810% one-way annual turnover, 6.5
  holdings on average — and **95.3% invested**, against a predicted ~55%. Prediction 4 is
  **falsified**. Breadth decides how many assets are held, not how much is invested: equal weight
  over a shrinking eligible set concentrates rather than de-risking, at the extreme into one asset
  at 100%. The benchmark is a **rotation, not a risk reducer**, and the two levers it declined turn
  out to be the whole mechanism by which the paper's version goes defensive.
- **Open threads:** the book has never been priced — the licensed engines are not installed in this
  clone, so predictions 1 to 3 stay open. At 810% turnover, whether anything survives commission is
  the only question that matters next.
