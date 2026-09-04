# Blueprint — Experiment 1

> **The hypothesis, fixed once written.** Thesis, rules, success criteria and key risks, recorded
> *before* any code runs.
>
> **This file does not change when results arrive.** A hypothesis edited after its test is no longer
> a hypothesis — that is the whole reason it is kept apart from the result. What the experiment
> actually produced is in [`FINDINGS_1.md`](FINDINGS_1.md).
>
> Planning lives in [`BRAINSTORMING_1.md`](BRAINSTORMING_1.md), the running log in
> [`JOURNAL_1.md`](JOURNAL_1.md).
>
> Recorded 2026-09-03, at v0.3.0, before the notebook's rule cell was written. The four predictions
> in *What this experiment should show* were fixed from `Data/analyzer.ipynb` **before** any book was
> constructed and before the engine had ever been run on this universe.

---

## Experiment 1 — Regime Rotation, the declared benchmark

### Thesis

Hold every asset class that its own jump model currently calls calm, in equal weight, and hold cash
for the rest. That is the whole rule. It is the least clever thing that uses the regime signal at
all, and that is precisely why it is the benchmark: **every later idea — risk weighting, a
cross-sectional tilt, a forecasting layer, a cap — has to beat this to justify its own complexity.**

It is a deliberately modest yardstick. It does not claim the regime model is the best available
regime model, only that the signal is simple enough to be understood, that the assets are liquid
enough to be traded in size, and that the resulting book is stable enough to measure other things
against. Equal weighting is not a straw man: on a small universe it is a
[hard control to beat](../../Bibliotheca/BIBLIOGRAPHY.md), and it has no estimated parameters to be
wrong about.

### Rules

- **Selection.** An asset is eligible when `r_regime_bull == 1.0` — its own model, fitted on its own
  five years of history and refitted twice a year, currently places it in the higher-return regime.
  Null counts as ineligible: during the model's warm-up window nothing is held.
- **Sizing.** Equal weight across every eligible asset. No cap and no minimum holding count in this
  experiment — both exist in `Experiments/portfolio_construction.py` and are switched **off** here,
  because a constraint is a lever and levers get added one at a time.
- **Cash.** The uninvested residual goes to `BIL`, a real, priced, transaction-costed instrument.
  The engine's weight file has no cash row, so "go to cash" has to be expressible as a holding.
  **When nothing is eligible the book is 100% BIL.**
- **Timing.** Event-driven: the book is re-struck only on days the eligible set changes. Between
  triggers weights drift and nothing trades. A regime signal that has not changed is not a reason to
  pay commission.
- **Lag.** The set used on rebalance date *t* is the one observed at *t−1*, and the engine fills at
  *t*'s VWAP — one full day between the label and the fill. The source paper uses one more day than
  this; matching it exactly is the first sensitivity in *Open questions* below, not a change to this
  rule.
- **Screens deliberately absent.** No liquidity screen — every asset here is a multi-billion-dollar
  ETF and `r_liquidity_rank` would never bind. No volatility target — that is a lever, and it belongs
  to whichever later experiment claims it. No cross-sectional ranking — with twelve assets and no
  holding cap, the eligible set *is* the book, so a ranking would have nothing to do.

### What this experiment should show

**Predictions, fixed before the run.** All four come from `Data/analyzer.ipynb`, which measured the
signal but constructed no book. Getting these right is worth more than a good Sharpe; getting them
wrong is worth more than a bad one.

| # | Prediction | Where it comes from | What would falsify it |
| --- | --- | --- | --- |
| 1 | **Volatility and maximum drawdown fall** against holding the same assets always | The good regime has lower forward volatility on 11 of 12 assets, at every jump penalty from 5 to 100 | Volatility within a point of the always-invested book |
| 2 | **Return does not rise, and may fall** | The good regime earns more on only 5 of 12 assets; the mean forward spread is −5.1 points | A return gain large enough to matter — which would be evidence of a bug before it was evidence of skill |
| 3 | **Sharpe improves, and the improvement comes from the denominator** | 1 and 2 together. Decompose it before believing it | Sharpe improving mainly through the numerator |
| 4 | **Cash is a large, time-varying part of the book** — averaging roughly half, and going nearly flat in crises | Mean breadth is 56%, and 21% of days sit at or below 25% breadth | An average cash weight near zero, which would mean the eligibility column is not doing what the analyzer says |

**A fifth thing to watch, which is not a prediction because nothing licenses one:** costs. The
trigger fires on any change in the eligible set across twelve assets, and each asset switches about
3.8 times a year. Whether the resulting turnover eats the volatility benefit is the question this
experiment exists to answer, and it is genuinely open.

### Success criteria

As the benchmark, Experiment 1 does not need to win. It needs to be a **fair, stable yardstick**:

1. Reproducible from a clean clone, through the pipeline, with no manual step.
2. A tradeable trigger frequency — not a rule that fires every day.
3. Net-of-cost results reported against every benchmark in `backtest_engine.BENCHMARK_TICKERS`.
4. The four predictions above evaluated explicitly in `FINDINGS_1.md`, **including the ones that turn
   out wrong.**

**Graduation: not applicable.** The benchmark's job is to be the thing others are measured against,
so it stays in the Lab even if it scores well.

### Key risks

- **The signal is a risk signal, and this book spends it on return.** Equal weight over the eligible
  set does nothing with the fact that the eligible assets are the *calm* ones; it treats a calm bond
  ETF and a calm small-cap ETF identically. That mismatch is the most likely reason this book
  disappoints, and it is exactly what an inverse-volatility variant would attack.
- **Whipsaw at the boundary.** A regime that flips back within days pays two round trips for
  nothing. The median spell is 43 trading days, but the shortest observed spells are 1 to 3 days.
  Measured in the construction diagnostics, deliberately not fixed here.
- **Correlated eligibility.** The twelve assets do not switch independently — March 2020 turned
  nearly all of them bearish at once. When breadth collapses the book is in cash, which is the
  intended behaviour, but it means the strategy has one big bet, risk-on against risk-off, wearing
  twelve small ones.
- **Cash drag in a rising market.** Being half invested on average across a decade that was mostly a
  bull market is a large opportunity cost. If the book loses to buy-and-hold on return, this is the
  mechanism, and it is not a bug.
- **Point-in-time integrity.** This universe carries no delisted names — twelve live ETFs — so the
  survivorship control that matters elsewhere is inert here. **That is a weakness of the example, not
  a strength of the strategy**, and any repository built from it on a real universe inherits the
  control rather than the exemption.
- **The signal may not be what earns the return.** If the book beats its benchmarks because it was
  long duration in a falling-rate decade rather than because of the regime model, the honest product
  is a cheaper asset-allocation fund. That is what step 6 exists to answer.

### Open questions this experiment deliberately does not answer

Each is a later experiment, and each has to beat this one:

1. **The extra delay day.** The source paper executes at *t+2*; this executes at *t+1*. One constant.
2. **Inverse-volatility sizing.** Already implemented behind the same interface, switched off here.
3. **A weight cap and a minimum holding count.** The paper caps at 40% and goes fully to cash below
   four bullish assets; both are levers this benchmark declines.
4. **A forecasting layer.** The paper's second half predicts *tomorrow's* regime rather than
   identifying today's, and is the stated remedy for prediction 2.
