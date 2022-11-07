from typing import Callable, Literal, Optional, Union

import pandas as pd

from ambrosial.swan import SwiggyAnalytics

GTYPE = Literal["average", "total"]


def get_display_order(df: pd.DataFrame) -> list[str]:
    display_order: list[tuple[str, float]] = []
    for name, grouped_df in df.groupby(by="y"):
        display_order.append((name, grouped_df["x"].mean()))
    display_order.sort(key=lambda x: x[1], reverse=True)
    return [i[0] for i in display_order]


def _dataframe(
    instances: dict[str, Union[list[int], list[float]]],
    threshold: int,
    gtype: GTYPE,
) -> pd.DataFrame:

    df: dict[str, list] = {"y": [], "x": []}
    for category_name, value_list in instances.items():
        if len(value_list) < threshold:
            continue
        if gtype == "average":
            df["x"].extend(value_list)
            df["y"].extend([category_name] * len(value_list))
        else:
            df["x"].append(sum(value_list))
            df["y"].append(category_name)
    return pd.DataFrame(df).sort_values(by=["x"], ascending=False)


def _df_restaurant_deltime(
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: GTYPE,
) -> pd.DataFrame:
    instances = {
        f"{restaurant.name}\n{restaurant.area_name}": [i / 60 for i in values]
        for restaurant, values in swan.orders.grouped_instances(
            key="restaurant",
            attr="delivery_time_in_seconds",
        ).items()
    }
    return _dataframe(instances, threshold=threshold, gtype=gtype)


def _df_item_spending(
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: GTYPE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.items.grouped_instances(key="name", attr="effective_item_price")
    return _dataframe(instances=instances, threshold=threshold, gtype=gtype)


def _df_restaurant_spending(
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: GTYPE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = {
        f"{restaurant.name}\n{restaurant.area_name}": total_list
        for restaurant, total_list in swan.orders.grouped_instances(
            key="restaurant", attr="order_total"
        ).items()
    }
    return _dataframe(instances=instances, threshold=threshold, gtype=gtype)


def _df_item_count(
    swan: SwiggyAnalytics,
    threshold: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.DataFrame(swan.items.grouped_count(group_by="name"), index=["x"])
    df = df.transpose().reset_index(0, names=["y", "x"])
    return df[df["x"] >= threshold]


def _df_restaurant_count(swan: SwiggyAnalytics, threshold: int) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            f"{restaurant.name}\n{restaurant.area_name}": count
            for restaurant, count in swan.restaurants.group().items()
        },
        index=["x"],
    )
    df = df.transpose().reset_index(0, names=["y", "x"])
    return df[df["x"] >= threshold]


def _df_coupon_discount(
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: GTYPE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.offers.grouped_instances(
        key="coupon_applied",
        attr="total_offer_discount",
    )
    return _dataframe(instances=instances, threshold=threshold, gtype=gtype)


def _df_payment_method(
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: GTYPE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.payments.grouped_instances(
        key="paymentMethod",
        attr="amount",
    )
    return _dataframe(instances=instances, threshold=threshold, gtype=gtype)


def _df_payment_type(
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: GTYPE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    instances = swan.payments.grouped_instances(
        key="paymentMethodDisplayName",
        attr="amount",
    )
    return _dataframe(instances=instances, threshold=threshold, gtype=gtype)


def get_dataframe(
    code: Literal["rd", "rc", "is", "rs", "cd", "pm", "pt", "ic"],
    swan: SwiggyAnalytics,
    threshold: int,
    gtype: Optional[Literal["total", "average"]] = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    func_dict: dict[str, Callable[..., tuple[pd.DataFrame, pd.DataFrame]]] = {
        "rd": _df_restaurant_deltime,
        "rc": _df_restaurant_count,
        "is": _df_item_spending,
        "rs": _df_restaurant_spending,
        "cd": _df_coupon_discount,
        "pm": _df_payment_method,
        "pt": _df_payment_type,
        "ic": _df_item_count,
    }
    return (
        func_dict[code](swan=swan, threshold=threshold)
        if gtype is None
        else func_dict[code](swan=swan, threshold=threshold, gtype=gtype)
    )
