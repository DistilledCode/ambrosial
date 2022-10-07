from datetime import date
from typing import Any, Callable, Literal, Optional

from july.utils import date_range

from ambrosial.swan import SwiggyAnalytics


def july_heatmap_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    july_args = {
        "cmap": kwargs.pop("cmap", "golden"),
        "month_grid": kwargs.pop("month_grid", True),
        "dpi": kwargs.pop("dpi", 400),
        "colorbar": kwargs.pop("colorbar", True),
        "fontsize": kwargs.pop("fontsize", 15),
        "titlepad": kwargs.pop("titlepad", 50),
    }
    return {**kwargs, **july_args}


def get_details(
    code: Literal["oa", "on"],
    swan: SwiggyAnalytics,
    drange: Optional[tuple[str, str]],
    bins: str,
) -> tuple[list[date], list[int]]:
    func_dict: dict[str, Callable[..., tuple[list[date], list[int]]]] = {
        "oa": _get_order_amount_details,
        "on": _get_order_number_details,
    }
    return func_dict[code](swan, drange, bins)


def _get_order_amount_details(
    swan: SwiggyAnalytics,
    drange: Optional[tuple[str, str]],
    bins: str,
) -> tuple[list[date], list[int]]:
    value_dict = swan.orders.tseries_amount(bins)
    date_range_ = _get_date_range(drange, value_dict)
    values = [value_dict.get(str(date_).replace("-", " "), 0) for date_ in date_range_]
    return date_range_, values


def _get_order_number_details(
    swan: SwiggyAnalytics,
    drange: Optional[tuple[str, str]],
    bins: str,
) -> tuple[list[date], list[int]]:
    value_dict = swan.orders.tseries_orders(bins)
    date_range_ = _get_date_range(drange, value_dict)
    values = [value_dict.get(str(date_).replace("-", " "), 0) for date_ in date_range_]
    return date_range_, values


def _get_date_range(
    drange: Optional[tuple[str, str]],
    value_dict: dict[str, Any],
) -> list[date]:
    if drange is None:
        return date_range(
            min(value_dict).replace(" ", "-"),
            max(value_dict).replace(" ", "-"),
        )
    left, right = drange
    left = min(value_dict).replace(" ", "-") if left == "-" else left
    right = max(value_dict).replace(" ", "-") if right == "-" else right
    return date_range(left, right)
