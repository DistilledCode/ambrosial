import statistics as st
from typing import Any, Callable, Literal

import pandas as pd

from ambrosial.swan import SwiggyAnalytics


def _dataframe(
    instances: dict[Any, Any],
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df: dict[str, list[Any]] = {"y": [], "x": []}
    ordering = {}
    for category_name, list_val in instances.items():
        if len(list_val) < threshold:
            continue
        ordering[category_name] = {
            "count": len(list_val),
            "total": sum(list_val),
            # "average": st.mean(list_val),
            "std_dev": st.stdev(list_val) if len(list_val) > 1 else 0,
        }
        df["y"].extend([category_name] * len(list_val))
        df["x"].extend(list_val)
    ordering_df = pd.DataFrame(ordering)
    ordering_df = ordering_df.transpose().reset_index(0, names=["category_name"])
    return pd.DataFrame(df), ordering_df


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
    return _dataframe(instances=instances, threshold=threshold)


def _df_coupon_discount(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.offers.grouped_instances(
        key="coupon_applied",
        attr="total_offer_discount",
    )
    return _dataframe(instances=instances, threshold=threshold)


def _df_payment_method(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.payments.grouped_instances(
        key="paymentMethod",
        attr="amount",
    )
    return _dataframe(instances=instances, threshold=threshold)


def _df_payment_type(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.payments.grouped_instances(
        key="paymentMethodDisplayName",
        attr="amount",
    )
    return _dataframe(instances=instances, threshold=threshold)


def get_dataframe(
    code: Literal["rd", "is", "od", "pm", "pt"],
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    func_dict: dict[str, Callable[..., tuple[pd.DataFrame, pd.DataFrame]]] = {
        "rd": _df_restaurant_deltime,
        "is": _df_item_spending,
        "od": _df_coupon_discount,
        "pm": _df_payment_method,
        "pt": _df_payment_type,
    }

    return func_dict[code](swan=swan, threshold=threshold)
