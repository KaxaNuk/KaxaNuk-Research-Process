<!-- example: begin -->

# Liquid Momentum

**Own the most heavily traded stocks that went up over the past year, equally weighted, and hold
nothing else.**

> **Status: objective written, reading for its claims in progress.** Six notes exist, read from the
> abstracts and, for one paper, two sections; the fine-tuning pass of `OBJECTIVE.md` is still owed.
> `Universe/Investable_Universe.csv` holds 788 identifiers, delisted names kept, and no dated
> membership. Nothing from `Data/` on is built: no data, no book, no number.

This is the public `example` branch of the KN Research Process: one strategy worked through the
process, for reading and copying. A strategy of your own starts from `main`, never from here.

## Where it stands

| | |
| --- | --- |
| **The rule** | `r_momentum_12_1` positive — the twelve-month return ending a month ago — inside the top quintile of `r_liquidity_rank`, equally weighted, the rest in cash |
| **The claims** | 1, the signal: it selects stocks whose following month beats the universe average — untested. 2, the sizing: equal weight captures that without a risk model — untested. 3, the construction: the screen makes every position exitable in a day at ordinary volume — true by construction, and expected to cost return |
| **Read for them** | for claim 1, Jegadeesh & Titman (1993) and Asness, Moskowitz & Pedersen (2013), and Jegadeesh (1990) for the skipped month; against the screen, Lesmond, Schill & Zhou (2004) and Ibbotson, Chen, Kim & Hu (2013); on the drawdown, Daniel & Moskowitz (2016). Korajczyk & Sadka (2004), the counterweight to Lesmond et al., is the highest-value lead, unread |
| **Decided** | the window skips the latest month; momentum is a Refinery column, so a sweep costs no download; claim 3 is worded as a cost; the top-quintile cut was chosen for roundness |
| **Open** | five design questions — sizing, absolute or relative, timing, exitability, the seed's look-ahead — and the audit's remaining findings, in `JOURNAL_1.md`, 2026-09-16 |
| **Next, in order** | the fine-tuning pass of `OBJECTIVE.md`; dated membership for the seed; the `c_*` and `r_*` columns and the drivers, run as curator, `universe.ipynb`, refinery, `analyzer.ipynb`; the benchmark entry in `BRAINSTORMING_1.md`; `BLUEPRINT_1.md` before the rule |

## The process, briefly

Eight steps, each a folder, and where `liquid-momentum` is on each. The work does not run in step
order: the objective comes before any paper, and the universe and the data before the blueprint.

| # | Step | What it is | Here |
| --- | --- | --- | --- |
| 1 | **Bibliotheca** | the idea and its claims, then the reading that argues with them | `OBJECTIVE.md` written; six notes in `Bibliotheca/Papers/`, indexed in `BIBLIOGRAPHY.md` |
| 2 | **Universe** | the eligible list, point in time, delisted names kept | the seed, with no dated membership |
| 3 | **Data** | curator, refinery, analyzer: the columns, and whether a feature carries signal | not built; `OBJECTIVE.md` names the columns |
| 4 | **Portfolio** | the rule, turned into weights | not reached: `BLUEPRINT_1.md` comes first |
| 5 | **Backtest** | the simulation, net of costs, in the Backtest Engine | not reached |
| 6 | **Attribution** | which part of the return was factor exposure, and which was selection | not reached |
| 7 | **Paper trading** | a rehearsal on unseen data, and the graduation gate | not reached; the gate is in `Paper_Trading/BITACORA.md` |
| 8 | Production | real capital | outside this repository |

Every file from `Data/` on is still the description of what is expected in it, so it can be read
before it is written.

- **The KaxaNuk Investment Lab** runs steps 3 to 6, from the Data Curator to Attribution Analysis.
  None of its modules has run here yet.
- **The agent skills** teach Claude or Codex the process and the Lab. They are not committed: a
  clone gets them with `uv run apm install --target claude`.
- **The researcher**, [KaxaNuk-Researcher](https://github.com/KaxaNuk/KaxaNuk-Researcher), keeps
  `Bibliotheca/`. The six notes were first written from abstracts; since then one backfill into the
  note convention, one `audit` and one `read` of two sections of Asness, Moskowitz & Pedersen, each
  in `Bibliotheca/LOG.md`.

Every decision is dated in
[`Experiments/Experiment_1/JOURNAL_1.md`](Experiments/Experiment_1/JOURNAL_1.md).

<!-- example: end -->

Built on the [KN Research Process](https://github.com/KaxaNuk/KaxaNuk-Research-Process): eight
steps as a folder structure. That repository's README says what each folder is for, where each
kind of logic goes and, under *Starting your own strategy*, the order to work in; this one does not
repeat it. **Next:** [`OBJECTIVE.md`](OBJECTIVE.md), the idea and its claims, before any paper is
read.

| Read | For |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the idea, and the status of each claim inside it |
| [`RESULTS.md`](RESULTS.md) | every number this repository has measured, and what it cost |
| [`AGENTS.md`](AGENTS.md) | how work is done here, and the bar a result has to clear |
| [`SETUP.md`](SETUP.md) | how this repository is set up on a new machine |
