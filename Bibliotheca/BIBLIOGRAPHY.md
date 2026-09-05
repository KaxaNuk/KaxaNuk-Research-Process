# Bibliotheca — the index

**Step 1 of the KN Research Process.** Nothing here is a strategy; everything here is a reason a
strategy is shaped the way it is. [`../OBJECTIVE.md`](../OBJECTIVE.md) states what we believe, and
this folder is where those beliefs are supposed to come from.

**In plain words:** a literature review with a thesis at the end of it. **It produces** a referenced
hypothesis, in the repo, dated. **It prevents** backtesting a hunch you cannot defend afterwards.

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

**A source listed without a note is a *lead*, not a citation.** It is here because somebody thought
it would answer a question this repository has. Nothing may be claimed on its authority until it has
been read and a note written.

**PDFs are gitignored.** They sit beside the notes on disk; only the notes are committed — which is
right twice over: no binaries in the tree, and no redistribution of licensed material. **Do not
download papers, books or datasets without asking.** Links go here; files arrive on request.

## What a note looks like

Every note opens with the same four fields, so provenance is always in the same place: where it
lives, the citation and when the link was last checked, whether a local copy is held, and the date
it was read into this repository along with what was read — the whole paper, or an abstract.

| Note | Body |
| --- | --- |
| **Paper** | *What it says*, in the authors' terms — then *what it implies for this strategy*, as a blockquote |
| **Book** | one section per idea, each headed by the claim that chapter makes, each with a blockquoted implication; then a distillation table and *what this book does not settle for us* |

Four rules separate a note from a summary:

1. **The implication is a blockquote, always.** It is the only part that is *ours*, and it has to be
   visually separable from what the source said.
2. **A heading states the source's claim, never our verdict.** Our verdict lives in the blockquote,
   where it can change when a result moves; a heading carrying a verdict rots silently.
3. **Record contradictions as contradictions.** When a source says to do the opposite of what we do,
   that stays visible rather than being smoothed into agreement. It is usually the most useful line
   in the note.
4. **Never invent a URL or a page number.** A missing link is recorded as a task, because a gap
   phrased as a task gets closed and one phrased as a fact does not. A wrong citation is worse than
   none.

**A note that does not say what it changes about this strategy is a summary, and summaries are
available elsewhere.**

> **Read a source because you have a question, not because it is a good source.** Part 1 is empty on
> purpose: it fills as *your* idea raises questions. Parts 2 to 5 are seeded with the standard
> reading behind the later steps — leads, none of them read yet.

---

## Part 0 — Where this process comes from

Investment research did not evolve by replacement; it evolved by addition. Each step and each
control of this process is an answer to a question the field asked, in roughly this order. The table
is provenance rather than reading notes: none of these rows is a note, and none needs to be, because
what they changed is the process itself.

| The question | Who answered it | What it settled | Where it lives here |
| --- | --- | --- | --- |
| What do prices carry? | Dow, Bachelier, Nelson (1889–1903) | prices embed collective information; uncertainty is modelled probabilistically | the premise that a rule struck on prices can carry information at all |
| Is there value apart from price? | Graham & Dodd (1934), Damodaran (1994) | valuation is a model with explicit assumptions, not a number | `BLUEPRINT_N.md`: state the mechanism before the test |
| How is capital allocated across many bets? | Markowitz (1952) | risk lives in covariance; portfolios over assets | step 4, and the Portfolio Construction module |
| Which risk is rewarded? | Sharpe (1964), Lintner (1965) | beta earns a premium — **performance attribution is born** | step 6's first cut: market exposure against everything else |
| What is skill, measurably? | Jensen (1968) | alpha is the residual after the risk adjustment; measurement precedes belief | graduation criterion 2 asks for **idiosyncratic** alpha |
| Must alpha be proven? | Fama (1970) | alpha is rare; evidence beats intuition | the bar in `AGENTS.md`, and *the five ways a backtest lies* |
| How many risks are there? | Ross (1976) | multiple priced factors, even when unnamed | why step 6 uses a multi-factor model, not a single beta |
| Which factors, empirically? | Fama & French (1992, 1993), Carhart (1997) | value, size, momentum; research becomes systematic | the factor sets step 6 reads |
| Why do inefficiencies survive? | Kahneman & Tversky (1979), Shiller (1981) | loss aversion, bias, asymmetric preferences | the economic-reason clause: a mechanism, not a pattern |
| Why is being right not enough? | Shleifer & Vishny (1997) | arbitrage is costly and capital-constrained | costs and capacity as a gate criterion; results accepted net |
| What framework survives both? | Lo (2004) | markets adapt; strategies have life cycles; regimes matter | step 7 exists because alpha decays; one-regime caveats in every findings file |
| What does durable research look like? | Asness (1997), Asness, Moskowitz & Pedersen (2013) | factors persist but cycle; robustness beats intuition | sweeps read as curves; rejected results reported as loudly as promising ones |
| What is actually yours? | Paleologo (2021) | **alpha is what remains after risk is removed** | step 6 and the alpha decomposition |
| Who finds clean signals faster? | Dixon, Halperin & Bilokon (2020) | learning replaces assumptions about the data-generating process | outside this process today; a stage that learns still passes the same gate |
| How should research be designed? | Guo, Wang, Ni & Shum (2022) | research is a system, not a model | the process itself: discretionary at design, systematic at scale |

## Part 1 — The core idea

The evidence under the claims in `OBJECTIVE.md` themselves — **including the sources that argue
against them**. This is the part of the bibliography that should argue with you, and it is empty
until your strategy has a question of its own.

| Source | What it bears on |
| --- | --- |
| | |

## Part 2 — Universe and data: what is investable, and what the data does to you

*Sources about the inputs rather than the idea. Add whatever your instrument type demands — an ETF
book owes a reading on premium and discount to net asset value, a crypto book one on exchange
idiosyncrasy, a futures book one on roll.*

| Source | What it bears on |
| --- | --- |
| Brown, Goetzmann, Ibbotson & Ross (1992) — *Survivorship Bias in Performance Studies* | why the seed must retain delisted names. *No note yet.* |
| Shumway (1997) — *The Delisting Bias in CRSP Data* | why the last day of a delisted name is an open gap here. *No note yet.* |

## Part 3 — Portfolio construction and sizing

*How the book is built once the selection is made — step 4. Seeded with the standard reading; none
of it has a note, so none of it may be claimed on yet.*

| Source | What it bears on |
| --- | --- |
| Markowitz (1952) — *Portfolio Selection* | mean-variance optimisation, and the origin of the idea that risk lives in covariance. *No note yet.* |
| DeMiguel, Garlappi & Uppal (2009) — *Optimal Versus Naive Diversification* | **the control every construction variant has to beat.** Equal weighting is not a straw man, and on a narrow universe it is hard to beat out of sample. *No note yet.* |
| Ledoit & Wolf (2004) — *Honey, I Shrunk the Sample Covariance Matrix* | a covariance estimated from daily data over few securities is mostly noise; this is the standard repair. *No note yet.* |
| López de Prado (2016) — *Building Diversified Portfolios that Outperform Out of Sample* | hierarchical risk parity — one of the alternatives the Portfolio Construction module offers. *No note yet.* |
| Moreira & Muir (2017) — *Volatility-Managed Portfolios* | scaling exposure by recent volatility. **The cheap rival to any risk-aware strategy.** *No note yet.* |

## Part 4 — Backtest and attribution

*What a result has to survive, and how the return gets taken apart — steps 5 and 6.*

| Source | What it bears on |
| --- | --- |
| Brinson & Fachler (1985) — *Measuring Non-US Equity Portfolio Performance* | the allocation / selection / interaction split step 6 runs under this name. *No note yet.* |
| Brinson, Hood & Beebower (1986) — *Determinants of Portfolio Performance* | the companion, and the origin of the claim that allocation dominates selection. *No note yet.* |
| Novy-Marx & Velikov (2016) — *A Taxonomy of Anomalies and Their Trading Costs* | why results are accepted net only. *No note yet.* |
| Harvey & Liu (2015) — *Backtesting* | how much to haircut a reported Sharpe for the search that produced it. *No note yet.* |

## Part 5 — Research integrity: what stops us fooling ourselves

One source per control claimed in [`../AGENTS.md`](../AGENTS.md), *the five ways a backtest lies*.
These are not optional reading: each corresponds to something the process actually does, or admits
it does not.

| Source | The control it stands behind |
| --- | --- |
| Brown, Goetzmann, Ibbotson & Ross (1992) | the point-in-time universe retains delisted names. *No note yet.* |
| Shumway (1997) | **a gap, not a control.** The final day of a delisted name is unaudited. *No note yet.* |
| Sullivan, Timmermann & White (1999) — *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap* | any rule that was searched for rather than stated first. *No note yet.* |
| Harvey, Liu & Zhu (2016) — *… and the Cross-Section of Expected Returns* | the information-coefficient table screens, it does not prove; publish the trial count. *No note yet.* |
| Bailey & López de Prado (2014) — *The Deflated Sharpe Ratio* | the best of N variants is the maximum of N draws. *No note yet.* |
| Bailey, Borwein, López de Prado & Zhu (2014) — *Pseudo-Mathematics and Financial Charlatanism* | the argument for step 7 existing at all, and for freezing parameters at graduation. *No note yet.* |
| Novy-Marx & Velikov (2016) | results are accepted **net** only. *No note yet.* |

**One control has no paper behind it: look-ahead.** The point-in-time discipline — decide on
yesterday's information, trade at the next available price, name every `current_*` column for what
it is — is practitioner discipline rather than a literature, and this index says so instead of
citing a weak fit. **The cheapest evidence is your own**: if your signal is fitted, read the same
model causally and smoothed and report the gap. That measurement is worth more here than a citation.
