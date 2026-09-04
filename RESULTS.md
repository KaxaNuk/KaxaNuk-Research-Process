# Results

> **Executive summary of everything this repository has measured.**
>
> Experiment sections are compiled from the `FINDINGS_N.md` files and cite each one. **When a number
> changes, change it in `FINDINGS_N.md` first**, then update this file — a summary that leads its
> sources is how two numbers for the same book start to circulate.
>
> The idea being tested is in [`OBJECTIVE.md`](OBJECTIVE.md). The bar a result has to clear before
> anyone believes it is in [`AGENTS.md`](AGENTS.md).
>
> Last regenerated end to end on **2026-09-03**, from a data pull made the same day.

## The project in three sentences

**No book has been priced.** Steps 1 to 4 are complete — there is a real book, written and passing
every invariant — but steps 5 and 6 need licensed engines that are not installed here, so there is no
CAGR, no Sharpe and no attribution in this file, and saying so plainly is the point of having it.

**Two things have nevertheless been settled, and both were surprises.** The regime signal is a *risk*
signal and not a return signal — the good regime has lower forward volatility on 11 of 12 assets and
higher forward return on only 5, at every model setting tested. And the benchmark book **does not go
defensive**: equal weight over a shrinking eligible set concentrates rather than de-risks, which
falsified the blueprint's fourth prediction before the engine was ever needed.

**Look-ahead was measured at 44 annualised points**, by reading one fitted model two ways — the size
of the mistake this whole process exists to prevent.

---

## Before any experiment: what the data already says

Findings from step 3, `Data/analyzer.ipynb`, over the twelve-asset ETF universe. **They live here
rather than only in the notebook because notebook outputs are stripped before committing**, and a
finding that exists only as cell output does not exist.

Regime labels run 2015-01-07 to 2026-09-01. Every figure is measured on the return earned the day
*after* the label, so nothing below is a description of the day it happened.

### The signal separates risk, not return

| | Assets where it holds | Mean effect, annualised |
| --- | ---: | ---: |
| **Good regime has lower forward volatility** | **11 of 12** | **−5.6 points** |
| Good regime has higher forward return | 5 of 12 | −5.1 points |

Gold is the single asset whose volatility does not fall. The return result fails hardest on US
equities — IVV −12.7, IJH −17.0, IWM −13.7 points — and works on the bond and commodity sleeves.
The mechanism is not mysterious: the sharpest positive days arrive *inside* the drawdown the model
has correctly labelled bad.

**This is what the method's own authors predict.** Shu, Yu and Mulvey call regime identification
[*interpretative rather than predictive*](Bibliotheca/Papers/Shu_Yu_Mulvey_2024_Downside_Risk_Reduction_Using_Regime_Switching_Signals.md),
and their published strategy raises the S&P 500's Sharpe from 0.48 to 0.68 almost entirely by cutting
volatility and drawdown. Our measurement was made before that paper was read, and agrees with it.

### It is not an artefact of the setting chosen

The jump penalty is the model's only real knob. Read as a curve, not a cell:

| Jump penalty | Regime switches / asset / year | Return spread | Volatility drop |
| ---: | ---: | ---: | ---: |
| 5 | 12.0 | −5.8% (4 of 12 positive) | +6.3% (11 of 12) |
| 15 | 7.6 | −6.0% (3 of 12) | +5.8% (11 of 12) |
| 30 | 5.3 | −5.2% (5 of 12) | +5.8% (11 of 12) |
| **50 — in use** | **3.9** | **−5.1% (5 of 12)** | **+5.6% (11 of 12)** |
| 100 | 2.3 | −0.7% (5 of 12) | +4.9% (11 of 12) |

Switching frequency falls monotonically, exactly as the model's design says it should. **The sign of
both results holds across the whole range.** The setting in use was chosen on persistence — a median
spell of 43 trading days, 3.8 switches a year — and deliberately not on return.

### What look-ahead is worth here: 44 points a year

The same fitted model can be read two ways. The **smoothed** labels are the best explanation of a
finished stretch of history and are allowed to know what happened next; the **causal** labels use only
today and everything before it. They agree on 81% of days, and disagree exactly at the turning points.

| Reading | Mean good-minus-bad forward return | Assets positive |
| --- | ---: | ---: |
| Smoothed — uses the future | **+38.9%** | 12 of 12 |
| Causal — tradable | −5.1% | 5 of 12 |

**The gap is 44.0 annualised points, and it is one line of code.** A regime chart built the wrong way
looks magnificent and is worth nothing. This measurement is why
[`Data/Refinery/jump_model.py`](Data/Refinery/jump_model.py) returns the causal label, and why
`AGENTS.md` treats look-ahead as the control with the highest expected cost.

### The cross-sectional features, screened

Mean per-date Spearman IC against forward returns, inside the eligible pool. **A screening tool, not
evidence** — twelve assets is a small cross-section, and the fundamental law says an information
ratio scales with the square root of the number of independent bets.

| Feature | IC 21d | IC 63d | IC 252d | IR 252d | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| `r_return_ewm_hl21_rank` | +0.026 | +0.051 | **+0.131** | 0.23 | the strongest, and only at a one-year horizon |
| `r_liquidity_rank` | +0.052 | +0.095 | +0.119 | 0.21 | a size effect across asset classes, not a signal |
| `r_sortino_hl21_rank` | −0.002 | +0.038 | +0.053 | 0.10 | weaker than its parts, which is a warning about the ratio |
| `r_downside_deviation_hl21_rank` | +0.051 | +0.024 | +0.033 | 0.06 | risk is paid for — the sign is a premium, not skill |

Everything usable sits at the 252-day horizon and nothing does at 21 days, so **any experiment
selecting on these has to hold for a year to collect them**, which is a construction constraint
before it is a signal.

### What the universe itself constrains

| | |
| --- | --- |
| Assets | 12 ETFs, three groups (5 equity, 4 fixed income, 3 real assets) |
| Priced | 2010-01-04 to 2026-09-01 |
| Universe complete from | 2011-04-07 — SPBO's inception, the youngest member |
| **All assets carry a regime from** | **2016-04-12** — the honest start of a whole-universe backtest |
| Mean pairwise return correlation | 0.35, from −0.28 to 0.96 |
| Mean breadth | 56% of assets in their good regime; 21% of days at or below 25% |

The 2016 date is the one that costs something: a five-year training window turns sixteen years of
prices into ten years of signal, and a backtest that starts earlier is quietly comparing books drawn
from different universes.

---

## The experiments

Each experiment ranks its variants over **one window shared by all of them**
(`backtest_engine.align_to_common_start`), and those windows can differ between experiments.

> **Read the Sharpe column down, not across.** An experiment's winner is comparable to *its own*
> control row, not to another experiment's headline. The `vs control` column is the one that carries
> meaning across rows.

| Exp | Book | CAGR | Sharpe | Max DD | Control Sharpe | vs control | Status | Findings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| **1** | equal weight over the calm asset classes | | | | — | — | **built, not priced** | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |

### Experiment 1, structurally — what step 4 settled without an engine

| Property | Value |
| --- | ---: |
| Book window | 2015-01-09 to 2026-08-18 |
| Rebalances | 461 — **40 a year**, event-driven on any change in the eligible set |
| One-way turnover | **~810% a year** |
| Holdings | 6.5 mean, 0 minimum, 12 maximum |
| Largest single weight | **100%** at its worst |
| Invested share | **95.3%** of trading days |
| Group drift vs an always-invested equal-weight book | Real Assets +2.6 pts, Fixed Income −2.1, Equity −2.1 |

**The blueprint's fourth prediction was falsified here.** It predicted the book would average roughly
half in cash, reasoning from 56% mean breadth. It averages 95.3% invested. Breadth decides *how many*
assets are held, not *how much* is invested: equal weight over the eligible set always sums to one
whenever anything qualifies, so as breadth falls the book **concentrates instead of de-risking** — at
the extreme into a single asset at 100%.

**This is a rotation, not a risk reducer**, and the two levers the benchmark deliberately declined —
a weight cap and a minimum holding count — turn out to be the entire mechanism by which the source
paper's version goes defensive. Turning them on is Experiment 2.

The near-zero group drift is the good news: the strategy has no structural tilt toward equities,
bonds or real assets, so no later result can be dismissed as *it was just long bonds*.

### Against the world

The comparisons every experiment is reported against, buy and hold over the priced window
(2010-01-04 to 2026-09-01), from `Data/analyzer.ipynb` section 2. **These are the numbers a strategy
has to beat**, and three of the twelve assets it can choose from already beat a 60/40.

| Instrument | Return | Volatility | Sharpe |
| --- | ---: | ---: | ---: |
| IVV — US large cap | 14.7% | 17.2% | 0.86 |
| IJH — US mid cap | 13.2% | 20.0% | 0.66 |
| IWM — US small cap | 12.9% | 22.2% | 0.58 |
| IYR — REITs | 10.1% | 19.8% | 0.51 |
| GLD — gold | 9.1% | 16.8% | 0.55 |
| EFA — developed ex-US | 8.5% | 18.3% | 0.46 |
| EEM — emerging | 7.1% | 21.6% | 0.33 |
| HYG — high yield | 5.4% | 8.2% | 0.66 |
| DBC — commodities | 3.9% | 17.4% | 0.23 |
| SPBO — corporates | 3.5% | 7.3% | 0.48 |
| SPTL — long treasuries | 3.4% | 13.6% | 0.25 |
| AGG — aggregate bonds | 2.5% | 4.7% | 0.54 |

`AOR` (a 60/40 balanced allocation) and `SPY` are downloaded as the reported-against benchmarks; they
are excluded from the cross-section by the Refinery's membership allowlist.

### The trial count

**One model configuration, five jump penalties swept and published, no variant selected on return.**
Published because a reader cannot discount a best-of-N result without knowing N — see
[Bailey & López de Prado](Bibliotheca/Papers/Bailey_LopezDePrado_2014_The_Deflated_Sharpe_Ratio.md).

---

## What stands — reuse, do not rebuild

- **The causal-versus-smoothed comparison** in `Data/analyzer.ipynb` section 5. It is a general test,
  not a regime-specific one: any fitted signal can be read both ways, and the gap is the look-ahead.
- **The regime label itself** as a *risk* input. 11 of 12 assets, at every penalty. Do not re-derive
  it; do not re-litigate whether it works.
- **The first-usable date, 2016-04-12.** Any experiment starting earlier is not measuring the whole
  universe.

## What is closed — do not re-propose without a new argument

- **"Hold the good-regime assets, expect more return."** Measured, negative, on 7 of 12 assets and
  on average, at every penalty from 5 to 100. Any proposal that needs this to be true has to explain
  why the measurement is wrong first.
- **Choosing the jump penalty on Sharpe ratio.** It is what the source paper does and it is the
  practice `AGENTS.md` forbids. We publish the sweep instead, and accept that we cannot claim the
  paper's numbers.

### The uncomfortable one

**Two of them now, and the second is worse than the first.**

**The strategy is named after the half of the idea that did not survive.** "Regime Rotation" implies
moving toward what is going up; what the data supports is moving away from what is turbulent. The
honest version of the thesis is a defensive one, and a defensive strategy has to be judged against a
lower-volatility benchmark than the S&P 500 — which changes the comparison in the table above more
than any single number in it.

**And the benchmark book is not defensive either.** It is 95% invested and it *concentrates* as
breadth falls, rather than stepping aside. So the book currently in this repository does not
implement the honest version of the thesis any more than the name does. It is fixable in one line
and it is Experiment 2 — but until then, **nothing here has tested the idea `OBJECTIVE.md` actually
states.** That is the most important sentence in this file.

## Open leads, ranked

1. **Price the benchmark book.** It exists; it has never been through the engine. At 810% annual
   turnover the only question that matters is whether anything survives the commission, and the
   engine's per-share model is the only way to find out.
2. **Turn on the cap and the minimum holding count.** They are what make the source paper's book
   defensive, they are already implemented in `portfolio_construction.py`, and the benchmark
   declined them on purpose so that Experiment 2 has exactly one thing to change.
3. **Add the forecasting layer.** The source paper's second half predicts *tomorrow's* regime rather
   than identifying today's. It is the stated remedy for the result above and it is what would
   reopen claim 2.
4. **Test against volatility management.** [Moreira & Muir (2017)](Bibliotheca/BIBLIOGRAPHY.md)
   scale exposure by recent volatility with no regime model at all. If that does the same job, the
   regime model has to justify its complexity.
5. **Widen the universe.** Twelve assets caps every cross-sectional statistic here. Sector or country
   ETFs at the same cost would raise the ceiling on anything built on the ranks.

## Excluded runs

Variants removed from the tables above rather than reported with a caveat. **A metric computed over
a truncated or rejected run does not belong in the same column as a complete one.**

| Variant | Why |
| --- | --- |
| *(none yet)* | |

## Known limitations

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | **Nothing has been priced.** Experiment 1 reaches step 4; steps 5 and 6 need licensed engines this clone does not have | Every figure above is a property of a signal or a weight file, not of a traded book. None is net of costs |
| 2 | **Nothing is out of sample.** No experiment has reached step 7 | In-sample selection is what the deflation literature warns about |
| 3 | Twelve assets is a small cross-section | Every IC above is noisy; the fundamental law caps what breadth this thin can deliver |
| 4 | The example trades ETFs, not the indices the paper studied | Tracking error, expense ratios and premium/discount to NAV are unmodelled |
| 5 | The window is 2010-2026, and the signal window 2015-2026 | One decade, dominated by a single equity bull market and two sharp drawdowns |
| 6 | The training window is five years, not the paper's eleven | The ETFs do not have eleven years of common history. Regimes are fitted on less evidence than the source used |
| 7 | Curator output is not reproducible across download dates | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
| 8 | The Deflated Sharpe Ratio has never been computed | The one number that would say whether a winner survives its own trial count |
| 9 | No control arm exists differing in exactly one thing | Which lever earns a margin would be inferred, not measured |

> **Under the bar in [`AGENTS.md`](AGENTS.md), most of this file is a reason to run an experiment
> rather than a result.** That is the correct state for a repository at step 3.

---
---

# Appendix — where each number comes from

Every path below is gitignored and rebuilt by running its stage.

| Output | Path | Rebuilt by |
| --- | --- | --- |
| Per-security prices and features | `Data/Curator/Time_Series/` | `uv run python Data/curator.py` |
| The cross-sectional panel | `Data/Refinery/Time_Series/` | `uv run python Data/refinery.py` |
| Signal information coefficients | `Data/Analyzer/signal_information_coefficients.csv` | `Data/analyzer.ipynb` |
| Analyzer charts | `Data/Analyzer/Charts/` | `Data/analyzer.ipynb` |
| Universe diagnostics | `Universe/Security_Master.csv`, `Data_Issues.csv`, `Charts/` | `Universe/universe.ipynb` |
| Engine results, per experiment | `Experiments/Experiment_N/Backtest/` | that experiment's notebook |
| Attribution figures | `Experiments/Experiment_N/Attribution/` | that experiment's notebook |
| Books, per experiment | `Experiments/Experiment_N/Portfolio/` | that experiment's notebook |
| Which benchmarks are fetched, and which are reported against | `Data/curator.py`, `Experiments/backtest_engine.py` | — |

## The model's configuration, in one place

Everything in `Data/Refinery/custom_calculations.py`. Changing any of these invalidates every number
above and costs one `refinery.py` run — deliberately, no download.

| Setting | Value | Chosen how |
| --- | --- | --- |
| Features | 8 — EWM return, log downside deviation and Sortino at half-lives 5/10/21 | taken from the source paper, unmodified |
| Regimes | 2 | the source paper |
| Jump penalty | 50.0 | on persistence, from the published sweep — never on return |
| Training window | 1260 days (5 years) | the longest the ETF histories support |
| Refit interval | 126 days (about 6 months) | the source paper |
| Outlier clipping | 3 standard deviations of the training window | the source paper |
