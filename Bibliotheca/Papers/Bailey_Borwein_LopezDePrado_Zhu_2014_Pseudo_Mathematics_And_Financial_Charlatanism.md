# Bailey, Borwein, López de Prado & Zhu (2014) — *Pseudo-Mathematics and Financial Charlatanism*

> **Link:** not recorded. Add it here as `[Title](URL)` the next time this source is opened — every
> note is meant to carry one, and a wrong link is worse than none.
>
> **Citation:** Notices of the American Mathematical Society 61(5), 458-471. Cited from the journal
> reference only; this entry has not been link-checked.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a downloaded copy sits beside this note and
> only the note is committed.
>
> **Read into this repository:** with the template, 2026-09-03. **This implication is written for
> any strategy.** Re-read the source against yours and rewrite the blockquote; then replace this
> line with the date you did.

## What it says

With enough trials, an in-sample optimal strategy can be produced from pure noise — and backtest
overfitting reliably produces *negative* out-of-sample performance rather than merely disappointing
performance.

## What it implies for this strategy

> **The argument for step 7 existing at all.** A backtest is not evidence that a rule works; paper
> trading on unseen data is the first test not contaminated by the search that produced the rule.
>
> It is also the reason parameters freeze at graduation. A paper-trading script that re-fits
> anything re-introduces exactly the search this paper warns about, which is why
> [`../../Paper_Trading/BITACORA.md`](../../Paper_Trading/BITACORA.md) states the no-re-fitting rule
> as a contract rather than a guideline.
