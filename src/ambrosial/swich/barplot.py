from typing import Any, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from july.rcmod import update_rcparams
from matplotlib.ticker import MaxNLocator

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.barplot import GTYPE, get_dataframe, get_display_order


class BarPlot:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def restaurant_deltime(
        self,
        threshold: int = 4,
        gtype: GTYPE = "average",
        errorbar: tuple[str, int] = ("ci", 95),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="rd", swan=self.swan, threshold=threshold, gtype=gtype)
        axis_labels = (f"{gtype.title()} Delivery Time (minutes)", "Restaurant")
        title = f"{gtype.title()} Delivery Time Of Restaurants"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            gtype=gtype,
            **kwargs,
        )

    def item_spending(
        self,
        threshold: int = 4,
        gtype: GTYPE = "total",
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="is", swan=self.swan, threshold=threshold, gtype=gtype)
        axis_labels = ("Amount Spent (₹)", "Item Name")
        title = f"{gtype.title()} Amount Spent on Items"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            gtype=gtype,
            **kwargs,
        )

    def restaurant_spending(
        self,
        threshold: int = 5,
        gtype: GTYPE = "total",
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="rs", swan=self.swan, threshold=threshold, gtype=gtype)
        axis_labels = ("Amount Spent (₹)", "Restaurant Name")
        title = f"{gtype.title()} Amount Spent in Restaurants"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            gtype=gtype,
            **kwargs,
        )

    def item_count(
        self,
        threshold: int = 4,
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="ic", swan=self.swan, threshold=threshold)
        axis_labels = ("Item Count", "Item Name")
        title = "Number of Items Ordered"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            **kwargs,
        )

    def restaurant_count(
        self,
        threshold: int = 5,
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="rc", swan=self.swan, threshold=threshold)
        axis_labels = ("Order Count", "Restaurant Name")
        title = "Number of Orders from Restaurant"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            **kwargs,
        )

    def coupon_discount(
        self,
        threshold: int = 0,
        gtype: GTYPE = "total",
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="cd", swan=self.swan, threshold=threshold, gtype=gtype)
        axis_labels = (f"{gtype.title()} Availed Discount (₹)", "Coupon Code")
        title = f"{gtype.title()} Availed Discount on Orders"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            gtype=gtype,
            **kwargs,
        )

    def payment_method(
        self,
        threshold: int = 0,
        gtype: GTYPE = "total",
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="pm", swan=self.swan, threshold=threshold, gtype=gtype)
        axis_labels = (f"{gtype.title()} Transaction Amount (₹)", "Payment Method")
        title = "Transaction Amount v/s Payment Method"
        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            gtype=gtype,
            **kwargs,
        )

    def payment_type(
        self,
        threshold: int = 0,
        gtype: GTYPE = "total",
        errorbar: tuple[str, int] = ("sd", 1),
        **kwargs: Any,
    ) -> None:
        df = get_dataframe(code="pt", swan=self.swan, threshold=threshold, gtype=gtype)
        axis_labels = (f"{gtype.title()} Transaction Amount (₹)", "Payment Type")
        title = "Transaction Amount v/s Payment Type"

        self._make_barplot(
            df=df,
            labels=(axis_labels, title),
            errorbar=errorbar,
            gtype=gtype,
            **kwargs,
        )

    def _make_barplot(
        self,
        df: tuple[pd.DataFrame, pd.DataFrame],
        labels: tuple[tuple[str, str], str],
        errorbar: tuple[str, int],
        gtype: Optional[GTYPE] = None,
        **kwargs: Any,
    ) -> plt.Axes:
        axis_labels, title = labels
        update_rcparams(
            titlepad=12,
            titlesize="large",
            fontsize=15,
            ymargin=0.02,
            xmargin=0.02,
        )
        display_order = get_display_order(df) if gtype == "average" else None
        bp = sns.barplot(
            data=df,
            x="x",
            y="y",
            order=display_order,
            errorbar=errorbar,
            capsize=0.2,
            errcolor=(1, 0, 0, 1),
            errwidth=1.25,
            linewidth=1.0,
            edgecolor=".1",
            facecolor=(0, 0, 0, 0),
            **kwargs,
        )
        bp.xaxis.set_major_locator(MaxNLocator(nbins=12))
        bp.set_title(title)
        bp.set_xlabel(axis_labels[0], labelpad=12)
        bp.set_ylabel(axis_labels[1], labelpad=12)
        bp.tick_params(labelsize=12)
        bp.grid(True, axis="x", ls=":")
        plt.subplots_adjust(left=0.225, right=0.975, top=0.925)
        return bp
