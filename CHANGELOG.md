# Changelog

Every notable change to this repository, newest first. The format follows the
[KaxaNuk Data Curator convention](https://kaxanuk-data-curator.readthedocs.io/en/latest/release_notes/v0/index.html):
`## X.Y.Z (YYYY-MM-DD)` with `### Added / Changed / Deprecated / Fixed / Removed`, and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) in its numbering.

## Versioning

This is a research repository, not a library, so there is no public API to version. What the team
actually depends on is **the results and the pipeline that produces them**, so that is what the
number tracks:

| Bump | Means | Triggered by |
| --- | --- | --- |
| **MAJOR** | **Published results are invalidated.** Anything quoted from an earlier version has to be re-derived before it can be repeated. | Changing the universe, the date window, the backtest engine or its cost model, or the definition of an existing strategy. Removing a stage. |
| **MINOR** | **New capability; existing results still stand.** | A new experiment, a new signal, a new stage or diagnostic, a new document. Anything additive. |
| **PATCH** | **Nothing about any result changes.** | Bug fixes in tooling, documentation, repository hygiene, refactors that produce byte-identical output. |

Two conventions that follow from reading it this way:

- **A result that changes is a MAJOR bump even if the code change was one line.** The severity is
  measured in what a reader has to throw away, not in the size of the diff.
- **Re-running the pipeline on refreshed data is not a version bump at all.** The strategy did not
  change; only the data did. Say so in the entry and leave the number alone.

**1.0.0 is reserved** for the first strategy that reaches **Paper trading** (step 7 of the KN
Research Process) with its results reproduced from a clean clone. Until then the repository stays on
`0.x`, where the leading zero is doing real work: it says the results are still moving.

**While on `0.x`, a result-invalidating change bumps MINOR rather than MAJOR** — the standard pre-1.0
convention. The first MAJOR bump a repository built from this template ever takes will therefore be
`2.0.0`.

---

## 0.2.0 (2026-09-03)

**MINOR** — additive. The Bibliotheca gains the two books whose method the process runs, and the
lineage the process descends from.

### Added

* **Part 0 of `Bibliotheca/BIBLIOGRAPHY.md` — the process itself.** A lineage table from the KaxaNuk
  deck *Intro to Investment Research*: fifteen questions the field asked in order, who answered each,
  what it settled, and which step or rule of this process descends from it. Provenance, not notes —
  none of the rows is a reading note, because the process is what they changed.
* **Two book notes**, written for any strategy and asking to be re-read against yours:
  [Paleologo (2021)](Bibliotheca/Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md) — total
  PnL as an idiosyncratic series plus a factor series (section 8.1.1, the contract of step 6),
  selection, sizing and timing by counterfactual books, and why a factor model built on relative
  factors is blind to an absolute rule; and
  [Grinold & Kahn (2000)](Bibliotheca/Books/Grinold_Kahn_2000_Active_Portfolio_Management/INDEX.md) —
  the information ratio, the fundamental law IR ≈ IC × √BR, the IC as an out-of-sample correlation,
  the information horizon behind the analyzer's decay chart, and costs as the price of breadth.
* Part 5 now states the one control with no paper behind it — look-ahead — rather than citing a weak
  fit, and the *cited without a note* section records Paleologo (2025), Brinson & Fachler (1985) and
  Brinson, Hood & Beebower (1986) as the trail behind the attribution stage.

### Changed

* `AGENTS.md`'s Bibliotheca section says nine notes ship, in Parts 0 and 5, bracketing the four
  parts that belong to the strategy.

---

## 0.1.0 (2026-09-03)

**MINOR** — the template instantiated. No strategy, no data, no result: the KN Research Process with
nothing in it yet.

### Added

* The eight-step **KN Research Process** as a folder structure, steps 1–7 inside the repository and
  step 8 outside it. Each stage owns its outputs and reads only from the stages above it.
* **Four control documents at the root** — `OBJECTIVE.md`, `RESULTS.md`, `CHANGELOG.md`,
  `AGENTS.md` — with stated contracts, plus `README.md` and a one-line `CLAUDE.md`.
* **One experiment folder, `Experiments/Experiment_1/`**, the benchmark slot, carrying the four
  per-experiment files with their contracts in the header — `BLUEPRINT_1.md` (fixed once written),
  `BRAINSTORMING_1.md` (forward-looking), `JOURNAL_1.md` (append-only, oldest first),
  `FINDINGS_1.md` (feeds `RESULTS.md`) — and a notebook with a fixed section contract in which
  exactly one cell, the rule, is the strategy.
* The two shared modules, `Experiments/panel.py` and `Experiments/engine.py`, and the Data stage's
  three blocks: `Data/curator.py` with a six-function `Data/Curator/custom_calculations.py` (four
  engine-required columns and one two-function worked example), `Data/refinery.py` with a
  four-function `Data/Refinery/custom_calculations.py`, and `Data/analyzer.ipynb`.
* `Universe/universe.ipynb` and the **787-row `Universe/Investable_Universe.csv` seed** — the KaxaNuk
  point-in-time US-equity universe, delisted names retained — so a clean clone runs stages 1–4 with
  the public Data Curator alone.
* `Bibliotheca/` with the note convention and **seven research-integrity notes** — survivorship,
  delisting bias, data-snooping, multiple testing, Sharpe deflation, backtest overfitting, trading
  costs — one per control `AGENTS.md` claims. Their implications are written for *any* strategy;
  each says so and asks to be rewritten against yours.
* `Paper_Trading/BITACORA.md` with the five-criterion graduation gate, and the two skeleton scripts
  carrying their contracts as docstrings.
* Dev container, `Config/.env.template`, Ruff configuration and `.gitignore` as in the reference
  implementation, plus a `.venv/` rule the reference relied on a global excludes file for.

### Provenance

Extracted from **Golden-Flow 0.9.0** (commit `10a0d6b`), the KaxaNuk Investment Lab's reference
implementation, on 2026-09-03. Everything specific to that strategy — its rules, its three
experiments, its results, its fifteen signal papers and its book note — was removed; everything the
process itself needs was kept. Two things were fixed on the way rather than inherited: the shared
`panel.py` no longer names any strategy column, and the six Lab libraries are mapped onto the
stages they replace in `AGENTS.md`.
