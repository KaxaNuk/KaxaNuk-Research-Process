# KN Research Process

**A template to speed up the investment research process.** KaxaNuk's eight steps as a
folder structure, with the conventions that let two people share a tool without
explaining it first.

**There is no code on `main`.** Every file here is a short description of what is expected in it —
what that stage produces, what it prevents, and where its logic belongs. Clone it, fill it in with
your own idea, and you have a repository whose shape is already agreed.

The universe is one CSV whose only required column is `main_identifier`, and every stage reads it
without knowing what is in it: **equities, ETFs, FX, crypto, commodities or futures all run the
same process.**

> **Want to see it filled in?** One strategy worked end to end — the pipeline, the notebooks, the
> measurements and a falsified prediction left in place — is on the `example` branch KaxaNuk keeps
> beside `main`. The public template ships `main` only. It is there to be read, not built on.

**Where this lives.** `main` is public at
[`KaxaNuk/KaxaNuk-Research-Process`](https://github.com/KaxaNuk/KaxaNuk-Research-Process). Get it
with *Use this template* on GitHub and follow **Setup** below: four commands, every one of them run
in the repository root, because that root is the only folder the whole thing lives in. Claude can do
the same from the `start-a-strategy` prompt in
[`KaxaNuk/KaxaNuk-APM`](https://github.com/KaxaNuk/KaxaNuk-APM), which copies the template and
installs the skills into that same root — that prompt is still being written. Issues and pull
requests are welcome: the process improves in public, the way the Data Curator did.

---

## Eight steps, one repo

Each stage owns its outputs and reads only from the stage above it. **Steps 1 to 7 are the Lab, and
this repository.** Step 8 is the one that leaves it.

| # | Step | In plain words | It produces | It prevents | Where |
| --- | --- | --- | --- | --- | --- |
| 1 | **Bibliotheca** | a literature review with a thesis at the end of it | a referenced hypothesis, in the repo, dated | backtesting a hunch you cannot defend afterwards | `Bibliotheca/` |
| 2 | **Universe** | the eligible list, rebuilt for each date rather than for today | a point-in-time membership table | survivorship bias — testing on the winners that survived | `Universe/` |
| 3 | **Data** | curation, then refinery, then analysis — in that order | a reproducible dataset, and the evidence a feature carries signal | beautiful results that came from broken inputs | `Data/` |
| 4 | **Portfolio** | how much of what, and how often you change your mind | a weighting scheme with position and turnover limits | a good signal in a portfolio nobody could hold | `Experiments/Experiment_N/` |
| 5 | **Backtest** | the simulation, run by the Backtest Engine | a performance curve and a cost-aware track record | paper returns that real trading would have erased | `Experiments/Experiment_N/Backtest/` |
| 6 | **Attribution** | which part of the return did you actually earn? | a factor and idiosyncratic breakdown of performance | selling factor beta as if it were alpha | `Experiments/Experiment_N/Attribution/` |
| 7 | **Paper trading** | a dress rehearsal on data nobody has seen yet | out-of-sample evidence and an operations checklist | finding the plumbing problems on day one of funding | `Paper_Trading/` |
| 8 | Production | real capital, real monitoring, a real drawdown policy | a funded, monitored strategy with an owner | research that stays research forever | **elsewhere** |

**A stage that recomputes something an earlier stage produced has broken the process**, even when
the number matches — because the next experiment will compute it slightly differently and the two
stop being comparable.

---

## What is in here

```
OBJECTIVE.md          the idea, and the status of each claim inside it
RESULTS.md            every number this repository has measured
AGENTS.md             how work is done here: the workflow, and the bar a result must clear
CHANGELOG.md          every version, and what a version number means here

Bibliotheca/          step 1 - one note per source, and BIBLIOGRAPHY.md as the index
Universe/             step 2 - Investable_Universe.csv (the seed) and universe.ipynb
Data/                 step 3 - curator.py, refinery.py, analyzer.ipynb, and the two
                               custom_calculations.py where your columns go
Experiments/          steps 4-6 - one folder per idea (four documents and a notebook), and the
                               four modules every experiment shares
Paper_Trading/        step 7 - the graduation gate, and the frozen rule of anything that passes
Config/               .env.template - copy to .env and fill in your keys
```

**Nothing under `Data/` or inside an experiment's output folders is committed.** Every file there is
downloaded, derived, or dropped in by hand. A regenerable file is not a backed-up file: discarding
all changes removes every one of them — `Config/.env` included, and that one cannot be regenerated.

---

## The six Lab modules

One module per stage, each reading the previous module's output, so you can enter the pipeline
wherever your work already is.

| Module | # | What it does |
| --- | --- | --- |
| **Data Curator** | 1 | pulls raw market and fundamental data from any provider and aligns it on one calendar |
| **Data Refinery** | 2 | cleans, adjusts and reshapes the curated data into analysis-ready series |
| **Data Analyzer** | 3 | builds features and tests whether they carry signal, before you model anything |
| **Portfolio Construction** | 4 | turns a signal into weights, position limits and a rebalancing rule |
| **Backtest Engine** | 5 | runs the rules over history with costs and no look-ahead, and returns the track record |
| **Attribution Analysis** | 6 | splits the return into known factor exposure and the part that is actually yours |

**Two doors.** The platform drives the same pipeline from a workspace instead of a terminal — build
a universe, download data, construct a portfolio, run a backtest and attribution, each step tracked
to completion. The other door is `pip install`: the open-source libraries are public on
[PyPI](https://pypi.org/project/kaxanuk.data-curator/) and
[GitHub](https://github.com/KaxaNuk), no account and no platform login required.

The **licensed** engines — Backtest Engine and Attribution Analysis — are deliberately absent from
`pyproject.toml`, so their index URLs and keys never enter version control. Install them by hand,
and **guard their imports**: every notebook that uses one should report what is missing and skip, so
the pipeline still runs and produces its portfolio deliverables. It produces no results, by design.

---

## The conventions worth keeping

Everybody will have their own ideas, and that is the point of a template rather than a framework.
But when we want to share a tool, some names have to mean the same thing in both repositories.

### Where each kind of logic goes

**The prefix tells you which stage owns a column, and therefore which file to open.**

| Prefix | Built by | Scope | Change it when |
| --- | --- | --- | --- |
| `m_*` | the provider, via the Curator | raw market data | never — it is what arrived |
| `c_*` | `Data/Curator/custom_calculations.py` | **one security's own history** | you need a new per-security quantity |
| `r_*` | `Data/Refinery/custom_calculations.py` | **securities against each other, per date** | you need a rank, a breadth reading, or a fitted model |
| `current_*` | `Data/refinery.py`, joined from the security master | **today's classification — not point-in-time** | you group or report by something new. Never select on it |

Two rules follow, and one exception worth knowing:

- **A `c_*` column that needs to see other securities is misplaced** and belongs in the Refinery.
- **Widening the Curator's schema forces a refetch of every identifier.** That is deliberate — it
  is what stops a folder holding a mix of schemas — but it means the Curator is the wrong home for
  anything you intend to tune.
- **So a fitted column lives in the Refinery even when it is per-security.** Its settings are
  exactly what an experiment sweeps, and **a sweep must never cost a download.** Its *inputs* —
  arithmetic with nothing to tune — stay in the Curator.

### The names

| Name | What it is |
| --- | --- |
| `Universe/Investable_Universe.csv` | the seed. One row per security; **`main_identifier` is the only required column**, and every other column is yours |
| `Universe/Security_Master.csv` | the seed plus what the provider knows, written by step 2 |
| `Universe/Data_Issues.csv` | what is wrong with the downloaded files, written by step 2 |
| `Data/Curator/Time_Series/` | one file per identifier: `m_*` and `c_*` |
| `Data/Refinery/Time_Series/` | the same rows plus `r_*` and `current_*` — **the panel every experiment reads** |
| `Experiments/Experiment_N/` | one folder per idea: `BLUEPRINT_N.md`, `BRAINSTORMING_N.md`, `JOURNAL_N.md`, `FINDINGS_N.md`, and the notebook |
| `Portfolio/portfolio_weights.csv` | the book, in the shape the Backtest Engine reads |

### The four shared modules

Everything specific to a strategy lives in its notebook, where a reader can see it. Four modules are
shared between experiments — one per Lab library — for one reason: **if they differed between
experiments, comparing experiments would be meaningless.** Each ships beside the notebook as a
description of what it must do; `example` has them filled in.

| Module | Owns |
| --- | --- |
| `securities_panel.py` | reading the refined files, stitching renamed securities into one position, pivoting to `dates x securities` |
| `portfolio_construction.py` | turning an eligible set into weights — the seam the Portfolio Construction library replaces |
| `backtest_engine.py` | writing the weight file, running the engine, reading results back, aligning variants onto one window |
| `attribution_analysis.py` | shaping the hand-supplied index and factor files into what the attribution library reads, and saying what is missing before it tries |

**A strategy column is named in exactly two kinds of place: a notebook's setup cell, and the rule.**
Never in a shared module, so a signal cannot become every later experiment's default without anyone
deciding it.

---

## The tools

Install once, use for every strategy.

| Tool | Job |
| --- | --- |
| **GitHub Desktop** | where your work lives, and how you get it back after you break it |
| **PyCharm** | the editor, the interpreter and the terminal in one window |
| **Claude** | your pair for the parts you have not written before |
| **APM packages** | how Claude learns the six Lab modules and this process — what each does, how it is called, and what it must never be asked to do |

APM is the Agent Package Manager. `uv sync` installs the CLI, because it is in the `dev` group, and
`apm install` fetches KaxaNuk's packages from
[`KaxaNuk/KaxaNuk-APM`](https://github.com/KaxaNuk/KaxaNuk-APM) — the process, the Data Curator's
calculations, and one skill per Lab module as they are written. **They install into the repository
root, beside the process folders**, which is what Setup below does and the order it does it in.
Nothing here needs them to be read; a filled-in repository is faster with them.

### A researcher beside the process

[`KaxaNuk/KaxaNuk-Researcher`](https://github.com/KaxaNuk/KaxaNuk-Researcher) is a companion you
name and teach — one per person, not per strategy. It keeps its own library of what you have
read, reads this repository's `Bibliotheca/`, and drafts the claims in `OBJECTIVE.md` and the
hypothesis in each `BLUEPRINT_N.md` from those notes, every prediction citing the note it came
from. It is a separate project, and it is being built.

---

## Setup

**One folder is the whole project.** The repository root holds the process folders *and* the local
setup — `.venv/`, `.claude/`, `apm_modules/`, `apm.yml`. Nothing is installed a level above it and
nothing is nested a level below it, so opening that one folder in PyCharm or Claude gives you the
research tree and the agent tooling at the same time, already pointing at each other.

Python 3.14, [uv](https://docs.astral.sh/uv/) and GitHub Desktop, then five steps in this order.

1. **Make the repository, named after the strategy.** *Use this template* on
   [`KaxaNuk/KaxaNuk-Research-Process`](https://github.com/KaxaNuk/KaxaNuk-Research-Process) and
   call it what the strategy is — `fcf-yield-quality`. **Do not create a folder to put it in:** the
   repository name *is* the folder name.
2. **Clone it.** GitHub Desktop, into wherever you keep work. Cloning into `D:\Research` gives you
   `D:\Research\fcf-yield-quality`, and **that folder is the root** every step below runs in.
3. **Build the environment**, from the root. `uv sync` creates `.venv/` and installs the `dev`
   group, which is where `apm-cli` comes from — so this step has to come before step 4.
4. **Install the agent tooling**, from the root. `apm init` writes `apm.yml`; `apm install` fetches
   KaxaNuk's packages into `apm_modules/` and deploys their skills, commands and rules into
   `.claude/`. All four are already in `.gitignore` — the setup is yours, not the repository's.
5. **Copy the credential file** and fill in a data-provider key.

```bash
uv sync
```

```bash
apm init -y --target claude
```

```bash
apm install KaxaNuk/KaxaNuk-APM/common
```

```bash
cp Config/.env.template Config/.env
```

The two KaxaNuk entries in `.env` are engine licences: steps 1 to 4 run without them, and steps 5
and 6 should report what is missing and skip. **Never print a value from that file** — not into a
commit, a notebook output or a log line. An exposed key is rotated, not edited out.

### What the root looks like when it is right

```
fcf-yield-quality/          <- clone here, open here, run everything here
    .claude/                installed by APM      \
    apm_modules/            installed by APM       |  ignored: your local setup
    apm.yml                 written by apm init    |
    .venv/                  written by uv sync    /
    Bibliotheca/            \
    Universe/                |  the process, from the template
    Data/                    |
    Experiments/             |
    Paper_Trading/           |
    Config/                 /
    OBJECTIVE.md  RESULTS.md  AGENTS.md  CHANGELOG.md  README.md
```

**The failure to avoid is a wrapper folder.** Making an empty folder, running the APM setup in it
and cloning the template inside it gives you two of everything: the wrapper has no
`pyproject.toml`, so APM writes a `requirements-dev.txt` and a second `apm.yml` and `.claude/`
there, and Claude opened at the wrapper reads that empty one and never sees the research tree. If
you already have that layout, delete the wrapper's `apm.yml`, `apm.lock.yaml`, `apm_modules/`,
`.claude/`, `.gitignore` and `requirements-dev.txt`, and open the repository folder itself.

---

## Starting your own strategy

**Setup is done, and you are already inside the thing you are filling in** — one folder, the
process and the tooling in it. In order:

1. **Put your securities in `Universe/Investable_Universe.csv`.** One row each; `main_identifier`
   is the only required column. Add whatever else your strategy groups by.
2. **Write `OBJECTIVE.md`** — the idea, and the claims inside it, *before* anything is measured.
3. **Write your `c_*` and `r_*` columns** into the two `custom_calculations.py`, and fill in the
   Curator and Refinery drivers that call the libraries.
4. **Run steps 2 and 3**, in this order: curator, then `universe.ipynb`, then refinery, then
   `analyzer.ipynb`. The universe notebook sits *between* the two Data commands, because it
   profiles what the curator downloaded and writes the master the refinery joins.
5. **Write `BLUEPRINT_1.md` before the rule.** A hypothesis edited after its test is not a
   hypothesis.

**To see it filled in**: the `example` branch, where KaxaNuk keeps it beside `main`.

---

## The documents

**Two files answer "is this worth anything?"** — [`OBJECTIVE.md`](OBJECTIVE.md) says what we are
trying to do, [`RESULTS.md`](RESULTS.md) says how far we got and what it cost.

| Document | What it holds |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the main idea, and the status of each claim inside it |
| [`RESULTS.md`](RESULTS.md) | the executive summary of every experiment, compiled from the `FINDINGS_N.md` files |
| [`CHANGELOG.md`](CHANGELOG.md) | every version, newest first, and what a version number means here |
| [`AGENTS.md`](AGENTS.md) | **how work is done** — the workflow, the restrictions, and the bar a result has to clear |
| [`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) | the index of sources, each linking to its note |
| [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) | what graduation means, and the gate |

Four documents inside every `Experiments/Experiment_N/`, and the split between them is the whole
point: `BLUEPRINT` is frozen so a result cannot quietly reshape the question it was meant to answer,
`JOURNAL` is append-only so the path is recoverable, `FINDINGS` is rewritten so there is one current
answer, and `BRAINSTORMING` looks forward so planning is never mistaken for history.

---

## Branches

| Branch | What it is |
| --- | --- |
| `main` | this — the process, with nothing in it. Public at `KaxaNuk/KaxaNuk-Research-Process` |
| `example` | one strategy worked end to end, for reading rather than building on. Kept by KaxaNuk beside `main`, not in the public template |
| `issues/<number>` | one per issue on the GitHub Project, cut from `main` and merged back into it. Where all work happens |

**[`AGENTS.md`](AGENTS.md) is next**: the workflow, the bar any new signal has to clear, and the
five ways a backtest lies.
