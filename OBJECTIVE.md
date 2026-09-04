# Objective

> **What this file is for.** One idea, one objective, and the claims inside it with their status.
> The first thing a CIO reads and the last thing that changes: a change here means a *different*
> strategy, not a better version of this one.
>
> This is the worked example. **To make the repository yours, rewrite this file first** — the
> section *Writing your own* at the bottom says what each part has to do.

## The main idea

> **Every asset spends its life alternating between a calm state and a turbulent one, and a model
> can tell which state it is in today from its own recent returns alone — without being told what a
> crisis looks like.**

Twelve asset classes, one ETF each, from US large caps to gold. A **statistical jump model** is
fitted to each asset separately on five years of its own daily history and refitted twice a year. It
sees eight numbers per day — exponentially weighted return, downside deviation and Sortino ratio at
half-lives of five, ten and twenty-one days — and sorts the days into two regimes, paying a penalty
every time it changes its mind. The penalty is what turns a volatility indicator into a regime
signal.

The strategy is named **Regime Rotation**, after the only decision it makes: which asset classes are
currently worth being in.

Two columns carry it. `r_regime_bull` is the per-asset eligibility switch. `r_sortino_hl21_rank` and
`r_return_ewm_hl21_rank` are the cross-sectional orderings that would choose among the assets that
qualify. Neither half is clever, and both are explainable in a sentence — which is what will let
attribution later say which half earned the return.

## The objective

**A rule that says, on any date, which asset classes are worth holding and why — and that can be
audited afterwards to say which part of the answer was right.** The deliverable is not a Sharpe
ratio; it is a rule simple enough that when it works we can say *why*, and when it fails we can say
*which part* failed.

Concretely, an acceptable end state is: *on any date the strategy names what it holds, gives a
one-sentence reason for each holding, and can point at an attribution that says how much of the
return came from the regime signal rather than from being long risk assets in a rising market.*

**The constraint is radical simplicity.** Complexity is added one lever at a time, and each addition
has to beat the simpler baseline to earn its place. The regime model is already the most complicated
thing here; nothing gets stacked on top of it until it has been understood on its own.

## The claims inside that sentence

They are tested separately and **their status is not the same.** This table is the only place a
reader sees which parts of the idea have survived contact with the data.

| | Claim | Status |
| --- | --- | --- |
| **1. Risk** | The regime label separates calm from turbulent: the good state has lower forward volatility | **measured** — holds for 11 of 12 assets, and at every jump penalty tested |
| **2. Return** | The good state also earns more | **falsified** — holds for 5 of 12 assets, mean spread negative, and negative at every penalty |
| **3. Selection** | Among the assets that qualify, ranking by Sortino or by momentum picks the better ones | **untested** — screened, not traded |
| **4. Construction** | Holding only qualifying assets bounds how much of the book can be in a falling asset class | **true by construction, untested as a source of return** |

Status vocabulary, so it means the same across strategies: **untested** · **measured** (the analyzer
says something; no book has been run) · **falsified** · **confirmed as a book** (it beats its
benchmarks through the engine) · **confirmed as a factor** (attribution assigns it the return) ·
**unexplained** (confirmed as a book, not as a factor — the usual state, and the interesting one) ·
**true by construction**.

### Claims 1 and 2 — risk yes, return no

Measured in `Data/analyzer.ipynb` section 4, over 2015-01 to 2026-09, on the return earned the day
*after* each label. Full numbers in [`RESULTS.md`](RESULTS.md).

- **Forward volatility is lower in the good state for 11 of 12 assets**, by 5.6 annualised points on
  average. Gold is the exception.
- **Forward return is higher in the good state for only 5 of 12**, and the average spread is −5.1
  points. The five where it works are the bond and commodity sleeves; it fails hardest on US
  equities, where the sharpest positive days arrive during the drawdown the model has correctly
  labelled bad.

Neither result is an artefact of the one setting chosen. Sweeping the jump penalty from 5 to 100
moves the switching rate from twelve times a year to twice, and **the sign of both results holds
across the whole range.**

This is what the source paper's own design implies: it identifies the regime in force and then adds
a *supervised* layer to forecast the next one, because identification is not prediction. What
settles claim 2 either way is a forecasting layer, which belongs in an experiment.

### Claim 3 — selection among the qualifying assets

`Data/analyzer.ipynb` section 8 gives the information coefficients. Inside the eligible pool the
strongest is one-month momentum against a one-year forward horizon, and the ranks that look
promising at a year look like noise at a month. On a twelve-asset cross-section these are directional
readings rather than evidence: the fundamental law says an information ratio scales with the square
root of the number of independent bets, and twelve is a small number of bets. **The IC table is a
screening tool.** Nothing here has been traded.

### Claim 4 — construction

True by construction and therefore the hardest to evidence: a screen that works by exclusion leaves
no trace in the book that was actually held. The counterfactual that would show it is the
exclusion-filter test — the same assets at the same weights with the regime switch forced on — which
`Experiments/backtest_engine.py` can price directly.

---

## What is not claimed

- **Not that the parameters are right.** The eight features and their half-lives are the source
  paper's, taken as given rather than searched for. The five-year training window and the biannual
  refit are choices; the jump penalty was picked on **persistence** — spells long enough to be
  tradable — and deliberately not on return. Taking parameters from a paper is a defence against
  data-snooping, not evidence of optimality.
- **Not that the model forecasts anything.** It identifies the regime in force. See claims 1 and 2.
- **Not that this is out of sample.** Nothing is, until an experiment reaches step 7.
- **Not that twelve ETFs are a serious universe.** They are a legible one. Every cross-sectional
  statistic here is noisy for that reason, and widening the universe is the cheapest way to raise
  the ceiling on anything built on top.
- **Not that the ETFs are the assets the paper studied.** The paper backtests total-return
  *indices* from 1991; this trades their ETF proxies from 2010, with tracking error, expense ratios
  and a much shorter history. `Universe/Investable_Universe.csv` records which index each ETF stands
  in for, so the substitution stays visible.

---

## Writing your own

Replace everything above. Five parts, and each has a job:

| Part | Its job | The failure it prevents |
| --- | --- | --- |
| **The main idea** | one sentence somebody outside the team could repeat | a strategy nobody can explain is a strategy nobody can debug |
| **The objective** | the *capability* a finished version gives the desk, not a number | "a Sharpe of 1.2" is not something you can tell whether you have achieved |
| **The claims** | the sentence broken into parts that can be tested separately, each with a status | a strategy that half works reads as working, unless the halves are listed |
| **What is not claimed** | what a reader might assume and would be wrong to | the reader assumes it anyway if you do not say |
| **The named columns** | which `c_*` or `r_*` column carries each half | attribution cannot say which half earned the return unless the halves have names |

Two rules that matter more than the format:

1. **Write it before the backtest.** The claims table is a set of predictions. A claim added after a
   result is an observation wearing a hypothesis's clothes.
2. **Keep the status column honest.** It is the one place a reader learns that part of the idea did
   not survive. The example's claim 2 is marked *falsified*, and that is the most useful row in the
   table.

---

**Where this stands, with every number and its caveats: [`RESULTS.md`](RESULTS.md).**
How work is done here, and the bar a result has to clear: [`AGENTS.md`](AGENTS.md).
