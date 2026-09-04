# Bibliotheca — the index

> Step 1 of the KN Research Process. Nothing here is a strategy; everything here is a reason a
> strategy is shaped the way it is. [`../OBJECTIVE.md`](../OBJECTIVE.md) states what we believe, and
> this folder is where those beliefs are supposed to come from.
>
> **This file is the index only.** One line per source, grouped by what it bears on. It carries no
> prose that is not also in a note.

## How this folder works

```
Bibliotheca/
├── BIBLIOGRAPHY.md                  # this file — the index, grouped by what a source bears on
├── Papers/
│   └── Author_Year_Title.md         # one note per paper
└── Books/
    └── Author_Year_Title/
        └── INDEX.md                 # one note per book, with per-chapter sections
```

**One `.md` per source, named `Author_Year_Title`.** A paper is a single file under `Papers/`; a
book gets a folder under `Books/` with an `INDEX.md`, because a book is read a chapter at a time and
each chapter earns its own section. The note convention — the four-field front matter, the
blockquoted implication, the rule that a heading states the source's claim and never our verdict —
is in [`../AGENTS.md`](../AGENTS.md).

**A source listed without a note is a *lead*, not a citation.** It is here because somebody thought
it would answer a question this repository has. Nothing may be claimed on its authority until it has
been read and a note written.

**PDFs are gitignored.** They sit beside the notes on disk; only the notes are committed — which is
right twice over: no binaries in the tree, and no redistribution of licensed material. **Do not
download papers, books or datasets without asking.** Links go here; files arrive on request.

> **Read a source because you have a question, not because it is a good source.** Parts 0 and 5 ship
> with the process itself and every strategy needs them. Parts 1 to 4 are the *example* strategy's
> reading, and are what you replace: they show the shape of a well-stocked bibliography for one idea,
> not the reading list for yours.

---

## Part 0 — The process itself: where it comes from, and the two books behind it

Investment research did not evolve by replacement; it evolved by addition. The KN Research Process is
a stack of answers to questions the field asked in order, and each of its steps and controls descends
from one of them. The lineage below is the KaxaNuk deck *Intro to Investment Research* (internal,
2026); it is provenance, not reading notes — none of these rows is a note, and none needs to be,
because the process is what they changed.

| Question the field asked | Who answered it | What it settled | Where it lives in this process |
| --- | --- | --- | --- |
| What do prices carry? | Dow (1889-1902), Bachelier (1900), Nelson (1903) | prices embed collective information; uncertainty is modelled probabilistically | the premise that a rule struck on prices can carry information at all |
| Is there value apart from price? | Graham & Dodd (1934), Damodaran (1994, 2001) | valuation is a model with explicit assumptions, not a number | `BLUEPRINT_N.md`: state the mechanism before the test |
| How is capital allocated across many bets? | Markowitz (1952, 1959) | risk lives in covariance; portfolios over assets | step 4, and the Portfolio Construction library |
| Which risk is rewarded? | Sharpe (1964), Lintner (1965) | beta earns a premium — **performance attribution is born** | step 6's first cut: market exposure against everything else |
| What is skill, measurably? | Jensen (1968) | alpha is the residual after the risk adjustment; measurement precedes belief | graduation criterion 2 asks for **idiosyncratic** alpha |
| Must alpha be proven? | Fama (1970) | alpha is rare; evidence beats intuition | the bar in `AGENTS.md`; *the five ways a backtest lies* |
| How many risks are there? | Ross (1976) | multiple priced factors, even when unnamed | why step 6 uses a multi-factor model, not a single beta |
| Which factors, empirically? | Fama & French (1992, 1993), Carhart (1997) | value, size, momentum; research becomes systematic | KN5FM's factor set |
| Why do inefficiencies survive? | Kahneman & Tversky (1979), Shiller (1981) | loss aversion, bias, asymmetric preferences | the economic-reason clause: a mechanism, not a pattern |
| Why is being right not enough? | Shleifer & Vishny (1997) | arbitrage is costly and capital-constrained | costs and capacity as gate criterion 4; results accepted net |
| What framework survives both? | Lo (2004) | markets adapt; strategies have life cycles; **regimes matter** | step 7 exists because alpha decays — and the example strategy is this row, made operational |
| What does durable research look like? | Asness (1997), Asness, Moskowitz & Pedersen (2013) | factors persist but cycle; robustness beats intuition | sweeps read as curves; rejected results reported as loudly as promising ones |
| What is actually yours? | Paleologo (2021, 2025) | **alpha is what remains after risk is removed** | step 6 and the alpha decomposition |
| Who finds clean signals faster? | Dixon, Halperin & Bilokon (2020) | learning replaces assumptions about the data-generating process | outside this process today; a stage that learns still passes the same gate |
| How should research be designed? | Guo, Wang, Ni & Shum (2022) | research is a system, not a model | the process itself: discretionary at design, systematic at scale |

The two books the template ships notes for are the ones whose *method* the process runs:

| Source | What it bears on |
| --- | --- |
| [Paleologo (2021) — *Advanced Portfolio Management*](Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md) | **step 6 and what follows it**: total PnL as idiosyncratic plus factor; selection, sizing and timing by counterfactual books; why a factor model is blind to an absolute rule |
| [Grinold & Kahn (2000) — *Active Portfolio Management*](Books/Grinold_Kahn_2000_Active_Portfolio_Management/INDEX.md) | **step 3's instrument**: the information coefficient, the fundamental law IR ≈ IC × √BR, information decay, and why the IC table screens rather than proves |

---

## Part 1 — The core idea: market regimes

*What the example strategy claims, and the sources that argue with it.* Replace this whole part with
the evidence under **your** idea — including whatever argues against it.

| Source | What it bears on |
| --- | --- |
| [Shu, Yu & Mulvey (2024) — *Dynamic Asset Allocation with Asset-Specific Regime Forecasts*](Papers/Shu_Yu_Mulvey_2024_Dynamic_Asset_Allocation_With_Asset_Specific_Regime_Forecasts.md) | **the paper the example implements**: the twelve-asset universe, the eight features, and why a forecasting layer sits on top of the jump model |
| [Shu, Yu & Mulvey (2024) — *Downside Risk Reduction Using Regime-Switching Signals*](Papers/Shu_Yu_Mulvey_2024_Downside_Risk_Reduction_Using_Regime_Switching_Signals.md) | **the finding this repository reproduced**: the signal cuts drawdown and volatility, and barely moves return. The authors call regime identification *interpretative rather than predictive* |
| Nystrup, Lindström & Madsen (2020) — *Learning hidden Markov models with persistent states by penalizing jumps*, Expert Systems with Applications 150, 113307 | **where the algorithm in `Data/Refinery/jump_model.py` comes from**: the jump penalty as the fix for hidden Markov models that switch too fast. *No note yet — read this before changing the model.* |
| Bemporad, Breschi, Piga & Boyd (2018) — *Fitting jump models*, Automatica | the original jump-model formulation, outside finance. *No note yet.* |
| Hamilton (1989) — *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*, Econometrica 57(2), 357-384 | the regime-switching model everything here is measured against, and the thing the jump penalty was invented to beat. *No note yet.* |
| Ang & Bekaert (2002) — *International Asset Allocation With Regime Shifts*, Review of Financial Studies | whether regimes are worth acting on across asset classes rather than within one. *No note yet — this is the closest thing to a direct challenge to the example's premise.* |
| Moskowitz, Ooi & Pedersen (2012) — *Time Series Momentum*, Journal of Financial Economics 104(2) | **the competing explanation.** A regime filter is a cousin of time-series momentum; if the two are the same trade, the regime model is an expensive way to buy it. *No note yet.* |

## Part 2 — Universe and data: what is investable, and what the data does to you

*Sources about the inputs rather than the idea. The survivorship and delisting notes live in Part 5,
because they are integrity controls first.*

| Source | What it bears on |
| --- | --- |
| [Brown, Goetzmann, Ibbotson & Ross (1992)](Papers/Brown_Goetzmann_Ibbotson_Ross_1992_Survivorship_Bias_In_Performance_Studies.md) | why `Universe/Investable_Universe.csv` must retain delisted names — see Part 5 |
| [Shumway (1997)](Papers/Shumway_1997_The_Delisting_Bias_In_CRSP_Data.md) | why the last day of a delisted name is an open gap here — see Part 5 |
| Petajisto (2017) — *Inefficiencies in the Pricing of Exchange-Traded Funds*, Financial Analysts Journal 73(1) | **the example trades ETFs, not indices.** Premiums and discounts to net asset value are a cost the backtest does not model. *No note yet.* |
| Ben-David, Franzoni & Moussawi (2017) — *Exchange-Traded Funds*, Annual Review of Financial Economics | what an ETF is as an instrument, and where its behaviour departs from the index it tracks. *No note yet.* |

## Part 3 — Portfolio construction and sizing

*How the book is built once the selection is made. Empty of notes because the example has not
reached step 4 — which is exactly what this part being empty is supposed to tell you.*

| Source | What it bears on |
| --- | --- |
| Markowitz (1952) — *Portfolio Selection*, Journal of Finance 7(1), 77-91 | the mean-variance optimisation the source paper feeds its regime forecasts into. *No note yet.* |
| DeMiguel, Garlappi & Uppal (2009) — *Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?*, Review of Financial Studies 22(5) | **the control every construction variant has to beat.** Equal weighting is not a straw man. *No note yet.* |
| Ledoit & Wolf (2004) — *Honey, I Shrunk the Sample Covariance Matrix*, Journal of Portfolio Management 30(4) | a twelve-asset covariance estimated on daily data is noisy; this is the standard repair. *No note yet.* |
| López de Prado (2016) — *Building Diversified Portfolios that Outperform Out of Sample*, Journal of Portfolio Management 42(4) | hierarchical risk parity — the alternative the Portfolio Construction library will offer. *No note yet.* |
| Moreira & Muir (2017) — *Volatility-Managed Portfolios*, Journal of Finance 72(4) | **the nearest rival to the example's whole thesis**: scaling exposure by recent volatility, with no regime model at all. If this does the same job more simply, the regime model has to justify itself. *No note yet.* |

## Part 4 — Backtest and attribution

*What a result has to survive, and how the return gets taken apart.*

| Source | What it bears on |
| --- | --- |
| [Novy-Marx & Velikov (2016)](Papers/NovyMarx_Velikov_2016_A_Taxonomy_Of_Anomalies_And_Their_Trading_Costs.md) | results are accepted net only — see Part 5 |
| Brinson & Fachler (1985) — *Measuring Non-US Equity Portfolio Performance*, Journal of Portfolio Management | the allocation / selection / interaction split the Attribution Analysis library runs under this name. *No note yet.* |
| Brinson, Hood & Beebower (1986) — *Determinants of Portfolio Performance*, Financial Analysts Journal 42(4) | the companion, and the origin of the claim that allocation dominates selection — which is precisely what the example strategy is a bet on. *No note yet.* |
| Harvey & Liu (2015) — *Backtesting*, Journal of Portfolio Management 42(1) | how much to haircut a reported Sharpe for the search that produced it. *No note yet.* |

## Part 5 — Research integrity: what stops us fooling ourselves

One source per control claimed in [`../AGENTS.md`](../AGENTS.md), *the five ways a backtest lies*.
These are not optional reading: each corresponds to something the repository actually does, or admits
it does not. **Their implications are written for any strategy; rewrite each against yours.**

| Source | The control it stands behind |
| --- | --- |
| [Brown, Goetzmann, Ibbotson & Ross (1992) — *Survivorship Bias in Performance Studies*](Papers/Brown_Goetzmann_Ibbotson_Ross_1992_Survivorship_Bias_In_Performance_Studies.md) | the point-in-time universe retains delisted names |
| [Shumway (1997) — *The Delisting Bias in CRSP Data*](Papers/Shumway_1997_The_Delisting_Bias_In_CRSP_Data.md) | **a gap, not a control.** The final day of a delisted name is unaudited |
| [Sullivan, Timmermann & White (1999) — *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap*](Papers/Sullivan_Timmermann_White_1999_Data_Snooping_Technical_Trading_Rules.md) | any rule that was searched for rather than stated first |
| [Harvey, Liu & Zhu (2016) — *… and the Cross-Section of Expected Returns*](Papers/Harvey_Liu_Zhu_2016_And_The_Cross_Section_Of_Expected_Returns.md) | the IC table is a screening tool, not evidence; publish the trial count |
| [Bailey & López de Prado (2014) — *The Deflated Sharpe Ratio*](Papers/Bailey_LopezDePrado_2014_The_Deflated_Sharpe_Ratio.md) | the best of N variants is the maximum of N draws |
| [Bailey, Borwein, López de Prado & Zhu (2014) — *Pseudo-Mathematics and Financial Charlatanism*](Papers/Bailey_Borwein_LopezDePrado_Zhu_2014_Pseudo_Mathematics_And_Financial_Charlatanism.md) | the argument for step 7 existing at all, and for freezing parameters at graduation |
| [Novy-Marx & Velikov (2016) — *A Taxonomy of Anomalies and Their Trading Costs*](Papers/NovyMarx_Velikov_2016_A_Taxonomy_Of_Anomalies_And_Their_Trading_Costs.md) | results are accepted **net** only |

**One control had no paper behind it: look-ahead.** The point-in-time discipline — decide on
yesterday's information, trade at the next available price, name every `*_current` column for what it
is — was practitioner discipline rather than a literature, and this index used to say so instead of
citing a weak fit. **The example strategy supplied the missing evidence itself**: `Data/analyzer.ipynb`
section 5 measures what one line of look-ahead is worth on this data, by reading the same fitted model
two ways. That measurement, not a citation, is the control's justification here. If you find the paper
that earns the row, add it anyway.

---

## Sources cited without a note

Recorded so the trail survives. None has been read into this repository.

- **Paleologo (2025) — *The Elements of Quantitative Investing*.** Named in the lineage deck beside
  the 2021 book. No note, no link recorded.
- **The reference implementation of the statistical jump model**, published by the first author of
  the two Shu papers: [`Yizhan-Oliver-Shu/jump-models`](https://github.com/Yizhan-Oliver-Shu/jump-models).
  Not a source and not a dependency — `Data/Refinery/jump_model.py` is written from the papers'
  description so the algorithm is readable in one file. Worth checking against when the model is
  changed. Link last checked 2026-09-03.
- The lineage sources in Part 0 that are not otherwise noted. They are provenance; a note is owed
  only when one of them answers a question your strategy raises.
