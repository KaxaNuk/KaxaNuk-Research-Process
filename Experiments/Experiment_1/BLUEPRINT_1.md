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
> Recorded <YYYY-MM-DD>, before the notebook's rule cell was written.

---

## Experiment 1 — <Strategy_Name>, the declared benchmark

### Thesis

<One paragraph. What book this rule produces and why it is a fair yardstick — sensible, liquid,
low-complexity — for judging whether any later idea adds value. Be modest on purpose: the benchmark
does not assert its signal is the best of its kind, only that it is simple enough to be understood,
liquid enough to be traded, and stable enough to measure other things against.>

### Rules

- **Selection:** <the eligibility condition, naming the column>.
- **Sizing:** <the weighting scheme, and which `portfolio_construction` weigher implements it. Say
  which constraints are switched off, and that each is a lever a later experiment has to earn>.
- **Cash:** <where the uninvested residual goes — the template parks it in a real priced
  instrument, because the engine's weight file has no cash row>.
- **Timing:** <calendar, or event-driven on a stated trigger. Say what happens between triggers>.
- **Lag:** <how many days between the signal and the fill, and what the engine adds on top>.
- **Screens deliberately absent**, and why each is redundant under the rules above.

### What this experiment should show

**Predictions, fixed before the run.** Each should come from `Data/analyzer.ipynb`, which measures
the signal but builds no book. Getting these right is worth more than a good Sharpe; getting them
wrong is worth more than a bad one.

| # | Prediction | Where it comes from | What would falsify it |
| --- | --- | --- | --- |
| 1 | <what the book should do> | <the analyzer section and its number> | <the observation that would refute it> |

<And note anything you are watching that you cannot predict, because nothing licenses a prediction
about it. Costs usually belong here.>

### Success criteria

As the benchmark, Experiment 1 does not need to win. It needs to be a **fair, stable yardstick**:

1. Reproducible from a clean clone, through the pipeline, with no manual step.
2. A tradeable trigger frequency — not a rule that fires every day.
3. Net-of-cost results reported against every benchmark in `backtest_engine.BENCHMARK_TICKERS`.
4. Every prediction above evaluated explicitly in `FINDINGS_1.md`, **including the ones that turn
   out wrong.**

**Graduation: not applicable.** The benchmark's job is to be the thing others are measured against,
so it stays in the Lab even if it scores well.

### Key risks

- **Survivorship and point-in-time integrity.** The universe must include delisted names; quantified
  in `Universe/universe.ipynb`.
- **<The signal's known weakness — slow exits, whipsaw, regime dependence — accepted here on
  simplicity grounds and attacked in a later experiment.>**
- **Concentration.** <How the weighting concentrates, and which diagnostics measure it.>
- **The signal may not be what earns the return.** If the book beats its benchmarks because of a
  factor exposure rather than the signal, the honest product is a cheaper factor fund. That is what
  step 6 exists to answer.

### Open questions this experiment deliberately does not answer

<Each is a later experiment, and each has to beat this one.>
