import statistics as st
from typing import Any, Callable, Literal

import pandas as pd

from ambrosial.swan import SwiggyAnalytics


def _df_restaurant_deltime(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df: dict[str, list[Any]] = {"y": [], "x": []}
    ordering = {}
    instances = swan.orders.grouped_instances(
        key="restaurant",
        attr="delivery_time_in_seconds",
    )

    for restaurant, deltime in instances.items():
        if len(deltime) < threshold:
            continue
        key = f"{restaurant.name}\n{restaurant.area_name}"
        ordering[key] = {
            "count": len(deltime),
            "total": sum(deltime) / 60,
            "average": st.mean(deltime) / 60,
            "std_dev": st.stdev(deltime) / 60 if len(deltime) > 1 else 0,
        }
        df["y"].extend([key] * len(deltime))
        df["x"].extend([i / 60 for i in deltime])
    ordering_df = pd.DataFrame(ordering)
    ordering_df = ordering_df.transpose().reset_index(0, names=["category_name"])
    return pd.DataFrame(df), ordering_df


def _df_item_spending(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.items.grouped_instances(key="name", attr="effective_item_price")
    df: dict[str, list[Any]] = {"y": [], "x": []}
    ordering = {}
    for name, amount in instances.items():
        if len(amount) < threshold:
            continue
        ordering[name] = {
            "count": len(amount),
            "total": sum(amount),
            "average": st.mean(amount),
            "std_dev": st.stdev(amount) if len(amount) > 1 else 0,
        }
        df["y"].extend([name] * len(amount))
        df["x"].extend(amount)
    ordering_df = (
        pd.DataFrame(ordering).transpose().reset_index(0, names=["category_name"])
    )
    return pd.DataFrame(df), ordering_df


def _df_coupon_discount(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.offers.grouped_instances(
        key="coupon_applied",
        attr="total_offer_discount",
    )
    df: dict[str, list[Any]] = {"y": [], "x": []}
    ordering = {}
    for coupon_code, discount in instances.items():
        if len(discount) < threshold:
            continue
        ordering[coupon_code] = {
            "count": len(discount),
            "total": sum(discount),
            "average": st.mean(discount),
            "std_dev": st.stdev(discount) if len(discount) > 1 else 0,
        }
        df["y"].extend([coupon_code] * len(discount))
        df["x"].extend(discount)
    ordering_df = pd.DataFrame(ordering)
    ordering_df = ordering_df.transpose().reset_index(0, names=["category_name"])
    return pd.DataFrame(df), ordering_df


def get_dataframe(
    code: Literal["rd", "is", "od"],
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    func_dict: dict[str, Callable[..., tuple[pd.DataFrame, pd.DataFrame]]] = {
        "rd": _df_restaurant_deltime,
        "is": _df_item_spending,
        "od": _df_coupon_discount,
    }

    return func_dict[code](swan=swan, threshold=threshold)
