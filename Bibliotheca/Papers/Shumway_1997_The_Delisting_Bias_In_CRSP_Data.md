# Shumway (1997) — *The Delisting Bias in CRSP Data*

> **Link:** not recorded. Add it here as `[Title](URL)` the next time this source is opened — every
> note is meant to carry one, and a wrong link is worse than none.
>
> **Citation:** Journal of Finance 52(1), 327-340. Cited from the journal reference only; this entry
> has not been link-checked.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a downloaded copy sits beside this note and
> only the note is committed.
>
> **Read into this repository:** with the template, 2026-09-03. **This implication is written for
> any strategy.** Re-read the source against yours and rewrite the blockquote; then replace this
> line with the date you did.

## What it says

Delisting returns are frequently missing from standard databases, and the missing ones are
disproportionately bad — performance-related delistings. Ignoring them biases measured returns
upward.

## What it implies for this strategy

> **Retaining a delisted ticker is not sufficient; the final return has to be handled too.** The
> curator takes whatever the provider supplies at the end of a delisted name's history, and the last
> day has never been audited on this stack.
>
> That is a live gap, not a solved control, and it compounds with a stated look-ahead: delisting
> exits use one day of hindsight, since a position is sold on the last day it still has a fill price
> and that is knowable only the day after. `Universe/Data_Issues.csv` is where the audit belongs,
> and it is listed among the known gaps in [`../../AGENTS.md`](../../AGENTS.md). If your strategy
> holds small or distressed names, this is the first control to close.
