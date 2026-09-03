# Blueprint — Experiment 1

> **The hypothesis, fixed once written.** Thesis, rules, success criteria and key risks, recorded
> *before* any code runs. Written by hand, or with the AI.
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
does not assert that its signal is the best of its kind, only that it is simple enough to be
understood, liquid enough to be traded, and stable enough to measure other things against.>

### Rules

- **Selection:** <the eligibility condition, naming the column — `c_<signal> == 1`>.
- **Ranking and sizing:** <the ranking column and the holding count; the weighting scheme; where
  the uninvested residual goes — the template parks it in `BIL`, a real priced instrument, because
  the engine's weight file has no cash row>.
- **Rebalancing:** <calendar, or event-driven on a stated trigger. State what happens between
  triggers — weights drift, nothing trades>.
- **Screens deliberately absent**, and why each is redundant under the rules above.

### Success criteria

As the benchmark, Experiment 1 does not need to win. It needs to be a **fair, stable yardstick**:

1. Fully reproducible from the pipeline, from a clean clone.
2. A tradeable frequency of rebalance triggers — not a rule that fires every day.
3. Net-of-cost results reported against SPY, QQQ and KN600.

**Graduation: not applicable.** The benchmark's job is to be the thing others are measured against,
so it stays in the Lab even if it scores well.

### Key risks

- **Survivorship and point-in-time integrity.** The universe must include delisted names;
  quantified in `Universe/universe.ipynb`.
- **<The signal's known weakness — slow exits, whipsaw, regime dependence — accepted here on
  simplicity grounds and attacked in a later experiment.>**
- **Concentration.** <How the weighting concentrates, and which diagnostics measure it — top-5
  weight share, effective N.>
- **Boundary churn.** <If the rule has a rank cut-off, how much trading comes from names flickering
  across it. Measured, and deliberately not fixed here.>
- **The signal may not be what earns the return.** If the book beats its benchmarks because it holds
  large, liquid, high-beta names rather than because of the signal, the honest product is a cheaper
  factor fund. This is what step 6 exists to answer.
