from collections import Counter
from statistics import NormalDist
from typing import Any, Optional

import folium
from folium.plugins import HeatMap, MarkerCluster

import ambrosial.swich.helper.map as helper
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.utils import get_curr_time
from ambrosial.swiggy.datamodel.restaurant import Restaurant
from ambrosial.swiggy.utils import create_path


# TODO: time series version of these maps?
#  https://www.kaggle.com/code/imoore/easy-tutorial-for-plotting-with-python/notebook
class Map:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan
        self.save_path = self.swan.swiggy.home_path / "swich" / "map"
        self.ndist = NormalDist(mu=0, sigma=0.00015)
        self.popup_frmt = (
            "<center><b>{name}, {area_name}<br>"
            "{customer_distance[1]} kms from {customer_distance[0]}<br>"
            "Value: {value}/{total}<br>"
            "<a href='{cover_image}'>Cover Image</a></b></center>"
        )
        self.hover_frmt = "<b>{name}, {area_name}</b>"
        create_path(self.save_path)

    @property
    def noise(self) -> float:
        return self.ndist.samples(1)[0]

    def count_density(
        self,
        city: Optional[str] = None,
        nationwide: bool = False,
        hover_frmt: Optional[str] = None,
        popup_frmt: Optional[str] = None,
        save: bool = True,
    ) -> folium.Map:
        if city:
            restaurants = [
                restaurant
                for restaurant in self.swan.swiggy.get_restaurants()
                if restaurant.city_name.lower() == city.lower()
            ]

        else:
            restaurants = self.swan.swiggy.get_restaurants()
        # restaurants = (
        #     self.swan.swiggy.get_restaurants()
        #     if city is None and nationwide is True
        #     else (
        #         restaurant
        #         for restaurant in self.swan.swiggy.get_restaurants()
        #         if restaurant.city_name.lower() == city.lower()
        #     )
        # )
        grouped = Counter(restaurants).most_common()
        return self._make_map(
            grouped=grouped,
            nationwide=nationwide,
            popup_frmt=popup_frmt,
            hover_frmt=hover_frmt,
            save=save,
        )

    def amount_density(
        self,
        city: Optional[str] = None,
        nationwide: bool = False,
        hover_frmt: Optional[str] = None,
        popup_frmt: Optional[str] = None,
        save: bool = True,
    ) -> folium.Map:
        all_instances = self.swan.orders.grouped_instances(key="restaurant")
        if city:
            filtered_instances = {
                restaurant: orders
                for restaurant, orders in all_instances.items()
                if restaurant.city_name.lower() == city.lower()
            }

        else:
            filtered_instances = all_instances

        grouped = [
            (restaurant, sum(order.order_total for order in orders))
            for restaurant, orders in filtered_instances.items()
        ]

        return self._make_map(
            grouped=grouped,
            nationwide=nationwide,
            popup_frmt=popup_frmt,
            hover_frmt=hover_frmt,
            save=save,
        )

    def _get_base_map(self, center: tuple[float, float], nw: bool) -> folium.Map:
        return folium.Map(
            location=center,
            tiles="stamentoner",
            zoom_start=4 if nw else 10,
            control_scale=True,
        )

    def _get_marker(
        self,
        coordinates: tuple[float, ...],
        frmt_dict: dict[str, Any],
        hover_frmt: str,
        popup_frmt: str,
    ) -> folium.Marker:
        return folium.Marker(
            location=tuple(i + self.noise for i in coordinates),
            icon=folium.Icon(color="green", icon="cutlery", prefix="fa"),
            tooltip=folium.Tooltip(text=hover_frmt.format(**frmt_dict)),
            popup=folium.Popup(
                html=popup_frmt.format(**frmt_dict),
                max_width=250,
                sticky=True,
            ),
        )

    def _make_map(
        self,
        grouped: list[tuple[Restaurant, int]],
        nationwide: bool,
        popup_frmt: Optional[str],
        hover_frmt: Optional[str],
        save: bool,
    ) -> folium.Map:
        popup_frmt = self.popup_frmt if popup_frmt is None else popup_frmt
        hover_frmt = self.hover_frmt if hover_frmt is None else hover_frmt

        weighted_coords, center_coords = helper.get_coords_oc(grouped, nationwide)
        total = sum(i[2] for i in weighted_coords)
        base_map = self._get_base_map(center_coords, nationwide)
        individual_layer = folium.FeatureGroup("Individual")
        cluster_layer = MarkerCluster(name="Cluster")
        for restaurant, value in grouped:
            frmt_dict = {**restaurant.dict(), "value": value, "total": total}
            individual_marker = self._get_marker(
                coordinates=tuple(restaurant.coordinates.values()),
                frmt_dict=frmt_dict,
                popup_frmt=popup_frmt,
                hover_frmt=hover_frmt,
            )
            cluster_marker = self._get_marker(
                coordinates=tuple(restaurant.coordinates.values()),
                frmt_dict=frmt_dict,
                popup_frmt=popup_frmt,
                hover_frmt=hover_frmt,
            )
            cluster_marker.add_to(cluster_layer)
            individual_marker.add_to(individual_layer)
        folium.TileLayer("OpenStreetMap").add_to(base_map)
        folium.TileLayer("stamenwatercolor").add_to(base_map)
        individual_layer.add_to(base_map)
        cluster_layer.add_to(base_map)
        HeatMap(weighted_coords, name="Heatmap", blur=5, radius=20).add_to(base_map)
        folium.LayerControl().add_to(base_map)
        if save:
            base_map.save(self.save_path / f"{get_curr_time()}order_count.html")
        return base_map
