import heapq
from collections import defaultdict
from datetime import date, timedelta
from typing import Any, Callable, Literal

from july.utils import date_range

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swiggy.datamodel.order import Order
from ambrosial.swiggy.datamodel.restaurant import Restaurant


def july_heatmap_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    july_args = {
        "cmap": kwargs.pop("cmap", "golden"),
        "month_grid": kwargs.pop("month_grid", True),
        "dpi": kwargs.pop("dpi", 400),
        "colorbar": kwargs.pop("colorbar", True),
        "fontsize": kwargs.pop("fontsize", 15),
        "titlepad": kwargs.pop("titlepad", 40),
    }
    return {**kwargs, **july_args}


def get_offer_info(swan: SwiggyAnalytics) -> tuple[list[date], list[int]]:
    value_dict: dict[date, int] = defaultdict(int)
    orders = swan.swiggy.get_orders()
    for order in orders:
        discount = sum(offer.total_offer_discount for offer in order.offers_data)
        value_dict[order.order_time.date()] += int(discount)
    drange = _get_drange_from_orders(orders)
    values = [value_dict.get(day, 0) for day in drange]
    return drange, values


def get_restaurant_info(
    code: Literal["count", "amount"],
    orders: list[Order],
) -> tuple[list[date], list[int]]:
    value_dict: dict[date, int] = defaultdict(int)
    for order in orders:
        if code == "count":
            value_dict[order.order_time.date()] += 1
        else:
            value_dict[order.order_time.date()] += order.order_total
    drange = _get_drange_from_orders(orders)
    values = [value_dict.get(day, 0) for day in drange]
    return drange, values


def get_grouped_restaurant(
    swan: SwiggyAnalytics,
    restaurant_id: int,
) -> tuple[Restaurant, list[Order]]:
    for restaurant, orders in swan.orders.grouped_instances(key="restaurant").items():
        if restaurant.rest_id == restaurant_id:
            return restaurant, orders
    raise ValueError(f"No restauarant with id {repr(restaurant_id)} found")


def get_order_info(
    code: Literal["oa", "on"],
    swan: SwiggyAnalytics,
    bins: str,
) -> tuple[list[date], list[int]]:
    func_dict: dict[str, Callable[..., tuple[list[date], list[int]]]] = {
        "oa": _get_order_amount,
        "on": _get_order_count,
    }
    return func_dict[code](swan, bins)


def _get_order_amount(
    swan: SwiggyAnalytics,
    bins: str,
) -> tuple[list[date], list[int]]:
    value_dict = swan.orders.tseries_amount(bins)
    date_range_ = _get_drange_from_str(value_dict)
    values = [value_dict.get(str(date_).replace("-", " "), 0) for date_ in date_range_]
    return date_range_, values


def _get_order_count(
    swan: SwiggyAnalytics,
    bins: str,
) -> tuple[list[date], list[int]]:
    value_dict = swan.orders.tseries_orders(bins)
    date_range_ = _get_drange_from_str(value_dict)
    values = [value_dict.get(str(date_).replace("-", " "), 0) for date_ in date_range_]
    return date_range_, values


def _get_drange_from_str(
    value_dict: dict[str, Any],
) -> list[date]:
    return date_range(
        min(value_dict).replace(" ", "-"),
        max(value_dict).replace(" ", "-"),
    )


def _get_drange_from_orders(
    orders: list[Order],
) -> list[date]:
    min_date = min(orders, key=lambda x: x.order_time).order_time.date()
    max_date = max(orders, key=lambda x: x.order_time).order_time.date()
    min_date = min_date.replace(day=1)
    max_date = (max_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return date_range(min_date, max_date)


def extreme_value_str(dates: list[date], values: list[int]) -> str:
    actual_min = heapq.nsmallest(2, set(values))[-1]
    actual_max, max_date = max(zip(values, dates), key=lambda x: x[0])
    min_date = None
    for day, val in zip(dates, values):
        if val == actual_min:
            min_date = day
            break
    return f"Min: {actual_min} on {min_date} | " f"Max: {actual_max} on {max_date}"
