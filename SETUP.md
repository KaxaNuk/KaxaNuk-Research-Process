# Setup

Everything needed to go from nothing to a repository you can work in. It is written so an agent —
Claude, Codex, Cursor — can follow it end to end when all it was told is *please help install
`https://github.com/KaxaNuk/KaxaNuk-Research-Process`*, and so a person can read it in two minutes.

**If the folder you are in already contains `Bibliotheca/`, `Universe/` and `Experiments/`, you have
the repository.** Skip to step 2.

## What you need first

Two tools. Python is **not** one of them — `uv` fetches the right version itself in step 2.

| Tool | Windows | macOS and Linux |
| --- | --- | --- |
| [git](https://git-scm.com) | `winget install --id Git.Git -e` — or install GitHub Desktop, which brings it | `xcode-select --install` on macOS; your package manager on Linux |
| [uv](https://docs.astral.sh/uv/) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

Open a **new** terminal after installing either, so it is on the path. `git --version` and
`uv --version` both answering is the whole check.

> **For the agent, before anything else.** If you were given only the URL, you are missing two things
> and must ask for the first: **the strategy's name** — it becomes the folder and repository name, so
> `fcf-yield-quality`, not `Experiment` — and **where to put it**, which defaults to the folder you are
> in. Then decide the root by looking at that folder, and say which folder you chose:
>
> - it is **empty** → it is the root;
> - it already holds `Bibliotheca/`, `Universe/` and `Experiments/` → the repository exists, go to step 2;
> - it holds `apm.yml`, `apm_modules/`, `.claude/` or `requirements-dev.txt` **without** those
>   folders → **stop**: that is a wrapper somebody prepared by hand, and the section below says why
>   and what to delete;
> - it holds anything else → create `<strategy-name>/` inside it, make that the root, and say so.
>
> Every command from step 1 on runs **in the root**. Never a level above it.

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
    uv.lock               written by uv sync - committed, it pins what a result came from
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

Name it after the strategy. **Do not create a folder to put it in:** the repository name is the
folder name, and that folder is the root.

**On Windows, clone somewhere short.** `D:\Research\...` is fine; a deep synced path such as
`C:\Users\<you>\OneDrive\Documents\Projects\...` is not. APM stages its downloads in a
directory several levels below the root, so a path that starts too deep fails part-way through
with `WinError 3: The system cannot find the path specified` — a real failure with a misleading
message. The same install run from a short path succeeds.

**The button.** *Use this template* on
[`KaxaNuk/KaxaNuk-Research-Process`](https://github.com/KaxaNuk/KaxaNuk-Research-Process), then clone
it with GitHub Desktop. Cloning into `D:\Research` gives you `D:\Research\fcf-yield-quality`, and
that is the root. This is the way that records the template relationship on GitHub.

**The GitHub CLI**, which records it the same way, if `gh` is installed and signed in:

```bash
gh repo create <strategy-name> --template KaxaNuk/KaxaNuk-Research-Process --private --clone
```

**Or a plain clone with a fresh history** — the way an agent with only a URL will usually go. Run
it from inside the empty root; the `.` at the end is what keeps the clone from making a folder
inside it:

```bash
git clone --depth 1 --branch main https://github.com/KaxaNuk/KaxaNuk-Research-Process .
```

Then start the strategy's own history. In bash, or the terminal on macOS and Linux:

```bash
rm -rf .git && git init && git add -A && git commit -m "Start from the KN Research Process template"
```

In PowerShell, which is what the Claude app and Codex drive on Windows:

```powershell
Remove-Item -Recurse -Force .git; git init; git add -A; git commit -m "Start from the KN Research Process template"
```

Only `main` is copied by any of the three. The `example` branch — one strategy worked end to end — is
kept by KaxaNuk for reading, and is not part of a new strategy.

> **For the agent.** Three things go wrong here, and none is a reason to stop.
>
> - **`git commit` refuses for want of an identity** on a machine that has never committed. Ask the
>   user for the name and email to use — never invent them — and set them for this repository only:
>   `git config user.name "<name>"` then `git config user.email "<email>"`. Then commit again.
> - **`gh repo create --template` copies asynchronously** on GitHub's side, so a clone that lands
>   empty seconds later is a race, not a failure: wait, then clone again.
> - **`git clone … .` refuses a non-empty directory.** That is deliberate — it is what stops a wrapper
>   folder from being created by accident. Go back to the root decision rather than around it.

---

## Step 2 — Build the environment

From the root:

```bash
uv sync
```

That creates `.venv/` and installs the pipeline. **If Python 3.13 is not on the machine, `uv`
downloads it** — there is nothing to install by hand. It also installs the `dev` group, which is
where the `apm` command in step 4 comes from, so this step has to come first.

**Why 3.13 and not the newest.** The Backtest Engine is documented for Python 3.12 or 3.13, and every
performance figure in this process comes from that engine, so the ceiling is its, not ours. The Data
Curator allows 3.12 to 3.14, which makes 3.13 the version that satisfies both.

---

## Step 3 — Put your keys in place

```bash
cp Config/.env.template Config/.env
```

Fill in a data-provider key. The two KaxaNuk entries are engine licences: steps 1 to 4 of the process
run without them, and steps 5 and 6 report what is missing and skip.

> **For the agent.** Never open, read back, print or echo `Config/.env`, and never put a value from it
> in a command that gets recorded. You may say **which keys are still empty, by name only** — and you
> cannot fill them: that is the one thing in this file only the user can do.

---

## Step 4 — The agent skills

KaxaNuk publishes its AI skills as APM packages: how each Lab library is called, how an experiment
is structured, how attribution is read, and the house rules on branches, style and changelogs. The
committed `apm.yml` names the set, so the command takes no package names.

**Nothing in the pipeline imports a skill.** The repository runs, the notebooks run and the results
are the same whether or not this step happens — so *no* is a real answer, and *later* costs nothing.

> **For the agent — install, or ask?** If the request already said so — *install it and the skills*,
> *install everything*, *set up the whole thing* — that is consent: run it. If the request was only to
> set the repository up, **ask first**, in one sentence, and take *no* as the answer it is. Either way
> say that the skills become discoverable in a **new** session, not this one.

From the root — **the same folder as steps 2 and 3, never a level above it** — with the target being
the agent you actually use:

```bash
uv run apm install --target claude
```

```bash
uv run apm install --target codex
```

`uv run` is not decoration: `apm` lives inside `.venv/` and is not on the path of a fresh terminal,
so a bare `apm install` says *command not found* on the very machine this file is for. Other targets
— `cursor`, `copilot`, `windsurf` and the rest — are in
[APM's target catalogue](https://github.com/microsoft/apm/blob/main/docs/src/content/docs/concepts/primitives-and-targets.md#target-catalogue).

**Want only some of them?** `apm.yml` names one package, `kaxanuk`, which is every KaxaNuk package
under one name. Replace that line with the packages you want — `common`, `data-curator`,
`backtest-engine`, `attribution-analysis`, `investment-lab` — and install again. Somebody who
licenses only the Attribution Analysis library, and has no research process at all, does not need
this repository: in their own project,

```bash
uv run apm install KaxaNuk/KaxaNuk-APM/attribution-analysis --target claude
```

The packages, and what each is for, are listed at
[`KaxaNuk/KaxaNuk-APM`](https://github.com/KaxaNuk/KaxaNuk-APM).

---

## What "done" looks like

From the root:

```bash
git status
```

**Exactly one new file should appear, and it is `uv.lock`. Commit it.** It pins the versions this
strategy's results came from, which is why the template deliberately ships without one and your
repository keeps one.

Everything else the commands produced — `.venv/`, `apm_modules/`, `.claude/`, `apm.lock.yaml` — is
ignored, and `apm.yml` was already committed because it is a declaration, like `pyproject.toml`.
**Anything else showing up means something was written in the wrong place.**

**If you took the plain-clone path, the repository exists only on this machine.** Nothing is lost
and nothing is wrong — but it is not backed up and nobody else can see it. In GitHub Desktop, *Add*
→ *Add existing repository*, then *Publish repository*. That is the whole of it, and it is the user's
to do, not the agent's.

Then open **this folder** — not a parent of it — in PyCharm, Claude or Codex.

> **For the agent — the hand-over.** Say the absolute path of the root, that it is the whole project
> and the folder to open, which `.env` keys are still empty by name, whether the skills were installed
> and that they appear in a new session, and whether the repository has a remote yet. Then stop.
> Starting research work is a different request.

---

## Next

[`README.md`](README.md) says what the repository is and where each kind of logic goes;
[`AGENTS.md`](AGENTS.md) says how work is done in it. The five things to do first are in the
*Starting your own strategy* section of the README, and the first is putting your securities in
`Universe/Investable_Universe.csv`.
