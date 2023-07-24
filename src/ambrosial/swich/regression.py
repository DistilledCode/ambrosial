from typing import Any, Literal, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from july.rcmod import update_rcparams
from matplotlib.pyplot import Axes
from matplotlib.ticker import MaxNLocator
from palettable.lightbartlein import diverging

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.regression import get_dataframe
from ambrosial.swich.utils import CustomFormatter, CustomLocator


class RegressionPlot:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan
        self.cmap = diverging.BlueOrange8_8_r.mpl_colormap
        self.scatter_kw_cb = {
            "color": None,
            "edgecolor": "black",
            "alpha": 0.80,
            "s": 80,
        }
        self.scatter_kw = {
            "color": "lawngreen",
            "edgecolor": "black",
            "alpha": 0.70,
            "s": 80,
        }
        self.line_kw_cb = {"color": "black", "linewidth": 3.0}
        self.line_kw = {"color": "tomato", "linewidth": 3.0}
        sns.set_theme(style="ticks")

    @property
    def maxnlocator(self) -> MaxNLocator:
        return MaxNLocator(nbins=10)

    def order_amount(self, **kwargs: Any) -> Axes:
        graph = self._make_regplot(code="oa", cbar=False, ro=False, **kwargs)
        return self._label_graph(
            graph=graph,
            title="Order Total",
            labels=("Order Count Over Time", "Order Total (in ₹)"),
        )

    def ordamt_ordfeeprcnt(self, remove_outliers: bool = True) -> Axes:
        graph = self._make_regplot(code="oa_ofp", cbar=False, ro=remove_outliers)
        return self._label_graph(
            graph=graph,
            title="Fee Percentage v/s Order Total",
            labels=("Order Total (in ₹)", "Fee as % of Order Total"),
        )

    def ordamt_ordfee(self, remove_outliers: bool = True) -> Axes:
        graph = self._make_regplot(
            code="oa_of",
            cbar=True,
            ro=remove_outliers,
            cbar_label="\tFee as % of\n\tOrder Total".expandtabs(tabsize=12),
        )
        return self._label_graph(
            graph=graph,
            title="Order Total v/s Order Fee",
            labels=("Order Fee (in ₹)", "Order Total (in ₹)"),
        )
        # robust and order are mutually exclusive

    def ordtime_orddist(self, remove_outliers: bool = True) -> Axes:
        graph = self._make_regplot(code="ot_od", cbar=False, ro=remove_outliers)
        return self._label_graph(
            graph=graph,
            title="Order Delivery Time v/s Order Distance",
            labels=("Order Distance (kms)", "Order Delivery Time (minutes)"),
        )

    def ordtime_punctuality_bool(self, remove_outliers: bool = True) -> Axes:
        graph = self._make_regplot(
            code="ot_p_b",
            cbar=False,
            ro=remove_outliers,
            logistic=True,
            y_jitter=0.15,
        )

        return self._label_graph(
            graph=graph,
            title="Punctuality v/s Order Delivery Time",
            labels=("Order Delivery Time (minutes)", "Was Order On Time\n"),
            y_tick_info=([0, 1], ["No", "Yes"]),
        )

    def orddist_punctuality_bool(self, remove_outliers: bool = True) -> Axes:
        graph = self._make_regplot(
            code="od_p_b",
            cbar=False,
            ro=remove_outliers,
            logistic=True,
            y_jitter=0.15,
        )
        return self._label_graph(
            graph=graph,
            title="Punctuality v/s Order Distance",
            labels=("Order Distance (kms)", "Was Order On Time\n"),
            y_tick_info=([0, 1], ["No", "Yes"]),
        )

    def ordtime_punctuality(self, remove_outliers: bool = True) -> Axes:
        cbar_label = "\tSLA\n\tDifference".expandtabs(tabsize=12)
        graph = self._make_regplot(
            code="ot_p",
            cbar=True,
            cbar_label=cbar_label,
            ro=remove_outliers,
        )
        title = (
            "Promised Delivery Time v/s Actual Delivery Time\n"
            "SLA Difference = Promised Time - Actual Time"
        )
        x_label = "Actual Delivery Time (minutes)"
        y_label = "Promised Delivery Time (minutes)"
        return self._label_graph(graph=graph, title=title, labels=(x_label, y_label))

    def ordamt_offramt(self, remove_outliers: bool = True) -> Axes:
        # TODO: add kwarg option for different properties like axes
        # TODO: also add option to make a regression line or not
        # without regeression line it's just a good ol scatter plot
        # TODO: Categorical plot wherever applicable
        graph = self._make_regplot(
            code="oa_oa",
            cbar=True,
            cbar_label="\tOffer Saving\n\t(in percent)".expandtabs(tabsize=12),
            ro=remove_outliers,
        )
        return self._label_graph(
            graph=graph,
            title="Offer Amount Availed v/s Order Amount Paid",
            labels=("Order Amount Paid (₹)", "Offer Amount Availed (₹)"),
        )

    def _make_regplot(
        self,
        code: Literal[
            "oa",
            "oa_ofp",
            "oa_of",
            "ot_od",
            "ot_p_b",
            "od_p_b",
            "ot_p",
            "oa_oa",
        ],
        cbar: bool,
        ro: bool,
        cbar_label: Optional[str] = None,
        **reg_kwargs: Any,
    ) -> Axes:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code, self.swan, ro)
        if cbar:
            sc_kw = {"c": df["color"], "cmap": self.cmap}
            sc_kw = {**sc_kw, **self.scatter_kw_cb}
        graph = sns.regplot(
            data=df,
            x="x",
            y="y",
            truncate=True,
            scatter=reg_kwargs.pop("scatter", True),
            fit_reg=reg_kwargs.pop("fit_reg", True),
            logistic=reg_kwargs.pop("logistic", False),
            y_jitter=reg_kwargs.pop("y_jitter", 0.0),
            order=reg_kwargs.pop("order", 1),
            line_kws=self.line_kw_cb if cbar else self.line_kw,
            scatter_kws={**sc_kw} if cbar else self.scatter_kw,
        )

        if cbar is True and cbar_label is not None:
            return self._make_cbar(graph, df, cbar_label)
        return graph

    def _make_cbar(self, graph: Axes, df: pd.DataFrame, label: str) -> Axes:
        sm = plt.cm.ScalarMappable(cmap=self.cmap)
        sm.set_array([])
        ax = graph.figure.get_axes()
        cbar = graph.figure.colorbar(
            sm,
            ax=ax,
            ticks=CustomLocator(ticks=10),
            format=CustomFormatter(vmax=max(df["color"]), vmin=min(df["color"])),
        )
        cbar.set_label(label, size=15, rotation="horizontal")
        return graph

    def _label_graph(
        self,
        graph: Axes,
        title: str,
        labels: tuple[str, str],
        x_tick_info: Optional[tuple[list, list]] = None,
        y_tick_info: Optional[tuple[list, list]] = None,
    ) -> Axes:
        x_label, y_label = labels
        graph.set_title(title, fontsize=15)
        graph.set_xlabel(x_label, fontsize=15, labelpad=10)
        graph.set_ylabel(y_label, fontsize=15, labelpad=10)
        if x_tick_info is None:
            graph.xaxis.set_major_locator(self.maxnlocator)
        else:
            xticks, xtick_labels = x_tick_info
            graph.set_xticks(xticks)
            graph.set_xticklabels(xtick_labels)
        if y_tick_info is None:
            graph.yaxis.set_major_locator(self.maxnlocator)
        else:
            yticks, ytick_labels = y_tick_info
            graph.set_yticks(yticks)
            graph.set_yticklabels(ytick_labels)
        graph.grid(True, axis="both", ls=":")
        return graph
