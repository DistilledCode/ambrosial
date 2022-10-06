from datetime import datetime
from typing import Any, Optional

from matplotlib.ticker import Formatter, Locator
from scipy import stats

__all__ = [
    "WC_ICONS",
    "WC_PALETTES",
    "get_curr_time",
]


WC_ICONS = (
    "fas fa-fish",
    "fas fa-bone",
    "fas fa-ice-cream",
    "fas fa-pepper-hot",
    "fas fa-wine-glass",
    "fas fa-bread-slice",
    "fas fa-drumstick-bite",
)

WC_PALETTES = (
    "cmocean.sequential.Matter_20",
    "colorbrewer.diverging.RdBu_11",
    "cartocolors.sequential.Purp_7",
    "colorbrewer.diverging.RdYlBu_9",
    "cartocolors.sequential.Peach_7",
    "cartocolors.diverging.Tropic_7",
    "cartocolors.sequential.BluGrn_7",
    "colorbrewer.diverging.Spectral_11",
    "lightbartlein.sequential.Blues7_7",
    "cartocolors.sequential.agSunset_7_r",
    "lightbartlein.diverging.BlueDarkOrange12_12",
)


class CustomFormatter(Formatter):
    def __init__(self, vmax: float, vmin: float) -> None:
        self.vmax = vmax
        self.vmin = vmin
        Formatter.__init__(self)

    def __call__(self, x: float, pos: Optional[float] = None) -> str:  # noqa: U100
        return str(round(x * (self.vmax - self.vmin) + self.vmin, 2))

    def format_ticks(self, values: list[float]) -> list[str]:
        self.set_locs(values)
        return [self(value, i) for i, value in enumerate(values)]

    def format_data(self, value: float) -> str:
        return self.__call__(value)

    def format_data_short(self, value: float) -> str:
        return self.format_data(value)


class CustomLocator(Locator):
    def __init__(self, ticks: int) -> None:
        self.ticks = ticks
        Locator.__init__(self)

    def __call__(self) -> list[float]:
        return [i / self.ticks for i in range(0, self.ticks + 1)]


def get_curr_time() -> str:
    return datetime.today().strftime("%Y%m%d_%H%M%S_")


def _remove_outlier(
    *args: list[Any],
    target: list[Any],
    tolerance: int,
) -> None:
    z = stats.zscore(target)
    # Read more at: https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
    # https://www.danielsoper.com/statcalc/calculator.aspx?id=53
    outlier_indices = [ind for ind, zscore in enumerate(z) if abs(zscore) >= tolerance]
    for index in reversed(outlier_indices):
        target.pop(index)
        for eachlist in args:
            eachlist.pop(index)


def remove_outliers(*args: list[Any], tolerance: int = 5) -> None:
    for i in range(len(args)):
        _remove_outlier(*args[0:i], *args[i + 1 :], target=args[i], tolerance=tolerance)
