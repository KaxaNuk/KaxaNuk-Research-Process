# Results

> **Executive summary of every experiment in this repository.**
>
> Compiled from the `FINDINGS_N.md` files, one per experiment, and citing each. **When a number
> changes, change it in `FINDINGS_N.md` first**, then update this file — a summary that leads its
> sources is how two numbers for the same book start to circulate.
>
> Every figure here comes from the **KaxaNuk Backtest Engine**: integer share counts, per-share
> commission on the unadjusted price, a cash reserve. There is no second backtest in this
> repository, by design. Last regenerated end to end on **<YYYY-MM-DD>** from a fresh data pull.
>
> The idea being tested is in [`OBJECTIVE.md`](OBJECTIVE.md). The bar a result has to clear before
> anyone believes it is in [`AGENTS.md`](AGENTS.md).
>
> **Template note.** Every table below is empty by design and every angle-bracketed slot is
> guidance. The shape is fixed; the numbers arrive from `FINDINGS_N.md`. Delete this paragraph when
> the first experiment reports.

## The project in three sentences

**<Does the benchmark book work, in one sentence with its CAGR and Sharpe?>**

**<What attribution says about where the return comes from — allocation against selection, factor
against idiosyncratic — and what that settles.>**

**<What the experiments after the benchmark found: which lever earned its place and which was
rejected, each in a clause.>**

---

## The experiments

Each experiment ranks its variants over **one window shared by all of them**
(`engine.align_to_common_start`), and **those windows can differ between experiments** — a variant
that needs twelve months of history starts later than one that needs none.

> **Read the Sharpe column down, not across.** An experiment's winner is comparable to *its own*
> control row, not to another experiment's headline. The `vs control` column is the one that carries
> meaning across rows.

| Exp | Book | CAGR | Sharpe | Max DD | Control Sharpe | vs control | Status | Findings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| **1** | <the benchmark rule, in five words> | | | | — | — | **the benchmark** | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |

### Experiment 1 against the world

Over <start> to <end>. $1M becomes **<$X>** under the benchmark, against <$Y> for SPY, <$Z> for QQQ
and <$W> for KN600.

| Strategy | CAGR | Vol | Sharpe | Sortino | Max DD |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Experiment 1 — benchmark** | | | | | |
| QQQ | | | | | |
| KN600 | | | | | |
| SPY | | | | | |

**Does it reproduce?** <Re-run from a wiped working copy and state the drift. Curator output
rebases every dividend-adjusted column on a re-pull, so a Sharpe moving in the third decimal is
that effect, not a strategy change.>

### The trial count

**<N ranked variants in Experiment 2, M in Experiment 3, plus any excluded run.>** Published because a
reader cannot discount a best-of-N result without knowing N — see
[Bailey & López de Prado](Bibliotheca/Papers/Bailey_LopezDePrado_2014_The_Deflated_Sharpe_Ratio.md).

---

## What stands — reuse, do not rebuild

- <A result, a module or a method that later work should start from rather than re-derive. One
  line each, with its number.>

## What is closed — do not re-propose without a new argument

- <Each rejected idea, with the number that rejected it. A negative result costs real work and
  stops the next person repeating it; this list is where that value is stored.>

### The uncomfortable one

<The finding that qualifies the idea itself rather than a lever — the claim in `OBJECTIVE.md` that
turned out weaker than stated. Every honest project has one; write it here rather than letting it
sit in a findings file.>

## Open leads, ranked

1. **<The single highest-value run outstanding, and what it would settle.>**
2. <The next.>

## Excluded runs

Variants removed from the tables above rather than reported with a caveat. **A metric computed over
a truncated or rejected run does not belong in the same column as a complete one**, and excluding by
name with a reason is how that stays honest.

| Variant | Why |
| --- | --- |
| <Exp N — variant> | <what went wrong, how it was caught, and what now prevents it> |

## Known limitations

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | **Nothing is out of sample.** No experiment has reached step 7 | Every number here is in-sample, and in-sample selection is what the deflation literature warns about |
| 2 | **No experiment has a control arm** differing in exactly one thing | Which lever earned a margin is inferred from per-lever rows, not measured |
| 3 | The attribution window is bound by factor-file coverage and benchmark-holdings start | It can be shorter than the backtest; the two are not directly comparable |
| 4 | Sector buckets use today's classification, not point-in-time | Names reclassified mid-window are misattributed before their move — the `*_current` suffix marks exactly this |
| 5 | Brinson-Fachler prices only tickers in the book | The allocation/selection split is indicative, not exact |
| 6 | Delisting exits use one day of hindsight | A position is sold on the last day it still has a fill price, knowable only the day after. The final row of a delisted name is **unaudited** |
| 7 | Dual share classes are two positions | Different ISINs, so the company key cannot merge them |
| 8 | Curator output is not reproducible across download dates | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
| 9 | The Deflated Sharpe Ratio has never been computed | The one number that would say whether a winner survives its own trial count |

> **Under the bar in [`AGENTS.md`](AGENTS.md), most numbers above are a reason to run an experiment
> rather than a result.**

---
---

# Appendix — the methods record

Not an executive summary. This exists so the next person does not re-try something already settled,
and so the count of what was tried is visible beside the winner.

## A. Every feature the analyzer measured

Mean per-date Spearman IC of each feature rank against forward returns, over the eligible pool.
From `Data/analyzer.ipynb` section 7, written to `Data/Analyzer/signal_information_coefficients.csv`.

| Feature | IC 21d | IC 63d | IC 252d | IR 252d | Verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| <feature> | | | | | <real / redundant inside this book / falsified / noise> |

## B. Portfolio construction — everything tried

| Construction | Result |
| --- | --- |
| <weighting or holding-count choice> | <Sharpe against control, and what else moved> |

## C. Selection and exit rules — everything tried

| Rule | Result |
| --- | --- |
| <screen, floor or stop> | <the curve, not the cell> |

## D. Where each number comes from

Every path below is gitignored and rebuilt by running its stage.

| Output | Path |
| --- | --- |
| Engine results, per experiment | `Experiments/Experiment_N/Backtest/*_backtest_results.xlsx` |
| Per-variant engine rankings | `Experiments/Experiment_N/Backtest/variant_performance.csv` |
| Attribution figures | `Experiments/Experiment_N/Attribution/` |
| Signal information coefficients | `Data/Analyzer/signal_information_coefficients.csv` |
| Universe diagnostics | `Universe/Charts/`, `Universe/Data_Issues.csv` |
| Per-experiment books | `Experiments/Experiment_N/Portfolio/` |
| Which benchmarks are fetched, and which are reported against | `Data/curator.py`, `Experiments/engine.py` |
