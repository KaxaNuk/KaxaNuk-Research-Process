# Setup

Everything needed to go from nothing to a repository you can work in. It is written so an agent —
Claude, Codex, Cursor — can follow it end to end when all it was told is *please help install
`https://github.com/KaxaNuk/KaxaNuk-Research-Process`*, and so a person can read it in two minutes.

**If the folder you are in already contains `Bibliotheca/`, `Universe/` and `Experiments/`, you have
the repository:** check the two tools below, then skip to step 2.

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
> in. A third is optional: **one sentence on the idea**, if the user has it ready — it seeds the README
> in step 5, and a placeholder is fine if not. Then decide the root by looking at that folder, and say
> which folder you chose:
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

Clone into one folder, open that folder, and run every command in it: nothing installed a level
above it, nothing nested a level below. What setup writes there — `.venv/`, `apm_modules/`,
`apm.lock.yaml`, and `.claude/` or, for Codex, `.agents/` and `.codex/` — is ignored; `uv.lock`,
which `uv sync` writes, is committed, and `apm.yml` comes committed with the template.

**The failure to avoid is a wrapper folder**: APM set up in an empty folder with the repository put
inside it. The wrapper has no `pyproject.toml`, so APM writes `requirements-dev.txt`, a second
`apm.yml` and a second `.claude/` there, and an agent opened at the wrapper never sees the research
tree. If you have that layout, delete the wrapper's `apm.yml`, `apm.lock.yaml`, `apm_modules/`,
`.claude/`, `.agents/`, `.mcp.json` and `requirements-dev.txt`, then move the repository folder up
and open it directly.

---

## Step 1 — Get the repository

Name it after the strategy: the repository name is the folder name, and that folder is the root.
The button and the CLI create it for you; for a plain clone, make that one empty folder yourself —
never a folder around it.

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
it from inside that empty folder; the `.` at the end keeps the clone from making another folder
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

Only `main` is copied by any of the three, on purpose. The `example` branch, one strategy worked
through the same folders, stays behind; the
[template's README](https://github.com/KaxaNuk/KaxaNuk-Research-Process) says how to copy a file from
it and what to strip. Never build on it.

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

That creates `.venv/` and installs the pipeline. **If neither Python 3.12 nor 3.13 is on the
machine, `uv` downloads 3.13** — there is nothing to install by hand. It also installs the `dev`
group, which is where the `apm` command in step 4 comes from, so this step has to come first.

**Why 3.13 and not the newest.** The Backtest Engine is documented for Python 3.12 or 3.13, and every
performance figure in this process comes from that engine, so the ceiling is its, not ours. The Data
Curator allows 3.12 to 3.14, which makes 3.13 the version that satisfies both.

---

## Step 3 — Put your keys in place

```bash
cp Config/.env.template Config/.env
```

Fill in the key for your data provider; the template has a line for FMP, Sharadar and LSEG.
`KNBE_API_KEY_KAXANUK` and `KNAA_API_KEY_KAXANUK` are the Backtest Engine and Attribution Analysis
licences: the process runs without them up to portfolio construction, and the backtest and
attribution report what is missing and skip.

> **For the agent.** Never open, read back, print or echo `Config/.env`, and never put a value from it
> in a command that gets recorded. You may say **which keys are still empty, by name only** — and you
> cannot fill them: that is the one thing in this file only the user can do.

---

## Step 4 — The agent skills

KaxaNuk publishes its agent skills — what Claude or Codex learns about this process and the Lab
libraries — as packages for APM, the Agent Package Manager: how each library that has a package is
called, how an experiment is structured, how attribution is read, and the house rules on branches,
style and changelogs. The committed `apm.yml` names the set, so the command takes no package names.

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
[APM's target catalogue](https://github.com/microsoft/apm/blob/main/docs/src/content/docs/concepts/primitives-and-targets.md#target-catalogue);
what they write is ignored the way `.claude/` is, except `.github/`, which Copilot shares with
anything else a repository keeps there.

**Want only some of them?** `apm.yml` names one package, `kaxanuk`, which is every KaxaNuk package
under one name. Replace that line with the packages you want — `common`, `data-curator`,
`backtest-engine`, `attribution-analysis`, `investment-lab` — and install again. `investment-lab` is
the one that carries the `experiment-lifecycle` skill the template's README leans on. In a project
of your own with `apm` on the path, `apm install KaxaNuk/KaxaNuk-APM/<package> --target claude`
installs one package with no `uv run`. The packages, and what each is for, are listed at
[`KaxaNuk/KaxaNuk-APM`](https://github.com/KaxaNuk/KaxaNuk-APM).

---

## Step 5 — Make the README the strategy's

The `README.md` you cloned describes the KN Research Process — the template, not your strategy. A
strategy repository's README describes **the strategy**: what it is, what it claims, where it
stands. Replace the whole file with this, filled in, and leave the process to the link:

```markdown
# <strategy-name>

<one sentence on the idea — or: The objective is not written yet; see OBJECTIVE.md.>

> **Status: set up, nothing measured.** Replace this line as the strategy moves, and the banner at
> the top of `AGENTS.md` with it.

Built on the [KN Research Process](https://github.com/KaxaNuk/KaxaNuk-Research-Process): eight
steps as a folder structure. That repository's README says what each folder is for, where each
kind of logic goes and, under *Starting your own strategy*, the order to work in; this one does not
repeat it. **Next:** [`OBJECTIVE.md`](OBJECTIVE.md), the idea and its claims, before any paper is
read.

| Read | For |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the idea, and the status of each claim inside it |
| [`RESULTS.md`](RESULTS.md) | every number this repository has measured, and what it cost |
| [`AGENTS.md`](AGENTS.md) | how work is done here, and the bar a result has to clear |
| [`SETUP.md`](SETUP.md) | how this repository is set up on a new machine |
```

Put the same status line in place of the banner at the top of `AGENTS.md`, and rename `name` and
`author` in `apm.yml` to the strategy's and yours. Then commit them together with `uv.lock`, the
other file the setup itself produced:

```bash
git add README.md AGENTS.md apm.yml uv.lock
git commit -m "README: <strategy-name>"
```

> **For the agent.** The name is the one you asked for at the start; the sentence too, if the user
> gave one — **never invent a thesis**, use the placeholder. `author` in `apm.yml` is the user's
> name: ask if you do not have it, never invent it. Everything else in the block is fixed. Do not
> keep the template's README under another name: the process lives upstream, and a copy here is a
> copy that drifts.

---

## What "done" looks like

From the root:

```bash
git status
```

**It should be clean.** Step 5 committed what the setup itself changed: the README, the `AGENTS.md`
banner, `apm.yml`'s name and author, and `uv.lock` — which pins the versions this strategy's results
will come from, and is why the template ships without one and your repository keeps one. Everything
else the commands produced — `.venv/`, `apm_modules/`, `.claude/`, `apm.lock.yaml` — is ignored.
**Anything showing up means something was written in the wrong place.**

**If you took the plain-clone path, the repository exists only on this machine.** Nothing is lost
and nothing is wrong — but it is not backed up and nobody else can see it. In GitHub Desktop, *Add*
→ *Add existing repository*, then *Publish repository*. That is the whole of it, and it is the user's
to do, not the agent's.

Then open **this folder** — not a parent of it — in PyCharm, Claude or Codex.

> **For the agent — the hand-over.** Say the absolute path of the root, that it is the whole project
> and the folder to open, that the README is now the strategy's, which `.env` keys are still empty
> by name, whether the skills were installed and that they appear in a new session, whether the
> repository has a remote yet, and that the next step is `OBJECTIVE.md`. Then stop.
> Starting research work is a different request.

---

## Next

The first thing to write is `OBJECTIVE.md`: the idea and its claims, before any paper is read. The
order after it is *Starting your own strategy* in the
[template's README](https://github.com/KaxaNuk/KaxaNuk-Research-Process), which also says where each
kind of logic goes; [`AGENTS.md`](AGENTS.md) says how work is done here.
