"""
Backtest engine -- step 5 of 8, the third shared module.  The one path from a book of weights to a
performance number, through the KaxaNuk Backtest Engine.

In plain words: the simulation, run by the engine, with costs and without peeking ahead.

Runs inside an experiment notebook, section 4, after the book has been written to `Portfolio/`.

What is expected here:

- Write the weight file the engine reads: `Portfolio/portfolio_weights.csv`, wide, keyed by the
  identifier the market-data files are named by, dates across the columns, every column summing to
  exactly 1.0.  The engine has no cash row, so the uninvested residual becomes a weight in the cash
  proxy -- going to cash pays commission and earns the bill yield, as it does in life.  A security
  that changed identifier mid-history occupies two rows, each non-zero only while that listing was
  live.
- Run the licensed engine and read its results back: the daily series it marks, and its summary
  statistics.  Import it inside a guard -- it installs from a licensed index, not PyPI -- and report
  and skip when it is absent, so a clone without a licence still produces everything except the
  numbers.
- Name the benchmarks a strategy is reported against, in one place, and clip the window to the
  shortest of them up front rather than discovering it as an error.
- Align every variant of an experiment onto one common window before ranking them.  A variant that
  starts a year later is not comparable on its own dates.

There is deliberately no second, lighter simulator here or anywhere.  One that disagrees with the
engine lets the reader pick the number they prefer, and every figure quoted in `RESULTS.md` comes
through this module.

It produces `Backtest/` -- the engine's workbook and the series drawn from it -- for `FINDINGS_N.md`
to record.

It prevents paper returns that real trading would have erased, and a difference in cost model or
window showing up as strategy skill.
"""
