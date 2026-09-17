# Objective

> **Step 1 of 8, with `Bibliotheca/`.** One idea, one objective, and the claims inside it with
> their status. The first thing a CIO reads and the last thing that changes: a change here means a
> *different* strategy, not a better version of this one.
>
> **Write it before any paper is read, and before anything is measured.** The claims table is a set
> of predictions; a claim written after the reading, or added after a result, is an observation
> wearing a hypothesis's clothes.

<!-- example: begin -->

> **This file is the worked example — `liquid-momentum`.** One strategy filled in, kept on the
> `example` branch so the shape can be read rather than imagined. **Written 2026-09-10, before any
> data was downloaded and before any rule was coded.** Starting your own: delete everything between
> the example markers and write yours in its place.

## The main idea

**Own the most heavily traded stocks that went up over the past year, equally weighted, and hold
nothing else.**

The signal is `r_momentum_12_1`, the total return over the twelve months ending one month ago; a
security is selected when it is positive. The screen is `r_liquidity_rank`, the per-date percentile
of `c_dollar_volume_63d`; a security is eligible in the top quintile. The sizing is equal weight
across whatever survives both, with the uninvested residual in cash. **Neither half is clever, and
that is deliberate** — both are explainable in a sentence, which is what lets step 6 say afterwards
which of them earned the return.

## The objective

A rule the desk can hold with real money in names it can get out of, and can explain in one sentence
to somebody who does not work here. The deliverable is not a Sharpe; it is a rule simple enough that
when it works we can say *why*, and when it fails we can say *which part* failed — the signal, the
screen, or the sizing.

**The design constraint every experiment respects: radical simplicity.** Complexity is added one
lever at a time, and each addition must beat the simpler baseline to earn its place. This strategy
has three moving parts and no optimiser.

## The claims inside that sentence

They are tested separately and **their status is not the same.** This table is the only place a
reader sees which parts of the idea have survived contact with the data, so keep it honest.

| | Claim | Status |
| --- | --- | --- |
| **1. The signal** | a positive twelve-month return, skipping the most recent month, selects stocks whose following month beats the universe average | **untested** |
| **2. The sizing** | equal weight across the eligible set captures that return without needing a risk model | **untested** |
| **3. The construction** | the top-quintile liquidity screen makes every position exitable in a day at ordinary volume | **true by construction, untested as a source of return** |

Status vocabulary, so it means the same across strategies: **untested** · **measured** (the analyzer
says something; no book has been run) · **falsified** · **confirmed as a book** (it beats its
benchmarks through the engine) · **confirmed as a factor** (attribution assigns it the return) ·
**unexplained** (confirmed as a book, not as a factor — the usual state, and the interesting one) ·
**true by construction**.

### 1. The signal — momentum

**The evidence it rests on.** [Jegadeesh & Titman
(1993)](Bibliotheca/Papers/Jegadeesh_Titman_1993_Buying_Winners_Selling_Losers.md) established that
stocks selected on three-to-twelve-month past returns keep outperforming for three to twelve months,
and that the effect is not explained by systematic risk. [Asness, Moskowitz & Pedersen
(2013)](Bibliotheca/Papers/Asness_Moskowitz_Pedersen_2013_Value_And_Momentum_Everywhere.md) find the
same premium in eight markets and asset classes on the twelve-months-skip-one specification. The
skip is not decoration: [Jegadeesh
(1990)](Bibliotheca/Papers/Jegadeesh_1990_Predictable_Behavior_Of_Security_Returns.md) shows the most
recent month *reverses*, so a window ending today nets a reversal against a continuation and
measures the difference.

**What is still open.** Whether any of it survives inside the liquid quintile. [Lesmond, Schill &
Zhou (2004)](Bibliotheca/Papers/Lesmond_Schill_Zhou_2004_Illusory_Nature_Of_Momentum_Profits.md)
argue momentum profits concentrate in exactly the high-cost names this strategy screens away.
[Asness, Moskowitz & Pedersen
(2013)](Bibliotheca/Papers/Asness_Moskowitz_Pedersen_2013_Value_And_Momentum_Everywhere.md) find
the premium inside a universe already cut to the largest, most liquid quintile of each market — a
capitalisation cut in a value-weighted long-short book, not our dollar-volume cut in an
equal-weighted long-only one, so it is evidence on the other side rather than an answer.

**What would settle it.** The information-coefficient table in `Data/analyzer.ipynb`, computed on
the screened universe, before any book is built. Nothing is in [`RESULTS.md`](RESULTS.md) yet.

### 2. The sizing — equal weight

**The evidence it rests on: none of ours.** Equal weighting is the control, not the proposal. The
standard reference for how hard it is to beat out of sample on a narrow universe is DeMiguel,
Garlappi & Uppal (2009), which is a **lead** in [`Bibliotheca/`](Bibliotheca/BIBLIOGRAPHY.md) and not
yet a note — so nothing may be claimed on its authority here.

**What would settle it.** A later experiment that proposes a weighting scheme and has to beat this
one. Until then the claim is that equal weight is *sufficient*, not that it is best.

### 3. The construction — the liquidity screen

**This claim is true by construction, and is expected to cost return rather than add it.**
[Ibbotson, Chen, Kim & Hu
(2013)](Bibliotheca/Papers/Ibbotson_Chen_Kim_Hu_2013_Liquidity_As_An_Investment_Style.md) find that
less liquid US stocks have historically earned *more*, and that the effect stands apart from size,
value and momentum. Screening to the top quintile therefore selects the low-return end of a
compensated style on purpose. The screen buys capacity, tradability and net-of-cost survival. **It is
not a source of alpha and must never be reported as one.**

**What would settle it.** Nothing in this experiment. A later one varies the threshold and reads the
sweep as a curve.

## What is not claimed

- **Not that the parameters are right.** The twelve-month window and the one-month skip were taken
  from the notes cited above rather than searched on our data; the top-quintile cut was chosen for
  roundness and has no note behind it. Neither is evidence of optimality: the first two are a
  defence against data-snooping, and each of the three is a curve a later experiment sweeps and
  publishes.
- **Not that this is out of sample.** Nothing is, until an experiment reaches step 7.
- **Not that the liquidity screen adds return.** See claim 3. If the book outperforms, the screen is
  not where the outperformance came from, and `FINDINGS_1.md` has to say so.
- **Not that momentum is safe.** [Daniel & Moskowitz
  (2016)](Bibliotheca/Papers/Daniel_Moskowitz_2016_Momentum_Crashes.md) document infrequent, severe
  momentum crashes in rebounds after market declines. A long-only book that holds cash when nothing
  has positive momentum carries a *different* exposure to that than the long-short book they study,
  and the difference is a prediction to be evaluated rather than an assumption to be made.
- **Not that a positive twelve-month return forecasts anything for one security.** The claim is
  about the average of the selected set. A reader will assume otherwise unless this says so.

## Where each half is named

| Half | The column | The stage that owns it |
| --- | --- | --- |
| the signal | `r_momentum_12_1` | Refinery — its window is what a later experiment sweeps, and **a sweep must never cost a download** |
| the screen | `r_liquidity_rank`, the per-date percentile of `c_dollar_volume_63d` | Refinery, over a Curator column |
| the sizing | none — equal weight is a rule, not a column | the rule cell of `Experiments/Experiment_1/experiment_1.ipynb` |

**Momentum is per-security arithmetic and could sit in the Curator. It does not, deliberately.**
Widening the Curator's schema forces a refetch of every identifier, so a column whose settings an
experiment will tune belongs one stage later. Its inputs — the adjusted close and `c_return_1d` —
stay in the Curator, where nothing about them is tunable. The convention is in
[`README.md`](README.md); this is the strategy that made us apply it.

<!-- example: end -->

---

## The five parts, and the job each does

| Part | Its job | The failure it prevents |
| --- | --- | --- |
| **The main idea** | one sentence somebody outside the team could repeat | a strategy nobody can explain is a strategy nobody can debug |
| **The objective** | the *capability* a finished version gives the desk, not a number | "a Sharpe of 1.2" is not something you can tell whether you have achieved |
| **The claims** | the sentence broken into parts testable separately, each with a status | a strategy that half works reads as working, unless the halves are listed |
| **What is not claimed** | what a reader might assume and would be wrong to | the reader assumes it anyway if you do not say |
| **The named columns** | which `c_*` or `r_*` column carries each half | attribution cannot say which half earned the return unless the halves have names |

---

**Where this stands, with every number and its caveats: [`RESULTS.md`](RESULTS.md).**
How work is done here, and the bar a result has to clear: [`AGENTS.md`](AGENTS.md).
