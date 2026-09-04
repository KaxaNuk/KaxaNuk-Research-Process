# Paleologo (2021) — *Advanced Portfolio Management: A Quant's Guide for Fundamental Investors*

> **Link:** [Wiley catalogue entry](https://www.wiley.com/en-us/Advanced+Portfolio+Management%3A+A+Quant%27s+Guide+for+Fundamental+Investors-p-9781119789796)
>
> **Citation:** Giuseppe A. Paleologo. John Wiley & Sons, 2021. ISBN 9781119789796.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a copy sits beside this note and only the
> note is committed.
>
> **Read into this repository:** with the template, 2026-09-03. **Every implication below is written
> for any strategy built on this process.** Re-read the chapters against yours and rewrite the
> blockquotes; then replace this line with the date you did.
>
> One section per chapter idea. Every section ends with what it means for a strategy built on this
> process, as a blockquote. Where the book contradicts something a strategy does, record that as a
> contradiction rather than smoothing it over.

The book is written for fundamental equity PMs who need the quant apparatus — risk models, sizing,
attribution — without becoming quants. That framing is why it is the one book the template ships:
it is the argument for why each machine part of the process exists, and **the source of the method
behind step 6 and the alpha decomposition that follows it.** Every paper in Part 5 argues about a
control; this book supplies the procedure for deciding whether a signal is doing anything at all.

---

## 1. The PnL of a strategy is the sum of an idiosyncratic series and a factor series

*(section 8.1.1, building on equation 7.1)*

Total performance over an interval is the sum, day by day, of idiosyncratic PnL and factor PnL —
and the factor PnL splits further into the PnL of the individual factors, which can be grouped into
country, industry and style:

```
total PnL(T) = Σ_{t=1..T} [ idio PnL(t) + factor PnL(t) ]
factor PnL(t) = factor PnL_1(t) + factor PnL_2(t) + …
```

> **What this implies for a strategy built on this process.** This is the contract of step 6. A
> book that beats its benchmark has been observed, not understood, until its return is split this
> way — which is why `AGENTS.md` makes attribution a step and not a nice-to-have, and why graduation
> criterion 2 asks for **idiosyncratic alpha**, not for alpha. The KN5FM output of the Attribution
> Analysis library is exactly this decomposition, factor by factor; Brinson-Fachler is the same idea
> over sectors. Record both in `FINDINGS_N.md`, and expect the honest answer to be *half factor,
> half idiosyncratic* rather than a clean pass.

## 2. Decompose the idiosyncratic part into selection, sizing and timing — by counterfactual books

*(sections 8.1–8.2, takeaways section 8.6)*

Once the factor part is known, split the idiosyncratic part three ways: **selection** (being right
about which names), **sizing** (the big positions being the good ones), **timing** (carrying risk
when views are better than average). The mechanism is counterfactual portfolios, not a formula:
to measure sizing, rewrite history with every position equalised within each date, side and gross
unchanged, and compare the Sharpe with the real book. Drop economically insignificant positions
first, or the analysis is dominated by slivers nobody was betting on.

> **What this implies for a strategy built on this process.** Every counterfactual is a weight file,
> and `Experiments/backtest_engine.py` prices weight files — so this decomposition costs one engine pass per
> counterfactual and no new data. Equal-weight the real book for sizing; draw random names from the
> eligible pool at the same sizes for selection; shift the entry dates for timing. The procedure,
> with the weight-file recipes, is the `alpha-decomposition` skill in the KaxaNuk APM package.
> **This is the test that says whether the signal is the strategy or a passenger in it.**

## 3. Momentum is relative; trend-following is absolute

*(section 5.2.3)*

**Momentum** ranks a stock against its peers and goes long the winners, short the losers — roughly
cross-sectional, roughly dollar-neutral. **Trend-following** holds whatever is going up, sized by
how much, with no reference to anyone else. The same six names produce a long-everything trend
portfolio and a long-two, short-two momentum portfolio.

> **What this implies for a strategy built on this process.** A factor model built on *relative*
> factors is close to invisible to an *absolute* rule — a moving-average cross, a breakout, a
> drawdown gate. So a book can beat every benchmark while KN5FM assigns ~0% to the factor its thesis
> is named after. **Treat that as the model's blindness, not the signal's weakness**, name the pillar
> correctly in `OBJECTIVE.md` (trend, not momentum, if that is what it is), and run the
> exclusion-filter counterfactual: the same book with the signal switched off.

## 4. Alpha estimates are far noisier than beta estimates

*(section 3.3)*

Regressing a stock's returns on the market gives a beta with a tight confidence interval and an
alpha whose interval is wider than the estimate itself. Alphas move a lot year to year; betas do
not.

> **What this implies for a strategy built on this process.** A headline "alpha versus SPY" deserves
> an error bar, and a single-window alpha is not a stable property of a strategy. What *is* precisely
> estimated is the exposure — beta, size — which is usually the part attribution says is doing the
> work. Report alpha with its interval or stop short of calling it stable.

## 5. Size positions by risk-adjusted alpha

*(sections 6.3–6.5, takeaways section 6.8)*

Form a view of expected idiosyncratic return per name, put every view on one horizon, neutralise
against factor loadings, then convert to sizes by a proportional rule (position proportional to
standardised alpha) or a shrunk mean-variance rule. The simplest proportional rule is often
preferable in practice.

> **What this implies for a strategy built on this process.** Most simple strategies size by
> something else — liquidity, equal weight, a rank. Under the book's framework that sizing carries
> no information about expected return; it is a constraint promoted to a weighting scheme. That can
> be a perfectly good design choice, but **say so in `OBJECTIVE.md` as a contradiction**, and measure
> what the sizing actually contributes with the counterfactual in section 2. This is where the
> Portfolio Construction library will land when it arrives.

## 6. Volatility targeting is the cheap drawdown lever

*(section 6.6, takeaway section 6.8 #6)*

Scale gross exposure over time so that predicted idiosyncratic dollar volatility hits a constant
target. The book states plainly that this improves risk-adjusted performance.

> **What this implies for a strategy built on this process.** Cheaper than per-name stops, because it
> re-sizes rather than liquidating and re-entering, and the same recommendation the drawdown
> literature reaches from the other direction. Worth testing before any stop rule is.

## 7. Stop-losses cost forgone profit, not commission

*(chapter 9, takeaways section 9.4)*

Stops are necessary — a put against the option-like payoff a PM holds — but their real cost is
performance given up, not transaction costs, and single- versus two-threshold rules differ little.

> **What this implies for a strategy built on this process.** The threshold is the whole decision.
> A stop set too tight turns a trending position into a whipsaw and makes drawdown *worse*; pick the
> threshold from a trade-off curve, never from a sweep's best cell — which is clause 2 of the bar in
> `AGENTS.md`.

## 8. Match position building to the alpha's horizon

*(section 8.3, takeaway section 8.6 #8)*

Build positions consistently with how long the alpha is expected to last; VWAP is a good heuristic;
most readers' participation rate is higher than it ought to be.

> **What this implies for a strategy built on this process.** The engine fills at VWAP and charges
> commission on the unadjusted VWAP, which is the recommended heuristic. What it does not model is
> participation — capacity is unmodelled everywhere in this process, and `AGENTS.md` says so under
> known gaps. A capacity check against ADTV is the first thing to add when a book grows.

## 9. Diversify as much as you can — but not more than that

*(section 8.2.2, takeaway section 8.6 #9)*

Diversification improves the Sharpe of a book with genuine skill, but the marginal benefit decays,
and past some point extra names dilute the edge without materially reducing risk.

> **What this implies for a strategy built on this process.** The holding count is an empirical
> question with a theoretical shape to check against — Sharpe against N — which makes it one of the
> rare sweeps that is defensible under the bar: there is a curve to read, not a cell to pick.

---

## Distilled into this process's language

| Book idea | Where it lands in the process |
| --- | --- |
| **Total PnL = idio + factor** | step 6's contract; graduation criterion 2 asks for the idio part |
| **Selection / sizing / timing by counterfactual books** | the `alpha-decomposition` skill; one engine pass per counterfactual |
| Momentum (relative) is not trend-following (absolute) | expect a factor model to be blind to a threshold signal; run the exclusion filter |
| Alpha estimates are noisy, betas are not | report alpha with an interval |
| Size by risk-adjusted alpha | if you size otherwise, record the contradiction and measure the sizing counterfactual |
| Volatility targeting improves risk-adjusted return | test before any stop |
| Stop-loss cost is forgone profit | thresholds from a curve, never a cell |
| Match execution to the alpha's horizon | capacity is the unmodelled gap |
| Diversify, not past dilution | Sharpe against holding count is a defensible sweep |

## What this book does not settle for us

- It assumes a **factor risk model is available** and mostly discusses what to do with one. This
  stack has KN5FM through the attribution stage but not inside portfolio construction, so the
  hedging and optimisation chapters (7, 11) are unreachable until the Portfolio Construction library
  lands.
- It is written for **long/short, factor-neutral** books. A long-only strategy that deliberately
  carries beta cannot take its neutralisation advice without becoming a different strategy.
- It says nothing about **universe construction or survivorship** (step 2), nor about **multiple
  testing and Sharpe deflation** — for both, see Part 5 of [`../../BIBLIOGRAPHY.md`](../../BIBLIOGRAPHY.md).
