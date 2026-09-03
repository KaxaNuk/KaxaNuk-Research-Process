# Sullivan, Timmermann & White (1999) — *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap*

> **Link:** not recorded. Add it here as `[Title](URL)` the next time this source is opened — every
> note is meant to carry one, and a wrong link is worse than none.
>
> **Citation:** Journal of Finance 54(5), 1647-1691. Cited from the journal reference only; this
> entry has not been link-checked.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a downloaded copy sits beside this note and
> only the note is committed.
>
> **Read into this repository:** with the template, 2026-09-03. **This implication is written for
> any strategy.** Re-read the source against yours and rewrite the blockquote; then replace this
> line with the date you did.

## What it says

Evaluates a large universe of technical trading rules — moving-average crossovers explicitly among
them — against the full set actually searched, using White's Reality Check. Rules that look strong
in isolation lose much of their significance once the size of the search is accounted for.

## What it implies for this strategy

> **The most uncomfortable entry in the folder for any rule that could have been searched for.** If
> your signal is a threshold, a window or a crossover, it is in the class this paper deflates.
>
> Two defences are available, and both are worth more if written down *before* the test: that the
> parameters were taken as given — the most widely known values, never tuned — and that the rule is
> used as a *filter* on a book built by something else rather than as the source of return. State in
> `BLUEPRINT_1.md` which of the two you are relying on. The first is verifiable from the
> repository's history; the second has to be tested, by running the same book with the signal
> switched off.
