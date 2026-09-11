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

## 0.7.1 (2026-09-11)

**PATCH** — what a `Bibliotheca/` holds, now that a researcher writes its notes a chapter at a
time. No result changes.

**What to do differently:** keep the PDFs beside their notes and let git ignore them, along with
`Bibliotheca/Extracts/`, where the researcher's script leaves a book's chapters as text. A book is
a folder — `Books/Author_Year_Title/INDEX.md` for the chapter table, one file per chapter read —
and `Bibliotheca/Knowledge/` is gone: the notes beside the sources are the library, `BIBLIOGRAPHY.md`
is its index and `Bibliotheca/LOG.md` its record. The files themselves are on
[`example`](../../tree/example).

### Added

* **`AGENTS.md` says who writes a note:** a person, or a researcher with `read`, after a plan and a
  go; whoever writes a note adds its row to `BIBLIOGRAPHY.md`. It was the one step-1 document the
  table did not name.
* **`.gitignore` keeps the PDFs and the extracts out**, as step 1's own section. Licensed material
  is not redistributed by a clone, and the extracts regenerate with one command.

### Changed

* **`README.md`'s `Bibliotheca/` row describes the folder as it is now** — notes beside their PDFs,
  a book as a folder of chapters, `LOG.md` — and its researcher section says what the companion
  actually does here rather than that it is being built. `KaxaNuk/KaxaNuk-Researcher` 0.3.0 is the
  version that writes these notes.

---

## 0.7.0 (2026-09-10)

**MINOR** — `main` is the shape and nothing else: six folders and the documents at the root. Every
file the process expects inside those folders moved to the public `example` branch, unchanged.

**What to do differently:** `main` no longer ships `Experiment_1`, the drivers, the notebooks or the
shared modules. Bring a file across from `example` when you need it — `README.md` gives the one
command — or let the `experiment-lifecycle` skill scaffold an experiment.

### Removed

* **Everything below the six folders**, moved to `example` as it was: `Bibliotheca/`'s index,
  `Knowledge/`, `Notes/`, `Papers/` and `Books/`; `Universe/`'s seed and notebook; `Data/`'s three
  drivers, the two `custom_calculations.py` and the data directories; `Experiments/`' four shared
  modules and `Experiment_1/`; `Paper_Trading/`'s gate and scripts. `Config/.env.template` stays,
  because setup needs it. A reader opening `main` now sees the shape in one screen, and a reader
  who wants the files finds all of them on one branch rather than half here and half there.

### Changed

* **`README.md`'s *What is in here* is the one place the folder contents are written down** — a
  table per folder saying which step owns it, what belongs in it and what is committed. The old
  tree listed files that are no longer on `main`.
* **`README.md`'s Setup section is a pointer to `SETUP.md`**, with no commands of its own. Two
  copies of the same commands had already started to differ.
* **`example` is public, in this repository, beside `main`.** `README.md`, `SETUP.md` and
  `AGENTS.md` said it was private; it holds no strategy, so there was nothing to keep private. A
  strategy worked end to end still stays in KaxaNuk's own repositories.

---

## 0.6.0 (2026-09-06)

**MINOR** — one prompt sets a strategy up from nothing. *Please help install
`https://github.com/KaxaNuk/KaxaNuk-Research-Process`* is now enough for an agent with no other
context, and the manifest names one package so the template cannot go stale.

**What to do differently:** the skills command is `uv run apm install --target claude` (or `codex`),
not a bare `apm install`, and there is nothing to install by hand before `uv sync` — not even Python.

### Changed

* **`SETUP.md` was run as an agent would run it, and rewritten where it broke.** Handed only the
  URL, an agent does not know the strategy's name — it now asks, and decides the root from what the
  current folder holds. `apm` lives inside `.venv/` and is not on a fresh terminal's path, so every
  skills command is `uv run apm …`. The fresh-history sequence is given in PowerShell as well as
  bash, because that is what the Claude app and Codex drive on Windows. A first commit on a machine
  that has never committed fails for want of a git identity; the agent asks for one and sets it for
  the repository only. Prerequisites shrink to git and uv, each with its one-line installer — `uv`
  downloads Python 3.13 itself. A hand-over paragraph says what the agent reports and where it stops.
* **`apm.yml` names one package, `kaxanuk`.** It is every KaxaNuk package under one name, and it
  resolves transitively — verified. The template listed four packages by hand and was already stale:
  `attribution-analysis` had shipped and a fresh install missed it. Replace the line with the packages
  you want if you want fewer.
* **The skills question has an answer when the request already gave one.** *Install it and the
  skills* is consent and the agent runs it; a bare *set this up* still gets asked. `AGENTS.md` and
  `SETUP.md` say the same rule.
* **A plain clone ends with no remote, and `SETUP.md` now says so** — GitHub Desktop, *Add existing
  repository*, *Publish*. The user's to do, not the agent's.

---

## 0.5.1 (2026-09-06)

**PATCH** — documentation. `SETUP.md` says what a finished setup actually leaves behind.

**What to do differently:** commit `uv.lock`. `uv sync` writes it, the template ships without one on
purpose, and your repository keeps it — it pins the versions a result came from.

### Fixed

* **The "what done looks like" check said `git status` would be clean; a real run leaves `uv.lock`
  untracked.** Running the file end to end from a fresh clone is what caught it, which is the reason
  the check is in `SETUP.md` at all.

---

## 0.5.0 (2026-09-06)

**MINOR** — the repository now carries its own setup instructions and declares which agent skills it
wants. No result changes; nothing in the pipeline moved.

**What to do differently:** set a strategy up from [`SETUP.md`](SETUP.md) rather than from a prompt
held in another repository. `apm install` needs no arguments, and it is a question you get asked
rather than a step you have to run.

### Added

* **`SETUP.md` — the whole of setup in one file**, written so an agent can follow it end to end:
  getting the repository (the template button, `gh repo create`, or a plain clone with a fresh
  history), the one-folder rule, `uv sync`, the credential copy, and — last, and as a question — the
  agent skills. It replaces the `start-a-strategy` prompt that lived in `KaxaNuk/KaxaNuk-APM`, on the
  rule that **the instruction to install a thing belongs with that thing**. A bootstrap you can only
  reach after installing the tool it bootstraps is a bootstrap that gets pasted from a URL.
* **`apm.yml`, committed.** It names the KaxaNuk packages this repository wants, so `apm install`
  takes no arguments and nobody types a package name. It carries no `targets` key on purpose: the
  template serves Claude Code, the Claude app, Codex and Cursor alike, so the target is set on the
  machine or passed per command.

### Changed

* **`.gitignore` stops ignoring `apm.yml`**, and says why: the manifest is a declaration, like
  `pyproject.toml`, while everything APM downloads and writes — `apm_modules/`, `.claude/`,
  `apm.lock.yaml` — is build output, ignored the way `.venv/` is. **A clean `git status` after a full
  setup is the test** that the split is right.
* **`AGENTS.md` opens with a *First run* block**, before anything about branches. An agent that finds
  no `.venv/` or `apm_modules/` offers `SETUP.md` instead of starting work in a repository that has
  not been set up, and the two rules it must not get wrong are restated there: never print a value
  from `Config/.env`, and ask before installing the skills.
* **`README.md`'s Setup section is three commands and a link.** One source, so the two cannot drift.
* **Python is `>=3.12,<3.14`, and 3.13 is the one to install.** The ceiling is the Backtest
  Engine's: it is documented for 3.12 or 3.13, and every performance figure here comes from that
  engine, so a version it cannot be installed beside is a version that cannot finish the pipeline.
  The Data Curator allows 3.12 to 3.14, which leaves 3.13 as the version that satisfies both. Ruff
  targets `py313` to match. Widen it when the engine supports 3.14.
* **`SETUP.md` says to clone somewhere short on Windows.** APM stages downloads several directories
  below the root, so a deep synced path fails part-way through with `WinError 3: The system cannot
  find the path specified`. The same install from a short path succeeds, which is why the message is
  worth naming: it reads like a missing file, not like a path-length limit.

---

## 0.4.1 (2026-09-05)

**PATCH** — documentation. `README.md` now states the setup order and the layout it has to produce.
No result and no file in the pipeline changed.

**What to do differently:** set a strategy up in **one** folder. The clone is the root; `uv sync`,
`apm init` and `apm install` all run in it, and the agent tooling lands beside the process folders
rather than in a directory above them.

### Changed

* **`README.md` gains an ordered Setup** — the repository named after the strategy, cloned, then
  `uv sync`, `apm init -y --target claude`, `apm install KaxaNuk/KaxaNuk-APM/common`, then the
  credential file. The order is a dependency: `apm-cli` arrives with the `dev` group, so the
  environment has to exist before APM can be initialised.
* **The setup section shows the root it should produce**, and names the failure it is there to
  prevent: a wrapper folder holding the clone. Initialising APM in an empty wrapper writes a second
  `apm.yml`, a second `.claude/` and a `requirements-dev.txt` that only exists because the wrapper
  has no `pyproject.toml` — and Claude opened at the wrapper reads that empty setup and never sees
  the research tree.
* **"The tools" moved above "Setup"**, so the README reads install-once, then set-one-strategy-up,
  then start it. The APM paragraph says where the packages land rather than only how the CLI
  arrives.

---

## 0.4.0 (2026-09-04)

**MINOR** — `main` becomes a description-only template. **There is no code on it any more:** every
file is a short statement of what is expected in it.

**What to do differently:** nothing on `main` runs. Read it to learn the shape, fill it in with your
own idea, or read the `example` branch KaxaNuk keeps beside `main` for one strategy worked end to
end.

### Added

* **`LICENSE` — MIT**, the Data Curator's licence, so the template can be public, forked and
  contributed to without friction. `main` lives at `KaxaNuk/KaxaNuk-Research-Process`.
* **The tools, and a researcher beside the process.** `README.md` names the four tools — GitHub
  Desktop, PyCharm, Claude, and the APM packages through which Claude learns the six modules — and
  points at `KaxaNuk/KaxaNuk-Researcher`, a companion that reads a strategy's `Bibliotheca/` and
  drafts the hypothesis in each blueprint from it.
* **Attribution in two layers and a third pass.** `AGENTS.md` now says what each layer answers:
  Brinson-Fachler names the lever that moved, the factor model separates compensated tilts from
  idiosyncratic alpha, and Brinson-Fachler on the residual says whether the Sharpe survives once
  the factor turns. The notebook, the module and the gate say the same.

### Removed

* **All executable code.** The Curator and Refinery drivers, the four shared experiment modules,
  the two calculation modules and every notebook code cell are now docstrings and markdown. A template whose example code has to be
  deleted before you can start is a template that gets started by deleting things.
* **The nine Bibliotheca notes and the lockfile** — they belong to a filled-in repository, and they
  are on `example`.
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
* **Bibliotheca notes carry their four fields as frontmatter**, so a tool can index what cites
  what, and **blueprint predictions cite a note or a measurement** — never nothing.

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
