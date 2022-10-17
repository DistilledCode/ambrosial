from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.barplot import get_dataframe

ORDER_BY_LITERALS = Literal["count", "total", "std_dev"]


class BarPlot:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def restaurant_deltime(
        self,
        threshold: int = 4,
        order_by: ORDER_BY_LITERALS = "count",
        ascending: bool = False,
        errorbar: tuple[str, int] = ("ci", 95),
    ) -> None:
        df, ordering_df = get_dataframe(code="rd", swan=self.swan, threshold=threshold)
        ordering_df.sort_values(by=[order_by], inplace=True, ascending=ascending)
        order_title_dict = {
            "count": "Number of Orders",
            "total": "Total Delivery Time",
            "average": "Average Delivery Time",
            "std_dev": "Std. Dev. of Delivery Time",
        }
        self._make_barplot(
            dataframes=(df, ordering_df),
            ordering_info=(order_by, order_title_dict),
            ascending=ascending,
            errorbar=errorbar,
            axis_labels=("Avg Delivery Time (minutes)", "Restaurant"),
        )

    def item_spending(
        self,
        threshold: int = 4,
        order_by: ORDER_BY_LITERALS = "total",
        ascending: bool = False,
        errorbar: tuple[str, int] = ("sd", 1),
    ) -> None:
        df, ordering_df = get_dataframe(code="is", swan=self.swan, threshold=threshold)
        ordering_df.sort_values(by=[order_by], inplace=True, ascending=ascending)
        order_title_dict = {
            "count": "Item Count",
            "totalal": "Total Amount Paid",
            "std_dev": "Std. Dev. of Item Cost",
        }
        self._make_barplot(
            dataframes=(df, ordering_df),
            ordering_info=(order_by, order_title_dict),
            ascending=ascending,
            errorbar=errorbar,
            axis_labels=("Average Item Cost", "Item Name"),
        )

    def coupon_discount(
        self,
        threshold: int = 0,
        order_by: ORDER_BY_LITERALS = "total",
        ascending: bool = False,
        errorbar: tuple[str, int] = ("sd", 1),
    ) -> None:
        df, ordering_df = get_dataframe(code="od", swan=self.swan, threshold=threshold)
        ordering_df.sort_values(by=[order_by], inplace=True, ascending=ascending)
        order_title_dict = {
            "count": "Coupon Count",
            "total": "Total Discount Availed",
            "std_dev": "Std. Dev. of Discount Availed",
        }
        self._make_barplot(
            dataframes=(df, ordering_df),
            ordering_info=(order_by, order_title_dict),
            ascending=ascending,
            errorbar=errorbar,
            axis_labels=("Average Discount Availed", "Coupon Code"),
        )

    def payment_method(
        self,
        threshold: int = 0,
        order_by: ORDER_BY_LITERALS = "total",
        ascending: bool = False,
        errorbar: tuple[str, int] = ("sd", 1),
    ) -> None:
        df, ordering_df = get_dataframe(code="pm", swan=self.swan, threshold=threshold)
        ordering_df.sort_values(by=[order_by], inplace=True, ascending=ascending)
        order_title_dict = {
            "count": "Method Count",
            "total": "Total Payment Made",
            "std_dev": "Std. Dev. of Amount Transacted",
        }
        self._make_barplot(
            dataframes=(df, ordering_df),
            ordering_info=(order_by, order_title_dict),
            ascending=ascending,
            errorbar=errorbar,
            axis_labels=("Average Amount Per Transaction", "Payment Method"),
        )

    def payment_type(
        self,
        threshold: int = 0,
        order_by: ORDER_BY_LITERALS = "total",
        ascending: bool = False,
        errorbar: tuple[str, int] = ("sd", 1),
    ) -> None:
        df, ordering_df = get_dataframe(code="pt", swan=self.swan, threshold=threshold)
        ordering_df.sort_values(by=[order_by], inplace=True, ascending=ascending)
        order_title_dict = {
            "count": "Type Count",
            "total": "Total Payment Made",
            "std_dev": "Std. Dev. of Amount Transacted",
        }
        self._make_barplot(
            dataframes=(df, ordering_df),
            ordering_info=(order_by, order_title_dict),
            ascending=ascending,
            errorbar=errorbar,
            axis_labels=("Average Amount Per Transaction", "Payment Type"),
        )

    def _make_barplot(
        self,
        dataframes: tuple[pd.DataFrame, pd.DataFrame],
        ordering_info: tuple[ORDER_BY_LITERALS, dict[str, str]],
        axis_labels: tuple[str, str],
        ascending: bool,
        errorbar: tuple[str, int],
    ) -> None:
        dataframe, ordering_dataframe = dataframes
        order_by, order_title_dict = ordering_info
        order = ordering_dataframe["category_name"]
        grid = sns.JointGrid(ratio=3, space=0.1, marginal_ticks=True)
        sns.barplot(
            data=ordering_dataframe,
            y="category_name",
            x=order_by,
            order=order,
            facecolor=(0, 0, 0, 0),
            edgecolor=".5",
            ax=grid.ax_marg_y,
        )
        sns.barplot(
            data=dataframe,
            x="x",
            y="y",
            order=order,
            errorbar=errorbar,
            capsize=0.2,
            errcolor=(1, 0, 0, 1),
            errwidth=1.25,
            linewidth=1.25,
            edgecolor=".1",
            facecolor=(0, 0, 0, 0),
            ax=grid.ax_joint,
        )
        order_title = order_title_dict.get(order_by)
        grid.ax_marg_y.set_title(order_title)
        title = f"Order of Labels: {order_title}\n{ascending = }; {errorbar = }"
        grid.ax_joint.set_title(title)
        grid.set_axis_labels(*axis_labels)
        grid.ax_marg_y.tick_params(labelbottom=True)
        grid.ax_marg_y.grid(True, axis="x", ls=":")
        grid.ax_joint.grid(True, axis="x", ls=":")
        grid.ax_marg_y.xaxis.set_major_locator(MaxNLocator(6))
        grid.ax_marg_x.remove()
        plt.subplots_adjust(left=0.20, top=1.25)
