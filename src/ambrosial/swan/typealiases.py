from datetime import datetime
from typing import Literal, TypedDict, Union

from pydantic import HttpUrl

# from ambrosial.swiggy.datamodel.item import Item
# from ambrosial.swiggy.datamodel.order import Order
from ambrosial.swiggy.datamodel.typealiases import OfferTypeHint, OrderTypeHint

# from ambrosial.swiggy.datamodel.address import Address


class Coordindates(TypedDict):
    id_version: str
    annotation: str
    latitude: float
    longitude: float


class OrderHistory(TypedDict):
    order_id: int
    order_time: datetime


class DeliveryTimeStats(TypedDict):
    mean: Union[int, float]
    median: Union[int, float]
    std_dev: Union[int, float]
    maximum: Union[int, float]
    minimum: Union[int, float]
    total_deliveries: int


class ItemSummary(TypedDict):
    total_quantity: int
    avg_base_price: float
    total_base_price: float
    total_discount: float
    total_actual_cost: float
    total_tax: float
    avg_actual_cost: float
    image_url: HttpUrl
    received_for_free: int


class RestaurantSummary(TypedDict):
    name: str
    restaurant_id: int
    count: int
    total_spent: int
    avg_spent: float
    total_saving: float
    avg_saving: float
    saving_percentage: float
    total_charges: float
    avg_charges: float
    total_distance: float
    items_ordered: dict[str, int]
    weekday_frequency: dict[str, int]
    hour_frequency: dict[str, int]
    image_url: HttpUrl


class DelTimeExtreme(TypedDict):
    promised: int
    actual: float
    order_id: int
    distance: float


class FreeDeliveries(TypedDict):
    total_amount: int
    break_up: OrderTypeHint.FREE_DEL_BREAK_UP


class DelTime(TypedDict):
    deliveries: int
    mean_promised: Union[int, float]
    mean_actual: Union[int, float]
    median: Union[int, float]
    std_dev: Union[int, float]
    minimum: DelTimeExtreme
    maximum: DelTimeExtreme


class Punctuality(TypedDict):
    on_time: int
    late: int
    max_delivery_time: int
    min_delivery_time: int


class Distance(TypedDict):
    distance_covered: float
    orders_placed: int
    distance_covered_per_order: float


class SuperBenefits(TypedDict):
    total_benefit: float
    other_super_discount: float
    free_deliveries: FreeDeliveries


class FurthestOrder(TypedDict):
    distance_covered: float
    restaurant: str
    items: list[str]
    delivered_by: str
    time_taken: str
    was_on_time: bool


class ExtremeDiscount(TypedDict):
    amount: float
    coupon: str
    order_id: list[int]


class OfferStatistics(TypedDict):
    total_discount: float
    discount_breakup: OfferTypeHint.DISCOUNT_SHARE
    average_discount: dict[Literal["orders_w_offers", "all_orders"], float]
    std_dev_discount: float
    minimum_discount: ExtremeDiscount
    maximum_discount: ExtremeDiscount
    mode_discount: list[float]
    median_discount: float
