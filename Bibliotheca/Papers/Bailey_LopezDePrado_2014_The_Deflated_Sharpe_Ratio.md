# Bailey & López de Prado (2014) — *The Deflated Sharpe Ratio*

> **Link:** not recorded. Add it here as `[Title](URL)` the next time this source is opened — every
> note is meant to carry one, and a wrong link is worse than none.
>
> **Citation:** Journal of Portfolio Management 40(5), 94-107. Cited from the journal reference
> only; this entry has not been link-checked.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a downloaded copy sits beside this note and
> only the note is committed.
>
> **Read into this repository:** with the template, 2026-09-03. **This implication is written for
> any strategy.** Re-read the source against yours and rewrite the blockquote; then replace this
> line with the date you did.

## What it says

Provides a Sharpe ratio corrected for the number of trials attempted, for non-normality, and for
track-record length. The maximum Sharpe across N backtests is a biased estimate of the best
strategy's true Sharpe, and the bias grows with N.

## What it implies for this strategy

> **Directly actionable, and the blocking item on graduation criterion 3.** Every experiment that
> ranks variants and quotes the winner is in exactly the situation this paper describes, and a
> margin of a few hundredths of Sharpe over a control is the size that deflation eats.
>
> Publishing the trial count is the minimum. Computing the deflated figure — with the count, the
> observed skew and kurtosis, and the track-record length — is the proper answer, and no candidate
> graduates without it. See [`../../Paper_Trading/BITACORA.md`](../../Paper_Trading/BITACORA.md).
