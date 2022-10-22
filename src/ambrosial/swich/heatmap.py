from typing import Any

import seaborn as sns
from july import colormaps, rcmod
from matplotlib.pyplot import Axes

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.heatmap import get_dataframe


class HeatMap:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan
        self.pattern = (
            r"The number of FixedLocator locations \([0-9]+\), "
            r"usually from a call to set_ticks, "
            r"does not match the number of ticklabels \([0-9]+\)."
        )

    def order_amount(
        self,
        bins: str = "month_+week_",
        drop_empty: bool = True,
        **hm_kwargs: Any,
    ) -> Axes:
        bin_ = self._get_bin_list(bins)
        data = self.swan.orders.tseries_amount(bins)

        return self._make_heatmap(
            data=data,
            bin_=bin_,
            drop_empty=drop_empty,
            title="Order Amount",
            **hm_kwargs,
        )

    def order_count(
        self,
        bins: str = "month_+day",
        drop_empty: bool = True,
        **hm_kwargs: Any,
    ) -> Axes:
        bin_ = self._get_bin_list(bins)
        data = self.swan.orders.tseries_orders(bins)

        return self._make_heatmap(
            data=data,
            bin_=bin_,
            drop_empty=drop_empty,
            title="Order Count",
            **hm_kwargs,
        )

    def _get_bin_list(self, bins: str) -> list[str]:
        bin_ = [attr for attr in bins.split("+") if attr]
        bin_ = list(dict.fromkeys(bin_))
        if len(bin_) != 2:
            raise ValueError(
                "Exactly two unique keys required for creating Heatmap. "
                f"{len(bin_)} given: {bin_}"
            )
        return bin_

    def _make_heatmap(
        self,
        data: dict[str, int],
        bin_: list[str],
        drop_empty: bool,
        title: str,
        **hm_kwargs: Any,
    ) -> Axes:
        rcmod.update_rcparams()
        df = get_dataframe(data=data, bin_=bin_)
        if drop_empty:
            df.dropna(axis=1, how="all", inplace=True)
            df.dropna(axis=0, how="all", inplace=True)
        hm = sns.heatmap(
            df,
            annot=hm_kwargs.pop("annot", True),
            fmt=hm_kwargs.pop("fmt", "g"),
            linewidths=hm_kwargs.pop("linewidths", 2.0),
            cmap=hm_kwargs.pop("cmap", colormaps.cmaps_dict["golden"]),
            square=hm_kwargs.pop("square", True),
            cbar=hm_kwargs.pop("cbar", False),
            xticklabels=True,
            yticklabels=True,
            **hm_kwargs,
        )
        hm.set_title(title, fontsize=15)
        return hm
