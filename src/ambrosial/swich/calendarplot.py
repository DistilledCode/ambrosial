import calendar
from typing import Any, Literal, Optional

import july
import matplotlib.pyplot as plt

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.calendarplot import get_details, july_calmon_args

BINS = "year+month+day"


class CalendarPlot:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def cal_order_amount(
        self,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: Any,
    ) -> None:
        self._calendar_plot(
            code="oa",
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def cal_order_number(
        self,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: Any,
    ) -> None:
        self._calendar_plot(
            code="on",
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def month_order_amount(
        self,
        month: int,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: Any,
    ) -> None:
        self._month_plot(
            code="oa",
            month=month,
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def month_order_number(
        self,
        month: int,
        date_range: Optional[tuple[str, str]] = None,
        show_plot: bool = False,
        **kwargs: Any,
    ) -> None:
        self._month_plot(
            code="on",
            month=month,
            date_range=date_range,
            show_plot=show_plot,
            kwargs=kwargs,
        )

    def _month_plot(
        self,
        code: Literal["on", "oa"],
        month: int,
        date_range: Optional[tuple[str, str]],
        show_plot: bool,
        kwargs: dict[str, Any],
    ) -> None:
        default_title = {
            "on": f"Number of orders in {calendar.month_abbr[month]}",
            "oa": f"Amount spent in {calendar.month_abbr[month]}",
        }
        date_range_, values = get_details(code, self.swan, date_range, BINS)
        kwargs.setdefault("title", default_title.get(code))
        jargs = july_calmon_args(kwargs)
        july.month_plot(dates=date_range_, data=values, month=month, **jargs)
        plt.suptitle(kwargs["title"], fontsize="x-large", y=1.0)
        if show_plot:
            plt.show()

    def _calendar_plot(
        self,
        code: Literal["on", "oa"],
        date_range: Optional[tuple[str, str]],
        show_plot: bool,
        kwargs: dict[str, Any],
    ) -> None:
        default_title = {
            "on": "Number of orders",
            "oa": "Amount Spent",
        }
        date_range_, values = get_details(code, self.swan, date_range, BINS)
        kwargs.setdefault("cmap", "golden")
        kwargs.setdefault("title", default_title.get(code))
        july.calendar_plot(dates=date_range_, data=values, **kwargs)
        plt.suptitle(kwargs["title"], fontsize="x-large", y=1.0)
        if show_plot:
            plt.show()
