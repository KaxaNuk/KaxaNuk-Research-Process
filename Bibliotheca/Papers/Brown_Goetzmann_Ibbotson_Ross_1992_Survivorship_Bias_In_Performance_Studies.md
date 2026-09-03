# Brown, Goetzmann, Ibbotson & Ross (1992) — *Survivorship Bias in Performance Studies*

> **Link:** not recorded. Add it here as `[Title](URL)` the next time this source is opened — every
> note is meant to carry one, and a wrong link is worse than none.
>
> **Citation:** Review of Financial Studies 5(4), 553-580. Cited from the journal reference only;
> this entry has not been link-checked.
>
> **Local copy:** none held. `*.pdf` is gitignored, so a downloaded copy sits beside this note and
> only the note is committed.
>
> **Read into this repository:** with the template, 2026-09-03. **This implication is written for
> any strategy.** Re-read the source against yours and rewrite the blockquote; then replace this
> line with the date you did.

## What it says

Conditioning a sample on survival manufactures apparent performance persistence and spurious
abnormal returns even when none exist in the underlying process. The bias is not a small correction
— it can generate the entire result.

## What it implies for this strategy

> The reason `Universe/Investable_Universe.csv` **retains delisted names** and is committed as the
> seed the whole pipeline grows from, and the reason `Universe/universe.ipynb` quantifies how much
> of the universe is dead rather than assuming it is negligible.
>
> This is control 1 of the five in [`../../AGENTS.md`](../../AGENTS.md). Any new universe arrives
> the same way, with its delisted names attached, before it is used for anything. When you rewrite
> this note, record what share of your universe is dead — the number `universe.ipynb` reports — so
> the reader knows how much the control is protecting.
