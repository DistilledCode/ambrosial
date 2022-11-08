import warnings
from collections import Counter, defaultdict
from typing import Literal

import numpy as np
import pandas as pd

from ambrosial.swan import SwiggyAnalytics

MONTH = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
WEEKDAY = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]
STRF_MAPPING = {
    "hour": "%H",
    "day": "%d",
    "week": "%w",
    "week_": "%A",
    "calweek": "%U",
    "month": "%m",
    "month_": "%B",
    "year": "%Y",
}


def get_dataframe(data: dict[str, int], bin_: list[str]) -> pd.DataFrame:
    drange = pd.date_range(start="2000-01-01", end="2000-12-31", freq="1H")
    for date in drange:
        data.setdefault(
            date.strftime(" ".join(STRF_MAPPING[b] for b in bin_)),
            np.NaN,
        )
    data_tuple = [(*key.split(" "), val) for key, val in data.items()]
    df = pd.DataFrame(data_tuple, columns=[*bin_, "value"])
    if "month_" in bin_:
        df["month_"] = pd.Categorical(df["month_"], categories=MONTH, ordered=True)
    if "week_" in bin_:
        df["week_"] = pd.Categorical(df["week_"], categories=WEEKDAY, ordered=True)
    df.sort_values(by=bin_, inplace=True)
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        return df.pivot(*bin_, "value")


def _offer_discount(swan: SwiggyAnalytics, bin_: list[str]) -> dict[str, int]:
    data: dict[str, int] = defaultdict(int)
    for order in swan.swiggy.get_orders():
        key = order.order_time.strftime(" ".join(STRF_MAPPING[b] for b in bin_))
        data[key] += int(sum(offer.total_offer_discount for offer in order.offers_data))
    return data


def _super_benefits(swan: SwiggyAnalytics, bin_: list[str]) -> dict[str, int]:
    return {
        key: int(val["total_benefit"])
        for key, val in swan.orders.tseries_super_benefits("+".join(bin_)).items()
    }


def _total_saving(swan: SwiggyAnalytics, bin_: list[str]) -> dict[str, int]:
    return dict(
        Counter(_super_benefits(swan, bin_)) + Counter(_offer_discount(swan, bin_))
    )


def _rest_del_time(swan: SwiggyAnalytics, bin_: list[str]) -> dict[str, int]:
    return {
        key: int(val["mean_actual"])
        for key, val in swan.orders.tseries_del_time("+".join(bin_)).items()
    }


def get_data(
    code: Literal["rdt", "od", "sb", "ts"],
    bin_: list[str],
    swan: SwiggyAnalytics,
) -> dict[str, int]:
    func_dict = {
        "rdt": _rest_del_time,
        "od": _offer_discount,
        "sb": _super_benefits,
        "ts": _total_saving,
    }
    return func_dict[code](swan, bin_)
