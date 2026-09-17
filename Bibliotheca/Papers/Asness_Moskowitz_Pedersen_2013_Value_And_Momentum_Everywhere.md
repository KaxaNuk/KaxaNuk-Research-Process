---
source: https://doi.org/10.1111/jofi.12021
citation: "Asness, C. S., Moskowitz, T. J., & Pedersen, L. H. (2013). Value and Momentum Everywhere. The Journal of Finance, 68(3), 929-985. DOI 10.1111/jofi.12021. Link last checked 2026-09-10."
local_copy: none
read: "2026-09-10 — published citation and headline result verified against the publisher's record and the abstract. 2026-09-16 — the data section on the stock universe and the portfolio-construction section read from the authors' copy, for the bullets under *What it changes*; not a full read. Verify any number against the source before quoting it."
---

<!-- example: begin -->

# Asness, Moskowitz & Pedersen (2013) — Value and Momentum Everywhere

*The abstract, and the sections on the stock universe and the portfolio construction, with the
citation checked against the publisher's record — not the full paper.*

## Why it is here

Claim 1 of [`OBJECTIVE.md`](../../OBJECTIVE.md) — *a positive twelve-month return, skipping the
most recent month, selects stocks whose following month beats the universe average* — and *what is
not claimed*: not that the parameters are right.

Why twelve-months-skip-one is a specification we **inherit** rather than one we searched for.

## Value and momentum premia appear consistently across eight markets and asset classes

The pair is found in individual stocks in four equity markets — the United States, the United
Kingdom, continental Europe and Japan — and in country equity index futures, government bonds,
currencies and commodity futures. Momentum is measured throughout on the past twelve-month return
skipping the most recent month.

> **For claim 1:** this is the defence recorded in [`OBJECTIVE.md`](../../OBJECTIVE.md) under *what
> is not claimed*. The 12-1 window was not chosen by trying windows on our data and keeping the
> best; it is the field's standing convention, applied here unchanged. A parameter taken from
> outside cannot have been overfitted to a sample it never saw.
>
> This is the cheapest protection against data-snooping available to a new strategy, and it costs
> nothing but the discipline of not tuning. The bar in [`AGENTS.md`](../../AGENTS.md) asks for the
> trial count beside any winner; a parameter that was never searched has a trial count of one.

## The premia share a common factor structure across otherwise unrelated asset classes

Value strategies correlate with other value strategies, and momentum with other momentum, across
markets that share little else. There is common global structure rather than a set of local
curiosities.

> **For claim 1:** the process is asset-class agnostic and so, on this evidence, is the signal. The
> universe here is one CSV whose only required column is `main_identifier`, and this paper is the
> reason a later `liquid-momentum` on ETFs, futures or currencies would be a variant of the same
> idea rather than a different idea wearing its name.

## The stock universe is cut to the largest, most liquid names in each market

The paper limits its stocks to "a very liquid set of securities that could be traded for reasonably
low cost at reasonable trading volume size": the largest names by market capitalisation up to 90%
of each market's total, "typically the largest quintile of securities". It finds the momentum
premium there, and says its results are conservative because the premia "are larger among smaller,
less liquid securities".

> **For claim 1:** this is the nearest published analogue to our claim inside a liquid universe, and
> it points the other way from
> [Lesmond, Schill & Zhou (2004)](Lesmond_Schill_Zhou_2004_Illusory_Nature_Of_Momentum_Profits.md).
> A capitalisation cut in a value-weighted long-short book is not our dollar-volume cut in an
> equal-weighted long-only one, so what is still open under claim 1 stays open and
> `Data/analyzer.ipynb` still owes the measurement — but it is evidence, and `OBJECTIVE.md` should
> weigh it beside the paper that argues against the design.

## What it changes

- **The 12-1 window is inherited, not searched.** It is the field's standing convention, so its
  trial count is one — the defence *what is not claimed* rests on.
- **The signal is asset-class agnostic on this evidence.** A later `liquid-momentum` on ETFs, futures
  or currencies is a variant of this idea, not a different one.
- **Claim 1 has evidence on both sides now.** The paper finds momentum inside a universe already cut
  to the large, liquid end of each market, where Lesmond, Schill & Zhou say the profits are not.
  Neither settles our screen: the analyzer measures it, on our universe, with our cut.
- **The analyzer owes the measurement this paper cannot give.** The paper's momentum is a
  long-short construction — zero-cost, market-neutral within each asset class, value-weighted in
  the sorted stock portfolios — on a universe cut by capitalisation; ours is long-only,
  cash-residual, equal-weighted, and cut on dollar volume. The premium existing in their
  construction is not evidence it survives in ours.
- **Does not settle** our costs or the liquidity style: it is not a costs paper — see
  [Lesmond, Schill & Zhou (2004)](Lesmond_Schill_Zhou_2004_Illusory_Nature_Of_Momentum_Profits.md) —
  and the style is
  [Ibbotson, Chen, Kim & Hu (2013)](Ibbotson_Chen_Kim_Hu_2013_Liquidity_As_An_Investment_Style.md).

<!-- example: end -->
