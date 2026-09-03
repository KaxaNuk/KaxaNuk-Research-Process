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

> **Read a source because you have a question, not because it is a good source.** The parts below
> are grouped by the claim each source bears on. Parts 1 to 4 are empty in the template: they fill
> as your strategy raises questions. Part 5 ships full, because every strategy needs those seven
> papers before it has a question of its own.

---

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

---

## Sources cited without a note

<Recorded so the trail survives: anything referenced in a journal or a blueprint that was never read
into a note. Name, what it was cited for, and "no note, no link recorded".>
