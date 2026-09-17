---
source: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1993.tb04702.x
citation: "Jegadeesh, N., & Titman, S. (1993). Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency. The Journal of Finance, 48(1), 65-91. DOI 10.1111/j.1540-6261.1993.tb04702.x. Link last checked 2026-09-10."
local_copy: none
read: "2026-09-10 — published citation and headline result verified against the publisher's record and the abstract; not a full re-read of the paper. Verify any number against the source before quoting it."
---

<!-- example: begin -->

# Jegadeesh & Titman (1993) — Returns to Buying Winners and Selling Losers

*The abstract only, with the citation checked against the publisher's record — not the full paper.*

## Why it is here

Claim 1 of [`OBJECTIVE.md`](../../OBJECTIVE.md) — *a positive twelve-month return, skipping the
most recent month, selects stocks whose following month beats the universe average*.

The paper momentum comes from, and the reason `r_momentum_12_1` exists at all.

## Buying past winners and selling past losers earns significant positive returns over three-to-twelve-month holding periods

Portfolios formed on returns over the previous three to twelve months, and held for three to twelve
months, generate significantly positive returns over the period the paper studies. The strategies
are formed on nothing but past price: no accounting input, no analyst estimate, no valuation model.

> **For claim 1:** this is its whole basis. It also fixes the shape of the rule rather than only its
> direction: a formation window inside three to twelve months, and a holding period short enough to
> stay inside the same range. Twelve months is the slow end of the formation range, the end that
> trades least. How often the book is re-struck is not stated in `OBJECTIVE.md`; it is one of the
> open design questions in `JOURNAL_1.md`, owed by the fine-tuning pass of the objective and settled
> in `BLUEPRINT_1.md`, and until then the shared portfolio module, still a description, re-strikes
> whenever the eligible set changes.

## The profits are not explained by systematic risk, nor by delayed reaction to common factors

The paper tests the obvious deflations — that the winners are simply riskier, or that the effect is
lead-lag transmission of common factor news — and reports that neither accounts for the returns.

> **For claim 1:** this is why momentum is worth a strategy rather than a footnote, and it is also
> why step 6 is not optional for us. The paper's evidence is that the return is not compensation for
> the systematic risks *it* tested. Our attribution runs against a modern factor set that includes a
> momentum factor — so a book that is *only* momentum should expect attribution to hand most of the
> return to that factor and little to selection. That is the expected outcome, not a disappointment,
> and `BLUEPRINT_1.md` should predict it before it is measured.

## Part of the abnormal return earned in the first year dissipates over the following two years

The returns are not permanent. A portion of what is earned in the twelve months after formation is
given back over the subsequent two years.

> **For claim 1:** holding must be short, and this is the reason. A buy-and-hold reading of the same
> signal would hand back part of what it earned. It is also the first argument against ever letting
> this book become a low-turnover one to save costs: the horizon is a property of the signal, not a
> dial.

## What it changes

- **The rule's shape is fixed, not only its direction:** a formation window inside three to twelve
  months and a holding period inside the same range. Twelve months is the slow end of the formation
  range, the end that trades least; the rebalance frequency is not stated in `OBJECTIVE.md` and is
  an open question in `JOURNAL_1.md`, to be settled in `BLUEPRINT_1.md`.
- **Step 6 is not optional, and its expected answer is written down first:** a book that is only
  momentum should see attribution hand most of the return to the momentum factor and little to
  selection — a prediction for `BLUEPRINT_1.md`, written before it is measured.
- **Holding stays short.** A buy-and-hold reading hands back part of what it earned, so the horizon
  is a property of the signal, not a dial to turn down for costs.
- **Anything claimed from it is about the effect's existence, never its current magnitude** — the
  sample ends decades before ours.
- **Does not settle** trading costs, the single largest threat to this strategy and the subject of
  [Lesmond, Schill & Zhou (2004)](Lesmond_Schill_Zhou_2004_Illusory_Nature_Of_Momentum_Profits.md);
  nor a liquid-only universe, a restriction the paper never applied; nor why to skip the most recent
  month, which comes from
  [Jegadeesh (1990)](Jegadeesh_1990_Predictable_Behavior_Of_Security_Returns.md).

<!-- example: end -->
