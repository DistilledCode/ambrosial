import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from july.rcmod import update_rcparams
from palettable.lightbartlein import diverging

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper.regression import get_dataframe
from ambrosial.swich.utils import CustomFormatter, CustomLocator

BINS = "per_minute_"


class RegressionPlot:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan
        self.cmap = diverging.BlueOrange8_8_r.mpl_colormap
        self.scatter_kws_cb = {
            "color": None,
            "edgecolor": "black",
            "alpha": 0.80,
            "s": 80,
        }
        self.scatter_kws = {
            "color": "lawngreen",
            "edgecolor": "black",
            "alpha": 0.70,
            "s": 80,
        }
        self.line_kws_cb = {"color": "black", "linewidth": 3.0}
        self.line_kws = {"color": "tomato", "linewidth": 3.0}
        sns.set_theme(style="ticks")

    def order_amount(self, bins: str = BINS) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="oa", swan=self.swan, bins=bins)

        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            line_kws=self.line_kws,
            scatter_kws=self.scatter_kws,
        )
        p.set_xticks(range(0, len(df), len(df) // 6))
        p.set_xticklabels(df["xlabel"][:: len(df) // 6])

        p.set_title(f'Order Total\nbins="{bins}"', fontsize=15)
        p.set_xlabel("")
        p.set_ylabel("Order Total    (in ₹)", fontsize=15)

    def ordamt_ordfeeprcnt(
        self,
        bins: str = BINS,
        remove_outliers: bool = True,
    ) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="oa_ofp", swan=self.swan, bins=bins, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            line_kws=self.line_kws,
            scatter_kws=self.scatter_kws,
        )
        p.set_title(f'Fee Percentage v/s Order Total\nbins="{bins}"', fontsize=15)
        p.set_xticks([int(i) for i in np.linspace(min(df["x"]), max(df["x"]), 10)])
        p.set_yticks([float(i) for i in np.linspace(min(df["y"]), max(df["y"]), 10)])
        p.set_ylabel("Fee as % of Order Total\n", fontsize=15)
        p.set_xlabel("Order Total    (in ₹)", fontsize=15)

    def ordamt_ordfee(self, bins: str = BINS, remove_outliers: bool = True) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="oa_of", swan=self.swan, bins=bins, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            line_kws=self.line_kws_cb,
            scatter_kws={**self.scatter_kws_cb, "c": df["color"], "cmap": self.cmap},
        )
        p.set_title(f'Order Total v/s Order Fee\nbins="{bins}"', fontsize=15)
        p.set_xticks([int(i) for i in np.linspace(min(df["x"]), max(df["x"]), 10)])
        p.set_yticks([int(i) for i in np.linspace(min(df["y"]), max(df["y"]), 10)])
        p.set_xlabel("Order Fee    (in ₹)", fontsize=15)
        p.set_ylabel("Order Total    (in ₹)", fontsize=15)
        sm = plt.cm.ScalarMappable(cmap=self.cmap)
        sm.set_array([])
        ax = p.figure.get_axes()
        cbar = p.figure.colorbar(
            sm,
            ax=ax,
            ticks=CustomLocator(ticks=10),
            format=CustomFormatter(vmin=min(df["color"]), vmax=max(df["color"])),
        )
        cbar.set_label(
            """
                        Fee as % of
                        Order Total
            """,
            size=15,
            rotation="horizontal",
        )
        # robust and order are mutually exclusive

    def ordtime_orddist(self, remove_outliers: bool = True) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="ot_od", swan=self.swan, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            line_kws=self.line_kws,
            scatter_kws=self.scatter_kws,
        )
        p.set_title("Order Delivery Time v/s Order Distance", fontsize=15)
        p.set_xticks(
            [
                round(float(i), 2)
                for i in np.linspace(
                    min(df["x"]),
                    max(df["x"]),
                    10,
                )
            ]
        )
        p.set_yticks(
            [
                round(float(i), 2)
                for i in np.linspace(
                    min(df["y"]),
                    max(df["y"]),
                    10,
                )
            ]
        )
        p.set_xlabel("Order Distance  (kms)", fontsize=15)
        p.set_ylabel("Order Delivery Time  (minutes)\n", fontsize=15)

    def ordtime_punctuality_bool(self, remove_outliers: bool = True) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="ot_p_b", swan=self.swan, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            logistic=True,
            y_jitter=0.15,
            line_kws=self.line_kws,
            scatter_kws=self.scatter_kws,
        )
        p.set_title("Punctuality v/s Order Delivery Time\n", fontsize=15)
        p.set_xticks(
            [
                round(float(i), 2)
                for i in np.linspace(
                    min(df["x"]),
                    max(df["x"]),
                    10,
                )
            ]
        )
        p.set_yticks([0, 1])
        p.set_yticklabels(["No", "Yes"])
        p.set_xlabel("Order Delivery Time  (minutes)", fontsize=15)
        p.set_ylabel("Was Order On Time\n", fontsize=15)

    def orddist_punctuality_bool(self, remove_outliers: bool = True) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="od_p_b", swan=self.swan, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            logistic=True,
            y_jitter=0.15,
            line_kws=self.line_kws,
            scatter_kws=self.scatter_kws,
        )
        p.set_title("Punctuality v/s Order Distance\n", fontsize=15)
        p.set_xticks(
            [
                round(float(i), 2)
                for i in np.linspace(
                    min(df["x"]),
                    max(df["x"]),
                    10,
                )
            ]
        )
        p.set_yticks([0, 1])
        p.set_yticklabels(["No", "Yes"])
        p.set_xlabel("Order Distance (km)", fontsize=15)
        p.set_ylabel("Was Order On Time\n", fontsize=15)

    def ordtime_punctuality(self, remove_outliers: bool = True) -> None:
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="ot_p", swan=self.swan, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            line_kws=self.line_kws_cb,
            scatter_kws={**self.scatter_kws_cb, "c": df["color"], "cmap": self.cmap},
        )
        p.set_title(
            "Promised Delivery Time v/s Actual Delivery Time\n"
            "SLA Difference = Promised Time - Actual Time",
            fontsize=15,
        )
        p.set_xticks(np.linspace(min(df["x"]), max(df["x"]), 10))
        p.set_yticks(np.linspace(min(df["y"]), max(df["y"]), 10))
        p.set_xlabel("Actual Delivery Time  (minutes)", fontsize=15)
        p.set_ylabel("Promised Delivery Time  (minutes)", fontsize=15)
        sm = plt.cm.ScalarMappable(cmap=self.cmap)
        sm.set_array([])
        ax = p.figure.get_axes()
        cbar = p.figure.colorbar(
            sm,
            ax=ax,
            ticks=CustomLocator(ticks=10),
            format=CustomFormatter(vmax=max(df["color"]), vmin=min(df["color"])),
        )
        cbar.set_label(
            """
                SLA
                Difference
            """,
            size=15,
            rotation="horizontal",
        )

    def ordamt_offramt(self, remove_outliers: bool = True) -> None:
        # TODO: add kwarg option for different properties like axes
        # TODO: also add option to make a regression line or not
        # without regeression line it's just a good ol scatter plot
        # TODO: Categorical plot wherever applicable
        update_rcparams(xmargin=0.05, ymargin=0.05, titlepad=20)
        df = get_dataframe(code="oa_oa", swan=self.swan, ro=remove_outliers)
        p = sns.regplot(
            data=df,
            x="x",
            y="y",
            scatter=True,
            truncate=True,
            fit_reg=True,
            order=1,
            line_kws=self.line_kws_cb,
            scatter_kws={**self.scatter_kws_cb, "c": df["color"], "cmap": self.cmap},
        )
        p.set_title(
            "Offer Amount Availed v/s Order Amount Paid",
            fontsize=15,
        )
        p.set_xticks(np.linspace(min(df["x"]), max(df["x"]), 10))
        p.set_yticks(np.linspace(min(df["y"]), max(df["y"]), 10))
        p.set_xlabel("Order Amount Paid  (₹)", fontsize=15, labelpad=10)
        p.set_ylabel("Offer Amount Availed  (₹)", fontsize=15, labelpad=10)
        p.grid(True, axis="both", ls=":")
        sm = plt.cm.ScalarMappable(cmap=self.cmap)
        sm.set_array([])
        ax = p.figure.get_axes()
        cbar = p.figure.colorbar(
            sm,
            ax=ax,
            ticks=CustomLocator(ticks=10),
            format=CustomFormatter(vmax=max(df["color"]), vmin=min(df["color"])),
        )
        cbar.set_label(
            """
                Offer Saving
                (in percent)
            """,
            size=15,
            rotation="horizontal",
        )
