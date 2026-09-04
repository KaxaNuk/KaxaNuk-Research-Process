# Shu, Yu & Mulvey (2024) — *Downside Risk Reduction Using Regime-Switching Signals: A Statistical Jump Model Approach*

> **Link:** [Journal of Asset Management](https://link.springer.com/article/10.1057/s41260-024-00376-x)
> · preprint at [arXiv:2402.05272](https://arxiv.org/abs/2402.05272)
>
> **Citation:** *Journal of Asset Management* 25(5), 493-507, 2024. Previously circulated as
> *Regime-Aware Asset Allocation: a Statistical Jump Model Approach*. Links last checked 2026-09-03.
>
> **Local copy:** none held.
>
> **Read into this repository:** 2026-09-03, at v0.3.0. Read in full from the arXiv HTML of v2.

The single-asset companion to
[*Dynamic Asset Allocation with Asset-Specific Regime Forecasts*](Shu_Yu_Mulvey_2024_Dynamic_Asset_Allocation_With_Asset_Specific_Regime_Forecasts.md).
**Its title is its finding**, and that finding is the one this repository's Data stage independently
reproduced.

## What it says

One index at a time — S&P 500, DAX, Nikkei 225 — from 1990 to 2023, at 10 basis points per side.

**A statistical jump model on three features**, all exponentially weighted from excess returns:
downside deviation at a 10-day half-life, and the Sortino ratio at 20 and 60 days. Two regimes.
Trained on a 3,000-day (about twelve-year) window, with the model parameters re-solved every six
months and daily regime assignment done by online inference against fixed parameters.

**The strategy is binary.** Bull regime, 100% in the index; bear regime, 100% in three-month
treasury bills. A regime identified on day *t* is executed on day *t+2* — a deliberate one-day
trading delay, so nothing is traded on information that was not yet available.

**λ is chosen by time-series cross-validation on Sharpe ratio**, over an eight-year lookback window,
re-selected monthly. The authors are explicit that this differs from prior work, which chose λ on
statistical criteria.

**The results are lopsided in a specific direction.** On the S&P 500 the strategy raises the Sharpe
from 0.48 to 0.68, cuts maximum drawdown from −55.2% to −26.6% and volatility from 18.2% to 13.1% —
while raising annual return only from 10.2% to 11.2%. DAX and Nikkei show the same shape, with larger
return gains on the two indices whose buy-and-hold was worst. The jump model beats a hidden Markov
model on every index, and keeps beating it when the trading delay is stretched to five or ten days,
which the authors attribute to the greater persistence of jump-inferred signals.

**On what the model is for**, the authors say it plainly: regime identification is *interpretative
rather than predictive*, and the strategy's profitability rests on the assumption of regime
persistence rather than on forecasting accuracy.

## What it implies for this strategy

> **This is the paper that predicts our own result, and we found it independently before reading
> it.** `Data/analyzer.ipynb` measures the causal regime label separating forward *volatility* on 11
> of 12 assets and forward *return* on only 5 — and this paper's headline is a 27-point drawdown
> reduction against a 1-point return improvement. A signal that reduces risk without adding return
> is not a broken signal; it is this signal, working as documented. It changes what the strategy
> should claim, not whether it is worth running.
>
> **Their sentence is the one to quote in `OBJECTIVE.md`:** regime identification is interpretative
> rather than predictive. Any variant here that reports a large *return* gain from the regime label
> alone is disagreeing with the authors of the method, and should be checked for look-ahead before
> it is believed — a check `Data/analyzer.ipynb` section 5 now performs by construction.
>
> **The one-day trading delay is the design we must copy, not merely respect.** Their regime on day
> *t* trades on *t+2*. That is stricter than the engine's default of trading at the next available
> price, and the difference is a whole day of the sharpest moves. **Experiment 1 should implement the
> paper's delay explicitly rather than inheriting whatever the engine happens to do.**
>
> **Where we deliberately disagree: choosing λ on Sharpe.** Selecting the model's only real knob by
> the metric the strategy is judged on is the practice `Bibliotheca` Part 5 exists to warn about,
> whatever the cross-validation scheme around it. We choose λ on persistence and publish the sweep.
> The cost is honest and should be stated: **we cannot claim their numbers**, because we did not use
> their selection rule.
>
> **The feature sets differ between the two papers and nobody says why.** Three features here, eight
> in the multi-asset paper, with no stated reason for the change. We use the eight. If a variant ever
> needs a smaller feature set, this is the precedent for one — and the fact that two papers by the
> same authors disagree is itself a warning that the feature set is less settled than either implies.
