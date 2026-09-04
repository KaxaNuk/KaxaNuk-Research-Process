# Objective

> **What this file is for.** One idea, one objective, and the claims inside it with their status.
> The first thing a CIO reads and the last thing that changes: a change here means a *different*
> strategy, not a better version of this one.
>
> **Write it before the backtest.** The claims table is a set of predictions. A claim added after a
> result is an observation wearing a hypothesis's clothes.
>
> Every angle-bracketed slot is guidance. Replace it, then delete this blockquote.

## The main idea

> **<One sentence somebody outside the team could repeat. What the strategy owns, why, and the
> plain-language feature it owns it by.>**

<Two or three sentences naming the signal and the sizing in the panel's own vocabulary — the `c_*`
or `r_*` column each one reads. Neither half needs to be clever; both need to be explainable in a
sentence, because that is what lets attribution later say which half earned the return.>

The strategy is named `<Strategy_Name>`, after <what the name encodes>.

## The objective

**<What a finished version would let the desk do — the capability, not the number.>** The
deliverable is not a Sharpe; it is a rule simple enough that when it works we can say *why*, and
when it fails we can say *which part* failed.

Concretely, an acceptable end state is: *<on any date the strategy names what it holds, gives a
one-sentence reason for each, and can point at an attribution saying how much of the return came
from the signal rather than from a factor exposure>.*

**The constraint is <the one design constraint every experiment respects — for example, radical
simplicity: complexity is added one lever at a time, and each addition must beat the simpler
baseline to earn its place>.**

## The claims inside that sentence

They are tested separately and **their status is not the same.** Keep this table honest: it is the
only place a reader sees which parts of the idea have survived contact with the data.

| | Claim | Status |
| --- | --- | --- |
| **1. <Signal>** | <what selecting on this is claimed to produce> | **untested** |
| **2. <Sizing>** | <what weighting by this is claimed to add> | **untested** |
| **3. <Construction>** | <a property the rules guarantee — a screen, an exclusion> | **true by construction, untested as a source of return** |

Status vocabulary, so it means the same across strategies: **untested** · **measured** (the analyzer
says something; no book has been run) · **falsified** · **confirmed as a book** (it beats its
benchmarks through the engine) · **confirmed as a factor** (attribution assigns it the return) ·
**unexplained** (confirmed as a book, not as a factor — the usual state, and the interesting one) ·
**true by construction**.

### Claim 1 — <signal>

<What the benchmark experiment showed, in numbers, citing `RESULTS.md`. Then what attribution said.
A book that beats its benchmarks while the factor model assigns its named factor ~0% is the
situation to expect, not an anomaly. Say which test would settle it.>

### Claim 2 — <sizing>

<The analyzer's information coefficient for the sizing variable inside the eligible pool, with its
sign. If the sign is wrong, say so here and restate the claim in the weaker form that survives.>

### Claim 3 — <construction>

<Why it is true by construction, and why that makes it the hardest claim to evidence: a screen that
works by exclusion leaves no trace in the book. Name the counterfactual run that would show it.>

---

## What is not claimed

- **Not that the parameters are right.** <Which parameters were taken as given rather than tuned,
  and why that is a defence against data-snooping rather than evidence of optimality.>
- **Not that this is out of sample.** Nothing is, until an experiment reaches step 7.
- <Anything a reader might assume the strategy claims and would be wrong to.>

---

## The five parts, and the job each does

| Part | Its job | The failure it prevents |
| --- | --- | --- |
| **The main idea** | one sentence somebody outside the team could repeat | a strategy nobody can explain is a strategy nobody can debug |
| **The objective** | the *capability* a finished version gives the desk, not a number | "a Sharpe of 1.2" is not something you can tell whether you have achieved |
| **The claims** | the sentence broken into parts testable separately, each with a status | a strategy that half works reads as working, unless the halves are listed |
| **What is not claimed** | what a reader might assume and would be wrong to | the reader assumes it anyway if you do not say |
| **The named columns** | which `c_*` or `r_*` column carries each half | attribution cannot say which half earned the return unless the halves have names |

---

**Where this stands, with every number and its caveats: [`RESULTS.md`](RESULTS.md).**
How work is done here, and the bar a result has to clear: [`AGENTS.md`](AGENTS.md).
