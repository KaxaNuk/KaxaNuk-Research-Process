# Agents — how work is done here

[`README.md`](README.md) says what this repository **is**, how to run it, and where each kind of
logic goes. **This file says how work is done in it**: who writes each document and when it changes,
the restrictions, and the bar a result has to survive before anyone believes it. It does not repeat
the README, so read that first.

> **Status: the template.** No strategy, no data, no result — the process with nothing in it yet.
> [`OBJECTIVE.md`](OBJECTIVE.md) says what a strategy has to state and [`RESULTS.md`](RESULTS.md) what it
> has to report; both are empty by design. Replace this banner with your own status when you take
> the repository over.

## How work reaches `main`

Two long-lived branches with different jobs, plus one short-lived kind.

| Branch | What it is | Cut from | Merges into |
| --- | --- | --- | --- |
| `main` | **the template** — the process, the pipeline and the contracts, with no strategy in them. Always runnable, always lints, notebook outputs always stripped | — | — |
| `example` | one strategy worked end to end, for reading rather than building on: what a filled-in repository is supposed to look like | `main` | never |
| `issues/<number>` | one per GitHub issue. Where all work happens | `main` | `main` |

`issues/27-B` and `issues/27-C` when one issue needs a second attempt, or splits into parallel lines
of work: same issue, same discussion, separate history.

**`example` never merges back.** It is a demonstration, not a feature branch: everything in it that
belongs to the *process* is on `main` already, and everything else is a strategy nobody else should
inherit. When the process changes on `main`, the example is rebuilt on top of it — never merged
into it.

**Nothing else lives in the branch list.** A long-lived branch that is not one of these two is a fork
nobody remembers to update.

### The issue exists before the branch

An idea goes on the **GitHub Project** first. The issue is where the *why* lives; the branch is only
where the *what* happens. A branch with no issue is work whose reasoning cannot be reviewed, and in
this repository the reasoning is the product.

```
idea  ->  issue on the Project board  ->  issues/<number> cut from main  ->  PR into main
```

1. **Open the issue.** State the question, not the solution.
2. **Cut the branch** — `git switch -c issues/<number> main`.
3. **For an experiment, `BLUEPRINT_N.md` is the first commit on that branch**, before the rule cell.
   That is the same rule as always; the branch just makes it visible in the diff, so a reviewer can
   see the hypothesis was written before the answer.
4. **Work**, committing against the issue.
5. **PR into `main`**, once the pipeline has been re-run end to end from a wiped working copy.

### Before any pull request

- `uvx ruff check .` passes, notebooks included.
- **Notebook outputs are stripped.** The committed notebook is the method; `FINDINGS_N.md` is the
  record.
- The `CHANGELOG.md` entry is part of the change-set, not a follow-up. If you cannot write the entry,
  the change-set is not finished.
- **If a published number moved, the PR says which** — and `FINDINGS_N.md` changed before
  `RESULTS.md`, never the other way round.

**`main` is not where you work.** It is where work arrives.

## Who writes each document, and when it changes

| Document | Who writes it | Changes when |
| --- | --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | a person, first | almost never — a change here means a *different* strategy |
| [`RESULTS.md`](RESULTS.md) | the AI, from the findings files | a `FINDINGS_N.md` changes |
| [`CHANGELOG.md`](CHANGELOG.md) | whoever lands a change-set | any change-set lands. It also defines what a version number means here |
| `AGENTS.md` | anyone | the process changes |
| `BLUEPRINT_N.md` | a person, or with the AI | **never, once written.** A hypothesis edited after its test is not a hypothesis |
| `BRAINSTORMING_N.md` | a person, or with the AI | thinking happens — **before** the work |
| `JOURNAL_N.md` | the AI, as work proceeds | append only. Earlier entries are corrected by new entries, never edited |
| `FINDINGS_N.md` | the AI, from the journal | a result changes. It is rewritten, so there is exactly one current answer |

The split between the four experiment files is the whole point. `BLUEPRINT` is frozen so a result
cannot quietly reshape the question it was meant to answer. `JOURNAL` is append-only so the path is
recoverable. `FINDINGS` is rewritten so there is one current answer. `BRAINSTORMING` looks forward so
planning is never mistaken for history.

```
Experiments/Experiment_N/FINDINGS_N.md   ──┐
                        one per idea       ├──>  RESULTS.md   (executive summary)
                                          ──┘
```

**`RESULTS.md` is compiled from the findings files and cites each one.** When a number changes,
change it in `FINDINGS_N.md` first. Never the other way round — a summary that leads its sources is
how two numbers for the same book start to circulate.

**One exception, and it is deliberate:** findings from step 3 go straight into `RESULTS.md`, under
*Before any experiment*. Notebook outputs are stripped before committing, so a step-3 measurement
that lives only in a cell output does not survive the commit.

Repository-level history — choosing the benchmark, the data step, the architecture — belongs in
`JOURNAL_1.md`. Experiment 1 is the declared benchmark and therefore the shared context; later
journals point there rather than copying it.

## What a source note looks like

Every note in `Bibliotheca/` opens with the same four fields, so provenance is always in the same
place:

```markdown
# Author(s) (Year) — *Title*

> **Link:** [Where it lives](URL)
>
> **Citation:** journal, volume, pages. When the link was last checked.
>
> **Local copy:** held beside this note / none held.
>
> **Read into this repository:** YYYY-MM-DD, at vX.Y.Z. What was read — the whole paper, or an abstract.
```

| Note | Body |
| --- | --- |
| **Paper** | `## What it says`, in the authors' terms — then `## What it implies for this strategy`, as a blockquote |
| **Book** | one `## N. <the claim the chapter makes>` per idea, each with a blockquoted implication; then a distillation table and `## What this book does not settle for us` |

Four rules that separate a note from a summary:

1. **The implication is a blockquote, always.** It is the only part that is *ours*, and it has to be
   visually separable from what the source said.
2. **A heading states the source's claim, never our verdict.** Our verdict lives in the blockquote,
   where it can change when a result moves; a heading carrying a verdict rots silently.
3. **Record contradictions as contradictions.** When a source says to do the opposite of what we do,
   that stays visible rather than being smoothed into agreement. It is usually the most useful line
   in the note.
4. **Never invent a URL or a page number.** A missing link is recorded as a task — *"not recorded;
   add it as `[Title](URL)` the next time this source is opened"* — because a gap phrased as a task
   gets closed and one phrased as a fact does not. A wrong citation is worse than none.

**A note that does not say what it changes about this strategy is a summary, and summaries are
available elsewhere.** A source listed in `BIBLIOGRAPHY.md` without a note is a *lead*: nothing may
be claimed on its authority until it has been read.

## The experiment notebook's section contract

`experiment_N.ipynb` is the same shape every time, so any experiment can be read by someone who has
read one:

| Section | Contains |
| --- | --- |
| Position in the pipeline · What this notebook does not do | what it claims, and the standing warnings |
| 0 · Setup | imports, paths, and **the strategy's columns** — the only strategy names outside the rule |
| 1 · The panel | load and stitch — inline in the benchmark, through `securities_panel.py` everywhere else |
| 2 · The rule | selection, sizing, timing. **The one cell you write.** It must produce `selected_matrix`, `REBALANCE_DATES` and `target_weights`; 2.1 asserts the invariants every rule must pass |
| 3 · Construction | the book, plus the diagnostics a person would run it on: trigger frequency, turnover, concentration, drift |
| 4 · Backtest | one engine pass, guarded import, reports-and-skips without a licence |
| 5 · Attribution | Brinson-Fachler and the factor model, guarded the same way |
| 6 · Verdict | what it concluded, **in words**. A notebook that ends in a number and no sentence gets read as whatever the reader hoped |
| Handoff · Open items | what the next stage consumes; what this one left open |

Everything after section 2 is strategy-agnostic given those three objects. That is what makes the
notebook a template rather than an example.

**Experiment 1 deliberately does not import `securities_panel.py`.** It writes the loading steps inline, because
it is the baseline everything else is measured against, and a baseline that cannot be read top to
bottom without chasing an import is a worse baseline.

---

# Restrictions

## One experiment at a time

**When working on `Experiment_N`, do not open another experiment's files** — notebook, findings,
journal or brainstorming — to decide what this one should do. Each experiment stands on its own
hypothesis. Reading another's answers first is how a parameter tuned on one book quietly becomes the
default of the next, and how three experiments become one experiment reported three times. If you are
told to look at another experiment, **limit it to the minimum the request needs.**

Two standing exceptions, and only two:

- **Experiment 1 is the declared benchmark.** Its rules and published numbers are shared context.
  Note what it is *not*: not a null. It is a real strategy with a real return, so beating it is a
  higher bar than beating a no-model control. **Its rules freeze once `FINDINGS_1.md` reports** — a
  change invalidates every comparison in `RESULTS.md`, so improvements go into a new experiment.
- **`RESULTS.md` is the shared record.** Comparing *final* results across experiments is the whole
  point of having several. What is forbidden is borrowing another experiment's *choices* before your
  own are made.

## The bar any new signal must clear

1. **State the economic reason before running.** A rule needs a stated mechanism in its
   `BLUEPRINT_N.md` *before* it is tested. A result that arrives before a hypothesis is an
   observation, not evidence.
2. **Read sweeps as curves, not cells.** A parameter degrading monotonically across three settings is
   information; a variant beating its control by 0.001 Sharpe is not.
3. **Count the trials and publish the count.** The best of eleven variants at a few hundredths of
   Sharpe over its control is exactly the margin the Deflated Sharpe Ratio is designed to eat.
4. **Accept results net, or not at all.** On a book turning over 300% a year, the difference between
   a flat cost model and the engine's per-share commission was a third of the winning edge.
5. **Attribute before believing.** A strategy that beats its benchmark has not been understood until
   attribution says which part is factor exposure and which part is selection. This stack can do it,
   so "we could not tell" is not an available answer.
6. **Never choose a parameter on the metric it will be judged by.** Choose it on a property of the
   *signal* — persistence, coverage, turnover — and publish the sweep. Choosing on Sharpe is common
   in the literature and it is still selection on the outcome.
7. **Prefer the feature anyone can explain in a sentence.** Complexity is added one lever at a time,
   and each addition must beat the simpler baseline to earn its place.
8. **Report the rejected result as loudly as the promising one.** A negative result costs real work
   and stops the next person repeating it. It stays in `RESULTS.md` with its numbers intact.

## Other standing rules

- **Every performance figure comes from the KaxaNuk Backtest Engine**, through `backtest_engine.py`. There is
  deliberately no second, lighter simulator: one that disagrees just lets the reader pick the number
  they prefer.
- **Do not change a committed result to make it agree with a new run.** If the numbers moved, find
  out why first, and record it.
- **Do not quietly drop a bad run.** A run that cannot be believed is excluded **by name**, with its
  reason, in `RESULTS.md`. Graceful degradation that hides a missing benchmark is a bug, not a
  convenience.
- **Do not commit binaries or notebook outputs.** No charts, no engine workbooks, no PDFs.
- **Do not put logic in a file that cannot be traced to a stage.** If a reader cannot tell which step
  owns a file, it does not belong here, however correct it is.
- **Do not touch Production.** Step 8 is not in this repository and nothing here deploys.
- **Never print a value from `Config/.env`** — not into a commit, a notebook output, a log line, or a
  command that gets recorded. An exposed key is rotated, not edited out.
- **Never use the `§` symbol** in documents here. Write "section" or name the heading.
- **Mark example content as you add it.** `# --- example: begin ---` in Python,
  `<!-- example: begin -->` in Markdown, and `# EXAMPLE-ONLY CELL` on a whole notebook cell.
  Nothing consumes these; they exist so a person starting their own strategy can see what to
  delete without running anything and without a diff. An unmarked example is a line somebody
  will later mistake for process.

---

# Research integrity — the five ways a backtest lies

The part of the process that has nothing to do with Python. The literature behind each is in
[`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) Part 5.

### 1. Survivorship bias

A universe built from *today's* members has silently deleted everything that failed. The backtest
then discovers that markets go up.

**What we do:** the seed is point-in-time and **retains delisted names**; `universe.ipynb` quantifies
how much of the universe is dead and writes `Data_Issues.csv`. Any new universe arrives the same way,
with its delisted names attached, before it is used for anything.

**What we do not do:** audit the *last day* of a delisted name. Shumway says the missing delisting
returns are disproportionately the bad ones. **Open gap.**

### 2. Look-ahead

A signal computed from information that did not exist yet will always work.

**What we do:** every rule is struck on **shifted** data, and the engine trades at the next available
price rather than at the close of the signal day. `backtest_engine.align_to_common_start` carries a book
strictly backwards, so giving two variants the same first day leaks nothing. Any *fitted* signal is
returned in its causal form, and the smoothed form is available only where it is explicitly labelled
as not tradable.

**If your signal is fitted, measure what that costs.** Read the same model causally and smoothed and
report the gap. It is the cheapest audit in the process and routinely the largest number in it: the
two series agree on most days and differ exactly at the turning points, which is where the money is.

**The one deliberate violation is named in its own column suffix:** `*_current` columns come from
today's security master, so any period before a reclassification is misattributed. That is why the
suffix exists, and why anything bucketed on it is read as indicative.

**One real leak of this class remains, and it is stated:** delisting exits use one day of hindsight,
because a position is sold on the last day it still has a fill price and that is knowable only the
day after.

### 3. Overfitting and multiple testing

Try enough rules and one will look brilliant. The Sharpe of the best of *N* trials is not the Sharpe
of a strategy; it is the maximum of *N* draws.

**What we do:** economic reason first, sweeps read as curves, parameters never chosen on the metric
they are judged by, and **the trial count published beside the winner**.

**What the template does not do for you:** compute the deflated figure. Publishing the count is the
minimum, not the answer, and no candidate graduates without the deflated Sharpe.

### 4. Costs, capacity, and what the engine does not model

A backtest with no costs describes a market that does not exist.

**What we do:** the engine charges per-share commission on the **unadjusted** price and holds integer
share counts and a cash reserve; turnover is reported in the portfolio diagnostics; results are only
ever accepted **net**.

**What it does not model is stated wherever it matters.** For a long/short book that is borrow cost,
short rebate and margin — a headline caveat on the whole experiment, not a footnote. For an ETF book
it is premium and discount to net asset value. **Capacity is not modelled anywhere.**

### 5. Dirty data presented as a finding

An unadjusted split, a stale price, a ticker reused by a different company — each produces a plausible
number and no error.

The instructive case on the reference implementation was not dirty data but a **truncated run**: the
engine stopped valuing one book partway, most of its days came back null, and the summary sheet still
computed cleanly over the stub and read as a plausible result. A 30-name equity book cannot have a
single-digit decade drawdown, which is the only reason it was caught. `backtest_engine.py` flags truncated
runs, and a truncated variant is excluded **by name** in `RESULTS.md`.

## Data facts that cost real time

Stack facts, not strategy facts. Each was learned the expensive way.

- **Curator output is not reproducible across download dates.** Dividend adjustment is computed from
  the present, so a re-pull rebases every adjusted column. A Sharpe that moves in the third decimal
  between runs is that effect, not a strategy change. **A known property, not a licence to overwrite
  history.**
- **Three adjustment families are carried and each does a different job**: unadjusted for commission,
  split-adjusted for liquidity, dividend-and-split for signal and P&L. Using the wrong one produces a
  plausible number and no error.
- **Prices arrive as fixed-point decimals, not floats.** Anything statistical has to cast at the
  boundary; comparing a decimal column against a float literal raises, which is the good case.
- **Ticker changes are stitched by ISIN** in `Experiments/securities_panel.py`. Left unstitched, a security that
  changed ticker is two positions.
- **Dual share classes cannot be stitched** — different ISINs, so the company key cannot merge them,
  and the bet on that issuer is doubled whenever both are held.
- **The cash proxy and the benchmarks live in `Time_Series/` alongside the universe**, because the
  engine resolves every ticker it prices against one directory. They stay out of the cross-section
  because the Refinery takes membership from `Investable_Universe.csv` — an allowlist, so there is no
  second list to forget to update.
- **Coverage is checked before conclusions.** A column at 60% coverage is not quietly averaged over
  the 60%; the refinery reports per-column coverage on every run, and `curator.py --report` says what
  is present before any network call.
- **`rank(pct=True)` over *n* values averages to `(n+1)/2n`, not to 0.5.** On twelve securities
  that is 0.542; on eight hundred it is 0.5006. A causality check written against 0.5 therefore fails
  on every date of a narrow universe and passes on a wide one, which is the worst possible failure
  mode. Check against the identity, not against a half.

## What attribution must report

Recorded here because it qualifies the whole project, and because it is the criterion most stacks
cannot evaluate at all.

Step 6 runs both KaxaNuk methodologies and reports, in `FINDINGS_N.md`:

- **Brinson-Fachler:** cumulative alpha split into **allocation**, **selection** and **interaction**.
  *Is the return the groups the book leans into, or the things it picks inside them?* On a
  multi-asset book that is nearly the whole question.
- **A factor model:** total excess return split into **factor exposure** and **idiosyncratic**
  return. *How much of this is a factor fund wearing the strategy's name?*

**What it settles:** whether there is genuine idiosyncratic alpha. That is graduation criterion 2
evaluated, not deferred.

**What to expect it not to settle:** an *absolute* rule — a security judged against its own history —
is close to invisible to a factor model built on *relative* factors, so a book can beat every
benchmark while the model assigns ~0% to the factor its thesis is named after. That is a finding, not
a failure. The follow-ups are counterfactual books the engine can already price: the same holdings
with the signal switched off, positions equalised within each date, a random draw from the eligible
pool at the same sizes, and the same holdings with entry dates shifted. Those four separate the
exclusion filter, sizing skill, selection skill and timing skill.

---

# Known gaps

Written down so the trust boundary is explicit rather than discovered. A repository built from this
one inherits them until it closes them.

- **No unit tests exist.** The two worst bugs on the reference implementation were both silent-wrong
  rather than loud-broken. The functions worth pinning first are pure and trivial to test:
  `jump_model._smoothed_labels`, `jump_model._advance_values`, `backtest_engine.align_to_common_start`,
  `backtest_engine.to_engine_frame`, `refinery.read_investable_tickers`. The house test rule assumes a `src/`
  package layout this repository does not use, so **the layout is the first decision to make.**
- **Notebook functions are not type-hinted.** The `.py` modules comply; functions defined inside
  notebooks do not, which is why `ANN` is not in the Ruff selection.
- **Three stages are hand-rolled pending their libraries.** Each says so in its docstring and names
  the interface the library will replace.
- **The last day of a delisted name is unaudited**, and **capacity is unmodelled**.
- **Attribution has never been run here.** The benchmark holdings and factor files are supplied by
  hand and no provider sells them; nothing in the pipeline stages them for you.
- **Nothing is out of sample** until an experiment reaches step 7, and **no experiment has a control
  arm** until one is built differing in exactly one thing.

## Where the six Lab libraries land

Each KaxaNuk Investment Lab library maps onto exactly one stage. Three are live; three are in
development, and those three are exactly the stages this repository hand-rolls today. **A hand-rolled
stage says so in its docstring and names the interface the library will replace**, so the swap is a
one-file change when it comes.

| Library | Status | Stage here |
| --- | --- | --- |
| Data Curator | **live** | `Data/curator.py` — the driver, calling the public library |
| Data Refinery | in development | `Data/refinery.py` — a hand-rolled stacker |
| Data Analyzer | in development | `Data/analyzer.ipynb` — a hand-rolled EDA with the IC table as its instrument |
| Portfolio Construction | in development | `Experiments/portfolio_construction.py` -- `equal_weight` and `inverse_volatility` behind one signature; MVO and HRP arrive as another function of the same shape |
| Backtest Engine | **live** | `Experiments/backtest_engine.py`, step 5 |
| Attribution Analysis | **live** | `Experiments/attribution_analysis.py`, step 6 |

The **licensed** engines — Backtest Engine and Attribution Analysis — are deliberately absent from
`pyproject.toml`, so their index URLs and keys never enter version control. Install them by hand:

```bash
uv pip install kaxanuk-backtest-engine --extra-index-url https://license:YOUR_KEY@YOUR_SERVER/simple/
```

Every notebook guards those imports and reports-and-skips without them, so the pipeline still runs
and produces its portfolio deliverables — but it produces **no results**, by design.

# Code style

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

The rules are an organisation-level dependency and are not committed here. `uvx ruff check .` is,
and the whole repository — notebooks included — passes it.

# Dependencies reference

Consult these when you need a dependency's current API rather than recalling it.

- [KaxaNuk Investment Lab](https://www.kaxanuk.mx/lab) — what the platform components are
- [Backtest Engine documentation](https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/)
- [pandas API](https://pandas.pydata.org/docs/reference/index.html) ·
  [numpy API](https://numpy.org/doc/stable/reference/index.html) ·
  [matplotlib API](https://matplotlib.org/stable/api/index.html) ·
  [pyarrow API](https://arrow.apache.org/docs/python/api.html)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/) · [uv](https://docs.astral.sh/uv/) ·
  [Ruff rules](https://docs.astral.sh/ruff/rules/)
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs)
