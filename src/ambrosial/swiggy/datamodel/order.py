from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt

from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.restaurant import Restaurant
from ambrosial.swiggy.datamodel.typealiases import OfferTypeHint, OrderTypeHint


class Offer(BaseModel):
    order_id: int
    coupon_applied: str
    super_type: str
    total_offer_discount: NonNegativeFloat
    discount_type: str
    description: str
    discount_share: OfferTypeHint.DISCOUNT_SHARE

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
    paymentMeta: Optional[dict] = None
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
    tipDetails: Optional[dict] = None
    order_id: int
    address: Address
    items: list[Item]
    charges: OrderTypeHint.CHARGES
    is_coupon_applied: bool
    offers_data: list[Offer]
    order_time: datetime
    customer_id: str
    order_status: OrderTypeHint.ORDER_STATUS
    post_status: OrderTypeHint.POST_STATUS
    order_type: str
    sla_time: NonNegativeInt
    delivery_boy: OrderTypeHint.DELIVERY_BOY
    restaurant: Restaurant
    payment_method: str
    payment_transaction: list[Payment]
    order_delivery_status: OrderTypeHint.ORDER_DELIVERY_STATUS
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
    rating_meta: OrderTypeHint.RATING_META
    customer_user_agent: str
    payment_txn_id: str
    order_payment_method: str
    is_refund_initiated: bool
    cust_lat_lng: OrderTypeHint.CUST_LAT_LNG
    is_long_distance: bool
    on_time: bool
    sla_difference: int
    actual_sla_time: NonNegativeInt
    payment_txn_status: OrderTypeHint.PAYMENT_TXN_STATUS
    rain_mode: int
    is_super_long_distance: bool
    previous_cancellation_fee: NonNegativeInt
    mCancellationTime: NonNegativeInt
    free_del_break_up: OrderTypeHint.FREE_DEL_BREAK_UP
    order_tags: list[str]
    updated_at: str
    conservative_last_mile_distance: NonNegativeFloat

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)
