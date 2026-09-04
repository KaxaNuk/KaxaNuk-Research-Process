# Changelog

Every notable change to this repository, newest first. The format follows the
[KaxaNuk Data Curator convention](https://kaxanuk-data-curator.readthedocs.io/en/latest/release_notes/v0/index.html):
`## X.Y.Z (YYYY-MM-DD)` with `### Added / Changed / Deprecated / Fixed / Removed`, and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) in its numbering.

## What a version number means here

This is a research repository, not a library, so there is no public API to version. What the team
actually depends on is **the results and the pipeline that produces them**, so that is what the
number tracks:

| Bump | Means | Triggered by |
| --- | --- | --- |
| **MAJOR** | **Published results are invalidated.** Anything quoted from an earlier version has to be re-derived before it can be repeated. | Changing the universe, the date window, the backtest engine or its cost model, or the definition of an existing strategy. Removing a stage. |
| **MINOR** | **New capability; existing results still stand.** | A new experiment, signal, stage, diagnostic or document. Anything additive. |
| **PATCH** | **Nothing about any result changes.** | Bug fixes in tooling, documentation, repository hygiene, refactors that produce byte-identical output. |

Three conventions follow from reading it that way:

- **A result that changes is a MAJOR bump even if the code change was one line.** Severity is measured
  in what a reader has to throw away, not in the size of the diff.
- **Re-running the pipeline on refreshed data is not a version bump at all.** The strategy did not
  change; only the data did. Say so in the entry and leave the number alone.
- **While on `0.x`, a result-invalidating change bumps MINOR** — the standard pre-1.0 convention. The
  first MAJOR bump a repository built from this template ever takes will therefore be `2.0.0`.

**1.0.0 is reserved** for the first strategy that reaches **paper trading** (step 7) with its results
reproduced from a clean clone. Until then the leading zero is doing real work: it says the results are
still moving.

## How to write an entry

One entry per change-set, newest at the top. Under the heading, **one sentence saying what a reader
has to do differently** — that is the part people actually read. Then the `Added / Changed / Removed`
lists, each item written for somebody who was not in the room:

- **Say what moved and why, not what file you touched.** "The regime model lives in the Refinery so a
  penalty sweep costs no download" is an entry; "updated custom_calculations.py" is a diff.
- **Name anything that invalidates a number**, and say which number.
- **A removal is a change-set too.** Deleting a stage that nobody could trace is worth an entry.

---

## 0.3.0 (2026-09-03)

**MINOR** — the template gains a worked example, and stops being US-equity-shaped. Nothing published
is invalidated because nothing had been published: at 0.2.0 there were no results.

**What to do differently:** the repository is now multi-asset by default and the universe is twelve
lines of CSV. If you are starting a strategy, replace `Universe/Investable_Universe.csv` and the two
`custom_calculations.py` files, and read `README.md` rather than `AGENTS.md` first.

### Added

* **A worked example that runs end to end in under a minute** — twelve asset-class ETFs, a
  statistical jump model labelling each one's regime daily. Universe, data and analysis are complete;
  no book has been backtested. After
  [Shu, Yu & Mulvey (2024)](Bibliotheca/Papers/Shu_Yu_Mulvey_2024_Dynamic_Asset_Allocation_With_Asset_Specific_Regime_Forecasts.md).
* **`Experiments/attribution_analysis.py`** — step 6, split out of the engine so the two KaxaNuk
  libraries live in one module each. It owns the shaping of the hand-supplied index data into the
  tables the library auto-detects, and reports which of its four inputs are missing before it
  tries. Getting that layout wrong makes the loader read the attribution transposed rather than
  fail, which is why the shaping is not left in a notebook.
* **`Experiments/portfolio_construction.py`** — step 4, behind one swappable signature: given
  the securities eligible today and a returns history already cut off before today, return
  weights summing to **at most** one. `equal_weight` and `inverse_volatility` ship; a
  minimum-variance optimiser, hierarchical risk parity, or a call into the KaxaNuk Portfolio
  Construction library are the same shape, so swapping one is one line in the rule cell.
* **Experiment 1 is written and built.** `BLUEPRINT_1.md` fixed four predictions from the
  analyzer *before* the rule cell existed, and the construction stage **falsified one of them**
  without the engine: the book is 95.3% invested, not the predicted ~55%, because equal weight
  over a shrinking eligible set concentrates rather than de-risking. The benchmark is a
  rotation, not a risk reducer.
* **`dev`, the architecture with nothing in it.** An orphan branch carrying the folder structure
  and its `.gitkeep` files and nothing else — no code, no documents, no shared history with
  `main`. What you copy when you want the shape and intend to write every line yourself.
* **Example markers in the source.** `# --- example: begin ---`, `<!-- example: begin -->` and
  `# EXAMPLE-ONLY CELL` mark every line that belongs to the worked example rather than to the
  process, so somebody starting their own strategy can see what to delete without a diff.
* **The branching model, written down.** `main` (the repository), `dev` (the empty architecture),
  and `issues/<number>` cut from `main` and merged back into it — one per issue on the GitHub
  Project, opened before the branch because the issue is where the reasoning lives. `AGENTS.md`
  carries the loop and the pull-request checklist.
* **A run order that is stated in six places.** `README.md` numbers the six commands, and every
  file in the pipeline says where it sits in that order in its first paragraph, so wherever you
  land you know what must have run before it.
* **`Data/Refinery/jump_model.py`** — a statistical jump model in one readable file: coordinate
  descent over a dynamic program, deterministic initialisation from the training returns, and a
  rolling refit that never lets a model label a day it was trained on. It returns the **causal**
  label; the smoothed one is available only where it is labelled as not tradable.
* **Nine `c_*` feature columns** in the Curator — the source paper's eight, at its half-lives, plus
  the daily total return they are built on. Arithmetic only, no fitted parameter, which is why they
  can live in a stage a refetch is expensive in.
* **Eight `r_*` columns** in the Refinery: the regime label, its bull switch, cross-sectional breadth,
  and per-date ranks of momentum, Sortino, downside deviation and liquidity.
* **A measurement of what look-ahead is worth: 44 annualised points**, from reading one fitted model
  two ways in `Data/analyzer.ipynb` section 5. `Bibliotheca` Part 5 previously recorded look-ahead as
  the one control with no evidence behind it; this closes that.
* **A step-3 findings section in `RESULTS.md`.** Notebook outputs are stripped before committing, so a
  measurement that lived only in a cell output did not survive the commit. Findings from the Data
  stage now have a durable home.
* Two paper notes, and Parts 1 to 4 of `BIBLIOGRAPHY.md` restocked with real leads for regimes,
  universe and data, portfolio construction, and backtest and attribution. A source without a note is
  now explicitly a *lead*, not a citation.

### Changed

* **`Universe/Investable_Universe.csv` is twelve ETFs instead of 787 US equities**, with a schema the
  strategy chooses: only `ticker` and `name` are required. Every stage downstream reads it without
  knowing what is in it, so a crypto, FX or futures seed runs the same pipeline.
* **`Data/curator.py` rewritten** — 851 lines to 652, and the reduction is the smaller half of it.
  Work is handed out one identifier at a time through a plain thread pool with thread-local
  providers, replacing a chunked worker scheme, a shared mutable tally object and a lock-guarded
  progress counter; `download_identifier` now returns an outcome string instead of mutating shared
  state, so it can be read and tested on its own. The equity-only `sector_sample` mode and the
  hand-supplied price-series staging are gone.
* **The daily return moved from the Refinery to the Curator**, as `c_return_1d`. It is a function of
  one security's own history, so it was in the wrong stage — and the whole feature set is built on it.
* **`Data/refinery.py` joins whatever the security master classifies by**, reporting and skipping a
  column the master does not carry instead of joining it in as nulls. The `sector`/`industry`
  hard-coding is gone; the `_current` suffix rule that made it safe stays.
* **`Universe/universe.ipynb` rewritten**, from 49 cells to 20, and no longer equity-shaped. It now
  answers the question everybody forgets: **when does each asset become usable?** On the example a
  five-year training window moves the honest start of a backtest from 2010 to 2016-04-12.
* **`Data/analyzer.ipynb` rewritten**, from a generic EDA to a set of questions with answers: what
  diversification exists, whether the signal separates risk or return, what look-ahead is worth, and
  whether the conclusion survives the parameter sweep.
* **`AGENTS.md` cut from 624 lines to 379.** Everything the README now covers — the eight steps, the
  column convention, setup, credentials, the shared modules — was removed rather than restated. What
  is left is what the README does not say: who writes each document, the restrictions, the integrity
  controls, and the known gaps. Versioning moved here, to the file that already explained it.
* **`README.md` rewritten as the entry point**: five numbered steps that run the example, then a
  walkthrough of the eight process steps in the order to do them, then one table saying where each
  kind of logic goes. **The run order is now stated as a dependency**: the universe notebook profiles
  files the curator downloaded, and writes the security master the refinery joins, so it sits between
  them. Running the refinery first is not an error and that is the problem — it names the columns it
  drops and carries on.
* **The shared modules are renamed for what they hold**: `Experiments/panel.py` is now
  `securities_panel.py`, and `Experiments/engine.py` is now `backtest_engine.py` — joined by the new
  `portfolio_construction.py`, so `Experiments/` now reads as panel in, weights, engine out. They stay two files
  rather than becoming one because `securities_panel.py` is pure pandas while `backtest_engine.py`
  reaches for the licensed KaxaNuk library, and merging would put two very different dependencies in
  the module every notebook imports just to read data. `panel` also collides with a PyPI package of
  that name.
* **`securities_panel.py` names no classification column in `BASE_PANEL_COLUMNS`.** Classification is
  optional and discovered from the files, so a security master that classifies by something else — or
  not at all — changes one tuple. It also now raises a readable error naming the missing columns
  instead of failing inside `read_csv`.
* **`Experiments/backtest_engine.py` reports against `AOR` and `SPY`**, the benchmarks the curator actually
  fetches. AOR is primary: a multi-asset book measured only against the S&P 500 is being asked the
  wrong question. The attribution file names are now visibly placeholders, since attribution has
  never been run here.
* `OBJECTIVE.md` states the example strategy and, at the bottom, how to write your own. Its claims
  table carries a **falsified** row, which is the most useful row in it.
* The bar in `AGENTS.md` gains a clause: **never choose a parameter on the metric it will be judged
  by.** The source paper selects its jump penalty on cross-validated Sharpe; we select on persistence
  and publish the sweep, and accept that this costs us the ability to claim its numbers.

### Removed

* `stage_supplied_price_series` and its engine-column fallbacks from the Curator. It existed to stage
  a hand-supplied index price series into the market-data directory; the example's benchmarks are
  downloadable, and machinery kept for a file that does not exist teaches the reader to keep
  machinery for files that do not exist. The drop-zone directories and the *what is missing* report
  stay.
* The `sector_sample` download mode. `r_liquidity_zscore` moves to the skeleton, where it is
  the worked example of per-date normalisation; the example branch has real features instead.
* **The 787-row US-equity universe, deleted rather than archived.** A template carrying two universes
  makes a reader ask which one is real. It is recoverable from history at
  `53ba89d:Universe/Investable_Universe.csv` if it is ever needed again, and the ~400 MB of
  downloaded equity price files it produced went with it — all of them regenerable by one command
  against that seed.

---

## 0.2.0 (2026-09-03)

**MINOR** — additive. The Bibliotheca gains the two books whose method the process runs, and the
lineage the process descends from.

### Added

* **Part 0 of `Bibliotheca/BIBLIOGRAPHY.md` — the process itself.** A lineage table from the KaxaNuk
  deck *Intro to Investment Research*: fifteen questions the field asked in order, who answered each,
  what it settled, and which step or rule of this process descends from it. Provenance, not notes.
* **Two book notes**:
  [Paleologo (2021)](Bibliotheca/Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md) — total
  PnL as an idiosyncratic series plus a factor series, selection/sizing/timing by counterfactual
  books, and why a factor model built on relative factors is blind to an absolute rule; and
  [Grinold & Kahn (2000)](Bibliotheca/Books/Grinold_Kahn_2000_Active_Portfolio_Management/INDEX.md) —
  the information ratio, the fundamental law IR ≈ IC × √BR, and the information horizon behind the
  analyzer's decay chart.
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
