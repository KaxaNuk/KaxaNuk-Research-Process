# Agents — how work is done here

[`README.md`](README.md) says what this repository **is** and where each kind of logic goes. This
file says **how work is done in it**: who writes each document, the restrictions, and the bar a
result has to survive before anyone believes it. It does not repeat the README, so read that first.

> **Status: the template.** No strategy, no data, no result, and no code — every file is a
> description of what is expected in it. Replace this banner with your own status when you take the
> repository over.

## How work reaches `main`

| Branch | What it is | Cut from | Merges into |
| --- | --- | --- | --- |
| `main` | **the template** — the process and the contracts, with no strategy in them | — | — |
| `example` | one strategy worked end to end, for reading rather than building on | `main` | never |
| `issues/<number>` | one per issue on the GitHub Project. Where all work happens | `main` | `main` |

Use `issues/27-B` and `issues/27-C` when one issue needs a second attempt or splits into parallel
lines of work: same issue, same discussion, separate history. **`example` never merges back** —
everything in it that belongs to the *process* is on `main` already, and the rest is a strategy
nobody else should inherit. When the process changes, the example is rebuilt on top of it.

### The issue exists before the branch

An idea goes on the **GitHub Project** first. The issue is where the *why* lives; the branch is only
where the *what* happens. A branch with no issue is work whose reasoning cannot be reviewed, and in
this repository the reasoning is the product.

```
idea  ->  issue on the Project board  ->  issues/<number> cut from main  ->  PR into main
```

1. **Open the issue.** State the question, not the solution.
2. **Cut the branch** — `git switch -c issues/<number> main`.
3. **For an experiment, `BLUEPRINT_N.md` is the first commit on that branch**, before the rule. The
   branch makes it visible in the diff that the hypothesis was written before the answer.
4. **Work**, committing against the issue.
5. **PR into `main`**, once the pipeline has been re-run end to end from a wiped working copy.

### Before any pull request

- `uvx ruff check .` passes, notebooks included.
- **Notebook outputs are stripped.** The committed notebook is the method; `FINDINGS_N.md` is the
  record.
- The `CHANGELOG.md` entry is part of the change-set, not a follow-up. If you cannot write the
  entry, the change-set is not finished.
- **If a published number moved, the PR says which** — and `FINDINGS_N.md` changed before
  `RESULTS.md`, never the other way round.

**`main` is not where you work.** It is where work arrives.

## Who writes each document, and when it changes

| Document | Who writes it | Changes when |
| --- | --- | --- |
| `OBJECTIVE.md` | a person, first | almost never — a change here means a *different* strategy |
| `RESULTS.md` | the AI, from the findings files | a `FINDINGS_N.md` changes |
| `CHANGELOG.md` | whoever lands a change-set | any change-set lands |
| `AGENTS.md` | anyone | the process changes |
| `BLUEPRINT_N.md` | a person, or with the AI | **never, once written.** A hypothesis edited after its test is not a hypothesis |
| `BRAINSTORMING_N.md` | a person, or with the AI | thinking happens — **before** the work |
| `JOURNAL_N.md` | the AI, as work proceeds | append only. Earlier entries are corrected by new entries, never edited |
| `FINDINGS_N.md` | the AI, from the journal | a result changes. It is rewritten, so there is exactly one current answer |

**`RESULTS.md` is compiled from the findings files and cites each one.** When a number changes,
change it in `FINDINGS_N.md` first — a summary that leads its sources is how two numbers for the
same book start to circulate. **One deliberate exception:** findings from step 3 go straight into
`RESULTS.md`, because notebook outputs are stripped before committing and a measurement living only
in a cell output does not survive the commit.

Repository-level history — choosing the benchmark, the data step, the architecture — belongs in
`JOURNAL_1.md`. Experiment 1 is the declared benchmark and therefore the shared context; later
journals point there rather than copying it.

---

# Restrictions

## One experiment at a time

**When working on `Experiment_N`, do not open another experiment's files** to decide what this one
should do. Each experiment stands on its own hypothesis. Reading another's answers first is how a
parameter tuned on one book quietly becomes the default of the next, and how three experiments
become one experiment reported three times.

Two standing exceptions, and only two:

- **Experiment 1 is the declared benchmark**, so its rules and published numbers are shared
  context. It is not a null: it is a real strategy with a real return. **Its rules freeze once
  `FINDINGS_1.md` reports** — a change invalidates every comparison in `RESULTS.md`, so
  improvements go into a new experiment.
- **`RESULTS.md` is the shared record.** Comparing *final* results across experiments is the whole
  point of having several. What is forbidden is borrowing another experiment's *choices* before your
  own are made.

## The bar any new signal must clear

1. **State the economic reason before running.** A result that arrives before a hypothesis is an
   observation, not evidence.
2. **Read sweeps as curves, not cells.** A parameter degrading monotonically across three settings
   is information; a variant beating its control by 0.001 Sharpe is not.
3. **Count the trials and publish the count.** A reader cannot discount a best-of-N result without
   knowing N.
4. **Accept results net, or not at all.** On a high-turnover book, the difference between a flat
   cost model and real per-share commission can be a third of the winning edge.
5. **Attribute before believing.** A strategy that beats its benchmark has not been understood until
   attribution says which part is factor exposure and which part is selection. This stack can do it,
   so "we could not tell" is not an available answer.
6. **Never choose a parameter on the metric it will be judged by.** Choose it on a property of the
   *signal* — persistence, coverage, turnover — and publish the sweep.
7. **Prefer the feature anyone can explain in a sentence.** Complexity is added one lever at a time,
   and each addition must beat the simpler baseline to earn its place.
8. **Report the rejected result as loudly as the promising one.** A negative result costs real work
   and stops the next person repeating it.

## Other standing rules

- **Every performance figure comes from the KaxaNuk Backtest Engine.** There is deliberately no
  second, lighter simulator: one that disagrees just lets the reader pick the number they prefer.
- **Do not change a committed result to make it agree with a new run.** If the numbers moved, find
  out why first, and record it.
- **Do not quietly drop a bad run.** A run that cannot be believed is excluded **by name**, with its
  reason, in `RESULTS.md`.
- **Do not commit binaries or notebook outputs.** No charts, no engine workbooks, no PDFs.
- **Do not put logic in a file that cannot be traced to a stage.** If a reader cannot tell which
  step owns a file, it does not belong here, however correct it is.
- **Do not touch Production.** Step 8 is not in this repository and nothing here deploys.
- **Never print a value from `Config/.env`** — not into a commit, a notebook output, a log line, or
  a command that gets recorded. An exposed key is rotated, not edited out.
- **Never use the section symbol** in documents here. Write "section" or name the heading.
- **Mark example content as you add it.** `# --- example: begin ---` in Python,
  an HTML comment of the same words in Markdown, and `# EXAMPLE-ONLY CELL` on a whole notebook cell.
  Nothing consumes these; they exist so a person starting their own strategy can see what to delete.

---

# Research integrity — the five ways a backtest lies

The part of the process that has nothing to do with Python.

| # | The lie | What the process does | What it still does not do |
| --- | --- | --- | --- |
| 1 | **Survivorship bias.** A universe built from *today's* members has deleted everything that failed, and the backtest discovers that markets go up | the seed is point-in-time and **retains delisted names**; step 2 quantifies how much of the universe is dead | audit the *last day* of a delisted name. The missing delisting returns are disproportionately the bad ones |
| 2 | **Look-ahead.** A signal computed from information that did not exist yet always works | every rule is struck on **shifted** data and fills at the next available price; a fitted signal is used in its causal form, and the smoothed form only where it is labelled as not tradable | remove the one stated leak: a delisting exit needs one day of hindsight, because a position is sold on the last day it still has a fill price |
| 3 | **Overfitting.** Try enough rules and one looks brilliant. The Sharpe of the best of *N* trials is the maximum of *N* draws | economic reason first, sweeps read as curves, parameters never chosen on the metric they are judged by, **the trial count published beside the winner** | compute the deflated figure. Publishing the count is the minimum, not the answer |
| 4 | **Costs and capacity.** A backtest with no costs describes a market that does not exist | commission on the **unadjusted** price, integer share counts, a cash reserve, turnover reported, results accepted **net** | model capacity, anywhere. Borrow cost, short rebate and margin are a headline caveat on any long/short book, not a footnote |
| 5 | **Dirty data presented as a finding.** An unadjusted split, a stale price, a reused identifier — each produces a plausible number and no error | coverage checked before conclusions; a truncated engine run is flagged and the variant excluded **by name** | catch what nobody thought to check. The instructive case was a run that stopped valuing a book partway and still summarised cleanly over the stub |

**The one deliberate look-ahead is named in its own column prefix.** A `current_*` column comes from
today's security master, so any period before a reclassification is misattributed. That is why the
prefix exists, and why anything bucketed on it is read as indicative.

**If your signal is fitted, measure what look-ahead costs.** Read the same model causally and
smoothed and report the gap. It is the cheapest audit in the process and routinely the largest
number in it: the two series agree on most days and differ exactly at the turning points, which is
where the money is.

## What attribution must report

Step 6 runs both methodologies and reports, in `FINDINGS_N.md`:

- **Brinson-Fachler:** cumulative alpha split into **allocation**, **selection** and
  **interaction**. *Is the return the groups the book leans into, or the things it picks inside
  them?*
- **A factor model:** total excess return split into **factor exposure** and **idiosyncratic**
  return. *How much of this is a factor fund wearing the strategy's name?*

**What it settles:** whether there is genuine idiosyncratic alpha — graduation criterion 2
evaluated, not deferred.

**What to expect it not to settle:** an *absolute* rule is close to invisible to a factor model
built on *relative* factors, so a book can beat every benchmark while the model assigns roughly
nothing to
the factor its thesis is named after. That is a finding, not a failure. The follow-ups are
counterfactual books the engine can already price: the same holdings with the signal switched off,
positions equalised within each date, a random draw from the eligible pool at the same sizes, and
the same holdings with entry dates shifted. Those four separate the exclusion filter, sizing skill,
selection skill and timing skill.

---

# Code style

PEP 8 plus a stricter house layer, shared across KaxaNuk repositories and installed by APM rather
than committed here. One-line summary: *optimise for the reader who has never seen this file.*

- **No import aliases**, and **no abbreviations** — no variable name under three characters.
- **No nested functions, ever.**
- **One item per line** in any comma-separated construct holding two or more items.
- **Type hints everywhere**; quoted annotations rather than a `__future__` import.
- **Assign the error message to `msg` before raising it**, and leave blank lines around
  `return` / `raise` / `yield`.
- **Docstrings are prose, not sections**, and never repeat what the type hints already say. Say
  *why*.

What is committed is the style check, and the whole repository passes it. Nothing checks the process
itself; the rules above rest on review.

```bash
uvx ruff check .
```
