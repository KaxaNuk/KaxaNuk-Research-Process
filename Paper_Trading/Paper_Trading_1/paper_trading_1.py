"""
The frozen rule for the first strategy to graduate -- a placeholder until one does.

Empty of logic on purpose.  `Paper_Trading_N` mirrors the `Experiment_N` it was promoted from, so
that the lineage of a paper-traded book is never in question, and this directory is the skeleton
showing that convention rather than a strategy already running.

When a strategy graduates, this file holds its selection and weighting rule **copied out of the
experiment notebook and then left alone**.  The duplication is intentional: the notebook is the
record of how the rule was *chosen*, including everything tried and rejected, and it stays free to
be edited by the next piece of research.  This file is the record of what is *being traded*, and a
change to it is a change to a live book, not a change to an experiment.

`../daily_update.py` calls into here; it never re-derives the rule itself.

See `../BITACORA.md` for the gate, and `../../RESULTS.md` for the numbers a candidate is judged on.
"""
