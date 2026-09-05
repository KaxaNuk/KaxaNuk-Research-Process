"""
Data Curator -- step 3 of 8, block 1 of 3.  The only file in this repository that talks to a data
provider.

In plain words: you describe the data you want -- provider, identifiers, dates and columns -- and
the KaxaNuk Data Curator fetches it, aligns the calendar, handles splits and dividends, and writes
one file per identifier, the same way every run.

Runs first.  Nothing has to exist before it except `Universe/Investable_Universe.csv` and a
provider key in `Config/.env`.  `Universe/universe.ipynb` profiles what this writes.

What is expected here is a short driver, not a framework:

- Read the identifiers from `Universe/Investable_Universe.csv`, column `main_identifier`.  The
  seed is the authority on what exists, so it drives the download.
- Build one Data Curator configuration: the date window, those identifiers, and the output columns
  -- the provider's `m_*` columns plus the `c_*` columns defined in
  `Data/Curator/custom_calculations.py`.  Fix the end date rather than using today, so two people
  running a week apart get comparable files.
- Call the public library once (`pip install kaxanuk.data_curator`).  It loops over the
  identifiers, skips one that fails and says why, and writes `<identifier>.csv` for each.
- Point its output at `Data/Curator/Time_Series/`.  The library's default folder is `Output/`;
  here every stage has one home, and this is the Curator's.

Two groups ride along in the same folder although they are not in the seed: a cash proxy, because
a book that goes to cash has to hold a real priced instrument, and the benchmarks the strategy is
reported against.  The backtest engine prices everything from one directory, so a benchmark filed
anywhere else is a benchmark it cannot price.  Neither enters the cross-section, because
`Data/refinery.py` takes membership from the seed.

Three adjustment families arrive from the provider and each does a different job.  Carry all
three: an unused column costs bytes, a missing one costs a refetch of every identifier.

    unadjusted            recovers the split and dividend ratios; commission is charged on it
    split-adjusted        traded value, which is liquidity in today's share terms
    dividend-and-split    the total-return series a signal and the backtest P&L run on

Two folders beside the time series are drop zones, not outputs: `Benchmarks/` for an index's daily
holdings and returns, `Factors/` for a factor model's returns.  No price provider sells them;
attribution reads them; steps 1 to 5 run without them.

Credentials come from `Config/.env` and are never printed -- not into a log line, a notebook
output or a commit.  An exposed key is rotated, not edited out.

It produces `Data/Curator/Time_Series/<identifier>.csv`, `m_*` plus `c_*`, read by
`Universe/universe.ipynb` and `Data/refinery.py`.

It prevents beautiful results that came from broken inputs -- and a dataset nobody else can
rebuild.
"""
