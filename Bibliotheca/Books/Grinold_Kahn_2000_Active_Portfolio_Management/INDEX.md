# Grinold & Kahn (2000) — *Active Portfolio Management: A Quantitative Approach for Producing Superior Returns and Controlling Risk*

> **Link:** not recorded. Add it here as `[Title](URL)` the next time this source is opened — every
> note is meant to carry one, and a wrong link is worse than none.
>
> **Citation:** Richard C. Grinold and Ronald N. Kahn. McGraw-Hill, second edition, 2000.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a copy sits beside this note and only the
> note is committed.
>
> **Read into this repository:** with the template, 2026-09-03, from the second edition's chapter
> structure and its standard results. **Every implication below is written for any strategy built on
> this process.** Re-read the chapters against yours and rewrite the blockquotes; then replace this
> line with the date you did.

The book behind step 3. `Data/analyzer.ipynb` measures an **information coefficient** for every
candidate feature and reads its **decay**; this is where both ideas come from, and the one place the
"screening tool, not evidence" rule in `AGENTS.md` is derived rather than asserted.

---

## 1. The information ratio is the measure of active management

*(chapter 5, Residual Risk and Return: The Information Ratio)*

Active management is judged on **residual** return — return after the benchmark's contribution is
removed — and the right summary of it is the information ratio: residual return per unit of residual
risk. Value added is a function of the information ratio and the manager's risk aversion, not of
raw return.

> **What this implies for a strategy built on this process.** Every table in `RESULTS.md` is read
> against a control row for this reason: the number that carries meaning is the gap to the
> benchmark's own rule on the same window, per unit of risk, not the headline CAGR. It is also why
> the Backtest Engine's Sharpe against SPY, QQQ and KN600 is criterion 1 of the graduation gate and
> raw return is not.

## 2. The fundamental law of active management: IR ≈ IC × √BR

*(chapter 6, The Fundamental Law of Active Management)*

The information ratio a manager can achieve is approximately the **information coefficient** — the
correlation between forecasts and realised residual returns — times the square root of **breadth**,
the number of independent forecasts made per year. The law assumes the forecasts are independent
and the portfolio is unconstrained; both assumptions fail in practice, and the law is an upper bound
rather than a promise.

> **What this implies for a strategy built on this process.** A per-date IC of a few hundredths is a
> normal, usable signal *only* if there is breadth behind it — many names, re-ranked often. That is
> the arithmetic behind two of the template's design facts: the analyzer computes IC **per date
> across the cross-section**, because the cross-section is where breadth lives; and holding count and
> rebalance frequency are not free parameters but the breadth term of this law, traded against the
> costs in section 6. A high-IC signal on ten names rebalanced yearly is a story; a low-IC signal on
> a few hundred names rebalanced monthly can be a business.

## 3. A forecast is refined, not used raw: alpha = IC × volatility × score

*(chapter 10, Forecasting Basics)*

The basic forecasting formula converts a raw signal into an expected residual return by scaling a
standardised score by the signal's information coefficient and the asset's residual volatility.
Raw signals are never alphas; they become alphas only after this shrinkage, which is what stops a
noisy feature from being sized as if it were certain.

> **What this implies for a strategy built on this process.** A rank is a score, not an alpha.
> Sizing positions in proportion to a raw rank implicitly assumes an IC of one. When the Portfolio
> Construction library arrives this is the transformation it will apply; until then, a strategy that
> sizes by rank or by liquidity should say — in `OBJECTIVE.md`, as Paleologo's note also asks — that
> its sizing carries no forecast at all.

## 4. Information analysis: the IC is measured, out of sample, as a correlation with what happened

*(chapter 12, Information Analysis)*

The information coefficient is estimated by correlating the forecasts made on a date with the
residual returns that followed, over many dates. The estimate is noisy, it is compared against
what a naive forecast would have achieved, and a signal is judged by the consistency of its IC over
time as much as by its level.

> **What this implies for a strategy built on this process.** This is section 7 of the analyzer,
> line by line: per-date Spearman IC against forward returns, its standard deviation, and the ratio
> of the two — the information ratio of the *signal*. **Sign first, consistency second, size last**
> is the reading order the chapter licenses. And the estimate's noise is why `AGENTS.md` calls the IC
> table a screening tool: a feature that passes has earned a backtest, not a belief.

## 5. Information has a horizon: it decays, and the decay sets the turnover

*(chapter 13, The Information Horizon)*

Forecasts lose value as time passes. The rate at which a signal's information decays determines how
often positions must be refreshed to capture it — and therefore how much turnover, and cost, the
signal implies before any portfolio rule is applied.

> **What this implies for a strategy built on this process.** Section 6.1 of the analyzer — rank
> autocorrelation at lags of one, five, twenty-one, sixty-three and two hundred and fifty-two days —
> is this chapter made operational. A feature whose rank autocorrelation collapses within a month
> cannot drive selection in a book that rebalances monthly; it can only be an exit signal. Read the
> IC table and the decay chart together before committing a feature to an experiment.

## 6. Transactions costs and turnover cap what breadth can pay for

*(chapter 16, Transactions Costs, Turnover, and Trading)*

Trading costs scale with turnover, and turnover is the price of breadth. Past the point where the
marginal cost of refreshing positions exceeds the marginal information gained, more breadth lowers
the information ratio rather than raising it.

> **What this implies for a strategy built on this process.** The reason results are only ever
> accepted **net**, and the reason turnover is a first-class diagnostic in every experiment
> notebook. On a high-turnover book the difference between a flat cost model and the engine's
> per-share commission has been a third of a thin edge. Breadth is bought; this chapter is the
> invoice.

## 7. Performance analysis separates skill from exposure

*(chapter 17, Performance Analysis)*

Realised performance is decomposed into the part explained by exposures to known risk factors and
the residual attributable to skill, with the statistical caveat that skill is hard to distinguish
from luck over the track records most managers have.

> **What this implies for a strategy built on this process.** The same question step 6 answers with
> KN5FM and Brinson-Fachler, thirty years earlier, and the same warning as Paleologo's section 3.3:
> the exposure part is estimated well and the skill part is not. Criterion 2 of the graduation gate
> is this chapter's question asked of one book.

---

## Distilled into this process's language

| Book idea | Where it lands in the process |
| --- | --- |
| The information ratio is the measure | every result read against a control row, per unit of risk |
| **IR ≈ IC × √BR** | IC is computed per date across the cross-section; holding count and rebalance frequency are the breadth term |
| Alpha = IC × volatility × score | a rank is a score, not an alpha; sizing by rank assumes IC = 1 |
| **IC measured out of sample as a correlation** | analyzer section 7: sign, consistency, size — in that order |
| **The information horizon** | analyzer section 6.1: rank decay sets the tradeable holding period |
| Costs cap what breadth can pay for | results net only; turnover a first-class diagnostic |
| Performance analysis: skill against exposure | step 6, and graduation criterion 2 |

## What this book does not settle for us

- It is written for **forecast-driven, optimised** portfolios. A threshold rule — hold what qualifies,
  weight by something simple — has no explicit forecast to refine, so chapters 10 and 14 describe a
  construction this process will only reach when the Portfolio Construction library lands.
- Its IC is a correlation with **residual** return, after a risk model. The analyzer's IC is against
  **total** forward return, because no risk model is available before step 6. That is a stated
  simplification, and one more reason the IC table screens rather than proves.
- It says nothing about **survivorship, delisting or data-snooping** — for those, see Part 5 of
  [`../../BIBLIOGRAPHY.md`](../../BIBLIOGRAPHY.md).
