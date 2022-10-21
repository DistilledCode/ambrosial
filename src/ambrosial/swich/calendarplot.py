import calendar
import heapq
from typing import Any, Literal

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
        **kwargs: Any,
    ) -> None:
        self._calendar_plot(
            code="oa",
            kwargs=kwargs,
        )

    def cal_order_count(
        self,
        **kwargs: Any,
    ) -> None:
        self._calendar_plot(
            code="on",
            kwargs=kwargs,
        )

    def month_order_amount(
        self,
        month: int,
        year: int,
        **kwargs: Any,
    ) -> None:
        self._month_plot(
            code="oa",
            month=month,
            year=year,
            kwargs=kwargs,
        )

    def month_order_count(
        self,
        month: int,
        year: int,
        **kwargs: Any,
    ) -> None:
        self._month_plot(
            code="on",
            month=month,
            year=year,
            kwargs=kwargs,
        )

    def _month_plot(
        self,
        code: Literal["on", "oa"],
        month: int,
        year: int,
        kwargs: dict[str, Any],
    ) -> None:
        date_range_, values = get_details(code, self.swan, bins=BINS)
        month_total = sum(
            value
            for day, value in zip(date_range_, values)
            if day.month == month and day.year == year
        )
        default_title = {
            "on": "Total Order Count in "
            f"{calendar.month_abbr[month]}, {year}: {month_total}",
            "oa": "Total Amount Spent in "
            f"{calendar.month_abbr[month]}, {year}: {month_total}",
        }
        kwargs.setdefault("title", default_title.get(code))
        jargs = july_calmon_args(kwargs)
        july.month_plot(
            dates=date_range_,
            data=values,
            month=month,
            year=year,
            cmin=int(heapq.nsmallest(2, set(values))[-1] * 0.90),
            **jargs,
        )
        plt.suptitle(kwargs["title"], y=1.0)

    def _calendar_plot(
        self,
        code: Literal["on", "oa"],
        kwargs: dict[str, Any],
    ) -> None:
        date_range_, values = get_details(code, self.swan, BINS)
        default_title = {
            "on": f"Total Order Count: {sum(values)}",
            "oa": f"Total Amount Spent: {sum(values)}",
        }
        kwargs.setdefault("cmap", "golden")
        kwargs.setdefault("title", default_title.get(code))
        july.calendar_plot(dates=date_range_, data=values, **kwargs)
        plt.suptitle(kwargs["title"], y=1.0)
