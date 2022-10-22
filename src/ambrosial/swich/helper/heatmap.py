import warnings

import numpy as np
import pandas as pd

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
