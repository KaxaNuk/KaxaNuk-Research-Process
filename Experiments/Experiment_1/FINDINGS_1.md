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

## The predictions, evaluated

**Every prediction in the blueprint gets a row, including the ones that were wrong.** A falsified
prediction is worth more than a correct one: it says something about the strategy that nobody knew,
and it cost one run to find out.

| # | Prediction | Outcome | What it changed |
| --- | --- | --- | --- |
| 1 | <as written in the blueprint> | <confirmed / falsified, with the number> | <what is now understood differently> |

## The book, priced by the engine

Last full re-run **<YYYY-MM-DD>**, from a wiped working copy with every input re-downloaded. Priced
by the **KaxaNuk Backtest Engine v<X.Y.Z>** over <start> to <end>.

| Strategy | CAGR | Vol | Sharpe | Sortino | Max DD |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Experiment 1 — benchmark** | | | | | |
| <benchmark 1> | | | | | |

## What the benchmark actually is, structurally

<From `Portfolio/portfolio_summary.csv`. Rebalance frequency, turnover, holdings, concentration,
invested share, and any structural tilt — with a reading of what a bad value would have meant.>

## Attribution — is this the signal, or a factor exposure wearing its name?

<Brinson-Fachler: allocation, selection, interaction. The factor model: factor against idiosyncratic.
State the window, which is bound by factor-file coverage and is usually shorter than the backtest.>

### What this settles, and what it does not

**Settles:** <the question attribution answered.>

**Does not settle:** <what remains, and which counterfactual book would settle it — the same
holdings with the signal off, positions equalised, a random draw at the same sizes, entry dates
shifted.>

## What is open, ranked

1. <The single highest-value run outstanding, and what it would settle.>

## Caveats

| # | Caveat | Effect |
| --- | --- | --- |
| 1 | <what a reader must know before quoting a number above> | <what it does to that number> |
