"""
Securities panel -- steps 4 to 6 of 8, the first of four modules shared by every experiment.  It
turns the refined files into the matrices a rule is written against.

In plain words: one loader, so every experiment measures the same universe the same way.  A
notebook that reads the panel its own way has broken the comparison before the rule is written.

Runs inside an experiment notebook, after `Data/refinery.py` has written
`Data/Refinery/Time_Series/`.

What is expected here:

- Read every refined file for a security in `Universe/Investable_Universe.csv`, and only those --
  the cash proxy and the benchmarks sit in the Curator folder for the engine, not for the
  cross-section.
- Key positions by security, not by listing.  A point-in-time universe contains renamed securities
  -- two identifiers sharing one ISIN, each carrying part of the history -- and left alone they
  become two positions and a double-counted company at the changeover.  Stitch the legs; where two
  overlap on a date, the one still reporting later is the surviving listing.
- Pivot the long panel into one wide `dates x securities` matrix per column the notebook asks for:
  the signal, the mark price, the fill price, and whatever else the rule reads.  A matrix per input
  is what lets the whole rule be a handful of whole-matrix statements instead of a loop over files.
- Name no strategy column.  The columns to load arrive as arguments from the notebook's setup cell.
  A signal declared here becomes every later experiment's default without anyone deciding it.
- Fail readably: a column the files do not carry is named in the error, not discovered inside a
  read.

It produces the matrices section 1 of every experiment notebook starts from, and nothing on disk.

It prevents two experiments that appear to disagree about a strategy when they only disagree
about how the panel was loaded.
"""
