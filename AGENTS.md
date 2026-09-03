# Agents — how work is done in this repository

Research repository for a single US-equity idea on the **KaxaNuk** stack, built from the **KN
Research Process** template — the KaxaNuk Investment Lab's process as a folder structure. If you are
looking for how a strategy travels from a belief to a paper-traded book, the answer is the layout
below.

[`README.md`](README.md) explains what the repository *is* and how to run it. **This file explains
how work is done in it** — what belongs in each file, who writes it, when it changes, and the rules
a result has to survive before anyone believes it.

> **Status: template. Nothing has been tested here.** There is no strategy in this repository yet.
> Read [`OBJECTIVE.md`](OBJECTIVE.md) to see what one has to state and [`RESULTS.md`](RESULTS.md)
> to see what it has to report. When a strategy lives here, replace this banner with its status.

## The control documents

Four files at the root carry the whole state of the project. Everything else is code, or a note
feeding one of them.

| Document | Holds | Reader | Changes when |
| --- | --- | --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the main idea, and what this strategy is trying to do | anyone, first | almost never — a change here means a different strategy |
| [`RESULTS.md`](RESULTS.md) | the executive summary of every experiment | CIO, PM, researcher | a `FINDINGS_N.md` changes |
| [`CHANGELOG.md`](CHANGELOG.md) | every version of the repository, newest first | whoever needs to know what moved | any change-set lands |
| `AGENTS.md` | this file — the process and the restrictions | anyone doing work here | the process changes |

**`OBJECTIVE.md` plus `RESULTS.md` are the two files a CIO or PM needs.** One says what we are
trying to do, the other says how far we got and what it cost. If a question about the value of this
project cannot be answered from those two, they are wrong and should be fixed.

### How results flow

```
Experiments/Experiment_N/FINDINGS_N.md   ──┐
                                            ├──>  RESULTS.md  (executive summary)
                        one per idea       ──┘
```

**`RESULTS.md` is compiled from the `FINDINGS_N.md` files and cites each one.** When a number
changes, change it in `FINDINGS_N.md` first and then update the summary. Never the other way round —
a summary that leads its sources is how two numbers for the same book start to circulate.

## The KN Research Process

Eight steps. **Steps 1-7 are the Investment Lab — this repository.** Step 8 lives elsewhere: a
strategy leaves the Lab when it joins the KN Fund allocation.

| # | Step | The question it answers | Where it lives |
| --- | --- | --- | --- |
| 1 | **Bibliotheca** | What do we believe, and on what evidence? | `Bibliotheca/`, `OBJECTIVE.md` |
| 2 | **Universe** | Which securities are investable, point-in-time? | `Universe/` |
| 3 | **Data** | Curation, refinery, analysis — what can we measure? | `Data/` |
| 4 | **Portfolio** | How is the book constructed? | `Experiments/Experiment_N/Portfolio/` |
| 5 | **Backtest** | How would it have performed, net of costs? | `Experiments/Experiment_N/Backtest/` |
| 6 | **Attribution** | Where do the alpha and the risk actually come from? | `Experiments/Experiment_N/Attribution/` |
| 7 | **Paper trading** | Does it hold up on data the rule has never seen? | `Paper_Trading/` |
| 8 | Production | Joins the KN Fund allocation | **outside this repository** |

**Each step reads only from the steps above it**, and each owns its outputs. A notebook that
recomputes a column the refinery already produced has broken the process even if the number comes
out the same — the next experiment will compute it slightly differently and the two stop being
comparable.

A step is finished when its output is reproducible from the step above by re-running one command or
one notebook, never by a manual fix-up nobody wrote down.

### The six Lab libraries are the stage layout

Each KaxaNuk Investment Lab library maps onto exactly one stage of this repository. Three are live;
three are in development, and those three are exactly the stages this template hand-rolls today.
**A hand-rolled stage says so in its docstring and names the interface the library will replace**,
so the swap is a one-file change when it comes.

| Library | Status | Stage | What is here today |
| --- | --- | --- | --- |
| Data Curator | **live** | `Data/curator.py` | the driver, calling the public library |
| Data Refinery | in development | `Data/refinery.py` | a hand-rolled stacker: read Curator files, resolve `r_*` by parameter name, write Refinery files with the same rows |
| Data Analyzer | in development | `Data/analyzer.ipynb` | a hand-rolled ten-section EDA with the IC table as its instrument |
| Portfolio Construction | in development | step 4, in the experiment notebook | hand-rolled weighting in the rule cell; MVO and HRP will arrive as library calls |
| Backtest Engine | **live** | `Experiments/engine.py` | the one path from a weight file to a number |
| Attribution Analysis | **live** | `Experiments/engine.py`, step 6 | Brinson-Fachler and KN5FM constants |

> **Step 6 exists on this stack, and it is the point of it.** Attribution is not a nice-to-have —
> it is the only thing that separates a strategy from a factor exposure wearing a strategy's name.
> On the reference implementation it qualified the headline result rather than confirming it, which
> is exactly what it is for. See *What attribution must report* below.

## Bibliotheca — the evidence base

Step 1. Papers and books that support building an experiment against
[`OBJECTIVE.md`](OBJECTIVE.md), or that argue against one.

```
Bibliotheca/
├── BIBLIOGRAPHY.md                      # the index, grouped by the claim each source bears on
├── Papers/
│   └── Author_Year_Title.md             # one note per paper
└── Books/
    └── Author_Year_Title/
        └── INDEX.md                     # one note per book, with per-chapter sections
```

**One `.md` per source, named `Author_Year_Title`.** A paper is a single file under `Papers/`; a book
gets a folder under `Books/` with an `INDEX.md`, because a book is read a chapter at a time and each
chapter earns its own section.

`BIBLIOGRAPHY.md` is the index only: one line per source, grouped by the claim it bears on.

### What a note looks like

Every note opens with the same four-field front matter, so provenance is always in the same place:

```markdown
# Author(s) (Year) — *Title*

> **Link:** [Where it lives](URL)
>
> **Citation:** journal, volume, pages. When the link was last checked.
>
> **Local copy:** held beside this note / none held.
>
> **Read into this repository:** YYYY-MM-DD, at vX.Y.Z.
```

- **A missing link says what to do about it**, not merely that it is missing: *"not recorded. Add it
  here as `[Title](URL)` the next time this source is opened."* A gap phrased as a task gets closed;
  one phrased as a fact does not. **Never invent a URL** — a wrong link is worse than none.
- **"Read into this repository" is the staleness marker.** A note distilled against last quarter's
  numbers was written against figures that have since moved, and the reader needs to know that
  without checking `git log`.

Then the body:

| Note | Body |
| --- | --- |
| **Paper** | `## What it says`, in the authors' terms — then `## What it implies for this strategy`, as a blockquote |
| **Book** | one `## N. <the claim the book makes>` per chapter idea, each with its chapter reference and a blockquoted implication; then a distillation table and a `## What this book does not settle for us` |

Three rules that make the difference between a note and a summary:

1. **The implication is a blockquote, always.** It is the only part that is *ours*, and it has to be
   visually separable from what the source said.
2. **A book heading states the source's claim, never our verdict.** Our verdict lives in the
   blockquote, where it can change when a result moves; a heading carrying a verdict rots silently.
3. **Record contradictions as contradictions.** When a source says to do the opposite of what the
   strategy does, that stays visible rather than being smoothed into agreement — it is usually the
   most useful line in the note.

**A note that does not say what it changes about this strategy is a summary, and summaries are
available elsewhere.**

**PDFs are gitignored** — they sit beside the notes on disk, and only the notes are committed. That
is right twice over: no binaries in the tree, and no redistribution of licensed material.
**Do not download papers, books or datasets without asking.**

> **Read a source because you have a question, not because it is a good source.** The seven
> research-integrity notes ship with the template because every strategy needs them before it has a
> question of its own; everything else in the folder should arrive because a result raised a
> question. On the reference implementation, the single most useful note was a book read *after*
> attribution reported something nobody could explain — and it supplied the explanation.

## Universe — what is investable

Step 2. `Universe/Investable_Universe.csv` is **the seed**: the KaxaNuk point-in-time US-equity
ticker list, which **retains delisted names**, committed because the whole pipeline grows from it.
`Universe/universe.ipynb` enriches it into `Security_Master.csv` and `Data_Issues.csv`.

**Eligibility is decided here and nowhere else.** The Data stage reads the security master and does
not second-guess it.

## Data — curation, refinery, analysis

Step 3. Three blocks, in order. The first two are plain modules because their output is a file; the
third is a notebook because its output is an argument.

| File | Owns |
| --- | --- |
| `Data/curator.py` | the download driver. Entry point; resumable; the only thing that talks to a provider |
| `Data/Curator/custom_calculations.py` | the `c_*` columns, computed during the pull |
| `Data/refinery.py` | stacking the per-ticker files into the one panel every experiment reads |
| `Data/Refinery/custom_calculations.py` | the `r_*` columns, computed across the cross-section |
| `Data/analyzer.ipynb` | EDA, and the information coefficients features are chosen from |

### Column naming — the convention that makes the panel readable

| Prefix | Built by | Scope |
| --- | --- | --- |
| `m_*` | the data provider, via the Curator | raw market data |
| `c_*` | `Data/Curator/custom_calculations.py` | **per ticker** — one name's own history |
| `r_*` | `Data/Refinery/custom_calculations.py` | **cross-sectional** — names against each other, per date |
| `*_current` | `Data/refinery.py` | joined from the security master — **not point-in-time** |

**The prefix tells you which stage owns a column, and therefore where to change it.** A `c_*` column
that needs to see other tickers is misplaced and belongs in the refinery.

Four `c_*` columns are **engine infrastructure and never removed**: `c_split_ratio`,
`c_dividend_split_ratio`, `c_vwap` (the commission price) and `c_vwap_dividend_and_split_adjusted`
(the fill price). The template ships one worked example beside them — dollar volume, one day and 63
days — and nothing else. Your signal goes here.

### The analyzer is where a feature earns its place

It exists to find data errors and outliers, and to measure whether a feature carries information at
all. **A feature that fails there does not get a book built on it** — and one that passes has earned
a backtest, not a belief. The IC table is a screening tool.

Its highest use is a prediction: when the IC table says a weighting variable has the wrong sign
inside the eligible pool, it is predicting that weighting by it will cost return. Write the
prediction down before the backtest. A prediction made from the data and then confirmed by the
engine is the strongest methodological result an experiment can report.

### Data facts that cost real time

Stack facts, not strategy facts. Every one was learned on the reference implementation.

- **Curator output is not reproducible across download dates.** Dividend adjustment is computed from
  the present, so a re-pull rebases every adjusted column. A Sharpe that moves in the third decimal
  between two runs is that effect, not a strategy change. **This is a known property, not a licence
  to overwrite history.**
- **Three adjustment families are carried and used for different jobs**: unadjusted for commission,
  split-adjusted for liquidity, dividend-and-split for signal and P&L. Using the wrong one produces a
  plausible number and no error.
- **Ticker changes are stitched by ISIN** in `Experiments/panel.py`. Left unstitched, a company that
  changed ticker is two positions.
- **Dual share classes cannot be stitched** — different ISINs, so the company key cannot merge them,
  and the bet on that issuer is doubled whenever both classes are held.
- **The tradable benchmarks live in `Time_Series/` alongside the universe**, because the engine
  resolves every ticker it prices against one directory. They are excluded from the cross-section by
  name in `Data/refinery.py`, which is what stops a benchmark leaking into a rank.
- **Coverage is checked before conclusions.** A column at 60% coverage is not quietly averaged over
  the 60%; the refinery reports per-column coverage on every run, and `curator.py --report` says what
  is present before any network call.

## Experiments — one idea per folder

Steps 4 to 6. Each `Experiments/Experiment_N/` is one idea, self-contained, with four markdown files
and a notebook. The template ships `Experiment_1/`, the benchmark slot.

### The four files

| File | What it holds | Who writes it | When it changes |
| --- | --- | --- | --- |
| `BLUEPRINT_N.md` | **the hypothesis** — thesis, rules, success criteria, key risks | by hand, or with the AI | **never, once written.** A hypothesis edited after its test is not a hypothesis |
| `BRAINSTORMING_N.md` | **planning** — ideas, what to try next, what was considered and dropped | by hand, or with the AI | whenever thinking happens, before the work |
| `JOURNAL_N.md` | **the running log** — every iteration, dated, oldest first | the AI, as work proceeds | append only; earlier entries are never edited except by a new correcting entry |
| `FINDINGS_N.md` | **the latest results worth keeping** | the AI, from the journal | rewritten when a result changes; **feeds `RESULTS.md`** |

The split matters. `BLUEPRINT` is fixed so a result cannot quietly reshape the question it was meant
to answer. `JOURNAL` is append-only so the path is recoverable. `FINDINGS` is rewritten so there is
exactly one current answer. `BRAINSTORMING` looks forward so planning is not mistaken for history.

Repository-level history — choosing the benchmark, the data step, the architecture — belongs in
`JOURNAL_1.md`, Experiment 1 being the declared benchmark and therefore the shared context. Later
experiments' journals point there rather than copying it.

### The folders

- `Portfolio/` — step 4 output: the books this experiment produced, over time. Gitignored.
- `Backtest/` — step 5 output: performance series and engine workbooks. Gitignored.
- `Attribution/` — step 6 output: the factor and Brinson-Fachler decompositions. Gitignored.

### The notebook

`experiment_N.ipynb` holds the strategy itself and follows the same section contract every time:

| Section | Contains |
| --- | --- |
| Position in the pipeline · What this notebook does not do | what the experiment claims, and the standing warnings |
| 0 · Setup | imports, paths, and **the strategy's columns** — the only strategy names outside the rule |
| 1 · The panel | load and stitch — inline in the benchmark, through `panel.py` everywhere else |
| 2 · The rule | selection, sizing, timing. **In the template this is the one cell you write**; it must produce `selected_matrix`, `REBALANCE_DATES` and `target_weights`, and 2.1 asserts the invariants every rule must pass |
| 3 · Construction | the book, and the diagnostics a person would run it on: trigger frequency, turnover, concentration, sector drift |
| 4 · Backtest | one engine pass, guarded import, reports-and-skips without a licence |
| 5 · Attribution | Brinson-Fachler and KN5FM, guarded the same way |
| 6 · Verdict | what it concluded, in words — a notebook that ends in a number and no sentence gets read as whatever the reader hoped |
| Handoff · Open items | what the next stage consumes; what this one left open |

Everything after section 2 is strategy-agnostic given those three objects. That is what makes the
notebook a template rather than an example.

### The two shared modules

Everything specific to a strategy lives in its own notebook. Only two things are shared, each for the
same reason: **if it differed between experiments the comparison would be meaningless.**

| Module | Owns | Breaks without it |
| --- | --- | --- |
| `Experiments/panel.py` | reading the refined files, ISIN stitching, pivoting to `dates × companies` | every notebook loading the panel its own way, so the experiments stop measuring the same universe |
| `Experiments/engine.py` | writing the weight file, running the engine, reading results back, aligning variants onto one window | a difference in cost model or window showing up as strategy skill |

**No strategy column is named in either module.** The columns a rule reads are declared in the
experiment notebook's setup cell and passed to `panel.load_company_panel` through `columns`. A
signal that leaks into shared code becomes every later experiment's default without anyone deciding
it — the reference implementation carried exactly that leak, and the template does not.

The two modules are also where the benchmark and attribution constants live, because this is the
stage that decides what results are *reported against*. `Data/curator.py` decides what gets
*fetched*. Those are the only two files that name a benchmark.

**Experiment 1 deliberately does not import `panel.py`.** It writes the loading steps inline, because
it is the baseline everything else is measured against, and a baseline that cannot be read top to
bottom without chasing an import is a worse baseline.

### One backtest, and only one

**Every performance figure comes from the KaxaNuk Backtest Engine**, reached through `engine.py`.
There is deliberately no second, lighter simulator: one that disagrees lets the reader pick whichever
number they prefer. The reference implementation had one for a while and it was doing the work — when
the engine replaced it, the winning margin fell by a third, because real per-share commission on a
high-turnover book is not a flat 5 basis points.

Variants are ranked by running **each one through the engine** over a window shared by all of them
(`engine.align_to_common_start`), never by an approximation.

## Config — environment variables and credentials

`Config/.env` holds **real credentials**. Three of them:

```
KNDC_API_KEY_FMP=...          # Financial Modeling Prep, read by Data/curator.py
KNBE_API_KEY_KAXANUK=...      # Backtest Engine licence
KNAA_API_KEY_KAXANUK=...      # Attribution Analysis licence
```

> **`Config/.env` is gitignored because it is SECRET**, not merely because it is machine-specific.
> **Never print a value from it**, never put one in a commit, a document, a notebook output or a log
> line, and never paste one into a command that gets recorded. If a key is ever exposed, it is
> rotated — not edited out of a file.

`Config/.env.template` **is committed** and is the only record of what a clone must create. The
`.gitignore` rule names `Config/.env` exactly, so the template is not caught by it; keep it that way.

Loading is done with **python-dotenv**, which is a real dependency here — `dotenv.load_dotenv()`
against `Config/.env`, in `Data/curator.py`, `Universe/universe.ipynb` and each experiment notebook.
**Do not hand-roll a `.env` parser**, and do not duplicate the loading logic into a shared module
that then has to be kept in step with three call sites.

Dev container settings — the Jupyter token and the host port — live in `.devcontainer/.env` instead,
which is a different file for a different reason: those are preferences, not secrets. Compose reads
`Config/.env` through `env_file` so the container gets the keys without them being restated in
`docker-compose.yml`, where an `environment:` entry would outrank the file and shadow it with an
empty value.

## Paper Trading — step 7

The last step inside the Lab, and the only one that runs on data the strategy has never seen.
**Nothing has graduated**, so `Paper_Trading/daily_update.py` and
`Paper_Trading/Paper_Trading_1/paper_trading_1.py` carry their contracts as docstrings and no logic.
Agreeing what the stage may and may not do is worth more than code written before there is a book to
run.

An experiment is **promoted**, not copied — `Paper_Trading/Paper_Trading_N/` mirrors the
`Experiment_N` it came from, so the lineage of a paper-traded book is never in question.

**The five-criterion graduation gate is in
[`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md)**, together with what a paper-trading run
is. Read it before proposing that anything graduate.

> **A paper-trading script that tunes anything is a backtest wearing a costume.** Parameters freeze
> at graduation.

## Restrictions

### One experiment at a time

**When working on `Experiment_N`, do not open another experiment's files** — notebook, findings,
journal or brainstorming — to decide what this one should do. Each experiment stands on its own
hypothesis. Reading another's answers first is how a parameter tuned on one book quietly becomes the
default of the next, and how three experiments become one experiment reported three times.

If you are told to look at another experiment, **limit it to the minimum the request needs.**

Two standing exceptions, and only two:

- **Experiment 1 is the declared benchmark.** Everything is measured against it, so its rules and its
  published numbers are shared context rather than contamination. Note what this is *not*: it is not
  a null. It is a real strategy with a real return, so beating it is a higher bar than beating a
  no-model control — and a variant that loses to it has lost to something a person would actually
  hold. **The benchmark's rules are frozen once `FINDINGS_1.md` reports**; a change to them
  invalidates every comparison in `RESULTS.md`, so improvements go into a new experiment.
- **`RESULTS.md` is the shared record.** Comparing *final* results across experiments is the whole
  point of having several. What is forbidden is borrowing another experiment's *choices* before your
  own are made.

### The bar any new signal must clear

Every clause was earned on the reference implementation, where each has a number behind it.

1. **State the economic reason before running.** A rule needs a stated mechanism in its
   `BLUEPRINT_N.md` *before* it is tested. A result that arrives before a hypothesis is an
   observation, not evidence.
2. **Read sweeps as curves, not cells.** A parameter degrading monotonically across three settings is
   information; a variant beating its control by 0.001 Sharpe is not.
3. **Count the trials and publish the count.** The best of eleven variants at a few hundredths of
   Sharpe over its control is exactly the margin the Deflated Sharpe Ratio is designed to eat. The
   count is what lets a reader discount the winner properly.
4. **Accept results net, or not at all.** On a book turning over 300% a year, the difference between
   a flat cost model and the engine's per-share commission was a third of the winning edge.
5. **Attribute before believing.** A strategy that beats its benchmark has not been understood until
   attribution says which part is factor exposure and which part is selection. This stack can do it,
   so "we could not tell" is not an available answer.
6. **Prefer the feature anyone can explain in a sentence.** Complexity is added one lever at a time,
   and each addition must beat the simpler baseline to earn its place.
7. **Report the rejected result as loudly as the promising one.** A negative result costs real work
   and stops the next person repeating it. It stays in `RESULTS.md` with its numbers intact.

### Other standing rules

- **Do not change a committed result to make it agree with a new run.** If the numbers moved, find
  out why first and record it.
- **Do not quietly drop a bad run.** A run that cannot be believed is excluded **by name**, with its
  reason, in `RESULTS.md`. Graceful degradation that hides a missing benchmark is a bug, not a
  convenience.
- **Do not commit binaries or notebook outputs.** No charts, no engine workbooks, no PDFs.
- **Do not put logic in files that cannot be traced to a stage.** If a reader cannot tell which step
  of the process owns a file, it does not belong here, however correct it is.
- **Do not touch Production.** Step 8 is not in this repository and nothing here deploys.
- **Never use the `§` symbol** in documents here. Write "section" or name the heading.

## Research integrity — the five ways a backtest lies

The part of the process that has nothing to do with Python. Every one of these bit the reference
implementation at least once. The literature behind each is in
[`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) Part 5, and ships with the template.

### 1. Survivorship bias

A universe built from *today's* index members has silently deleted every company that failed. The
backtest then discovers that stocks go up.

**What we do:** `Universe/Investable_Universe.csv` is point-in-time and **retains delisted names**;
`universe.ipynb` quantifies how much of the universe is dead and writes `Universe/Data_Issues.csv`.
Any new universe arrives the same way, with its delisted names attached, before it is used for
anything.

**What we do not do:** audit the *last day* of a delisted name. Shumway says the missing delisting
returns are disproportionately the bad ones. We take whatever the provider supplies. **Open gap.**

### 2. Look-ahead — the point-in-time discipline

A signal computed from information that did not exist yet will always work.

**What we do:** every rule is struck on **shifted** data — the decision on day *t* uses columns
through *t−1* — and the engine trades at the next available price, not at the close of the signal
day. `engine.align_to_common_start` carries forward a book strictly backwards, so giving two variants
the same first day leaks nothing. The template's rule scaffold and its invariants enforce both.

The one deliberate violation is named in its own column suffix: `*_current` columns come from
**today's** security master, so every period before a reclassification is misattributed. That is why
sector attribution is read as indicative, and why the suffix exists at all.

**One real leak of this class remains, and it is stated:** delisting exits use one day of hindsight,
because a position is sold on the last day it still has a fill price and that is knowable only the
day after.

### 3. Overfitting and multiple testing

Try enough rules and one will look brilliant. The Sharpe of the best of *N* trials is not the Sharpe
of a strategy; it is the maximum of *N* draws.

**What we do:** economic reason first, sweeps read as curves, and **the trial count published beside
the winner** in `RESULTS.md`.

**What the template does not do for you:** compute the deflated figure. Publishing the count is the
minimum, not the answer, and no candidate graduates without the deflated Sharpe.

### 4. Costs, capacity, and what the engine does not model

A backtest with no costs describes a market that does not exist.

**What we do:** the engine charges per-share commission on the **unadjusted** price and holds integer
share counts and a cash reserve; turnover is reported in the portfolio diagnostics; results are only
ever accepted **net**.

**What the engine does not model is stated wherever it matters.** For a long/short book that is
borrow cost, short rebate and margin — a headline caveat on the whole experiment rather than a
footnote. Capacity is not modelled anywhere.

### 5. Dirty data presented as a finding

An unadjusted split, a stale price, a ticker reused by a different company — each produces a
plausible number and no error. See *Data facts that cost real time* above.

The instructive case on the reference implementation was not dirty data but a **truncated run**: the
engine stopped valuing one book partway, most of its days came back null, and the summary sheet still
computed cleanly over the stub and read as a plausible result. A 30-name equity book cannot have a
single-digit decade drawdown, which is the only reason it was caught. `engine.py` flags truncated
runs, and a truncated variant is excluded by name in `RESULTS.md`.

## What attribution must report

Recorded here rather than left to an experiment folder, because it qualifies the whole project and
because it is the criterion most stacks cannot evaluate at all.

Step 6 runs both KaxaNuk methodologies against KN600 and reports, in `FINDINGS_N.md`:

- **Brinson-Fachler:** cumulative alpha split into **allocation**, **selection** and **interaction**.
  The question it answers: is the return the sectors the book leans into, or the names it picks inside
  them?
- **KN5FM:** total excess return split into **factor exposure** — beta, size, value, momentum,
  residual volatility, industries — and **idiosyncratic** return. The question it answers: how much
  of this is a factor fund wearing the strategy's name?

**What it settles:** whether there is genuine idiosyncratic alpha. That is graduation criterion 2
evaluated, not deferred.

**What to expect it not to settle:** an *absolute* rule — a name judged against its own history — is
close to invisible to a factor model built on *relative* factors, so a book can beat every benchmark
while the model assigns ~0% to the factor its thesis is named after. That is a finding, not a
failure. The follow-ups are counterfactual books the engine can already price: the same names with
the signal switched off (the exclusion-filter test), positions equalised within each date (sizing
skill), a random draw from the eligible pool at the same sizes (selection skill), and the same names
with entry dates shifted (timing skill).

## Known gaps

Written down so the trust boundary is explicit rather than discovered. These are the template's; a
repository built from it inherits them until it closes them.

- **No unit tests exist.** The two worst bugs on the reference implementation were both silent-wrong
  rather than loud-broken: a truncated engine run that still produced a plausible summary, and a
  benchmark leaking into the cross-section. Both live in pure functions that are trivial to pin —
  `engine.align_to_common_start`, `engine.to_engine_frame`, `engine._truncation_reason`,
  `refinery.read_investable_tickers`. The house test rule assumes a `src/` package layout this
  repository does not use, so **the layout is the first decision to make.**
- **Notebook functions are not type-hinted.** The `.py` modules comply with the house guide; the
  functions defined inside notebooks do not, which is why `ANN` is not in the Ruff selection.
- **Three stages are hand-rolled pending their libraries** — Data Refinery, Data Analyzer, Portfolio
  Construction. Each names the interface it will hand over.
- **The last day of a delisted name is unaudited**, and **capacity is unmodelled**.
- **Nothing is out of sample** until an experiment reaches step 7, and **no experiment has a control
  arm** until one is built differing in exactly one thing.

## Versioning

There is no public API to version. What the team depends on is **the results and the pipeline that
produces them**, so that is what the number tracks.

| Bump | Means | Triggered by |
| --- | --- | --- |
| **MAJOR** | published results are invalidated | changing the universe, window, engine or cost model; changing an existing strategy's definition; removing a stage |
| **MINOR** | new capability; existing results stand | a new experiment, signal, stage, diagnostic or document |
| **PATCH** | no result changes | bug fixes, documentation, hygiene, refactors with byte-identical output |

- **A result that changes is a MAJOR bump even if the diff was one line.** Severity is measured in
  what a reader has to throw away.
- **Re-running the pipeline on refreshed data is not a bump at all.** The strategy did not change.
- **While on `0.x`, a result-invalidating change bumps MINOR** — the standard pre-1.0 convention. The
  first MAJOR bump a repository built from this template ever takes will therefore be `2.0.0`.
- **`1.0.0` is reserved** for the first strategy that reaches paper trading with its results
  reproduced from a clean clone.

`CHANGELOG.md` follows the [KaxaNuk Data Curator convention](https://kaxanuk-data-curator.readthedocs.io/en/latest/release_notes/v0/index.html):
`## X.Y.Z (YYYY-MM-DD)` with `### Added / Changed / Deprecated / Fixed / Removed`.

## Stack

- **Python** `>=3.14`, managed with [uv](https://docs.astral.sh/uv/). `uv.lock` is committed and the
  container installs with `--frozen`, so every clone resolves identical versions.
- **pandas / numpy** for the panel; the KaxaNuk Data Curator uses **PyArrow** underneath.
  **matplotlib** for charts. Nothing is aliased.
- **python-dotenv** for `Config/.env`. A real dependency, used directly at each call site.
- **KaxaNuk libraries** — Data Curator (**public**, on PyPI, declared in `pyproject.toml`); Backtest
  Engine and Attribution Analysis (**licensed**, installed from private indexes, deliberately absent
  from `pyproject.toml` so the index URLs and keys never enter version control). Every notebook guards
  those imports and reports-and-skips without them. Data Refinery, Data Analyzer and Portfolio
  Construction are **in development** and hand-rolled here until they land.
- **Jupyter** for the stages whose output is an argument (Universe, Analyzer, Experiments); plain
  modules for the stages whose output is a file (Curator, Refinery).
- **Ruff** for linting, configured in `pyproject.toml` to match the house rules.
- **Docker / devcontainer**, so a teammate needs Docker and nothing else. The base image's Python
  3.13 serves Jupyter; a uv-managed 3.14 at `/opt/venv` runs the notebooks.
- **Microsoft APM** for the AI scaffolding — gitignored, because it is an organisation-level
  dependency rather than a project one.

## Code style

PEP 8 plus a stricter house layer ("Bloom Code"), installed by APM and shared across KaxaNuk
repositories. One-line summary: *optimise for the reader who has never seen this file.*

- **No import aliases.** Not `pd`, not `np`, not `plt`.
- **No nested functions, ever.**
- **No abbreviations**, and no variable name under three characters.
- **One item per line** in any comma-separated construct holding two or more items.
- **Type hints everywhere**; quoted annotations rather than `from __future__ import annotations`.
- **Assign the error message to `msg` before raising it.**
- Blank lines around `return` / `raise` / `yield`.
- **Docstrings are prose, not NumPy sections**, and never repeat what the type hints already say.
  Say *why*.

The rules are not committed here — they are an organisation-level dependency. What is committed is
the enforcement:

```bash
uvx ruff check .
```

Four checks are deliberately disabled because they contradict the house rules, each commented at the
point of exclusion in `pyproject.toml`. **Read the comment before switching one back on.**

**Strip notebook outputs before committing.** The committed notebook is the *method*;
`FINDINGS_N.md` is the *record*.

```bash
uv run --group notebook jupyter nbconvert --clear-output --inplace Universe/universe.ipynb Data/analyzer.ipynb Experiments/*/experiment_*.ipynb
```

## Dependencies reference

Consult these when you need a dependency's current API rather than recalling it.

- [KaxaNuk Investment Lab](https://www.kaxanuk.mx/lab) — what the platform components are
- [Backtest Engine documentation](https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/)
- [pandas API](https://pandas.pydata.org/docs/reference/index.html)
- [numpy API](https://numpy.org/doc/stable/reference/index.html)
- [matplotlib API](https://matplotlib.org/stable/api/index.html)
- [pyarrow API](https://arrow.apache.org/docs/python/api.html)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
- [uv](https://docs.astral.sh/uv/) · [Ruff rules](https://docs.astral.sh/ruff/rules/)
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs)
