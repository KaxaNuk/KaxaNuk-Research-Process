# Bibliotheca — the index

> Step 1 of the KN Research Process. Nothing here is a strategy; everything here is a reason a
> strategy is shaped the way it is. [`../OBJECTIVE.md`](../OBJECTIVE.md) states what we believe, and
> this folder is where those beliefs are supposed to come from.
>
> **This file is the index only.** One line per source, grouped by the claim it bears on, each
> linking to its own note. It carries no prose that is not also in a note.

## How this folder works

```
Bibliotheca/
├── BIBLIOGRAPHY.md                  # this file — the index, grouped by claim
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
is in [`../AGENTS.md`](../AGENTS.md), *What a note looks like*.

**PDFs are gitignored.** They sit beside the notes on disk; only the notes are committed — which is
right twice over: no binaries in the tree, and no redistribution of licensed material.
**Do not download papers, books or datasets without asking.** Links go here; files arrive on an
explicit request.

> **Read a source because you have a question, not because it is a good source.** Parts 0 and 5 ship
> with the template: the two books behind the process's own machinery, and the seven papers behind
> its controls — the reading every strategy needs before it has a question of its own. Parts 1 to 4
> are empty on purpose: they fill as *your* strategy raises questions, and nothing enters them
> because it is a good book.

---

## Part 0 — The process itself: where it comes from, and the two books behind it

Investment research did not evolve by replacement; it evolved by addition. The KN Research Process
is a stack of answers to questions the field asked in order, and each of its steps and controls
descends from one of them. The lineage below is the KaxaNuk deck *Intro to Investment Research*
(internal, 2026); it is provenance, not reading notes — none of these rows is a note, and none needs
to be, because the process is what they changed.

| Question the field asked | Who answered it | What it settled | Where it lives in this process |
| --- | --- | --- | --- |
| What do prices carry? | Dow (1889-1902), Bachelier (1900), Nelson (1903) | prices embed collective information; uncertainty is modelled probabilistically | the premise that a rule struck on prices can carry information at all |
| Is there value apart from price? | Graham & Dodd (1934), Damodaran (1994, 2001) | valuation is a model with explicit assumptions, not a number | `BLUEPRINT_N.md`: state the mechanism before the test |
| How is capital allocated across many bets? | Markowitz (1952, 1959) | risk lives in covariance; portfolios over assets | step 4, and the Portfolio Construction library |
| Which risk is rewarded? | Sharpe (1964), Lintner (1965) | beta earns a premium — **performance attribution is born** | step 6's first cut: market exposure against everything else |
| What is skill, measurably? | Jensen (1968) | alpha is the residual after the risk adjustment; measurement precedes belief | graduation criterion 2 asks for **idiosyncratic** alpha |
| Must alpha be proven? | Fama (1970) | alpha is rare; evidence beats intuition | the bar in `AGENTS.md`; *the five ways a backtest lies* |
| How many risks are there? | Ross (1976) | multiple priced factors, even when unnamed | why step 6 uses a multi-factor model, not a single beta |
| Which factors, empirically? | Fama & French (1992, 1993), Carhart (1997) | value, size, momentum; research becomes systematic | KN5FM's factor set; the size and momentum rows in `FINDINGS_N.md` |
| Why do inefficiencies survive? | Kahneman & Tversky (1979), Shiller (1981) | loss aversion, bias, asymmetric preferences | the economic-reason clause: a mechanism, not a pattern |
| Why is being right not enough? | Shleifer & Vishny (1997) | arbitrage is costly and capital-constrained | costs and capacity as gate criterion 4; results accepted net |
| What framework survives both? | Lo (2004) | markets adapt; strategies have life cycles; regimes matter | step 7 exists because alpha decays; one-regime caveats in every findings file |
| What does durable research look like? | Asness (1997), Asness, Moskowitz & Pedersen (2013) | factors persist but cycle; robustness beats intuition | sweeps read as curves; rejected results reported as loudly as promising ones |
| What is actually yours? | Paleologo (2021, 2025) | **alpha is what remains after risk is removed**; construction matters as much as ideas | step 6 and the alpha decomposition — see the book note below |
| Who finds clean signals faster? | Dixon, Halperin & Bilokon (2020) | learning replaces assumptions about the data-generating process | outside this process today; a stage that learns would still have to pass the same gate |
| How should research be designed? | Guo, Wang, Ni & Shum (2022) | research is a system, not a model; humans impose structure, machines explore scale | the process itself: discretionary at design, systematic at scale |

The two books the template ships notes for are the ones whose *method* the process runs:

| Source | What it bears on |
| --- | --- |
| [Paleologo (2021) — *Advanced Portfolio Management*](Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md) | **step 6 and what follows it**: total PnL as idiosyncratic plus factor; selection, sizing and timing by counterfactual books; why a factor model is blind to an absolute rule |
| [Grinold & Kahn (2000) — *Active Portfolio Management*](Books/Grinold_Kahn_2000_Active_Portfolio_Management/INDEX.md) | **step 3's instrument**: the information coefficient, the fundamental law IR ≈ IC × √BR, information decay, and why the IC table screens rather than proves |

## Part 1 — The core idea

<The evidence under the claims in `OBJECTIVE.md` themselves — including the sources that argue
against them. This is the part of the bibliography that should argue with you.>

| Source | What it bears on |
| --- | --- |
| | |

## Part 2 — The signal

<Why the baseline rule should work at all, and what its known failure modes are.>

| Source | What it bears on |
| --- | --- |
| | |

## Part 3 — Sizing and risk

<The weighting scheme, volatility management, drawdown control.>

| Source | What it bears on |
| --- | --- |
| | |

## Part 4 — Exits and construction

<Stops, take-profit rules, holding counts, anything about how the book is built rather than what
goes in it.>

| Source | What it bears on |
| --- | --- |
| | |

## Part 5 — Research integrity: what stops us fooling ourselves

One source per control claimed in [`../AGENTS.md`](../AGENTS.md), *the five ways a backtest lies*.
These are not optional reading: each corresponds to something the repository actually does, or
admits it does not. **Their implications are written for any strategy; rewrite each against yours.**

| Source | The control it stands behind |
| --- | --- |
| [Brown, Goetzmann, Ibbotson & Ross (1992) — *Survivorship Bias in Performance Studies*](Papers/Brown_Goetzmann_Ibbotson_Ross_1992_Survivorship_Bias_In_Performance_Studies.md) | the point-in-time universe retains delisted names |
| [Shumway (1997) — *The Delisting Bias in CRSP Data*](Papers/Shumway_1997_The_Delisting_Bias_In_CRSP_Data.md) | **a gap, not a control.** The final day of a delisted name is unaudited |
| [Sullivan, Timmermann & White (1999) — *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap*](Papers/Sullivan_Timmermann_White_1999_Data_Snooping_Technical_Trading_Rules.md) | any rule that was searched for rather than stated first |
| [Harvey, Liu & Zhu (2016) — *… and the Cross-Section of Expected Returns*](Papers/Harvey_Liu_Zhu_2016_And_The_Cross_Section_Of_Expected_Returns.md) | the IC table is a screening tool, not evidence; publish the trial count |
| [Bailey & López de Prado (2014) — *The Deflated Sharpe Ratio*](Papers/Bailey_LopezDePrado_2014_The_Deflated_Sharpe_Ratio.md) | the best of N variants is the maximum of N draws |
| [Bailey, Borwein, López de Prado & Zhu (2014) — *Pseudo-Mathematics and Financial Charlatanism*](Papers/Bailey_Borwein_LopezDePrado_Zhu_2014_Pseudo_Mathematics_And_Financial_Charlatanism.md) | the argument for step 7 existing at all, and for freezing parameters at graduation |
| [Novy-Marx & Velikov (2016) — *A Taxonomy of Anomalies and Their Trading Costs*](Papers/NovyMarx_Velikov_2016_A_Taxonomy_Of_Anomalies_And_Their_Trading_Costs.md) | results are accepted **net** only |

**One control has no paper behind it: look-ahead.** The point-in-time discipline — decide on
yesterday's close, trade at the next available price, name every `*_current` column for what it is
— is practitioner discipline rather than a literature, and this index says so instead of citing a
weak fit. If you find the paper that earns the row, add it.

---

## Sources cited without a note

Recorded so the trail survives. None has been read into this repository.

- **Paleologo (2025) — *The Elements of Quantitative Investing*.** Named in the lineage deck beside
  the 2021 book. No note, no link recorded.
- **Brinson & Fachler (1985) — *Measuring Non-US Equity Portfolio Performance*, Journal of Portfolio
  Management; Brinson, Hood & Beebower (1986) — *Determinants of Portfolio Performance*, Financial
  Analysts Journal.** The origin of the allocation / selection / interaction decomposition the
  Attribution Analysis library runs under the Brinson-Fachler name. No note, no link recorded.
- The lineage sources in Part 0 that are not otherwise noted. They are provenance; a note is owed
  only when one of them answers a question your strategy raises.
