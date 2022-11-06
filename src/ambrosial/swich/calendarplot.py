import calendar
import heapq
from typing import Any, Literal

import july
import matplotlib.pyplot as plt

import ambrosial.swich.helper.ghubmap as helper
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.calendarplot import july_calmon_args


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
            code="oc",
            kwargs=kwargs,
        )

    def cal_offer_amount(
        self,
        **kwargs: Any,
    ) -> None:
        self._calendar_plot(
            code="of",
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
            code="oc",
            month=month,
            year=year,
            kwargs=kwargs,
        )

    def month_offer_amount(
        self,
        month: int,
        year: int,
        **kwargs: Any,
    ) -> None:
        self._month_plot(
            code="of",
            month=month,
            year=year,
            kwargs=kwargs,
        )

    def _month_plot(
        self,
        code: Literal["oc", "oa", "of"],
        month: int,
        year: int,
        kwargs: dict[str, Any],
    ) -> None:
        if code == "of":
            date_range_, values = helper.offer_plot_value(self.swan)
        else:
            date_range_, values = helper.get_order_info(code, self.swan)
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
            "of": "Total Offer Availed in "
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
        code: Literal["oc", "oa", "of"],
        kwargs: dict[str, Any],
    ) -> None:
        if code == "of":
            date_range_, values = helper.offer_plot_value(self.swan)
        else:
            date_range_, values = helper.get_order_info(code, self.swan)
        default_title = {
            "on": f"Total Order Count: {sum(values)}",
            "oa": f"Total Amount Spent: {sum(values)}",
            "of": f"Total Discount Availed: {sum(values)}\n"
            f"{helper.extreme_value_str(date_range_, values)}",
        }
        kwargs.setdefault("cmap", "golden")
        kwargs.setdefault("title", default_title.get(code))
        july.calendar_plot(dates=date_range_, data=values, **kwargs)
        plt.suptitle(kwargs["title"], y=1.0)
