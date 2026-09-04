# Shu, Yu & Mulvey (2024) — *Dynamic Asset Allocation with Asset-Specific Regime Forecasts*

> **Link:** [arXiv:2406.09578](https://arxiv.org/abs/2406.09578)
>
> **Citation:** arXiv preprint 2406.09578v1, submitted 13 June 2024. Princeton University. Link last
> checked 2026-09-03.
>
> **Local copy:** none held.
>
> **Read into this repository:** 2026-09-03, at v0.3.0. Read in full from the arXiv HTML.

**This is the paper the example strategy is built from.** The universe in
`Universe/Investable_Universe.csv` is its Table 1, and the eight `c_*` feature columns in
`Data/Curator/custom_calculations.py` are its Table 2.

## What it says

Twelve risky assets — US large, mid and small cap, EAFE, emerging markets, aggregate bonds, long
treasuries, high yield, corporates, REITs, commodities and gold — plus a risk-free asset, on daily
total-return indices from 1991 to 2023.

**A hybrid of two models.** An unsupervised **statistical jump model** identifies which of two
regimes each asset is in; a supervised **gradient-boosted classifier** then forecasts the *next
day's* regime from the same features plus five macro series (2-year yield, the 10y−2y slope, VIX,
stock-bond correlation). The forecasts feed a Markowitz mean-variance optimisation.

**The jump model.** Two regimes. It minimises the scaled squared distance from each day to its
regime's centre, plus a penalty λ paid every time the label changes. λ is chosen by time-series
cross-validation on a five-year validation window, over a logarithmic grid from 0 to 100. Trained on
an eleven-year lookback, retrained twice a year.

**The features are eight numbers derived from returns alone.** Exponentially weighted downside
deviation on a log scale at half-lives 5 and 21; exponentially weighted mean return at 5, 10 and 21;
exponentially weighted Sortino ratio at 5, 10 and 21. Three assets — aggregate bonds, treasuries and
gold — drop the downside-deviation features, because preliminary analysis showed those two do not
separate their regimes.

**From regime to weights.** Under a minimum-variance objective the bullish assets get an expected
return of 10 basis points and the bearish ones zero; under mean-variance the forecast is the average
historical return of same-regime days in the training window, with bearish forecasts floored at −10
basis points. Long only, 40% cap per asset, leverage capped at 1.0, an EWM covariance at a 252-day
half-life, and a 5 basis point one-way trading cost inside the objective. **If three or fewer of the
twelve assets are bullish, the whole book goes to the risk-free asset.**

Benchmarks are a daily-rebalanced 60/40 fix-mix, buy and hold, and the jump model on its own without
the forecasting layer.

## What it implies for this strategy

> **Take the features and the universe; leave the forecasting layer and the optimiser for an
> experiment.** The eight features are the paper's, at the paper's half-lives, and they live in the
> Curator precisely so they stay frozen — parameters taken from a paper rather than searched for are
> a defence against data-snooping, and that defence evaporates the moment we start tuning them.
>
> **The architecture is the argument.** The paper needs a *supervised* layer on top of the jump model
> because the jump model identifies the regime in force and does not forecast the next one. That is
> the reason `Data/analyzer.ipynb` finds the causal regime label separating forward volatility but
> not forward return: this repository has implemented the first half of the paper and is measuring
> what the first half alone is worth. **Adding the forecasting layer is the obvious Experiment 2.**
>
> **Three deviations, all deliberate, all recorded here so they are not mistaken for the paper's
> results.** We trade the ETF proxies rather than the indices, from 2010 rather than 1991, so the
> window is a third as long and carries tracking error and expense ratios the paper does not. We use
> a five-year training window rather than eleven, because the ETFs do not have eleven years of
> common history. And we do not drop the downside-deviation features for bonds and gold — the paper
> dropped them on in-sample inspection, which is a per-asset choice made from the data, and adopting
> it would import a decision we have not earned.
>
> **The contradiction worth keeping visible:** the paper selects λ by cross-validated *Sharpe ratio*.
> Under the bar in `AGENTS.md` that is choosing a parameter on the outcome it will be judged by. We
> pick λ on persistence instead — how long a regime spell lasts — and publish the whole sweep. That
> is a stricter standard than the paper's, and it costs us the ability to claim the paper's numbers.
>
> **The safety rule is the interesting piece of construction.** "Three or fewer bullish out of twelve
> means go to cash" is a breadth rule, not an asset rule, and it is why `r_regime_bull_breadth`
> exists in the Refinery. Whether it earns its place is an experiment, not an assumption.
