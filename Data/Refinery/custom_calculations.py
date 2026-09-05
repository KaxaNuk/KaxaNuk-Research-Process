"""
The `r_*` columns -- step 3 of 8, computed by the Data Refinery over the whole cross-section.

Two kinds of column live here, and only here:

1.  Anything that compares securities against each other on a date -- a rank, a breadth reading, a
    share of the cross-section.  No per-security calculation can express it.
2.  Anything with a fitted parameter, even when it is per-security.  A model has settings an
    experiment will sweep, and widening the Curator's schema costs a refetch of every identifier.
    A sweep must never cost a download, so the model's frozen inputs stay in the Curator and the
    model itself lives here.

What is expected here is one function per column, named exactly as the column, resolved by
parameter name the same way the Curator resolves its own.  Every parameter is a column of the
panel -- the date, `main_identifier`, any `c_*` or `r_*` column, any `current_*` column -- and a
function may group by any of them.  The column is registered by listing it in this module's output
tuple; nothing else registers it.

One requirement this module exists to enforce: causality.  Every cross-sectional column on date t
uses only the cross-section as of t, and every rolling window looks strictly backward.  A rank
taken over the pooled sample, or a mean over the whole history, would leak the future distribution
into every row and would not raise a single error doing it.

Rank convention: every `*_rank` column is a per-date percentile, ascending, so 1.0 is the highest
raw value in that day's cross-section.  A percentile over n values averages to (n + 1) / 2n, not to
0.5 -- 0.542 on 12 securities, 0.5006 on 800.  A check written against 0.5 fails on every date of
a narrow universe and passes on a wide one, which is the worst possible failure mode; check against
the identity.

The minimum that ships in a filled-in repository: a per-date liquidity rank, the universe size on
each date (the denominator behind every rank), and one worked example of per-date normalisation.
A column that reads a `current_*` column is marked as such, so the refinery can skip it before the
security master exists.

It produces the `r_*` columns in every file under `Data/Refinery/Time_Series/`.

It prevents a signal that knew the future distribution, and a rank that was silently pooled.
"""
