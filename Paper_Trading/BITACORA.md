# Paper Trading — step 7 of the KN Research Process

The last step inside the Investment Lab, and the only one that runs on data the strategy has never
seen. A backtest tells you what a rule *would* have done; paper trading tells you what it *does* — on
live prices, with live universe changes, and with the delistings and corporate actions a historical
file has already tidied up.

Step 8, Production, is not here: a strategy leaves this repository when it joins the KN Fund
allocation.

> **This file is the gate, not a log.** Under the document architecture described in
> [`../AGENTS.md`](../AGENTS.md), `JOURNAL_N.md` means an append-only dated record inside an
> experiment folder. This document is a contract — what graduation means and what has to be true
> before it happens — so it carries a different name to keep the two from being confused.

## What graduation means

An experiment is **promoted**, not copied. `Paper_Trading/Paper_Trading_N/` mirrors the
`Experiment_N` it came from, so the lineage of a paper-traded book is never in question. The
experiment notebook stays where it is — it remains the record of how the rule was chosen.

## The gate

Strong backtest results are necessary and **not sufficient**. All five must hold before an experiment
graduates.

| # | Criterion | Why it is on the list |
| --- | --- | --- |
| 1 | **Beats the benchmarks on risk-adjusted return** — engine Sharpe above SPY, QQQ and KN600, *and* above its own control row, over the same window | A strategy that only beats the index on raw return is usually just carrying more risk |
| 2 | **Attribution shows selection or idiosyncratic alpha**, not a pure factor exposure | If the return decomposes entirely into beta and size, the honest product is a cheaper factor fund, not this |
| 3 | **Conclusions survive parameter perturbation, and the trial count is deflated** | A result that appears at one threshold and vanishes at the next is a sweep artefact. Read the direction across a sweep, never the single best cell |
| 4 | **Costs and capacity are modelled and stated** — turnover, commission, and any assumption the engine does *not* model, borrow cost above all | The gap between a backtest and a fill is where strategies die |
| 5 | **Explicit sign-off.** | Graduation is a decision, not a threshold that trips automatically |

Every criterion is evidenced from the experiment's `FINDINGS_N.md` and from
[`../RESULTS.md`](../RESULTS.md). **If it cannot be evidenced from those, it has not been met.**

### Criterion 2 is evaluable here, and that is not universal

This stack has a real attribution stage — `kaxanuk.attribution_analysis`, Brinson-Fachler and the
KN5FM factor model — so "is this selection, or is it a size tilt?" is a question with an answer rather
than an admission. Repositories built on stacks without step 6 have to substitute a beta-matched
control book or an explicit regression on the market, and name the substitute in the sign-off. **Here
there is no substitute to name, which means there is also no excuse.**

Expect the answer to be a *pass with a qualification* rather than a clean pass. A book whose excess
return is roughly half factor exposure and half idiosyncratic has passed criterion 2 and has also
been told exactly how much of it is not the idea — which is the kind of thing the criterion exists to
surface, not a reason to soften it.

## What a paper-trading run is

Unlike an experiment, this stage is **not** a notebook. It is a script that can be run on a schedule,
because the question is no longer "what would this have done" but "what does it hold today, and how
is it doing":

- reads the same `Data/Refinery/Time_Series/` panel the experiment did, refreshed;
- applies the graduated rule with **no re-fitting** — the parameters are frozen at graduation;
- writes the target book for the date, and appends to a running performance record;
- flags divergence from the backtest's expected behaviour: turnover, holdings count, exposure.

`daily_update.py` (the scheduler over every graduated book) and
`Paper_Trading_1/paper_trading_1.py` (one graduated rule, frozen) are the skeleton for that. Both
carry their contract as a docstring and **no logic**: nothing has graduated yet, and agreeing what
the stage may and may not do is worth more than code written before there is a book to run.

One rule in that contract is worth repeating, because it is the whole point of the stage:
**a paper-trading script re-fits nothing.** Parameters are frozen at graduation. A run that tunes
anything is a backtest wearing a costume, and it re-introduces exactly the search that
[Bailey, Borwein, López de Prado & Zhu](../Bibliotheca/Papers/Bailey_Borwein_LopezDePrado_Zhu_2014_Pseudo_Mathematics_And_Financial_Charlatanism.md)
say produces negative out-of-sample performance.

## Current status

**Nothing has graduated. Nothing has been tested.** This is the template; the first candidate
arrives when an experiment's `FINDINGS_N.md` can evidence criterion 1.

When one does, record it here: which experiment, which variant, which criteria it clears, and —
above all — which it does not and why. The blocking items are the content of this section, not the
passing ones.

**`Paper_Trading_1/` is named for the experiment it would mirror.** If Experiment 1 is your
benchmark, its graduation is not applicable and this folder will be renamed for the experiment that
actually graduates. The convention is right; the number is a placeholder until then.
