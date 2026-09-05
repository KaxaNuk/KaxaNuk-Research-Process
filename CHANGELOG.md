# Changelog

Every notable change to this repository, newest first. The format is
`## X.Y.Z (YYYY-MM-DD)` with `### Added / Changed / Deprecated / Fixed / Removed`, and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) in its numbering.

## What a version number means here

This is a research repository, not a library, so there is no public API to version. What the team
depends on is **the results and the pipeline that produces them**, so that is what the number
tracks:

| Bump | Means | Triggered by |
| --- | --- | --- |
| **MAJOR** | **Published results are invalidated.** Anything quoted from an earlier version has to be re-derived before it can be repeated | Changing the universe, the date window, the backtest engine or its cost model, or the definition of an existing strategy. Removing a stage |
| **MINOR** | **New capability; existing results still stand** | A new experiment, signal, stage, diagnostic or document. Anything additive |
| **PATCH** | **Nothing about any result changes** | Bug fixes in tooling, documentation, repository hygiene, refactors that produce identical output |

Three conventions follow from reading it that way:

- **A result that changes is a MAJOR bump even if the code change was one line.** Severity is
  measured in what a reader has to throw away, not in the size of the diff.
- **Re-running the pipeline on refreshed data is not a version bump at all.** The strategy did not
  change; only the data did. Say so in the entry and leave the number alone.
- **While on `0.x`, a result-invalidating change bumps MINOR** — the standard pre-1.0 convention.

**1.0.0 is reserved** for the first strategy that reaches **paper trading** (step 7) with its
results reproduced from a clean clone. Until then the leading zero is doing real work: it says the
results are still moving.

## How to write an entry

One entry per change-set, newest at the top. Under the heading, **one sentence saying what a reader
has to do differently** — that is the part people actually read. Then the lists, each item written
for somebody who was not in the room:

- **Say what moved and why, not what file you touched.** "The regime model lives in the Refinery so
  a penalty sweep costs no download" is an entry; "updated custom_calculations.py" is a diff.
- **Name anything that invalidates a number**, and say which number.
- **A removal is a change-set too.** Deleting a stage that nobody could trace is worth an entry.

---

## 0.4.0 (2026-09-04)

**MINOR** — `main` becomes a description-only template. **There is no code on it any more:** every
file is a short statement of what is expected in it.

**What to do differently:** nothing on `main` runs. Read it to learn the shape, fill it in with your
own idea, or `git switch example` for one strategy worked end to end.

### Removed

* **All executable code.** The Curator and Refinery drivers, the two calculation modules and every
  notebook code cell are now docstrings and markdown. A template whose example code has to be
  deleted before you can start is a template that gets started by deleting things.
* **The four shared experiment modules**, the nine Bibliotheca notes and the lockfile — they belong
  to a filled-in repository, and they are on `example`.
* **The dev container** and its Docker build context. Setting the environment up is two commands,
  and a container that has to be rebuilt whenever the process changes is a second thing to maintain.

### Changed

* **Every remaining file describes what is expected in it**, in the same shape: what the stage is in
  plain words, what it produces, what it prevents, and the sections it owes. Learn the shape once.
* **`README.md` rewritten around the eight steps**, each with its plain-words sentence, its output
  and the failure it prevents, plus the six Lab modules mapped one per stage and the conventions
  worth keeping when two people share a tool.
* **`AGENTS.md` cut roughly in half.** The five ways a backtest lies are one table — the lie, what
  the process does, what it still does not do. Everything the README covers was removed rather than
  restated.
* **The source-note convention moved to `Bibliotheca/BIBLIOGRAPHY.md`**, next to the notes it
  governs. Its Part 0 keeps the lineage the process descends from, as provenance rather than notes.
* **`Universe/Investable_Universe.csv` requires only `main_identifier`** — the name the Data Curator
  asks a provider for. Every other column is yours, so an equity, ETF, FX, crypto or futures seed
  runs the same process.
* **`Config/.env.template` carries the Data Curator's provider keys**, not one.
* **Joined classification columns are prefixed `current_`**, not suffixed `_current`, so every column
  family is a prefix, and the prefix alone says which stage owns a column and whether it is
  point-in-time.

## 0.3.0 (2026-09-04)

**MINOR** — the template stops being US-equity-shaped, gains a fourth shared module, and splits into
two branches: `main` is the process with nothing in it, `example` is one strategy worked end to end.

**What to do differently:** the universe is now a CSV whose only required columns are `ticker` and
`name`, so the repository is multi-asset by default. Name your signal in two places —
`ELIGIBILITY_COLUMN` in `Data/analyzer.ipynb` and `SIGNAL_COLUMN` in the experiment notebook — and
the benchmark rule runs without being written.

### Added

* **`Experiments/portfolio_construction.py`** — step 4, behind one swappable signature: given the
  securities eligible today and a returns history already cut off before today, return weights
  summing to **at most** one. `equal_weight` and `inverse_volatility` ship; a minimum-variance
  optimiser, hierarchical risk parity, or a call into the KaxaNuk Portfolio Construction library are
  the same shape, so swapping one is one line in the rule cell.
* **`Experiments/attribution_analysis.py`** — step 6, split out of the engine so the two KaxaNuk
  libraries live in one module each. It owns the shaping of hand-supplied index data into the tables
  the library auto-detects, and reports which of its four inputs are missing before it tries. Getting
  that layout wrong makes the loader read the attribution transposed rather than fail, which is why
  the shaping is not left in a notebook.
* **A benchmark rule that works out of the box.** Section 2 of the experiment notebook holds
  everything the signal calls eligible, equally weighted, cash for the rest — event-driven, one day
  of lag. It runs as soon as `SIGNAL_COLUMN` is set, because a benchmark you have to write before you
  can measure anything is a benchmark that never gets written.
* **A run order that is stated in seven places.** `README.md` numbers the six commands, and every
  file in the pipeline says where it sits in that order in its first paragraph, so wherever you land
  you know what must have run before it.
* **The branching model, written down.** `main` (the template), `example` (one strategy, for reading)
  and `issues/<number>` cut from `main` and merged back into it — one per issue on the GitHub
  Project, opened before the branch because the issue is where the reasoning lives.
* **Example markers.** `# --- example: begin ---`, `<!-- example: begin -->` and
  `# EXAMPLE-ONLY CELL` mark any line that belongs to a worked example rather than to the process, so
  the two branches can be told apart by reading rather than by diffing.
* **A step-3 findings section in `RESULTS.md`.** Notebook outputs are stripped before committing, so
  a measurement that lived only in a cell output did not survive the commit. Findings from the Data
  stage now have a durable home.

### Changed

* **`Universe/Investable_Universe.csv` requires only `ticker` and `name`.** Every stage reads it
  without knowing what is in it, so a crypto, FX or futures seed runs the same pipeline. The 787-row
  US-equity seed is gone.
* **`Data/curator.py` rewritten** — 851 lines to 652, and the reduction is the smaller half of it.
  Work is handed out one identifier at a time through a plain thread pool with thread-local
  providers, replacing a chunked worker scheme, a shared mutable tally object and a lock-guarded
  progress counter; `download_identifier` now returns an outcome string instead of mutating shared
  state. An empty universe file is reported as a sentence rather than a traceback.
* **`Data/refinery.py` deletes refined files for securities no longer in the universe.** Leaving
  them was the worst kind of bug this stage can have: every cross-sectional column is computed over
  the securities present, so a stale file carries ranks taken against a universe that no longer
  exists, and anything reading the directory silently averages two incompatible cross-sections. It
  produced a plausible number and no error.
* **The daily return moved from the Refinery to the Curator**, as `c_return_1d`. It is a function of
  one security's own history, so it was in the wrong stage.
* **`Data/refinery.py` joins whatever the security master classifies by**, reporting and skipping a
  column the master does not carry instead of joining it in as nulls. The `sector`/`industry`
  hard-coding is gone; the `_current` suffix rule that made it safe stays.
* **The shared modules are renamed for what they hold**: `panel.py` is now `securities_panel.py` and
  `engine.py` is now `backtest_engine.py`, joined by the two new modules — so `Experiments/` reads as
  panel in, weights, engine out, attribution.
* **`securities_panel.py` names no classification column in `BASE_PANEL_COLUMNS`.** Classification is
  optional and discovered from the files, and a missing column raises a readable error naming it
  rather than failing inside `read_csv`.
* **`Universe/universe.ipynb` rewritten**, from 49 cells to 20, and no longer equity-shaped. It now
  answers the question everybody forgets: **when does each security become usable?** A five-year
  warm-up moves the honest start of a backtest by five years, and nothing else in the pipeline says
  so.
* **`Data/analyzer.ipynb` rewritten** around the information-coefficient table, with the two
  questions any signal owes an answer to written into its header: does it separate anything, and if
  it is fitted, what is look-ahead worth?
* **`AGENTS.md` cut from 624 lines to about 380.** Everything the README covers — the eight steps,
  the column convention, setup, credentials, the shared modules — was removed rather than restated.
  Versioning moved here, to the file that already explained it.
* **`README.md` rewritten as the entry point**: six numbered steps that run the pipeline, a
  walkthrough of the eight process steps in the order to do them, and one table saying where each
  kind of logic goes. **The run order is stated as a dependency**, because the universe notebook sits
  between two Data commands and running the refinery early does not fail — it silently drops columns.
* **The invariant that weights sum to 1.0 is now "at most 1.0".** A strategy that can go to cash
  cannot satisfy the stricter form, and the engine already parks the residual in a real, priced
  instrument.
* **The bar in `AGENTS.md` gains a clause:** never choose a parameter on the metric it will be judged
  by. Choose it on a property of the signal — persistence, coverage, turnover — and publish the
  sweep.

### Removed

* `stage_supplied_price_series` and its engine-column fallbacks from the Curator. It staged a
  hand-supplied index price series into the market-data directory; machinery kept for a file that
  does not exist teaches the reader to keep machinery for files that do not exist. The drop-zone
  directories and the *what is missing* report stay.
* The `sector_sample` download mode, and the 787-row US-equity universe with it.

## 0.2.0 (2026-09-03)

**MINOR** — additive. The Bibliotheca gains the two books whose method the process runs, and the
lineage the process descends from.

### Added

* **Part 0 of `Bibliotheca/BIBLIOGRAPHY.md` — where the process comes from.** Fifteen questions the
  field asked in order, who answered each, what it settled, and which step or rule of this process
  descends from it. Provenance, not notes.
* **Two book notes**: Paleologo (2021) — total PnL as an idiosyncratic series plus a factor series,
  selection, sizing and timing by counterfactual books, and why a factor model built on relative
  factors is blind to an absolute rule; and Grinold & Kahn (2000) — the information coefficient, the
  fundamental law, and the information horizon behind the analyzer's decay chart.
* Part 5 states the one control with no paper behind it — look-ahead — rather than citing a weak fit.

---

## 0.1.0 (2026-09-03)

**MINOR** — the template instantiated. No strategy, no data, no result: the KN Research Process with
nothing in it yet.

### Added

* The eight-step **KN Research Process** as a folder structure, steps 1-7 inside the repository and
  step 8 outside it. Each stage owns its outputs and reads only from the stages above it.
* **Four control documents at the root** — `OBJECTIVE.md`, `RESULTS.md`, `CHANGELOG.md`, `AGENTS.md`
  — with stated contracts, plus `README.md` and a one-line `CLAUDE.md`.
* **`Experiments/Experiment_1/`**, the benchmark slot, with its four per-experiment files and a
  notebook whose section contract leaves exactly one cell — the rule — to the strategy.
* The two shared modules, `Experiments/securities_panel.py` and `Experiments/backtest_engine.py`, and the Data stage's
  three blocks.
* `Universe/universe.ipynb` and the 787-row `Universe/Investable_Universe.csv` seed.
* `Bibliotheca/` with the note convention and **seven research-integrity notes**, one per control
  `AGENTS.md` claims.
* `Paper_Trading/BITACORA.md` with the five-criterion graduation gate, and two skeleton scripts
  carrying their contracts as docstrings.
* Dev container, `Config/.env.template`, Ruff configuration and `.gitignore`.

### Provenance

Extracted from **Golden-Flow 0.9.0** (commit `10a0d6b`), the KaxaNuk Investment Lab's reference
implementation, on 2026-09-03. Everything specific to that strategy was removed; everything the
process itself needs was kept.
