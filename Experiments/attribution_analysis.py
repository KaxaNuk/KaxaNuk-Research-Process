"""
Attribution analysis -- step 6 of 8, the fourth shared module.  Shapes what the KaxaNuk Attribution
Analysis library needs, and says what is missing before it tries.

In plain words: which part of the return did you actually earn?

Runs inside an experiment notebook, section 5, after the backtest.

What is expected here:

- Say what is present.  The library needs four inputs the pipeline does not produce: an index's
  daily holdings and its daily returns in `Data/Curator/Benchmarks/`, one or more factor-return
  files in `Data/Curator/Factors/`, and the book from step 5.  Check for them first and report the
  gap in a sentence, so a clone with no licence and no index files pays nothing to find out.
- Shape the hand-supplied files into the layout the library auto-detects: benchmark weights and a
  benchmark return series, both horizontal -- securities down, dates across -- with no nulls.
  Getting the orientation wrong does not fail; it makes the loader read the attribution transposed
  and report a plausible number.  That is why the shaping lives here and not in a notebook.
- Name the two output files and the date convention once, so switching to a different index is an
  edit here and no notebook names a file.
- Capture the library's figures.  It shows them and returns nothing, so this module has to catch
  them on the way past and write them to `Attribution/`, then leave the plotting state as it found
  it.

Expect two methodologies and a third pass, all reported.  Brinson-Fachler splits active return
into allocation, selection and interaction -- the lever that moved.  The factor model splits
excess return into compensated factor tilts and idiosyncratic alpha -- what was paid for, on
purpose or by accident.  Then Brinson-Fachler again on the residual, which says whether the
Sharpe survives once the factor turns.  Expect the answer to be partial -- an absolute rule is
close to invisible to a factor model built on relative factors -- and treat that as a finding.
The follow-ups are counterfactual books the engine can already price.  `AGENTS.md` has the
reasoning.

It produces `Attribution/` -- the figures and the two decompositions -- for `FINDINGS_N.md`, and
the answer to graduation criterion 2.

It prevents selling factor beta as if it were alpha, and an attribution read transposed because
nobody checked the table's shape.
"""
