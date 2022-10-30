import heapq
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, Literal

from july.utils import date_range

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.order import Order
from ambrosial.swiggy.datamodel.restaurant import Restaurant

# def timeit(func):
#     def wrapper_func(*args, **kwargs):
#         st = perf_counter()
#         result = func(*args, **kwargs)
#         print(perf_counter() - st)
#         return result

#     return wrapper_func


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


def offer_plot_value(swan: SwiggyAnalytics) -> tuple[list[date], list[int]]:
    value_dict: dict[date, int] = defaultdict(int)
    orders = swan.swiggy.get_orders()
    for order in orders:
        discount = sum(offer.total_offer_discount for offer in order.offers_data)
        value_dict[order.order_time.date()] += int(discount)
    drange = _get_drange_from_orders(orders)
    values = [value_dict.get(day, 0) for day in drange]
    return drange, values


def get_grouped_restaurant(
    swan: SwiggyAnalytics,
    restaurant_id: int,
) -> tuple[Restaurant, list[Order]]:
    restaurant = swan.swiggy.get_restaurant(restaurant_id=restaurant_id)
    orders = swan.restaurants.associated_orders(restaurant_id=restaurant_id)
    return restaurant, orders


def restaurant_plot_value(
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


def get_grouped_item(
    swan: SwiggyAnalytics,
    item_id: int,
) -> tuple[Item, list[Order]]:
    item = swan.swiggy.get_item(item_id=item_id)
    orders = swan.items.associated_orders(item_id=item_id)
    return item, orders


def item_plot_value(
    code: Literal["count", "amount"],
    orders: list[Order],
) -> tuple[list[date], list[int]]:
    value_dict: dict[date, int] = defaultdict(int)
    instances: list[tuple[Item, datetime]] = [
        (item, order.order_time) for order in orders for item in order.items
    ]
    for item, order_time in instances:
        if code == "count":
            value_dict[order_time.date()] += item.quantity
        else:
            value_dict[order_time.date()] += int(item.effective_item_price)
    drange = _get_drange_from_orders(orders)
    values = [value_dict.get(day, 0) for day in drange]
    return drange, values


def get_order_info(
    code: Literal["oa", "on"],
    swan: SwiggyAnalytics,
    bins: str,
) -> tuple[list[date], list[int]]:
    if code == "oa":
        value_dict = swan.orders.tseries_amount(bins)
    else:
        value_dict = swan.orders.tseries_count(bins)
    date_range_ = date_range(
        min(value_dict).replace(" ", "-"),
        max(value_dict).replace(" ", "-"),
    )
    values = [value_dict.get(str(date_).replace("-", " "), 0) for date_ in date_range_]
    return date_range_, values


def _get_drange_from_orders(
    orders: list[Order],
) -> list[date]:
    min_time = min(orders, key=lambda x: x.order_time).order_time
    max_time = max(orders, key=lambda x: x.order_time).order_time
    return _get_drange_from_datetime(min_time, max_time)


def _get_drange_from_datetime(
    min_time: datetime,
    max_time: datetime,
) -> list[date]:
    min_date = min_time.date()
    max_date = max_time.date()
    month_diff = (max_date.month - min_date.month) + (
        12 if min_date.month > max_date.month else 0
    )
    # if difference is less than 4 months then the graph is clipping into cbar
    if month_diff < 4:
        min_date = (min_date - timedelta(days=28 * (4 - month_diff))).replace(day=1)
    else:
        min_date = min_date.replace(day=1)
    max_date = (max_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    return date_range(min_date, max_date)


def extreme_value_str(dates: list[date], values: list[int]) -> str:
    actual_min = heapq.nsmallest(2, set(values))[-1]
    actual_max, max_date = max(zip(values, dates), key=lambda x: x[0])
    for day, val in zip(dates, values):
        if val == actual_min:
            min_date = day
            break
    return f"Min: {actual_min} on {min_date} | " f"Max: {actual_max} on {max_date}"
