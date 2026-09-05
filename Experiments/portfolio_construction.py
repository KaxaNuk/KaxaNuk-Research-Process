"""
Portfolio construction -- step 4 of 8, the second shared module.  Turns the set of securities a
rule calls eligible into the weights a book holds, and is the seam the KaxaNuk Portfolio
Construction library replaces.

In plain words: how much of what, and how often you change your mind.

Runs inside an experiment notebook, from the rule in section 2, on the matrices the securities
panel built.

What is expected here is one function signature and a few things behind it:

- The signature.  Given the securities eligible today and a returns history that has already been
  cut off before today, return one weight per security, summing to at most 1.0.  Every weighting
  scheme -- equal weight, inverse volatility, a minimum-variance optimiser, hierarchical risk
  parity, a call into the library -- is the same shape, so swapping one for another is one line in
  the rule cell and nothing else in the notebook moves.  That is what makes two experiments
  comparable rather than merely adjacent.
- At most one, not exactly one.  A strategy that can go to cash cannot satisfy the stricter form;
  the residual becomes a real, priced cash position when the weight file is written.
- The constraints every scheme respects, switched off by default: a maximum weight, a minimum
  holding count, a lookback for anything that estimates risk.  Each is a lever a later experiment
  has to earn by beating the book without it.
- The two timing helpers that cannot be forgotten if they live here: lag the eligibility so the
  set used on rebalance date t is the one observed at t-1, and rebalance only on the dates that set
  changes -- a signal that has not moved is not a reason to pay commission.
- Causality by construction.  A weigher never sees a date, only a history already cut off, so it
  cannot reach into the future even by accident.

It produces the `REBALANCE_DATES x securities` target weights the rule cell hands to the
diagnostics and the weight file.

It prevents a good signal in a portfolio nobody could hold -- and a weighting difference that reads
as a signal difference because each notebook invented its own sizing.
"""
