from typing import Callable, Literal

import pandas as pd

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.utils import remove_outliers


def _df_order_amount(swan: SwiggyAnalytics, **_: bool) -> pd.DataFrame:
    data = swan.orders.tseries_amount("per_minute_")
    df = pd.DataFrame(
        {
            "y": data.values(),
            "xlabel": [i.replace(" ", "\n") for i in list(data.keys())],
        }
    )
    df.insert(0, "x", range(len(df)))
    return df


def _df_ordamt_ordfeeprcnt(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    data_amt = swan.orders.tseries_amount("per_minute_")
    data_chrg = swan.orders.tseries_charges("per_minute_")
    amount = list(data_amt.values())
    total_charges = [sum(i.values()) for i in data_chrg.values()]
    charge_percnt = [chrg / amt * 100 for chrg, amt in zip(total_charges, amount)]
    if ro:
        remove_outliers(charge_percnt, amount)
    return pd.DataFrame({"x": amount, "y": charge_percnt})


def _df_ordamt_ordfee(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    data_amt = swan.orders.tseries_amount("per_minute_")
    data_fee = swan.orders.tseries_charges("per_minute_")
    total_amount = list(data_amt.values())
    total_fee = [sum(i.values()) for i in data_fee.values()]
    fee_prcnt = [fee / amt for fee, amt in zip(total_fee, total_amount)]
    if ro:
        remove_outliers(fee_prcnt, total_amount, total_fee)
    return pd.DataFrame({"x": total_fee, "y": total_amount, "color": fee_prcnt})


def _df_ordtime_orddist(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    distance: list[float] = []
    time_taken: list[float] = []
    for order in swan.swiggy.get_orders():
        if not order.mCancellationTime:
            distance.append(order.restaurant.customer_distance[1])
            time_taken.append(order.delivery_time_in_seconds / 60)
    if ro:
        remove_outliers(time_taken, distance)
    return pd.DataFrame({"x": distance, "y": time_taken})


def _df_ordtime_punctuality_bool(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    orders = swan.swiggy.get_orders()
    delivery_time: list[float] = []
    punctuality: list[bool] = []
    for order in orders:
        if not order.mCancellationTime:
            delivery_time.append(order.delivery_time_in_seconds / 60)
            punctuality.append(order.on_time)
    if ro:
        remove_outliers(delivery_time, punctuality)
    return pd.DataFrame({"x": delivery_time, "y": punctuality})


def _df_orddist_punctuality_bool(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    orders = swan.swiggy.get_orders()
    delivery_dist: list[float] = []
    punctuality: list[bool] = []
    for order in orders:
        if not order.mCancellationTime:
            delivery_dist.append(order.restaurant.customer_distance[1])
            punctuality.append(order.on_time)
    if ro:
        remove_outliers(delivery_dist, punctuality)
    return pd.DataFrame({"x": delivery_dist, "y": punctuality})


def _df_ordtime_punctuality(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    orders = swan.swiggy.get_orders()
    act_time: list[int] = []
    prom_time: list[int] = []
    sla_diff: list[int] = []
    for order in orders:
        if not order.mCancellationTime:
            act_time.append(order.actual_sla_time)
            prom_time.append(order.sla_time)
            sla_diff.append(order.sla_difference)
    if ro:
        remove_outliers(sla_diff, act_time, prom_time)
    return pd.DataFrame({"x": act_time, "y": prom_time, "color": sla_diff})


def _df_ordamt_offramt(swan: SwiggyAnalytics, ro: bool) -> pd.DataFrame:
    orders = swan.swiggy.get_orders()
    order_amount = []
    offer_amount = []
    offer_percentage = []
    for order in orders:
        if not order.mCancellationTime:
            order_amount.append(order.order_total)
            discount = sum(offer.total_offer_discount for offer in order.offers_data)
            offer_amount.append(discount)
            offer_percentage.append(discount / (discount + order.order_total))
    if ro:
        remove_outliers(order_amount, offer_amount, offer_percentage)
    return pd.DataFrame(
        {
            "x": order_amount,
            "y": offer_amount,
            "color": offer_percentage,
        }
    )


def get_dataframe(
    code: Literal[
        "oa",
        "oa_ofp",
        "oa_of",
        "ot_od",
        "ot_p_b",
        "ot_p",
        "od_p_b",
        "oa_oa",
    ],
    swan: SwiggyAnalytics,
    ro: bool,
) -> pd.DataFrame:
    func_dict: dict[str, Callable[..., pd.DataFrame]] = {
        "oa": _df_order_amount,
        "oa_ofp": _df_ordamt_ordfeeprcnt,
        "oa_of": _df_ordamt_ordfee,
        "ot_od": _df_ordtime_orddist,
        "ot_p_b": _df_ordtime_punctuality_bool,
        "ot_p": _df_ordtime_punctuality,
        "od_p_b": _df_orddist_punctuality_bool,
        "oa_oa": _df_ordamt_offramt,
    }

    return func_dict[code](swan, ro=ro)
