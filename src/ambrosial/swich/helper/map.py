from typing import Sequence

from ambrosial.swiggy.datamodel.order import Order
from ambrosial.swiggy.datamodel.restaurant import Restaurant

ZERO_MILE_STONE = (21.149850, 79.080598)


def _get_center(w_coords: list[tuple[float, ...]]) -> tuple[float, float]:
    map_center_lat, map_center_lng = 0.0, 0.0
    num = len(w_coords)
    for coordinate in w_coords:
        map_center_lat += coordinate[0] / num
        map_center_lng += coordinate[1] / num
    return map_center_lat, map_center_lng


def get_coords_oa(
    instances: dict[Restaurant, list[Order]],
    nationwide: bool,
) -> tuple[list[tuple[float, ...]], tuple[float, float]]:

    w_coords = [
        (
            *list(restaurant.coordinates.values()),
            sum(order.order_total for order in orders),
        )
        for restaurant, orders in instances.items()
    ]
    center_coords = ZERO_MILE_STONE if nationwide else _get_center(w_coords)
    return w_coords, center_coords


def get_coords_oc(
    grouped: Sequence[tuple[Restaurant, int]],
    nationwide: bool,
) -> tuple[list[tuple[float, ...]], tuple[float, float]]:
    w_coords = [(*list(i[0].coordinates.values()), i[1]) for i in grouped]
    center_coords = ZERO_MILE_STONE if nationwide else _get_center(w_coords)
    return w_coords, center_coords
