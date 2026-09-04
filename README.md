# KN Research Process

**The KaxaNuk Investment Lab's research process as a folder structure**, with the pipeline that makes
it run and no strategy in it yet. Clone it, put your universe in one CSV, name your signal in two
places, and the whole thing works end to end.

It is not an equity template. The universe is a CSV whose only required columns are `ticker` and
`name`, and every stage below reads it without knowing what is in it — **stocks, ETFs, FX, crypto,
commodities or futures all run the same pipeline.**

> **Want to see it filled in?** The `example` branch carries one strategy worked end to end — twelve
> asset-class ETFs and a regime model — with its objective, its measurements and a falsified
> prediction left in place. It is there to be read, not built on. `git switch example`.

---

## Run it

You need Docker, or Python 3.14 and [uv](https://docs.astral.sh/uv/). Then one credential: a
[Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs) key.

```bash
cp Config/.env.template Config/.env
```

Put your key in `KNDC_API_KEY_FMP`. The other two entries are KaxaNuk engine licences — steps 1 to 4
run without them, steps 5 and 6 report what is missing and skip.

```bash
uv sync --group notebook
```

One more line registers the notebook kernel, so the notebooks run the same Python locally as they do
in the container:

```bash
uv run python -m ipykernel install --user --name kn-research-process --display-name "KN Research Process (Python 3.14)"
```

### The whole run, in order

**Six steps. Do them in this order.** The whole thing is about three minutes of compute.

| # | Run | What it writes | Takes |
| --- | --- | --- | --- |
| **1** | `uv run python Data/curator.py --report` | nothing — tells you what is missing and what each gap breaks | instant |
| **2** | `uv run python Data/curator.py` | `Data/Curator/Time_Series/` — one price file per security | ~12 s |
| **3** | notebook `Universe/universe.ipynb` | `Universe/Security_Master.csv`, `Data_Issues.csv`, `Charts/` | ~20 s |
| **4** | `uv run python Data/refinery.py` | `Data/Refinery/Time_Series/` — the panel, with your `r_*` columns on it | ~20 s |
| **5** | notebook `Data/analyzer.ipynb` | `Data/Analyzer/` — the charts and the information-coefficient table | ~2 min |
| **6** | notebook `Experiments/Experiment_1/experiment_1.ipynb` | `Experiments/Experiment_1/Portfolio/` — the book | ~30 s |

Open the notebooks with:

```bash
uv run --group notebook jupyter lab
```

**Every file in the pipeline states its own place in this order, in its first paragraph** — so
wherever you land, you can tell what has to have run before it and what comes next.

> **The order is a dependency, not a preference.** Step 3 profiles files step 2 downloaded, and it
> writes the security master step 4 joins onto the panel — which is why it sits between two Data
> commands rather than before them. Run the refinery too early and it will not fail: it names the
> columns it is dropping and carries on, which is the right behaviour and the wrong outcome.
>
> **Steps 5 and 6 report and skip without the licensed engines.** You still get the full analysis
> and a real book; you do not get performance numbers. That is by design, not a broken clone.

<details>
<summary>In a dev container instead</summary>

`docker compose -f .devcontainer/docker-compose.yml up --build` serves JupyterLab on
`http://localhost:8888`. Two interpreters live in the image on purpose: the base image's Python 3.13
runs the Jupyter *server*, and a uv-managed Python 3.14 at `/opt/venv` runs the *notebooks*,
registered as the **KN Research Process (Python 3.14)** kernel — **pick that kernel.** The repository
is bind-mounted at `/workspace`, so anything you download survives a rebuild. Compose reads
`Config/.env`, so credentials reach the container without being restated anywhere.
</details>

---

## The eight steps

Steps 1 to 7 are the Lab, and this repository. Step 8 is outside it: a strategy leaves the Lab when
it joins the KN Fund allocation.

| # | Step | The question | Where | What you edit |
| --- | --- | --- | --- | --- |
| 1 | **Bibliotheca** | What do we believe, and on what evidence? | `Bibliotheca/` | one note per source |
| 2 | **Universe** | What is investable? | `Universe/` | `Investable_Universe.csv` |
| 3 | **Data** | What can we measure? | `Data/` | the two `custom_calculations.py` |
| 4 | **Portfolio** | How is the book built? | `Experiments/Experiment_N/` | the rule cell |
| 5 | **Backtest** | How would it have done, net? | `Experiments/Experiment_N/Backtest/` | nothing — one engine |
| 6 | **Attribution** | Where does the return come from? | `Experiments/Experiment_N/Attribution/` | nothing |
| 7 | **Paper trading** | Does it hold up unseen? | `Paper_Trading/` | nothing until it graduates |
| 8 | Production | Joins the KN Fund allocation | **elsewhere** | — |

**Each step reads only from the steps above it, and owns its outputs.** A notebook that recomputes
something an earlier stage produced has broken the process even when the number matches, because the
next experiment will compute it slightly differently and the two stop being comparable.

```
1  Bibliotheca/               ->  BIBLIOGRAPHY.md + one note per source
2  Universe/universe.ipynb    ->  Security_Master.csv, Data_Issues.csv, Charts/
3  Data/curator.py            ->  Data/Curator/Time_Series/    m_* + c_*   per security
   Data/refinery.py           ->  Data/Refinery/Time_Series/   + r_*       cross-sectional
   Data/analyzer.ipynb        ->  Data/Analyzer/               charts + the IC table
4  Experiments/securities_panel.py  the one panel loader, shared by every experiment
   Experiments/portfolio_construction.py   eligible set -> weights, one swappable signature
   Experiments/Experiment_N/   ->  Portfolio/
5  Experiments/backtest_engine.py  the one path from a book of weights to a number
                               ->  Backtest/
6  Experiments/attribution_analysis.py   where the return came from
                               ->  Attribution/
7  Paper_Trading/                  nothing has graduated yet
```

---

## The walkthrough

Run it in this order the first time. The order is a **recommendation**, not a constraint — but the
file names and column prefixes are a **convention**, and keeping them is what lets two people share
a tool without explaining it first.

### Step 1 · Bibliotheca — read before you build

[`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) is the index; every source gets its own
note. A note is not a summary — **it ends by saying what it changes about your strategy**, in a
blockquote, and that blockquote is the only part that is yours.

Ships with nine notes: the two books whose method the process runs, and the seven papers behind
its integrity controls. Everything else arrives because a result raised a question — and a source
listed without a note is a **lead**, not a citation.

### Step 2 · Universe — decide what is investable

Open [`Universe/Investable_Universe.csv`](Universe/Investable_Universe.csv). It ships with a header
row and nothing else. **Two columns are required — `ticker` and `name` — and the rest are yours.**
It carries `asset_class` and `asset_group` as a suggestion, because most strategies want to group
their securities somehow; a crypto seed would carry something else, and nothing downstream would
notice.

Then run `Universe/universe.ipynb` — **after the curator has downloaded, because it profiles those
files, and before the refinery, because it writes the `Security_Master.csv` the refinery joins.** It
fills in what the provider knows, writes `Data_Issues.csv`, and answers the question everybody
forgets to ask: **when does each asset actually become usable?** A file that starts in 2010 gives no
signal in 2010 if the feature needs five years of history first. That date, not the first row of the
price file, is the honest start of a backtest.

### Step 3 · Data — curate, refine, analyse

Three blocks. The first two are plain modules because their output is a file; the third is a notebook
because its output is an argument.

**`Data/curator.py`** downloads one file per ticker and computes the `c_*` columns while it goes.
Resumable, and it skips anything already on disk with the right header. `--report` makes no network
call at all and tells you what is present — run that first.

**`Data/refinery.py`** stacks those files into one panel and computes the `r_*` columns across it.
No network, so this is the command you re-run while you iterate.

**`Data/analyzer.ipynb`** is where a feature earns a backtest or is dropped. Its information
coefficient table is the instrument: the per-date correlation between each candidate feature and
forward returns, inside the pool your strategy actually selects from. **A feature that fails
there does not get a book built on it.**

### Step 4 to 6 · Experiments

One folder per idea, four markdown files and a notebook. **Write `BLUEPRINT_N.md` before the rule** —
a hypothesis edited after its test is not a hypothesis. Then one cell of `experiment_N.ipynb` is the
strategy, and everything after it runs unchanged.


Steps 5 and 6 need the licensed engines. Without them the notebook still builds and writes the book,
then reports what is missing and skips — so a clone with no licence gets everything except the
numbers.

### Step 7 · Paper trading

The only stage that runs on data the rule has never seen.
[`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) holds the five-criterion graduation gate.
Read it before proposing that anything graduate.

---

## Where your logic goes

The single most useful table here. **The prefix tells you which stage owns a column, and therefore
which file to open.**

| Prefix | Built by | Scope | Change it when |
| --- | --- | --- | --- |
| `m_*` | the provider, via the Curator | raw market data | never — it is what arrived |
| `c_*` | `Data/Curator/custom_calculations.py` | **one security's own history** | you need a new per-security quantity |
| `r_*` | `Data/Refinery/custom_calculations.py` | **securities against each other, per date** | you need a rank, a breadth reading, or a fitted model |
| `*_current` | `Data/refinery.py` | joined from the security master — **not point-in-time** | you classify securities by something new |

Two rules that follow, and one exception worth knowing:

- **A `c_*` column that needs to see other securities is misplaced** and belongs in the Refinery.
- **Widening the Curator's schema forces a refetch of every identifier.** That is deliberate — it is
  what stops the directory holding a mix of schemas — but it means the Curator is the wrong home for
  anything you intend to tune.
- **So a fitted column lives in the Refinery even when it is per-security.** A model fitted on one
  security's own history would be `c_*` by the naming rule alone. It belongs in the Refinery because
  its hyperparameters are exactly what an experiment sweeps, and **a sweep must never cost a
  download.** Its *inputs* — arithmetic with nothing to tune — stay in the Curator.

Four `c_*` columns are **engine infrastructure and never removed**: `c_split_ratio`,
`c_dividend_split_ratio`, `c_vwap` (the commission price) and `c_vwap_dividend_and_split_adjusted`
(the fill price).

### Only four things are shared between experiments

Everything specific to a strategy lives in its own notebook, where a reader can see it. Four
modules are shared, all for the same reason: **if they differed between experiments, comparing
experiments would be meaningless.** One per stage, and one per KaxaNuk library.

| Module | Owns | Breaks without it |
| --- | --- | --- |
| `Experiments/securities_panel.py` | reading the refined files, stitching ticker changes by ISIN, pivoting to `dates × securities` | every notebook loads the panel its own way, so experiments stop measuring the same universe |
| `Experiments/portfolio_construction.py` | turning an eligible set into weights — and the constraints every scheme respects | every notebook invents its own sizing, so a weighting difference is indistinguishable from a signal difference |
| `Experiments/backtest_engine.py` | writing the weight file, running the engine, reading results back, aligning variants onto one window | a difference in cost model or window shows up as strategy skill |
| `Experiments/attribution_analysis.py` | shaping the hand-supplied index data into the tables the attribution library auto-detects, and saying what is missing before it tries | a mis-shaped table makes the loader read the attribution transposed rather than fail |

**No strategy column is named in any of them.** The columns a rule reads are declared in the
experiment notebook's setup cell.

`portfolio_construction.py` is the seam the KaxaNuk **Portfolio Construction** library will replace.
Everything it offers is reached through one function signature — given the securities eligible today
and a returns history that has already been cut off before today, return weights summing to at most
one. `equal_weight` and `inverse_volatility` ship; a minimum-variance optimiser, hierarchical risk
parity, or a call into the library are the same shape. **Swapping one for another is one line in the
rule cell**, which is what makes two experiments comparable rather than merely adjacent.

### One backtest, and only one

**Every performance figure comes from the KaxaNuk Backtest Engine**, reached through `backtest_engine.py`.
There is deliberately no second, lighter simulator: one that disagrees just lets the reader pick the
number they prefer. On the reference implementation, replacing a flat-cost approximation with the
engine cut the winning margin by a third — real per-share commission on a high-turnover book.

---

## The documents

**Two files answer "is this worth anything?"** — [`OBJECTIVE.md`](OBJECTIVE.md) says what we are
trying to do, [`RESULTS.md`](RESULTS.md) says how far we got and what it cost.

| Document | What it holds |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the main idea, and the status of each claim inside it |
| [`RESULTS.md`](RESULTS.md) | the executive summary of every experiment, compiled from the `FINDINGS_N.md` files |
| [`CHANGELOG.md`](CHANGELOG.md) | every version, newest first, and what a version number means here |
| [`AGENTS.md`](AGENTS.md) | **how work is done** — the restrictions, and the bar a result has to clear |
| [`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) | the index of sources, each linking to its note |
| [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) | what graduation means, and the gate |

Four files inside every `Experiments/Experiment_N/`:

| Document | What it holds | Changes when |
| --- | --- | --- |
| `BLUEPRINT_N.md` | the hypothesis: thesis, rules, success criteria, key risks | **never, once written** |
| `BRAINSTORMING_N.md` | planning — ideas, and what was considered and dropped | thinking happens, before the work |
| `JOURNAL_N.md` | every iteration, dated, oldest first, append-only | work proceeds |
| `FINDINGS_N.md` | the latest results worth keeping; **feeds `RESULTS.md`** | a result changes |

---

## Starting your own strategy

**You are already in it.** `main` is the template: nothing here is a strategy, and the four
documents that hold one — `OBJECTIVE.md`, `RESULTS.md`, and the per-experiment files — ship as
contracts with the answers left out. In order:

1. **Put your securities in `Universe/Investable_Universe.csv`.** One row each; `ticker` and
   `name` are the only required columns.
2. **Write `OBJECTIVE.md`** — the idea, and the claims inside it, *before* anything is measured.
3. **Add your `c_*` and `r_*` columns** to the two `custom_calculations.py`, and list them in
   `CUSTOM_COLUMNS` / `REFINERY_COLUMNS`.
4. **Name your eligibility column** in `ELIGIBILITY_COLUMN` (`Data/analyzer.ipynb`) and
   `SIGNAL_COLUMN` (`Experiments/Experiment_1/experiment_1.ipynb`). Those two are the only
   strategy names outside the rule cell, and the notebook refuses to run until the second is set.
5. **Write `BLUEPRINT_1.md` before the rule.** A hypothesis edited after its test is not a
   hypothesis.

The benchmark rule in section 2 of the experiment notebook already works: hold everything the
signal calls eligible, equally weighted, cash for the rest. **It runs as soon as step 4 is done**,
which is deliberate — a benchmark you have to write before you can measure anything is a
benchmark that never gets written.

**To see it filled in**, `git switch example`.

## What a clone contains, and what it does not

**Only source is committed:** code, notebooks with outputs stripped, documentation, the folder
skeleton, and `Universe/Investable_Universe.csv` — the seed the whole pipeline grows from, and the
one file you change to make this repository about something else.

**Nothing under `Data/` is committed.** Every file there is downloaded, derived, or dropped in:

| What | Where | How it gets there |
| --- | --- | --- |
| Per-security time series | `Data/Curator/Time_Series/` | `Data/curator.py` downloads it |
| Cash proxy (`BIL`) and benchmarks (`AOR`, `SPY`) | `Data/Curator/Time_Series/` | same download — the engine prices every ticker from one directory |
| Cross-sectional panel | `Data/Refinery/Time_Series/` | `Data/refinery.py` derives it |
| Benchmark holdings and factor models | `Data/Curator/Benchmarks/`, `Factors/` | **you supply** — no price provider sells them |
| Charts and the IC table | `Data/Analyzer/` | `Data/analyzer.ipynb` rebuilds them |
| Books, performance series, attribution | `Experiments/*/Portfolio/`, `Backtest/`, `Attribution/` | each experiment notebook |

Without the two supplied groups the pipeline still runs end to end; attribution reports what is
missing and skips.

> **A regenerable file is not a backed-up file.** `git clean -fdx`, or "discard all changes" in a
> GUI, removes every one of them — `Config/.env` included, and that one cannot be regenerated.

**`Config/.env` is gitignored because it is secret**, not merely because it is machine-specific.
Never print a value from it, never put one in a commit, a notebook output or a log line. A key that
is exposed gets rotated, not edited out of a file.

---

## House style, and keeping it clean

PEP 8 plus a stricter house layer, whose one-line summary is *optimise for the reader who has never
seen this file*: no import aliases, no abbreviations, no nested functions, one item per line in any
comma-separated construct, type hints on everything. The rules live in an organisation-level APM
package and are not committed here. What is committed is the enforcement:

```bash
uvx ruff check .
```

Four checks are disabled because they contradict the house style, each commented at the point of
exclusion in `pyproject.toml`. **Read the comment before switching one back on.**

No binaries are committed — no charts, no workbooks, no PDFs — and notebook outputs are stripped
before committing. The committed notebook is the *method*; `FINDINGS_N.md` is the *record*.

```bash
uv run --group notebook jupyter nbconvert --clear-output --inplace Universe/universe.ipynb Data/analyzer.ipynb Experiments/*/experiment_*.ipynb
```

## How work reaches `main`

Two long-lived branches with different jobs, and one short-lived kind:

| Branch | What it is |
| --- | --- |
| `main` | this — the template: the process, the pipeline and the contracts, with no strategy in them |
| `example` | one strategy worked end to end, for reading rather than building on |
| `issues/<number>` | one per issue on the GitHub Project, cut from `main` and merged back into it. Where all work happens |

`example` never merges back: everything in it that belongs to the *process* is on `main` already,
and the rest is a strategy nobody else should inherit. **The issue exists before the branch**: it
is where the *why* lives, and in this repository the reasoning is the product.

[`AGENTS.md`](AGENTS.md) has the loop, and what a pull request has to satisfy before it lands.

**[`AGENTS.md`](AGENTS.md) is next**: the restrictions, the bar any new signal has to clear, and the
five ways a backtest lies.
