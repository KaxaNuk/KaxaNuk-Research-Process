# KN Research Process

**v0.1.0 — the template.** A US-equity research repository with no strategy in it yet: the
**KaxaNuk Investment Lab**'s eight-step process as a folder structure, its document architecture with
every file's contract stated, and the code that makes a clean clone run. Copy it to start a
strategy; the reference implementation it was extracted from is **Golden Flow**.

> **<The strategy's main idea, in one sentence, once there is one.>**

> **Status: template. Nothing has been tested here.** Read [`OBJECTIVE.md`](OBJECTIVE.md) to see
> what a strategy has to state, [`RESULTS.md`](RESULTS.md) to see what it has to report, and
> [`AGENTS.md`](AGENTS.md) to see how work is done.

## Starting a strategy from this template

In this order. Each step is the smallest change that makes the next one possible.

1. **Name it.** `name` in `pyproject.toml`; the kernel name and display name in
   `.devcontainer/Dockerfile`; `name` and the service in `.devcontainer/docker-compose.yml` and
   `.devcontainer/devcontainer.json`. Replace `<Strategy_Name>` wherever it appears in the documents.
2. **State the idea** in [`OBJECTIVE.md`](OBJECTIVE.md): the main idea, the objective, the claims
   inside it. Every slot in angle brackets is guidance; none survives.
3. **Write the hypothesis** in `Experiments/Experiment_1/BLUEPRINT_1.md` — *before* the rule. It
   never changes afterwards.
4. **Compute the signal.** Add its `c_*` function to `Data/Curator/custom_calculations.py` and list
   it in `CUSTOM_COLUMNS` in `Data/curator.py`. Cross-sectional features go in
   `Data/Refinery/custom_calculations.py`.
5. **Point the notebooks at it.** `SIGNAL_COLUMN` in `Universe/universe.ipynb`, `ELIGIBILITY_COLUMN`
   and the feature lists in `Data/analyzer.ipynb`, `SIGNAL_COLUMN` and `SIZING_COLUMN` in the
   experiment notebook's setup cell. Those are the only strategy names outside the rule itself.
6. **Write the rule** — section 2 of `Experiments/Experiment_1/experiment_1.ipynb`, the one cell that
   raises until you do. Everything after it runs unchanged.
7. **Fill `Config/.env`** from the template and run the pipeline, below.

## The documents

**Two files answer "is this worth anything?"** — [`OBJECTIVE.md`](OBJECTIVE.md) says what we are
trying to do, [`RESULTS.md`](RESULTS.md) says how far we got and what it cost.

| Document | What it holds |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the main idea, what the strategy is trying to do, and the status of the claims inside it |
| [`RESULTS.md`](RESULTS.md) | the executive summary of every experiment, compiled from the `FINDINGS_N.md` files, with the methods record as an appendix |
| [`CHANGELOG.md`](CHANGELOG.md) | every version of the repository, newest first |
| [`AGENTS.md`](AGENTS.md) | **how work is done here** — what belongs in each file, the restrictions, the bar a result must clear, the house rules |
| [`CLAUDE.md`](CLAUDE.md) | one line; points an AI assistant at `AGENTS.md` |
| [`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) | the index of papers and books, each linking to its own reading note |
| [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) | what graduation means, and the five-criterion gate |

Four files inside every `Experiments/Experiment_N/`:

| Document | What it holds | Changes when |
| --- | --- | --- |
| `BLUEPRINT_N.md` | the hypothesis: thesis, rules, success criteria, key risks | **never, once written** |
| `BRAINSTORMING_N.md` | planning — ideas and what to try next | thinking happens, before the work |
| `JOURNAL_N.md` | every iteration, dated, oldest first, append-only | work proceeds |
| `FINDINGS_N.md` | the latest results worth keeping; **feeds `RESULTS.md`** | a result changes |

[`AGENTS.md`](AGENTS.md) explains why those four are separate and who writes each.

## The pipeline

Eight steps. **Steps 1-7 are the Investment Lab — this repository.** Step 8 lives elsewhere: a
strategy leaves the Lab when it joins the KN Fund allocation.

| # | Step | Question | Where |
| --- | --- | --- | --- |
| 1 | Bibliotheca | What do we believe, and on what evidence? | `Bibliotheca/` |
| 2 | Universe | Which securities are investable, point-in-time? | `Universe/` |
| 3 | Data | Curation, refinery, analysis — what can we measure? | `Data/` |
| 4 | Portfolio | How is the book constructed? | `Experiments/Experiment_N/Portfolio/` |
| 5 | Backtest | How would it have performed, net of costs? | `Experiments/Experiment_N/Backtest/` |
| 6 | Attribution | Where do the alpha and the risk come from? | `Experiments/Experiment_N/Attribution/` |
| 7 | Paper trading | Does it hold up on data the rule has never seen? | `Paper_Trading/` |
| 8 | Production | Joins the KN Fund allocation | **outside this repository** |

```
1  Bibliotheca/                ->  BIBLIOGRAPHY.md + one note per source
2  Universe/universe.ipynb     ->  Security_Master.csv, Data_Issues.csv, Charts/
3  Data/curator.py             ->  Data/Curator/Time_Series/    m_* + c_*   (per ticker)
   Data/refinery.py            ->  Data/Refinery/Time_Series/   + r_*       (cross-sectional)
   Data/analyzer.ipynb         ->  Data/Analyzer/               EDA + signal ICs
4  Experiments/panel.py            the one panel loader, shared by every experiment
   Experiments/engine.py           the one path from a book of weights to a number
   Experiments/Experiment_N/   ->  Portfolio/
5                              ->  Backtest/
6                              ->  Attribution/
7  Paper_Trading/Paper_Trading_N/  nothing has graduated yet
```

Each stage owns its outputs and reads only from the stage above it. Nothing downstream recomputes
what an earlier stage produced — that separation is what keeps experiments comparable, because all
of them read an identical panel.

### The six Lab libraries are the stage layout

Each library maps onto one stage. Three are live; three are in development, and those three are
exactly the stages this template hand-rolls today. Where a stage is hand-rolled, its file says so
and names the interface the library will replace.

| Library | Status | Stage here |
| --- | --- | --- |
| Data Curator | live | `Data/curator.py` |
| Data Refinery | in development | `Data/refinery.py` — hand-rolled |
| Data Analyzer | in development | `Data/analyzer.ipynb` — hand-rolled |
| Portfolio Construction | in development | step 4, in the experiment notebook — hand-rolled |
| Backtest Engine | live | `Experiments/engine.py`, step 5 |
| Attribution Analysis | live | `Experiments/engine.py`, step 6 |

| Column family | Built by | Scope |
| --- | --- | --- |
| `m_*` | the data provider, via the Curator | raw market data |
| `c_*` | `Data/Curator/custom_calculations.py` | **per ticker** — one name's own history |
| `r_*` | `Data/Refinery/custom_calculations.py` | **cross-sectional** — names against each other, per date |
| `*_current` | `Data/refinery.py` | joined from the security master — **not point-in-time** |

### Why the Experiments stage has two modules and not just notebooks

Everything specific to a strategy — what it selects, how it sizes, when it trades — is written out in
that experiment's own notebook, where a reader can see it. Only two things are shared, both for the
same reason: **if they differed between experiments, the comparison between experiments would be
meaningless.**

| Module | What it owns | What breaks without it |
| --- | --- | --- |
| `Experiments/panel.py` | reading the refined files, stitching ticker changes into one company by ISIN, pivoting to `dates × companies` | every notebook loading the panel its own way, so the experiments stop measuring the same universe |
| `Experiments/engine.py` | writing the weight file, running the KaxaNuk engine, reading results back, aligning variants onto one window | every notebook re-deriving the engine call, so a difference in cost model or window shows up as strategy skill |

**No strategy column is named in either module.** The columns a rule reads are declared in the
experiment notebook's setup cell. Experiment 1 deliberately does **not** import `panel.py`: it writes
the loading steps inline, because it is the baseline everything else is measured against, and a
baseline that cannot be read top to bottom without chasing an import is a worse baseline.

## One backtest, and only one

**Every performance figure in this repository comes from the KaxaNuk Backtest Engine.** There is
deliberately no second, lighter simulator: a simpler backtest that disagrees with the engine is worse
than no backtest at all, because it lets the reader pick whichever number they prefer. The engine
models integer share counts, per-share commission on the unadjusted price, and a cash reserve.

The reference implementation had a second one for a while, and it was doing the work. When the engine
replaced it, the winning experiment's margin fell by a third — real commission on a high-turnover
book. That is the lesson this rule encodes.

Variants are ranked by running **each one through the engine** over a window shared by all of them
(`engine.align_to_common_start`), never by an approximation.

## Setup

### In a dev container (recommended)

The repository ships a dev container so a teammate needs Docker and nothing else — no local Python,
no `uv`, no matching interpreter version. Open the folder in VS Code or PyCharm and accept the
"reopen in container" prompt, or:

```bash
docker compose -f .devcontainer/docker-compose.yml up --build
```

JupyterLab is served on `http://localhost:8888`. Two interpreters live in the image on purpose: the
base image's Python 3.13 runs the Jupyter *server*, and a `uv`-managed Python 3.14 at `/opt/venv`
runs the *notebooks*, registered as the **KN Research Process (Python 3.14)** kernel — **pick that
kernel**, not the default one. The split exists because this project requires Python ≥3.14 and the
Jupyter base image tops out at 3.13.

The repository is bind-mounted at `/workspace`, so downloaded data and any file you write inside the
container lands on the host and survives a rebuild.

> **The licensed engines are not in the image.** They are deliberately absent from `pyproject.toml`
> so their index URLs and keys never enter version control, which means `uv sync` cannot install
> them. Stages 1-4 run in the container as built; to run the backtest and attribution stages too,
> install them once inside it — the change persists until the image is rebuilt.

### Locally

```bash
uv sync --group notebook
```

### 1. Configure credentials

```bash
cp Config/.env.template Config/.env
```

Then fill in the three keys. **`Config/.env` holds real secrets and is gitignored for that reason**;
`Config/.env.template` is committed and is the only record of what a clone must create.

```
KNDC_API_KEY_FMP=...          # data provider (Financial Modeling Prep)
KNBE_API_KEY_KAXANUK=...      # backtest engine licence
KNAA_API_KEY_KAXANUK=...      # attribution analysis licence
```

Compose injects them into the container automatically. Dev container *settings* — the Jupyter token
and the host port — live in `.devcontainer/.env` instead, copied from
`.devcontainer/.env.template`; those are preferences, not secrets.

### 2. Install the licensed KaxaNuk engines

The backtest engine and attribution analysis are **not on PyPI** and are deliberately kept out of
`pyproject.toml` and `uv.lock`, so the licensed index URLs and keys never enter version control.
Install them separately, substituting your own keys and servers from the welcome emails:

```bash
uv pip install kaxanuk-backtest-engine --extra-index-url https://license:YOUR_KEY@YOUR_SERVER/simple/
```

```bash
uv pip install kaxanuk-attribution_analysis --extra-index-url https://license:YOUR_KEY@YOUR_ATTRIBUTION_SERVER/simple/
```

Every notebook guards these imports and reports-and-skips without them, so the pipeline still runs
and produces its portfolio deliverables — but it produces **no results**, by design.

### 3. Build the data

```bash
uv run python Data/curator.py --report
```

Makes no network calls and tells you exactly what is present and what each missing file breaks.
**Run it first.**

```bash
uv run python Data/curator.py
```

```bash
uv run python Data/refinery.py
```

The curator is resumable and skips files already on disk with the expected header, so an interrupted
run picks up where it stopped and a single bad ticker costs one ticker rather than the whole batch.

### 4. Run the notebooks

In pipeline order: `Universe/universe.ipynb`, `Data/analyzer.ipynb`, then each
`Experiments/Experiment_N/experiment_N.ipynb`.

### 5. Strip outputs before committing

```bash
uv run --group notebook jupyter nbconvert --clear-output --inplace Universe/universe.ipynb Data/analyzer.ipynb Experiments/*/experiment_*.ipynb
```

The committed notebook is the *method*; `FINDINGS_N.md` is the *record*.

## What a fresh clone contains — and what it does not

**Only source is committed:** code, notebooks with outputs stripped, documentation, the folder
skeleton, and one seed file — `Universe/Investable_Universe.csv`, the KaxaNuk point-in-time US-equity
universe the whole pipeline grows from, delisted names retained. It is load-bearing twice over:
`Data/curator.py` downloads from it, and `Data/refinery.py` reads it back as the panel's membership
list, which keeps the cash proxy and the benchmarks out of every cross-sectional rank without naming
them anywhere.

**Nothing under `Data/` is committed.** Every file there is downloaded, derived, or dropped in by
you:

| What | Where | How it gets there |
| --- | --- | --- |
| Per-ticker time series | `Data/Curator/Time_Series/` | `Data/curator.py` downloads it |
| Cash proxy (`BIL`) and tradable benchmarks (`SPY`, `QQQ`) | `Data/Curator/Time_Series/` | same download — the engine needs every ticker it prices in one directory |
| Cross-sectional panel | `Data/Refinery/Time_Series/` | `Data/refinery.py` derives it |
| **KaxaNuk index files** | `Data/Curator/Benchmarks/` | **you supply**: `KN600.csv`, `index_daily_holdings_2017.csv`, `kn600_returns.csv` |
| **Factor models** | `Data/Curator/Factors/` | **you supply**: `f_*.csv` |
| Analyzer charts and the signal IC table | `Data/Analyzer/` | `Data/analyzer.ipynb` rebuilds them |
| Books, performance series, attribution figures | `Experiments/*/Portfolio/`, `Backtest/`, `Attribution/` | each experiment notebook |

The two supplied groups exist because no data provider serves them. **Without them** the pipeline
still runs end to end: the backtest measures against SPY and QQQ instead of all three benchmarks, and
the attribution stage reports what is missing and skips. Nothing crashes.

> **A regenerable file is not a backed-up file.** A `git clean -fdx`, or "discard all changes" in a
> GUI, removes every one of them — `Config/.env` included, and that one cannot be regenerated at all.

## House style

PEP 8 plus a stricter house layer ("Bloom Code") whose one-line summary is *optimise for the reader
who has never seen this file*: no import aliases, no abbreviations, no nested functions ever, one
item per line in any comma-separated construct, and type hints on everything.

The rules are **not committed here.** They are shared across KaxaNuk repositories and installed by
APM, so this repository keeps its whole agent setup out of version control — `apm.yml`,
`apm.lock.yaml`, `apm_modules/` and the `.claude/` tree APM writes are all gitignored. Nothing in the
pipeline depends on them being present.

What *is* committed is the enforcement. `pyproject.toml` configures Ruff to match the standard, and
the whole repository — notebooks included — passes:

```bash
uvx ruff check .
```

Where a rule contradicts the house style it is switched off **at the point of exclusion, with the
reason written down**. Read those comments before adding a rule back.

## Keeping the repository clean

No binaries are committed — no charts, no engine workbooks, no PDFs. All of it is either rebuilt by
the pipeline or licensed to a person rather than to a repository, and keeping it out is what keeps a
clone small and its diffs readable. `.gitignore` enforces this by extension, so an accidental
`git add` of a chart does nothing.

See [`AGENTS.md`](AGENTS.md) for the full process, the restrictions, and the bar any new signal has
to clear.
