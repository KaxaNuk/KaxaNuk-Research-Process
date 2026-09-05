# Results

> **Executive summary of everything this repository has measured.**
>
> Experiment sections are compiled from the `FINDINGS_N.md` files and cite each one. **When a number
> changes, change it in `FINDINGS_N.md` first**, then update this file — a summary that leads its
> sources is how two numbers for the same book start to circulate.
>
> **One exception:** findings from step 3 go straight into *Before any experiment* below. Notebook
> outputs are stripped before committing, so a step-3 measurement that lives only in a cell output
> does not survive the commit.
>
> Every performance figure comes from the **KaxaNuk Backtest Engine**. There is no second backtest
> in this repository, by design.
>
> Every table below is empty by design: the shape is fixed, the numbers arrive from the pipeline.
> Delete this blockquote when the first one reports.

## The project in three sentences

Does the benchmark book work, with its headline numbers. What attribution says about where the
return comes from. Which lever earned its place after the benchmark, and which was rejected.

---

## Before any experiment: what the data already says

Findings from step 3, `Data/analyzer.ipynb`: whether a candidate feature carries information, over
what horizon, and with which sign — and anything measured about the signal that does not need a
book. Cite the section each number came from.

---

## The experiments

Each experiment ranks its variants over **one window shared by all of them**, and those windows can
differ between experiments.

> **Read the Sharpe column down, not across.** An experiment's winner is comparable to *its own*
> control row, not to another experiment's headline. The `vs control` column is the one that carries
> meaning across rows.

| Exp | Book | CAGR | Sharpe | Max DD | Control Sharpe | vs control | Status | Findings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| **1** | the benchmark rule, in five words | | | | — | — | **the benchmark** | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |

### Against the world

The same book measured against every benchmark it reports against, over one stated window.

**Does it reproduce?** Re-run from a wiped working copy and state the drift. Curator output rebases
every dividend-adjusted column on a re-pull, so a Sharpe moving in the third decimal is that effect,
not a strategy change.

### The trial count

**How many variants were ranked, in each experiment, plus any excluded run.** Published because a
reader cannot discount a best-of-N result without knowing N.

---

## What stands — reuse, do not rebuild

A result, a module or a method later work should start from rather than re-derive. One line each,
with its number.

## What is closed — do not re-propose without a new argument

Each rejected idea, with the number that rejected it. A negative result costs real work and stops
the next person repeating it; this list is where that value is stored.

### The uncomfortable one

The finding that qualifies the idea itself rather than a lever — the claim in `OBJECTIVE.md` that
turned out weaker than stated. Every honest project has one; write it here rather than letting it
sit in a findings file.

## Open leads, ranked

The single highest-value run outstanding, and what it would settle. Then the next.

## Excluded runs

Variants removed from the tables above rather than reported with a caveat. **A metric computed over
a truncated or rejected run does not belong in the same column as a complete one**, and excluding by
name with a reason is how that stays honest.

| Variant | Why |
| --- | --- |
| | what went wrong, how it was caught, and what now prevents it |

## Known limitations

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | **Nothing is out of sample.** No experiment has reached step 7 | Every number here is in-sample, and in-sample selection is what the deflation literature warns about |
| 2 | **No experiment has a control arm** differing in exactly one thing | Which lever earned a margin is inferred from per-lever rows, not measured |
| 3 | Classification buckets use today's labels, not point-in-time | Anything reclassified mid-window is misattributed before its move — the `current_*` prefix marks exactly this |
| 4 | Delisting exits use one day of hindsight | A position is sold on the last day it still has a fill price, knowable only the day after |
| 5 | Curator output is not reproducible across download dates | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
| 6 | The Deflated Sharpe Ratio has never been computed | The one number that would say whether a winner survives its own trial count |

> **Under the bar in [`AGENTS.md`](AGENTS.md), most numbers above are a reason to run an experiment
> rather than a result.**
