import heapq
from typing import Any, Literal, Optional

import july
from matplotlib.pyplot import Axes

import ambrosial.swich.helper.ghubmap as helper
from ambrosial.swan import SwiggyAnalytics


class GitHubMap:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def order_amount(self, **kwargs: Any) -> Axes:
        return self._ghubmap_plot(
            code="oa",
            title="Total Amount Spent:",
            include_extreme_value_str=True,
            kwargs=kwargs,
        )

    def order_count(self, **kwargs: Any) -> Axes:
        return self._ghubmap_plot(
            code="oc",
            title="Total Order Count:",
            include_extreme_value_str=False,
            kwargs=kwargs,
        )

    def offer_discount(self, **kwargs: Any) -> Axes:
        return self._ghubmap_plot(
            code="od",
            title="Total Coupon Discount Availed:",
            include_extreme_value_str=True,
            kwargs=kwargs,
        )

    def super_benefits(self, **kwargs: Any) -> Axes:
        return self._ghubmap_plot(
            code="sb",
            title="Total Super Benefits Availed:",
            include_extreme_value_str=True,
            kwargs=kwargs,
        )

    def total_saving(self, **kwargs: Any) -> Axes:
        return self._ghubmap_plot(
            code="ts",
            title="Total Savings (Coupon + Super):",
            include_extreme_value_str=True,
            kwargs=kwargs,
        )

    def restaurant_count(
        self,
        restaurant_id: int,
        threshold: int = 3,
        **kwargs: Any,
    ) -> Optional[Axes]:
        return self._ghubmap_rest_plot(
            code="count",
            graph_info=(restaurant_id, threshold),
            title="Order count of:",
            include_extreme_value_str=False,
            kwargs=kwargs,
        )

    def restaurant_amount(
        self,
        restaurant_id: int,
        threshold: int = 3,
        **kwargs: Any,
    ) -> Optional[Axes]:
        return self._ghubmap_rest_plot(
            code="amount",
            graph_info=(restaurant_id, threshold),
            include_extreme_value_str=True,
            title="Amount spent for:",
            kwargs=kwargs,
        )

    def item_count(
        self,
        item_id: int,
        threshold: int = 3,
        **kwargs: Any,
    ) -> Optional[Axes]:
        return self._ghubmap_item_plot(
            code="count",
            graph_info=(item_id, threshold),
            title="Order count of:",
            include_extreme_value_str=False,
            kwargs=kwargs,
        )

    def item_amount(
        self,
        item_id: int,
        threshold: int = 3,
        **kwargs: Any,
    ) -> Optional[Axes]:
        """
        Inlcudes GST but excludes Packaging, Convenience, Cancellation,
        and Delivery Charges. Those are calculated for each order.
        """
        return self._ghubmap_item_plot(
            code="amount",
            graph_info=(item_id, threshold),
            include_extreme_value_str=True,
            title="Amount spent on:",
            kwargs=kwargs,
        )

    def _ghubmap_plot(
        self,
        code: Literal["oa", "oc", "od", "sb", "ts"],
        title: str,
        include_extreme_value_str: bool,
        kwargs: dict[str, Any],
    ) -> Axes:
        date_range_, values = helper.get_plot_values(code, self.swan)
        jargs = helper.july_heatmap_args(kwargs)
        title += f" {sum(values)}"
        if include_extreme_value_str:
            title += f"\n{helper.extreme_value_str(date_range_, values)}"
        return july.heatmap(
            dates=date_range_,
            data=values,
            title=title,
            cmin=int(heapq.nsmallest(2, set(values))[-1] * 0.75),
            **jargs,
        )

    def _ghubmap_rest_plot(
        self,
        code: Literal["count", "amount"],
        graph_info: tuple[int, int],
        title: str,
        include_extreme_value_str: bool,
        kwargs: dict[str, Any],
    ) -> Optional[Axes]:
        restaurant_id, threshold = graph_info
        restaurant, orders = helper.get_grouped_restaurant(self.swan, restaurant_id)
        date_range_, values = helper.restaurant_plot_value(code, orders)
        actual_values = [value for value in values if value > 0]
        if len(actual_values) < threshold:
            return None
        jargs = helper.july_heatmap_args(kwargs)
        title += f" {restaurant.name}, {restaurant.area_name} ({restaurant.rest_id})"
        title += f"\nTotal: {round(sum(actual_values),2)}"
        if include_extreme_value_str:
            title += f" | {helper.extreme_value_str(date_range_, values)}"

        return july.heatmap(
            dates=date_range_,
            data=values,
            title=title,
            cmin=int(heapq.nsmallest(2, set(values))[-1] * 0.70),
            **jargs,
        )

    def _ghubmap_item_plot(
        self,
        code: Literal["count", "amount"],
        graph_info: tuple[int, int],
        title: str,
        include_extreme_value_str: bool,
        kwargs: dict[str, Any],
    ) -> Optional[Axes]:
        item_id, threshold = graph_info
        item, orders = helper.get_grouped_item(self.swan, item_id)
        date_range_, values = helper.item_plot_value(code, orders)
        actual_values = [value for value in values if value > 0]
        if len(actual_values) < threshold:
            return None
        jargs = helper.july_heatmap_args(kwargs)
        restaurant = self.swan.swiggy.get_restaurant(restaurant_id=item.restaurant_id)
        title += f" {item.name} ({item.item_id})"
        title += f"\nRestaurant: {restaurant.name}, {restaurant.area_name}"
        title += f"\nTotal: {sum(actual_values)}"
        if include_extreme_value_str:
            title += f" | {helper.extreme_value_str(date_range_, values)}"
        return july.heatmap(
            dates=date_range_,
            data=values,
            title=title,
            cmin=int(heapq.nsmallest(2, set(values))[-1] * 0.70),
            **jargs,
        )
