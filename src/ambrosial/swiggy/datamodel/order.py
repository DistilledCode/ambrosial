from datetime import datetime
from typing import Any, Optional, Union

from pydantic import BaseModel

from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.restaurant import Restaurant


class Offer(BaseModel):
    order_id: int
    coupon_applied: str
    super_type: str
    total_offer_discount: float
    discount_share: dict[str, Union[int, float]]
    discount_type: str
    description: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Offer):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        # to have different hash from parent Order
        return hash(self.order_id // 2)


class Payment(BaseModel):
    order_id: str
    paymentMethod: str
    paymentMethodDisplayName: str
    transactionId: str
    amount: float
    paymentMeta: dict[str, Union[str, dict]]
    transactionStatus: str
    swiggyTransactionId: str
    pgTransactionId: str
    couponApplied: str
    paymentGateway: Optional[str] = None
    pgResponseTime: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Payment):
            return NotImplemented
        return self.transactionId == other.transactionId

    def __hash__(self) -> int:
        return hash(self.transactionId)


class Order(BaseModel):
    tipDetails: dict[str, Union[float, bool, str]]
    order_id: int
    address: Address
    items: list[Item]
    charges: dict[str, float]
    is_coupon_applied: bool
    offers_data: list[Offer]
    order_time: datetime
    customer_id: str
    order_status: str
    post_status: str
    order_type: str
    order_placement_status: str
    sla_time: int
    delivery_boy: dict[str, Any]
    restaurant: Restaurant
    payment_method: str
    payment_transaction: list[Payment]
    order_delivery_status: str
    ordered_time_in_seconds: int
    delivered_time_in_seconds: int
    delivery_time_in_seconds: int
    order_total: int
    order_total_with_tip: float
    item_total: float
    swiggy_money: float
    order_discount_without_freebie: float
    order_discount: float
    coupon_discount: float
    trade_discount: float
    order_discount_effective: float
    coupon_discount_effective: float
    trade_discount_effective: float
    free_delivery_discount_hit: int
    freebie_discount_hit: int
    super_specific_discount: float
    rating_meta: dict[str, Any]
    customer_user_agent: str
    # ! coordinates from where the order was placed?
    billing_lat: float
    billing_lng: float
    payment_txn_id: str
    order_payment_method: str
    is_refund_initiated: int
    cust_lat_lng: dict[str, float]
    is_long_distance: bool
    on_time: bool
    sla_difference: int
    actual_sla_time: int
    payment_txn_status: str
    rain_mode: str
    is_super_long_distance: bool
    device_id: str
    swuid: str
    sid: str
    previous_cancellation_fee: int
    coupon_type: str
    coupon_description: str
    mCancellationTime: int
    configurations: dict[str, bool]
    free_del_break_up: dict[str, Union[int, bool]]
    order_tags: list[str]
    updated_at: str
    conservative_last_mile_distance: float

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)
