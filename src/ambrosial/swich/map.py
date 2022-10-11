from collections import Counter
from statistics import NormalDist

import folium
from folium.plugins import HeatMap

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.utils import get_curr_time
from ambrosial.swiggy.utils import create_path


class Map:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan
        self.save_path = self.swan.swiggy.home_path / "swich" / "map"
        self.noise = NormalDist(mu=0, sigma=0.00015)
        create_path(self.save_path)

    def order_count(self, city: str) -> None:
        # TODO: Add ption for custum tooltip format
        # TODO: Show number of orders as quantiles in Layer
        restaurants = [
            restaurant
            for restaurant in self.swan.swiggy.get_restaurants()
            if restaurant.city_name.lower() == city.lower()
        ]
        grouped = Counter(restaurants).most_common()
        weighted_coordinates = [
            (*list(i[0].coordinates.values()), i[1]) for i in grouped
        ]
        map_center_lat = 0.0
        map_center_lng = 0.0
        num = len(weighted_coordinates)
        for coordinate in weighted_coordinates:
            map_center_lat += coordinate[0] / num
            map_center_lng += coordinate[1] / num

        base_map = folium.Map(
            location=(map_center_lat, map_center_lng),
            tiles="stamentoner",
            zoom_start=12.5,
            control_scale=True,
        )
        restaurant_marker = folium.FeatureGroup("Restaurants")
        for rest in grouped:
            folium.Marker(
                location=tuple(
                    i + self.noise.samples(1)[0] for i in rest[0].coordinates.values()
                ),
                tooltip=folium.Tooltip(
                    text=f"<b>{rest[0].name}</b><br><center>Count: {rest[1]}</center>"
                ),
                icon=folium.Icon(color="green", icon="cutlery", prefix="fa"),
            ).add_to(restaurant_marker)
        folium.TileLayer().add_to(base_map)
        restaurant_marker.add_to(base_map)
        HeatMap(weighted_coordinates, name="Heatmap", blur=12.5, radius=30).add_to(
            base_map
        )
        folium.LayerControl().add_to(base_map)
        base_map.save(self.save_path / f"{get_curr_time()}order_count.html")
