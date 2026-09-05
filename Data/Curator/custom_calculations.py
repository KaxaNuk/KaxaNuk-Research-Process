"""
The `c_*` columns -- step 3 of 8, computed by the Data Curator while it downloads.

`c_*` means one security's own history and nothing else.  The Curator works one identifier at a
time, so anything that compares securities against each other belongs one stage later, in
`Data/Refinery/custom_calculations.py`, as an `r_*` column.

What is expected here is one function per column, named exactly as the column:

- Each function's parameters are named after the columns it reads -- a provider column such as the
  dividend-and-split adjusted close, or another `c_*` column.  The Curator resolves the dependency
  order from the signatures, so the order of definition here does not matter.
- Each returns a column of the same length.  Prices arrive as fixed-point decimals; anything
  statistical casts to float once, at the boundary.
- A column is registered by listing it among the output columns `Data/curator.py` requests.
  Nothing else registers it.

The minimum a backtest needs -- and the first two pairs are never removed:

- the cumulative split ratio and the dividend-and-split ratio, recovered from the adjusted and
  unadjusted closes;
- the unadjusted VWAP, on which per-share commission is charged, and the dividend-and-split
  adjusted VWAP, the fill price;
- the one-day total return, because nearly every feature is built on it;
- a liquidity measure -- average daily traded value over about a quarter -- because capacity is a
  question every strategy has to answer.

Widening the schema changes every file's header, so the next run refetches every identifier.  That
is intended, because it is what stops the folder holding a mix of schemas, and it makes this the
wrong home for anything you intend to tune.  Put a model's frozen arithmetic inputs here and the
model itself in the Refinery: a sweep must never cost a download.

It produces the `c_*` columns in every file under `Data/Curator/Time_Series/`.

It prevents a feature computed on a price basis it should not use -- a plausible number and no
error.
"""
