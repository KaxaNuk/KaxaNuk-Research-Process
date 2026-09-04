"""
Step 6: taking a return apart, through the KaxaNuk Attribution Analysis library.

The backtest says *whether* a book worked.  This says **why**, and it is the only thing that
separates a strategy from a factor exposure wearing a strategy's name.  Two decompositions, and
`FINDINGS_N.md` reports both:

- **Brinson-Fachler** splits cumulative alpha into **allocation**, **selection** and
  **interaction**.  Is the return the groups the book leans into, or the things it picks inside
  them?  On a multi-asset book that is nearly the whole question.
- **A factor model** splits total excess return into **factor exposure** and **idiosyncratic**
  return.  How much of this is a factor fund under another name?

This module owns the *shaping* -- turning hand-supplied index data into the two tables the library
auto-detects -- and the *guarding*, so an experiment can ask what is missing before it tries.  It
deliberately does not own the library call: that is four directories and a dozen field names, and
burying it here would hide from the notebook what the attribution actually ran on.

**Nothing here has ever been run.**  The library is licensed and absent from a fresh clone, and its
two inputs are supplied by hand because no price provider sells an index's daily holdings or a
factor model.  Every function below is written against the library's documented contract, not
against a run that happened.  See the known gaps in `AGENTS.md`.

Why this is its own module rather than part of `backtest_engine.py`: they are two different KaxaNuk
libraries, two different licences and two different stages, and the engine is the one path from
weights to a number.  Keeping step 6 out of it means a book can be priced by somebody who has no
attribution licence at all, which is most people most of the time.
"""

__all__ = [
    "ATTRIBUTION_HOLDINGS_FILE",
    "ATTRIBUTION_RETURNS_DAY_FIRST",
    "ATTRIBUTION_RETURNS_FILE",
    "ATTRIBUTION_RETURNS_SERIES_NAME",
    "BENCHMARK_RETURNS_NAME",
    "BENCHMARK_WEIGHTS_NAME",
    "FACTOR_FILE_PATTERN",
    "AttributionInputs",
    "available_inputs",
    "build_benchmark_returns",
    "build_benchmark_weights",
    "figures_saved_to",
    "write_horizontal",
]

import contextlib
import dataclasses
import importlib.util
import pathlib
import typing

import matplotlib.pyplot
import pandas

# The panel's column names live in one place and are read from it, rather than re-declared here.
# Attribution and the backtest have to agree on which price they are talking about: if they ever
# ran on different bases the disagreement would surface as an unexplained residual rather than as
# an error, which is the worst way for a mistake to arrive.
from securities_panel import DATE_COLUMN

# The inputs a person drops into `Data/Curator/`, because no price provider sells them.  **These
# are placeholders**: rename them to match whatever you supply.  The holdings file has to be an
# index the book is genuinely comparable to -- attributing a multi-asset book against a
# single-country equity index produces numbers, and they mean nothing.
ATTRIBUTION_HOLDINGS_FILE = "index_daily_holdings.csv"
ATTRIBUTION_RETURNS_DAY_FIRST = True
ATTRIBUTION_RETURNS_FILE = "index_returns.csv"
ATTRIBUTION_RETURNS_SERIES_NAME = "BENCHMARK_INDEX"
FACTOR_FILE_PATTERN = "f_*.csv"

# What this module writes for the library to read back, without their extensions, because the
# library is told the stem and appends the format itself.
BENCHMARK_RETURNS_NAME = "benchmark_returns"
BENCHMARK_WEIGHTS_NAME = "benchmark_weights"

# The figures the library draws, in the order it draws them.  Named so `FINDINGS_N.md` can cite a
# stable filename rather than "the second chart".
FIGURE_NAMES = (
    "attribution_brinson_fachler.png",
    "attribution_factor_model.png",
)


@dataclasses.dataclass(frozen=True)
class AttributionInputs:
    """
    What step 6 found on disk, and what is missing.

    `ready` is the only thing a notebook needs to branch on; the rest exists so the skip message
    can say *which* input is absent.  A stage that says "skipped" without saying why is the
    graceful degradation `AGENTS.md` forbids.
    """

    factor_files: tuple[pathlib.Path, ...]
    holdings_path: pathlib.Path
    library_installed: bool
    ready: bool
    returns_path: pathlib.Path

    def explain(self) -> str:
        """One line naming every reason this stage cannot run, or that it can."""
        if self.ready:

            return (
                f"attribution inputs ready: {len(self.factor_files)} factor file(s),"
                f" holdings and returns present"
            )

        missing = []
        if not self.library_installed:
            missing.append("kaxanuk-attribution-analysis is not installed")
        if not self.holdings_path.is_file():
            missing.append(f"no {self.holdings_path.name}")
        if not self.returns_path.is_file():
            missing.append(f"no {self.returns_path.name}")
        if len(self.factor_files) == 0:
            missing.append(f"no {FACTOR_FILE_PATTERN} factor files")

        return "attribution skipped: " + "; ".join(missing)


def available_inputs(
    benchmark_directory: pathlib.Path,
    factor_directory: pathlib.Path,
) -> "AttributionInputs":
    """
    Report what step 6 has and has not been given, without importing the licensed library.

    Checked by looking for the module rather than importing it, so a clone with no licence pays
    nothing to find out that it has no licence.
    """
    library_installed = importlib.util.find_spec("kaxanuk.attribution_analysis") is not None
    holdings_path = benchmark_directory / ATTRIBUTION_HOLDINGS_FILE
    returns_path = benchmark_directory / ATTRIBUTION_RETURNS_FILE
    factor_files = (
        tuple(sorted(factor_directory.glob(FACTOR_FILE_PATTERN)))
        if factor_directory.is_dir()
        else ()
    )

    return AttributionInputs(
        factor_files=factor_files,
        holdings_path=holdings_path,
        library_installed=library_installed,
        ready=(
            library_installed
            and holdings_path.is_file()
            and returns_path.is_file()
            and len(factor_files) > 0
        ),
        returns_path=returns_path,
    )


def build_benchmark_returns(
    source: pathlib.Path,
    destination: pathlib.Path,
) -> pandas.DataFrame:
    """
    The index's daily returns, as the single-row table the library expects.

    `ATTRIBUTION_RETURNS_DAY_FIRST` is declared rather than inferred because pandas cannot tell
    `03/04` from `04/03`, and guessing wrong shifts the entire series by a day without raising.
    """
    returns = pandas.read_csv(
        source,
        parse_dates=[DATE_COLUMN],
        dayfirst=ATTRIBUTION_RETURNS_DAY_FIRST,
    ).set_index(DATE_COLUMN)
    series = returns.iloc[:, 0].rename(ATTRIBUTION_RETURNS_SERIES_NAME).dropna()

    return write_horizontal(series.to_frame().T, destination)


def build_benchmark_weights(
    source: pathlib.Path,
    destination: pathlib.Path,
) -> pandas.DataFrame:
    """
    The index's daily holdings, transposed to the table the library expects.

    Nulls become zero rather than being dropped: the library reads a null as a missing observation
    and a zero as "held nothing that day", and for an index constituent the second is what a blank
    cell means.
    """
    holdings = pandas.read_csv(
        source,
        parse_dates=[DATE_COLUMN],
    ).set_index(DATE_COLUMN)

    return write_horizontal(holdings.fillna(0.0).T, destination)


@contextlib.contextmanager
def figures_saved_to(
    directory: pathlib.Path,
    names: tuple[str, ...] = FIGURE_NAMES,
) -> typing.Iterator[list[pathlib.Path]]:
    """
    Write every figure the library draws into `directory`, and still show it inline.

    Everything this library produces is a side effect: log lines and matplotlib figures, with no
    object returned to save afterwards.  Under the notebook's inline backend `pyplot.show()`
    renders a figure and then *closes* it, so by the time the call returns there is nothing left.
    Intercepting `show` is the only place a figure can be caught.

    A context manager rather than a bare reassignment, because `pyplot.show` has to be given back:
    left patched, every later chart in the session would keep writing files into an attribution
    folder it has nothing to do with.  Yields the list of paths written.
    """
    directory.mkdir(parents=True, exist_ok=True)
    written: list[pathlib.Path] = []
    original_show = matplotlib.pyplot.show

    def save_then_show(*arguments, **keyword_arguments):
        """Save each open figure under the next available name, then show it as usual."""
        for number in matplotlib.pyplot.get_fignums():
            position = len(written)
            name = (
                names[position]
                if position < len(names)
                else f"attribution_figure_{position}.png"
            )
            path = directory / name
            matplotlib.pyplot.figure(number).savefig(path, dpi=160, bbox_inches="tight")
            written.append(path)

        return original_show(*arguments, **keyword_arguments)

    matplotlib.pyplot.show = save_then_show
    try:
        yield written
    finally:
        matplotlib.pyplot.show = original_show


def write_horizontal(
    frame: pandas.DataFrame,
    destination: pathlib.Path,
) -> pandas.DataFrame:
    """
    Write `frame` as the `Ticker x ISO-date` table both KaxaNuk loaders auto-detect.

    Defined once because it is a contract with the library rather than a formatting choice: get the
    index name or the date format wrong and the loader mis-detects the table's orientation instead
    of failing, which produces a transposed attribution and no error.
    """
    output = frame.copy()
    output.columns = pandas.DatetimeIndex(output.columns).strftime("%Y-%m-%d")
    output.index.name = "Ticker"
    output.to_csv(destination)

    return output
