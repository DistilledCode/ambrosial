from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt

from ambrosial.swiggy.datamodel import OfferTypes, OrderTypes
from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.restaurant import Restaurant


class Offer(BaseModel):
    order_id: int
    coupon_applied: str
    super_type: str
    total_offer_discount: NonNegativeFloat
    discount_type: str
    description: str
    discount_share: OfferTypes.DISCOUNT_SHARE

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
    amount: NonNegativeFloat
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
    tipDetails: OrderTypes.TIP_DETAILS
    order_id: int
    address: Address
    items: list[Item]
    charges: OrderTypes.CHARGES
    is_coupon_applied: bool
    offers_data: list[Offer]
    order_time: datetime
    customer_id: str
    order_status: OrderTypes.ORDER_STATUS
    post_status: OrderTypes.POST_STATUS
    order_type: str
    sla_time: NonNegativeInt
    delivery_boy: OrderTypes.DELIVERY_BOY
    restaurant: Restaurant
    payment_method: str
    payment_transaction: list[Payment]
    order_delivery_status: OrderTypes.ORDER_DELIVERY_STATUS
    ordered_time_in_seconds: NonNegativeInt
    delivered_time_in_seconds: NonNegativeInt
    delivery_time_in_seconds: NonNegativeInt
    order_total: NonNegativeInt
    order_total_with_tip: NonNegativeFloat
    item_total: NonNegativeFloat
    swiggy_money: NonNegativeFloat
    order_discount_without_freebie: NonNegativeFloat
    order_discount: NonNegativeFloat
    coupon_discount: NonNegativeFloat
    trade_discount: NonNegativeFloat
    order_discount_effective: NonNegativeFloat
    coupon_discount_effective: NonNegativeFloat
    trade_discount_effective: NonNegativeFloat
    free_delivery_discount_hit: NonNegativeInt
    freebie_discount_hit: NonNegativeInt
    super_specific_discount: NonNegativeFloat
    rating_meta: OrderTypes.RATING_META
    customer_user_agent: str
    # ! coordinates from where the order was placed?
    billing_lat: float
    billing_lng: float
    payment_txn_id: str
    order_payment_method: str
    is_refund_initiated: bool
    cust_lat_lng: OrderTypes.CUST_LAT_LNG
    is_long_distance: bool
    on_time: bool
    sla_difference: int
    actual_sla_time: NonNegativeInt
    payment_txn_status: OrderTypes.PAYMENT_TXN_STATUS
    rain_mode: int
    is_super_long_distance: bool
    device_id: str
    swuid: str
    sid: str
    previous_cancellation_fee: NonNegativeInt
    coupon_type: OrderTypes.COUPON_TYPE
    coupon_description: str
    mCancellationTime: NonNegativeInt
    configurations: OrderTypes.CONFIGURATIONS
    free_del_break_up: OrderTypes.FREE_DEL_BREAK_UP
    order_tags: list[str]
    updated_at: str
    conservative_last_mile_distance: NonNegativeFloat

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)
