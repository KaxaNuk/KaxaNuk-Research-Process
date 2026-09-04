# Findings — Experiment 1

> **Latest valuable results only.** This file is rewritten when a result changes, not appended to —
> the running history is in [`JOURNAL_1.md`](JOURNAL_1.md).
>
> **[`RESULTS.md`](../../RESULTS.md) is compiled from this file.** When a finding here changes,
> change it here first, then update the summary.
>
> The hypothesis this tested is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md).

## Status

**Step 4 complete, steps 5 and 6 not run.** The book exists, is written, and passes every
invariant. It has **not been priced**: `kaxanuk-backtest-engine` and
`kaxanuk-attribution-analysis` are licensed, absent from this clone, and the notebook reports and
skips without them. So there is no CAGR, no Sharpe and no attribution below.

**One prediction was settled anyway, and it was wrong.** Prediction 4 needed no engine, and
falsifying it changed what this strategy is understood to be.

## Prediction 4 — falsified

[`BLUEPRINT_1.md`](BLUEPRINT_1.md) predicted: *cash is a large, time-varying part of the book,
averaging roughly half, and going nearly flat in crises.* The reasoning was that mean breadth is
56%, so on a typical day only about seven of twelve assets qualify.

| | Predicted | Measured |
| --- | ---: | ---: |
| Invested share, averaged over trading days | ~55% | **95.3%** |
| Days at least 90% invested | few | **95.3%** |
| Days at most 25% invested | many | **4.7%** |
| Rebalances fully in cash | frequent | **7 of 461** |
| Longest fully-invested stretch | short | **1,618 trading days** |

**Why the prediction was wrong.** Breadth decides *how many* assets are held, not *how much* is
invested. Equal weight over the eligible set always sums to one whenever at least one asset
qualifies — so as breadth falls the book does not de-risk, it **concentrates**. At the extreme it
holds a single asset at 100%, which is what `max_weight` reaching 1.000 records. **The strategy as
specified is a rotation between asset classes, not a risk reducer.**

That is a mistake in the reasoning, not in the code, and it is worth more than a correct prediction
would have been. It says the two levers the blueprint deliberately declined — a weight cap and a
minimum holding count — are not refinements: **they are the entire mechanism by which the source
paper's version goes defensive**, and their absence is why this book does not. The paper caps at 40%
and moves fully to the risk-free asset below four bullish assets. Both exist in
`portfolio_construction.py`, switched off here, and turning them on is Experiment 2.

## What the benchmark actually is, structurally

From `Portfolio/portfolio_summary.csv` and `Portfolio/group_weights.csv`, over 2015-01-09 to
2026-08-18.

| Property | Value | Reading |
| --- | ---: | --- |
| Rebalances | 461 in 11.6 years — **40 a year** | Event-driven on any change across twelve assets. Tradeable, but not cheap |
| One-way turnover | **~810% a year** | The number that most threatens this strategy — see *What is open* |
| Holdings | 6.5 mean, 0 min, 12 max | Roughly half the universe on a typical day |
| Largest single weight | **100%** at its worst | The concentration described above |
| Invested share | 95.3% of trading days | Prediction 4, falsified |

**Asset-group drift is almost nil** — Real Assets +2.6 points, Fixed Income −2.1, Equity −2.1
against an always-invested equal-weight book. The strategy has no structural tilt toward one group;
it moves between them. That is a genuinely good property for a benchmark, and it means a later
result cannot be dismissed as *it was just long bonds*.

## Attribution — is this the signal, or a factor exposure wearing its name?

**Not run.** Requires `kaxanuk-attribution-analysis` plus two hand-supplied inputs — an index's
daily holdings and a factor model — neither of which has ever been placed in
`Data/Curator/Benchmarks/` or `Data/Curator/Factors/`. Nothing in the pipeline downloads them,
because no price provider sells them.

### What this settles, and what it does not

**Settles:** the shape of the book. A 40-times-a-year, roughly-half-the-universe, equally weighted
rotation with no group tilt and no meaningful cash position.

**Does not settle:** anything about performance. Predictions 1, 2 and 3 — volatility and drawdown
fall, return does not rise, Sharpe improves through the denominator — are all about a priced series
and remain open. They should be evaluated against a like-for-like control: the same twelve assets
held equally weighted at all times.

## What is open, ranked

1. **Price it.** Install the licensed engine and run sections 4 and 5. Everything above is a
   property of a weight file; none of it is a return.
2. **Turnover at 810% a year is the headline risk.** The blueprint flagged costs as the one thing
   nothing licensed a prediction about. At that rate the question is not whether the signal works
   but whether anything survives the commission, and the engine's per-share model is the only way to
   find out.
3. **Add the two declined levers, as Experiment 2.** A 40% cap and a four-asset minimum turn this
   rotation into the defensive book the blueprint thought it was describing. Both are one line.
4. **Inverse-volatility sizing, as Experiment 3.** The signal identifies calm; equal weight ignores
   that. `portfolio_construction.inverse_volatility` already exists behind the same interface.

## Caveats

| # | Caveat | Effect |
| --- | --- | --- |
| 1 | **Nothing here is net of costs, because nothing here is priced** | Every figure is a property of the target weights, not of a traded book |
| 2 | **Turnover is target-to-target, not realised** | The realised figure is lower; between rebalances winners drift up on their own |
| 3 | **Twelve live ETFs carry no delisted names** | The survivorship control is inert on this universe. That is a weakness of the example, not a strength of the strategy |
| 4 | **The signal window is 2015-2026**, inside prices that start 2010 | One decade, dominated by a single equity bull market and two sharp drawdowns |
| 5 | **The regime model trains on five years, not the source paper's eleven** | The ETFs do not have eleven years of common history |
| 6 | **Curator output is not reproducible across download dates** | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
