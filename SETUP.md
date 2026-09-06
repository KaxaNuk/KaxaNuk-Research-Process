# Setup

Everything needed to go from nothing to a repository you can work in. It is written so an agent —
Claude, Codex, Cursor — can follow it end to end, and so a person can read it in two minutes.

**If the folder you are in already contains `Bibliotheca/`, `Universe/` and `Experiments/`, you have
the repository.** Skip to step 2.

You need [Python 3.13](https://www.python.org/), [uv](https://docs.astral.sh/uv/) and
[git](https://git-scm.com) — GitHub Desktop installs the last one.

**Why 3.13 and not the newest.** The Backtest Engine is documented for Python 3.12 or 3.13, and
every performance figure in this process comes from that engine, so the ceiling is its, not ours.
The Data Curator allows 3.12 to 3.14, which makes 3.13 the version that satisfies both.

---

## The rule: one folder is the whole project

The repository root holds the process folders **and** the local setup. Nothing is installed a level
above it and nothing is nested a level below it:

```
<the root>/               <- clone here, open here, run everything here
    .claude/              installed by apm install    \
    apm_modules/          installed by apm install     |  ignored: yours, not the repository's
    apm.lock.yaml         written by apm install       |
    .venv/                written by uv sync          /
    apm.yml               committed with the template - it declares which skills to install
    Bibliotheca/          \
    Universe/              |
    Data/                  |  the process
    Experiments/           |
    Paper_Trading/         |
    Config/               /
    OBJECTIVE.md  RESULTS.md  AGENTS.md  CHANGELOG.md  README.md  SETUP.md
```

**The failure to avoid is a wrapper folder.** Making an empty folder, setting APM up in it, and then
putting the repository inside it gives you two of everything: the wrapper has no `pyproject.toml`, so
APM writes a `requirements-dev.txt` there beside a second `apm.yml` and a second `.claude/`. An agent
opened at the wrapper reads that empty setup and never sees the research tree.

If you already have that layout, delete the wrapper's `apm.yml`, `apm.lock.yaml`, `apm_modules/`,
`.claude/`, `.agents/`, `.mcp.json` and `requirements-dev.txt`, then move the repository folder up
and open it directly.

---

## Step 1 — Get the repository

Name it after the strategy — `fcf-yield-quality`, not `Experiment`. **Do not create a folder to put
it in:** the repository name is the folder name, and that folder is the root.

**On Windows, clone somewhere short.** `D:\Research\...` is fine; a deep synced path such as
`C:\Users\<you>\OneDrive\Documents\Projects\...` is not. APM stages its downloads in a
directory several levels below the root, so a path that starts too deep fails part-way through
with `WinError 3: The system cannot find the path specified` — a real failure with a misleading
message. The same install run from a short path succeeds.

**The button.** *Use this template* on
[`KaxaNuk/KaxaNuk-Research-Process`](https://github.com/KaxaNuk/KaxaNuk-Research-Process), then clone
it with GitHub Desktop. Cloning into `D:\Research` gives you `D:\Research\fcf-yield-quality`, and
that is the root.

**The GitHub CLI**, which records the template relationship the same way:

```bash
gh repo create <strategy-name> --template KaxaNuk/KaxaNuk-Research-Process --private --clone
```

**Or a plain clone, with a fresh history**, so the strategy's first commit is its own. Run this from
inside an empty folder that is already named after the strategy:

```bash
git clone --depth 1 --branch main https://github.com/KaxaNuk/KaxaNuk-Research-Process .
```

```bash
rm -rf .git && git init && git add -A && git commit -m "Start from the KN Research Process template"
```

Only `main` is copied by any of the three. The `example` branch — one strategy worked end to end — is
kept by KaxaNuk for reading, and is not part of a new strategy.

> **For the agent.** `gh repo create --template` copies asynchronously on GitHub's side, so a clone
> that lands empty seconds later is a race and not a failure: wait, then clone again. The plain-clone
> form clones into `.`, which git allows only in an empty directory — that is deliberate, and it is
> what stops a wrapper folder from being created by accident.

---

## Step 2 — Build the environment

From the root:

```bash
uv sync
```

That creates `.venv/` and installs the pipeline, plus the `dev` group — which is where the `apm`
command in step 4 comes from, so this step has to come first.

---

## Step 3 — Put your keys in place

```bash
cp Config/.env.template Config/.env
```

Fill in a data-provider key. The two KaxaNuk entries are engine licences: steps 1 to 4 of the process
run without them, and steps 5 and 6 report what is missing and skip.

> **For the agent.** Never open, read back, print or echo `Config/.env`, and never put a value from it
> in a command that gets recorded. You may say **which keys are still empty, by name only**. An
> exposed key is rotated, not edited out.

---

## Step 4 — The agent skills, if you want them

**Ask the user before running this step.** KaxaNuk publishes its AI skills as APM packages: how the
six Lab libraries are called, how an experiment is structured, how attribution is read, and the house
rules on branches, style and changelogs.

**Nothing in the pipeline imports a skill.** The repository runs, the notebooks run and the results
are the same whether or not this step happens — so *no* is a real answer, and *later* costs nothing.

If yes, from the root — **the same folder as steps 2 and 3, never a level above it**:

```bash
apm config set target claude
```

```bash
apm install
```

`apm install` with no arguments reads the committed `apm.yml`, so there is nothing to type. Use the
target the user actually works with — `codex`, `cursor`, `copilot` and the rest are listed in
[APM's target catalogue](https://github.com/microsoft/apm/blob/main/docs/src/content/docs/concepts/primitives-and-targets.md#target-catalogue)
— or pass it per command with `apm install --target codex`.

**Want only some of them?** Delete the lines you do not want from `apm.yml` before installing, or name
one package directly. Somebody who licenses only the Attribution Analysis library, and has no research
process at all, wants exactly this:

```bash
apm install KaxaNuk/KaxaNuk-APM/attribution-analysis
```

The packages, and what each is for, are listed at
[`KaxaNuk/KaxaNuk-APM`](https://github.com/KaxaNuk/KaxaNuk-APM).

> **For the agent.** Skills installed here are discoverable in a **new** session, not this one. Say so
> rather than claiming they are already active.

---

## What "done" looks like

From the root:

```bash
git status
```

**It should be clean.** `apm.yml` is committed because it is a declaration, like `pyproject.toml`;
`.venv/`, `apm_modules/`, `.claude/` and `apm.lock.yaml` are what the two commands *produced*, and
they are ignored the way `.venv/` always is. Anything else showing up means something was written in
the wrong place.

Then open **this folder** — not a parent of it — in PyCharm, Claude or Codex.

---

## Next

[`README.md`](README.md) says what the repository is and where each kind of logic goes;
[`AGENTS.md`](AGENTS.md) says how work is done in it. The five things to do first are in the
*Starting your own strategy* section of the README, and the first is putting your securities in
`Universe/Investable_Universe.csv`.
