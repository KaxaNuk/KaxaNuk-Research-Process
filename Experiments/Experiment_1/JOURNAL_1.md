# Journal — Experiment 1

> **Append-only, dated, oldest first.** Every iteration of this experiment, in the order it
> happened. Maintained by the AI as work proceeds.
>
> **Earlier entries are never edited.** The one exception is correcting an error, and the correction
> is written as a new entry saying what was wrong — not by rewriting the original.
>
> The hypothesis is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md); what to try next is in
> [`BRAINSTORMING_1.md`](BRAINSTORMING_1.md); the results that survive are in
> [`FINDINGS_1.md`](FINDINGS_1.md).

**Paths and figures inside entries are as they were written.** Where a path has since moved the
entry is left alone — it was correct on its date.

**Repository-level history belongs here** — choosing the benchmark, the data step, the architecture.
Experiment 1 is the declared benchmark and therefore the shared context; later experiments' journals
point here rather than copying it.

**Entry format:**

```
## YYYY-MM-DD — short topic

- Idea / question:
- What we tried / considered:
- Outcome / decision:
- Open threads:
```

---

The first entry is usually *repository instantiated from the template*: what this repository is for,
which template version it was created from, the strategy name, and everything `OBJECTIVE.md` still
leaves open.

<!-- example: begin -->

## 2026-09-10 — repository instantiated from the template

- **Idea / question:** the template describes what belongs in each file but shows none of it filled
  in, so the shape has to be imagined rather than read. Give it one worked strategy, simple enough
  that every part of it can be followed.
- **What we tried / considered:** the strategy is `liquid-momentum` — the most heavily traded stocks
  with a positive twelve-month return, equally weighted. Chosen because it has exactly three moving
  parts, one per claim in `OBJECTIVE.md`, and because the literature under it genuinely disagrees
  with itself, which is what makes step 1 worth doing rather than a formality.
- **Outcome / decision:** built on the `example` branch of `KaxaNuk/KaxaNuk-Research-Process` at
  template 0.7.0, alongside the descriptions rather than replacing them. Everything specific to the
  worked example sits between `<!-- example: begin -->` and `<!-- example: end -->` markers so a
  person starting their own strategy can see exactly what to delete.
- **Open threads:** everything past step 1. No universe, no data, no rule, no number.

## 2026-09-10 — step 1: the objective, and the six notes under it

- **Idea / question:** in what order do the objective and the literature actually get written? The
  process says `Bibliotheca/` produces "a referenced hypothesis", and `OBJECTIVE.md` says write it
  before anything is measured — but neither says which of the two comes first.
- **What we tried / considered:** writing the objective first and citing afterwards produces
  references chosen to support a sentence already written. Writing the whole literature review first
  has no stopping condition. **What worked was five passes**, and this is the part worth turning into
  a command:
    1. **Draft the idea in one sentence**, and split it into the three claims the file asks for —
       signal, sizing, construction. No citations yet; the draft exists to raise questions.
    2. **Turn each claim into the question that would settle it.** *Does momentum exist and over
       what window? What does screening to liquid names do to it? What does the bad period look
       like?* One question per claim, and the questions are what get read for — not "momentum",
       which has no stopping condition.
    3. **Find sources per question, and deliberately look for the ones that disagree.** Two of the
       six argue against the strategy. A Part 1 where every source agrees is one assembled to
       support a conclusion rather than to reach one.
    4. **Verify every citation before writing the note.** Journal, volume, issue, pages and a real
       link, checked against the publisher's record. `BIBLIOGRAPHY.md` forbids inventing a URL or a
       page number, and recalled citations are how invented ones get in.
    5. **Come back and rewrite the objective from the notes**, so each claim's evidence section
       points at a note that existed before the sentence did.
- **Outcome / decision:** three design decisions came out of the reading rather than out of the idea,
  which is the whole argument for doing step 1 before step 3:
    - **The formation window ends a month before the trade.** Jegadeesh (1990) shows the most recent
      month reverses, so `r_momentum_12_0` would net a reversal against a continuation and measure
      the difference. The column is `r_momentum_12_1`.
    - **Momentum lives in the Refinery, not the Curator**, even though it is per-security
      arithmetic. Its window is what a later experiment sweeps, and widening the Curator's schema
      forces a refetch of every identifier — a sweep must never cost a download. Its inputs stay in
      the Curator.
    - **Claim 3 is worded as a cost, not a benefit.** Ibbotson et al. (2013) find less liquid stocks
      have earned more, so the liquidity screen selects the low-return end of a compensated style on
      purpose. It buys capacity and net-of-cost survival, and if the book outperforms, the screen is
      not where that came from.
- **Open threads:**
    - **Korajczyk & Sadka (2004) is unread**, and it is the direct counterweight to Lesmond, Schill
      & Zhou. Until somebody reads it, the case against this strategy is recorded one-sided. Highest
      value next task in `Bibliotheca/`.
    - **No note has been read in full.** Every citation was verified against the publisher's record
      and every summary is of the paper's headline result; each note's `read:` field says so. No
      number from any of them may be quoted until that changes.
    - The universe is not chosen, so *the most liquid stocks* has no denominator yet.
      `Investable_Universe.csv` is still a header.
    - Claim 2 rests on a lead, not a note: DeMiguel, Garlappi & Uppal (2009) is cited nowhere and
      claimed on nowhere.

## 2026-09-10 — step 2 begins: the seed

- **Idea / question:** *the most liquid stocks* has no denominator until a universe exists. Step 2
  needs a seed before anything about liquidity can be ranked against anything.
- **What we tried / considered:** supplied as `KN_US_Equity_600.csv`, a wide file whose first row is
  `date_column` followed by every identifier as a column heading. The identifiers are the header,
  not a column, so they were taken from row 1 rather than read as records.
- **Outcome / decision:** `Universe/Investable_Universe.csv` now holds **788 unique identifiers**,
  sorted, in `main_identifier` and no other column — the seed's only required column, and everything
  else about a security is the provider's job in step 2 rather than ours here. Sorted rather than
  kept in file order, because nothing in the source order carried meaning and a sorted seed gives
  readable diffs when the universe changes.
- **What is right about it:** **the file retains delisted and acquired names** — TWTR, SIVB, FRC,
  ATVI, VMW, PXD, ESRX, CTXS, RAD, DISCA and KSU are all present. That is the first of *the five ways
  a backtest lies* answered by construction: a seed built from today's members would have deleted
  every one of them, and the backtest would have discovered that markets go up.
- **Open threads:**
    - **The file is named 600 and carries 788 identifiers.** The likely explanation is that 600 is
      the index size on any one date and 788 is the union across the history, which is exactly what a
      survivorship-free seed should look like. **It is a guess until somebody confirms it**, and it
      is worth confirming, because the alternative explanations are worse.
    - **Seven identifiers carry a hyphen** — `BRK-B`, `BF-A`, `BF-B`, `TAP-A`, `MKC-V`, `LEN-B`,
      `HEI-A`. Share classes are spelled differently by different providers (`BRK.B`, `BRK-B`,
      `BRK/B`), so these are the identifiers most likely to come back empty from the curator. Check
      them by name in `Universe/Data_Issues.csv` rather than reading a row count.
    - **A seed is not point-in-time membership.** This is a list of names that were in the index at
      some time, not a table of who was in it when. Building that, and finding each name's usable
      start date, is what `Universe/universe.ipynb` is for.
    - **The liquidity screen's denominator is now 788 names, not the market.** The top quintile is
      the top of *this* list, which is already a large-cap US list — so the screen is a cut inside an
      already-liquid universe, and its effect will be milder than the literature's. Worth saying
      before the analyzer runs, not after.

## 2026-09-16 — step 1 brought into the shared note convention, and a correction

- **Idea / question:** the researcher's note convention changed after the six notes were written —
  `Bibliotheca/Knowledge/` is gone, `Bibliotheca/LOG.md` records every read and audit, and a note
  names the claim it serves, tags each implication with it and closes with what it changes. Step 1
  had to match before any more notes arrive. The repository had also never been set up.
- **What we tried / considered:**
    - **`example` was fast-forwarded onto `researcher-note-convention-example`** (`8e35c40`, Sebas
      Blanco, 2026-09-11), so the convention's commit keeps its author. The uncommitted work of the
      entries above was re-applied on top, and `BIBLIOGRAPHY.md` resolved by hand: the convention's
      tree and its paragraph on `read`, with this branch's Part 1 and the rule that a folder appears
      with its first note.
    - **Merging `main` was ruled out, and stays ruled out.** `example` is an ancestor of `main`, and
      `main`'s 0.7.0 commit deletes every file inside the process folders but a `.gitkeep`, so a
      merge would fast-forward onto it. Process changes from `main` come across file by file.
    - **The six notes were reshaped without changing what they say:** `local_copy: none`, a
      provenance line, `## Why it is here` naming the claim with the note's own opening sentence as
      the reason, each implication tagged with its claim, and `## What it changes` built from the
      note's implications and its former *does not settle* bullets. In Lesmond, Schill & Zhou the
      heading *What follows for how the result is written up* was ours rather than the source's,
      against rule 2; its content moved into *What it changes*.
    - **`Bibliotheca/Extracts/` is ignored**, the line taken from `researcher-note-convention-main`
      (`40a06a4`), because the tree now says so. The three `.gitkeep` files under `Bibliotheca/`
      are gone.
    - **Setup ran for the first time:** `uv sync`, and `Config/.env` from the template. No agent
      skills.
- **Outcome / decision:**
    - **A correction to the 2026-09-10 instantiation entry**, which says this was built at template
      0.7.0. This branch carries the 0.6.0 process documents — `CHANGELOG.md`, `pyproject.toml` and
      `apm.yml` all say so — and 0.7.0 exists only on `main`.
    - **The strategy stays on `example`, local and not pushed**, until it is decided whether it
      lives on the public `example` or in a private repository. `main`'s 0.7.0 `AGENTS.md` calls
      the public `example` "not a strategy"; this branch's documents make it the home of one.
    - **The audit of `Bibliotheca/` found no broken links, orphans, duplicates or frontmatter
      problems**, and six findings, each a claim resting on something no note supports.
- **Open threads:**
    - **Five design questions to settle before `BLUEPRINT_1.md`**, none decided yet:
        - *sizing* — 1/N over the names that pass keeps the book invested until the set empties,
          while a fixed slot per top-quintile name lets cash build; the Daniel & Moskowitz note's
          cash prediction assumes the second;
        - *absolute or relative* — `r_momentum_12_1 > 0` is a time-series filter, while the
          evidence under claim 1 ranks winners against losers, so part of the book is market timing
          that no note covers;
        - *timing* — no rebalance frequency is stated, and the shared portfolio module rebalances
          whenever the eligible set changes, which on daily data is nearly every day;
        - *claim 3* — exitable in a day at ordinary volume depends on book size against volume,
          which the construction does not fix;
        - *the seed* — a union of names across history lets future index joiners in before they
          joined, a look-ahead pointing the same way as the signal. The body of
          `KN_US_Equity_600.csv` may hold the dated membership; the file was not found in the usual
          folders on this machine.
    - **The audit's six:** `OBJECTIVE.md` says the top-quintile cut was taken from the literature,
      with no note behind it, while the Ibbotson et al. note says it was chosen for roundness;
      claim 3's exitability has no note; and three notes lean on what no note supports — weaker
      reversal in heavily traded names (Jegadeesh 1990), falling execution costs and Korajczyk &
      Sadka's conclusion (Lesmond, Schill & Zhou), and capacity as what the screen buys (Ibbotson
      et al.).
    - **`README.md` says `example` has the shared modules filled in.** They are descriptions until
      steps 4 to 6 are written.

## 2026-09-16 — the order of work, and the process documents brought to it

- **Idea / question:** the README's *Starting your own strategy* put the universe first and the
  objective second, and the researcher's `objective` command drafted the claims *from* the notes.
  Both have the reading before the claim it is read for, which is the order the 2026-09-10 step 1
  entry above found not to work: reading with no claim has no stopping condition, and a claim
  written after the reading is shaped by it.
- **What we tried / considered:** one order, written down in three places.
    1. The objective — the idea and its claims — before any paper.
    2. The objective fine-tuned by reading for each claim, the sources that argue against it
       included; the narrow wave of reading.
    3. The investable universe, then the data.
    4. The blueprint, before the rule, every prediction citing a note from step 2 or an analyzer
       measurement.
    5. The broad wave of reading, and brainstorming.
    6. The cycle — portfolio construction, backtest, attribution — until it is finished.
    7. Every finished cycle into `RESULTS.md`, kept or rejected.
- **Outcome / decision:**
    - **The researcher's home carries it** (KaxaNuk-Researcher 0.4.0, on this machine): *The order
      of work* in its `AGENTS.md`; `objective` drafts the claims from the owner's words first and
      rewrites their evidence from the notes later; `read` and `blueprint` refuse a strategy that
      has skipped a step and name the step. Its `CLAUDE.md`, `AGENTS.md` and `RESEARCHER.md` load
      into a strategy session only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` set before
      the assistant starts; the skills, commands and agent load without it.
    - **The template carries it**: branch `order-of-work`, commit `453f146`, changelog 0.7.2 —
      stacked on `researcher-note-convention-main` (0.7.1), local, not pushed. `README.md`'s list is
      the eight steps, its step-1 row reads *the idea and its claims first, then the literature
      that argues with them*, and `SETUP.md` ends by naming `OBJECTIVE.md` as the first thing to
      do. This branch's `README.md`, `SETUP.md` and `BIBLIOGRAPHY.md` took the same text.
    - **Where this strategy stands against it:** step 1 done; step 2 in progress — six notes at
      abstract level, and the fine-tuning pass of `OBJECTIVE.md` still owed, which is where the
      audit's findings 5 and 6 and the five design gaps of the entry above belong; step 3 has a
      seed and no dated membership.
- **Open threads:**
    - `order-of-work` lands only after Sebas's 0.7.1 does, and this branch has no changelog entry
      for anything since 0.6.0.
    - Whether the desktop app honours the loading variable is untested; the fallback is a
      gitignored `CLAUDE.local.md` importing the researcher's `CLAUDE.md`.

## 2026-09-16 — correction: why merging `main` stays ruled out

- **Idea / question:** the entry *step 1 brought into the shared note convention* above gives the
  wrong reason for a right decision. It says `example` is an ancestor of `main` and a merge would
  fast-forward onto 0.7.0. That was true of `fac0a87`, not of the branch after the fast-forward to
  `8e35c40` the same entry records.
- **What we tried / considered:** `git merge-base example main` is `fac0a87`, and
  `git merge-base --is-ancestor example main` fails. A `git merge-tree` of the two shows one
  modify/delete conflict on `Bibliotheca/BIBLIOGRAPHY.md`, deleted in `main` and modified here.
- **Outcome / decision:** a merge of `main` would not fast-forward. It would be a merge commit
  carrying 0.7.0's deletions and a conflict on `BIBLIOGRAPHY.md`. It stays ruled out, for that
  reason; process changes from `main` still come across file by file.

## 2026-09-16 — the final check before the example is shown

- **Idea / question:** a walkthrough for a first-time user has to hold together across the three
  repositories it touches — this branch, the template's `main`, and the researcher's home — and
  teach three things: the Investment Lab, the research process with its APM skills, and the
  researcher. Seven reviewers with different lenses read all three; every finding was checked
  adversarially before an edit, 61 of 63 survived, and a second pass looked for what the first
  missed.
- **What we tried / considered:** four decisions, taken today.
    1. **`example` is the public worked example.** `main`'s 0.7.0 said the public `example` was the
       shape with no strategy, this branch's documents said it was private, and the branch is on the
       public remote. Both sides now describe it the same way: `liquid-momentum` worked through the
       process step by step, its own lines between example markers, public beside `main`. The
       template's `README.md`, `SETUP.md` and `AGENTS.md` say what to strip when a file is brought
       across, and the researcher's `read` fetches only `BIBLIOGRAPHY.md` and `LOG.md` from here.
    2. **This branch mirrors `main`'s version.** The 0.7.0, 0.7.1 and 0.7.2 entries came across into
       `CHANGELOG.md`, 0.7.3 records this change-set on both sides, and `pyproject.toml` and
       `apm.yml` say 0.7.3. The strategy itself is recorded here, never in the changelog.
    3. **Two edits to `OBJECTIVE.md`**, a person's file, on the owner's word: the top-quintile cut
       is said to have been chosen for roundness, with no note behind it — which closes the first of
       the audit's six — and claim 1's *what is still open* now weighs the Asness, Moskowitz &
       Pedersen note beside Lesmond, Schill & Zhou, because that paper finds the premium inside a
       universe already cut to the liquid quintile.
    4. **The KaxaNuk agent skills are installed on this branch** — `uv run apm install --target
       claude` from the root. What appeared: from `investment-lab`, `experiment-lifecycle` and
       `alpha-decomposition`; from the library packages, `data-curator-custom-calculations`,
       `backtest-engine-runs` and `attribution-analysis-runs`; from `common`, `how-we-work`,
       `apm-usage`, `devcontainer-aware-command-execution`, `propagate-mcp-env-vars`, the
       `initialize-apm` command and four rules. Nothing in the pipeline changed. They were
       discoverable in the same session that installed them, which `AGENTS.md` says not to count on.
- **Outcome / decision:** what else changed, by kind.
    - **Notes.** The Asness, Moskowitz & Pedersen note said liquidity does not enter the paper as a
      restriction; its stock universe is the largest, most liquid quintile of each market. Two
      sections were read for it, a claim heading was added, "four countries" became four equity
      markets, and "factor-neutral, broad universe" became what the paper does. The Jegadeesh &
      Titman note no longer asserts a monthly rebalance nobody has decided. `LOG.md` records the six
      notes' provenance as a backfill, and today's read.
    - **Order of work, everywhere it was still stated the old way:** the researcher paragraphs in
      both READMEs and in `BIBLIOGRAPHY.md`, `OBJECTIVE.md`'s header, the ambiguous "step 2" in the
      eight-step list, the benchmark exception, the researcher's own numbering — now eight steps on
      both sides.
    - **Stale claims here:** the template status banner in `AGENTS.md`, "`example` has them filled
      in", "it is being built", "four commands", the notebooks' `git switch example`, the setup
      test that demanded `apm_modules/`, the who-writes rows for the notes, the Setup section that
      repeated `SETUP.md` (now `main`'s pointer), the branches table.
    - **The benchmark loads the panel through `securities_panel.py`** like every later experiment;
      the notebook said it loaded inline, against the module's own contract.
    - **`CLAUDE.local.md` and the other APM targets' folders are ignored** on both branches, which
      closes the open thread of the order-of-work entry above.
    - **The researcher's home** (0.4.0, uncommitted): the fetch command, the "brings step 1 across"
      row, eight steps, the blueprint's "there may be none", the order of `read`'s checks, and three
      places that said KaxaNuk's `investment-lab` and `data-curator` packages did not exist — they
      do, and `investment-lab` carries `experiment-lifecycle`.
- **Open threads:**
    - **Steps 3 to 7 have no code.** The example teaches step 1 and the seed; it does not yet show
      the Investment Lab at work. The next body of work, in order: dated membership for the seed
      (`KN_US_Equity_600.csv` is still to be found on this machine), the `c_*` and `r_*` columns,
      the two drivers, `universe.ipynb`, `analyzer.ipynb`, then `BLUEPRINT_1.md`.
    - **The fine-tuning pass of `OBJECTIVE.md`** with the five design gaps and the audit's
      remaining findings is still owed before the blueprint.
    - **Nothing is pushed.** The documents describe the public `example` as this branch; that
      becomes true when it is pushed, and the researcher's fetch command assumes it. The template
      side is branch `order-of-work` (0.7.3) in a worktree, stacked on Sebas's unmerged 0.7.1.
    - **The seed and the six notes cannot carry an example marker.** The documents say so and name
      them among what to delete; a reader who copies `Bibliotheca/` whole inherits them.

## 2026-09-16 — the final check, second pass

- **Idea / question:** the entry above counts the first pass — 61 of 63 findings survived. A
  completeness critic then sent two more reviewers at what nobody had opened: the descriptions of
  steps 2, 3 and 7, and what the branch shows of the KaxaNuk agent skills.
- **What we tried / considered:** 23 more findings, each verified the same way; 15 survived, so the
  whole check stands at 76 confirmed and 10 refuted out of 86.
- **Outcome / decision:**
    - **The step descriptions stop contradicting the README.** `Data/curator.py` is no longer "the
      only file that talks to a provider" — `universe.ipynb` asks it too — and its install hint names
      the package `uv sync` already installed. A column with a setting an experiment sweeps, fitted
      or a window, lives in the Refinery: `r_momentum_12_1` had no home under the old wording. The
      null VWAP is one provider's habit, not every provider's. `Universe/Charts/` is gone.
    - **Graduation criterion 3 asks for what the process produces**: the trial count beside the
      winner, the sign-off saying whether the deflated figure was computed. `FINDINGS_1.md` gains the
      trial-count section `RESULTS.md` compiles from. Step 8 is funding, not a named fund, and
      Experiment 1 is the benchmark without an "if".
    - **The copilot target's paths under `.github/` are ignored** on both branches.
    - **A date slip in `Bibliotheca/LOG.md`**, written today, corrected before it was committed: the
      backfill entry said the notes were written on 2026-10-09; they were written on 2026-09-10.
- **Open threads:**
    - **The published `experiment-lifecycle` skill still lists the universe before the objective.**
      It belongs to `KaxaNuk-APM`, not to this repository or the researcher's; until it changes, the
      researcher's `AGENTS.md` says the strategy's `README.md` holds.
    - **Nothing is committed or pushed.** Until it is, `origin/example` is still `fac0a87`, and the
      fetch commands the template's `README.md` and the researcher's `read` give pull the old tree.

## 2026-09-17 — the example made readable, and where the strategy stands by name

- **Idea / question:** a first-time reader should meet the strategy on the first screen and the
  process in a few lines. Three lines in the entries above are no longer true — *nothing is
  committed or pushed*, the skills *installed on this branch*, and *the seed and the six notes
  cannot carry an example marker* — and the entries number the steps two ways.
- **What we tried / considered:** a fresh read of `main` after install and of this branch, by
  readers who had seen neither. `git log origin/example` shows the branch pushed; `.gitignore`
  lists `.claude/` and `apm_modules/`; each note's body sits between example markers, its
  frontmatter outside.
- **Outcome / decision:**
    - **`README.md` is the strategy's**, in the shape `SETUP.md` step 5 gives: the idea, the status
      banner `AGENTS.md` shares, a table of where it stands, the eight steps with where
      `liquid-momentum` is on each, and a line each on the Lab, the skills and the researcher. The
      template's README is no longer copied here; the copy had drifted.
    - **`AGENTS.md`, `SETUP.md`, `RESULTS.md`, `CHANGELOG.md` and `.gitignore` take `main`'s 0.7.4
      text** file by file, each with a marked note where this branch differs: work on
      `liquid-momentum` lands on `example`, never in a pull request into `main`, and setup step 5 is
      not run here.
    - **The notebooks, `BLUEPRINT_1.md`, `BRAINSTORMING_1.md` and `BITACORA.md` stay whole**, each
      with one marked line saying what is not written yet and why. `universe.ipynb` says the
      universe is decided in `Universe/`, the seed and the notebook; it said eligibility was decided
      in the notebook alone, which contradicted the Refinery screen `OBJECTIVE.md` names.
    - **Two notes send their predictions to `BLUEPRINT_1.md`**, to be evaluated in `FINDINGS_1.md`;
      they sent them to the findings. Logged in `Bibliotheca/LOG.md`.
    - **`example` was committed and pushed**, so the fetch commands pull this tree. This closes the
      *nothing is pushed* threads above.
    - **The skills are installed in a working copy, not on the branch.** `.claude/` and
      `apm_modules/` are ignored, so a clone has none until `uv run apm install --target claude`.
    - **The notes carry example markers** around their bodies, their frontmatter outside, so
      stripping the markers still leaves six files to delete whole. The seed carries none.
    - **From here on, entries on this public branch record the strategy's decisions and the
      repository's**, not the plumbing around them.
- **Open threads:**
    - **Where the strategy stands, by name:** the objective is written; the reading for its claims
      is in progress; the universe has a seed and no dated membership; nothing from the data on is
      built.
    - **Next, in order:** the fine-tuning pass of `OBJECTIVE.md`, with the five design questions and
      the audit's remaining findings; dated membership for the seed; the `c_*` and `r_*` columns and
      the drivers, run as curator, `universe.ipynb`, refinery, `analyzer.ipynb`; the benchmark entry
      in `BRAINSTORMING_1.md`; `BLUEPRINT_1.md` before the rule.
    - **The published `experiment-lifecycle` skill still lists the universe before the objective.**
      The template's README, *Starting your own strategy*, holds over it.

## 2026-09-17 — step 4 names its library, and step 6 reads a daily book

- **Idea / question:** two Lab libraries changed what this repository's later steps can promise.
  KaxaNuk's Portfolio Construction library exists, and Attribution Analysis published its
  documentation, which says the weights it reads must be a daily series.
- **What we tried / considered:** the Portfolio Construction source at 1.28.0, installed and run on
  made-up data outside this repository; every page of the attribution documentation, build 0.2.0;
  the step 4 to 6 module descriptions and the notebook read against both.
- **Outcome / decision:**
    - **Process 0.7.5 comes across** in `SETUP.md`, `apm.yml`, `pyproject.toml` and
      `CHANGELOG.md`, identical to `main` outside the markers.
    - **`portfolio_construction.py` calls the library inside its one signature**, one rebalance date
      at a time on the history before it: the library's methods that estimate from returns use
      whatever history they are built with. For `liquid-momentum` nothing changes — its sizing is
      equal weight, which needs no library — and the sizing question of 2026-09-16 stands.
    - **Step 6 will read the book's daily weights from `Backtest/`**, never
      `Portfolio/portfolio_weights.csv`, which holds only the rebalance dates and which the
      attribution library rejects. `attribution_analysis.py`, `backtest_engine.py` and the
      notebook's handoff table say so.
- **Open threads:**
    - **The attribution library computes Brinson-Fachler per asset**, while `AGENTS.md` and section 5
      of the notebook describe allocation as overweighting groups. Unresolved; it has to be settled
      before step 6 reports an allocation number as a group bet.
    - **The five design questions of 2026-09-16 stand**, unchanged.

<!-- example: end -->
