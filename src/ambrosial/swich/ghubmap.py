from typing import Any, Literal, Optional

import july
import matplotlib.pyplot as plt

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.ghubmap import get_details, july_heatmap_args

BINS = "year+month+day"


class GitHubMap:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def order_amount(
        self,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: Any,
    ) -> None:
        self._ghubmap_plot(
            code="oa",
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def order_count(
        self,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: Any,
    ) -> None:
        self._ghubmap_plot(
            code="on",
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def _ghubmap_plot(
        self,
        code: Literal["on", "oa"],
        date_range: Optional[tuple[str, str]],
        show_plot: bool,
        kwargs: dict[str, Any],
    ) -> None:
        date_range_, values = get_details(code, self.swan, date_range, BINS)
        jargs = july_heatmap_args(kwargs)
        july.heatmap(dates=date_range_, data=values, **jargs)
        if show_plot:
            plt.show()
