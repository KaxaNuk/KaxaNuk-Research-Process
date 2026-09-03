# Findings — Experiment 1

> **Latest valuable results only.** This file is rewritten when a result changes, not appended to —
> the running history is in [`JOURNAL_1.md`](JOURNAL_1.md).
>
> **[`RESULTS.md`](../../RESULTS.md) is compiled from this file.** When a finding here changes,
> change it here first, then update the summary.
>
> The hypothesis this tested is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md).

## Status

**Not yet run.** When it has: one line saying whether the benchmark is adopted, and the reminder
that the benchmark is not a graduation candidate — its job is to be the thing others are measured
against.

## The book, priced by the engine

Last full re-run **<YYYY-MM-DD>**, from a wiped working copy with every input re-downloaded. Priced
by the **KaxaNuk Backtest Engine v<X.Y.Z>** over <start> to <end> — integer share counts, per-share
commission on the unadjusted price, a cash reserve.

| Strategy | CAGR | Vol | Sharpe | Sortino | Max DD | Alpha vs SPY |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Experiment 1 — benchmark** | | | | | | |
| QQQ | | | | | | |
| KN600 | | | | | | |
| SPY | | | | | | |

**Does it reproduce?** <State the drift between two runs, and attribute it. Curator output rebases
every dividend-adjusted column on a re-pull; a Sharpe moving in the third decimal is that, not the
strategy.>

## What the benchmark actually is, structurally

| Property | Value | Reading |
| --- | ---: | --- |
| Rebalances | | <is the trigger busy?> |
| Turnover | | the cost the engine actually charges |
| Top-5 weight | | <is the weighting concentrated by construction?> |
| Effective N | | <N names behaving like how many?> |
| Largest weight ever | | |

<Any construction decision settled with numbers rather than preference — a holding-count comparison,
a cap dropped — goes here with the numbers.>

## Attribution — is this the signal, or a factor exposure wearing its name?

Step 6 ran both KaxaNuk methodologies over <start> to <end> against KN600, at <coverage>% factor
coverage of the book.

**Brinson-Fachler.** Cumulative alpha **<X>%**:

| Effect | Contribution | Reading |
| --- | ---: | --- |
| Allocation | | <does sector positioning contribute?> |
| Selection | | <picking the right names inside sectors> |
| Interaction | | |

**KN5FM factor model.** Total excess return of roughly **<X>%**, splitting into factor exposure
(<Y>%) and idiosyncratic return (<Z>%):

| Factor | Contribution | Reading |
| --- | ---: | --- |
| Beta | | |
| Size | | |
| Value | | |
| Momentum | | |
| Residual volatility | | |
| <largest industry contributor> | | |
| <largest industry detractor> | | |

### What this settles, and what it does not

**Settled:** <what the decomposition establishes — for example, that there is genuine idiosyncratic
alpha, so the book is not a pure factor exposure. That is graduation criterion 2 evaluated.>

**Not settled:** <the gap between the book's return and the factor the thesis is named after. If the
signal is an absolute rule and the factor model measures relative exposures, the model is close to
blind to it — say so, and name the run that would test it directly.>

## Caveats

- **The attribution window is shorter than the backtest**, bound by benchmark-holdings start and
  factor-file end. The two are not directly comparable.
- **Attribution numbers are only comparable across runs when the factor set is identical.** State
  how many factor files this run used.
- **Sector buckets use today's classification.** The `*_current` suffix marks it; sector attribution
  is read as indicative.
- **Brinson-Fachler prices only tickers in the book**, so the allocation/selection split is
  indicative rather than exact.
- **Nothing here is out of sample**, and no control arm exists.
