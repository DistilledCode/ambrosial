from typing import Any, Literal, Optional

import july
import matplotlib.pyplot as plt

import ambrosial.swich.helpers as helpers
from ambrosial.swan import SwiggyAnalytics

BINS = "year+month+day"


class HeatMap:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def order_amount(
        self,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        self._heatmap_plot(
            code="oa",
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def order_number(
        self,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        self._heatmap_plot(
            code="on",
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def _heatmap_plot(
        self,
        code: Literal["on", "oa"],
        date_range: Optional[tuple[str, str]],
        show_plot: bool,
        kwargs: dict[str, Any],
    ) -> None:
        date_range_, values = helpers.get_details(code, self.swan, date_range, BINS)
        jargs = helpers.july_heatmap_args(kwargs)
        july.heatmap(dates=date_range_, data=values, **jargs)
        if show_plot:
            plt.show()
