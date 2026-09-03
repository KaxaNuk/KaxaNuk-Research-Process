"""
The scheduled runner for every graduated book -- step 7 of the KN Research Process.

Empty of logic on purpose: nothing has graduated yet, and this file gets written when something
does.  It is committed as part of the skeleton so the shape of the stage is visible, and so the
contract below is agreed before there is code to argue about.

What it will do, once there is a book to run, is deliberately narrow:

- refresh `Data/Refinery/Time_Series/` and apply each graduated rule to the newest date;
- **re-fit nothing.**  Parameters are frozen at graduation.  A paper-trading run that tunes
  anything is a backtest wearing a costume, and it answers a question nobody asked;
- write that date's target book and append to the running performance record;
- flag divergence from what the backtest led us to expect -- turnover, holdings count, exposure.

Each graduated strategy lives in its own `Paper_Trading_N/paper_trading_N.py`, mirroring the
`Experiment_N` it was promoted from.  This module is the scheduler over them, not the strategy.

See `BITACORA.md` for the gate an experiment passes to get here.
"""
