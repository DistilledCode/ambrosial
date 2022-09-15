from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Union

from swiggy.address import DeliveryAddress
from swiggy.orderitem import OrderItem
from swiggy.restaurant import Restaurant


@dataclass(kw_only=True, frozen=True)
class Offer:
    order_id: int
    id: str
    coupon_applied: str
    super_type: str
    total_offer_discount: float
    discount_share: dict[str, Union[int, float]]
    discount_type: str
    description: str

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(kw_only=True)
class Payment:
    paymentMethod: str
    paymentMethodDisplayName: str
    transactionId: str
    amount: float
    paymentMeta: dict[str, Optional[Union[str, dict]]]
    transactionStatus: str
    swiggyTransactionId: str
    pgTransactionId: str
    couponApplied: str
    paymentGateway: Optional[str] = None
    pgResponseTime: str

    def __post_init__(self):
        self.order_id = self.transactionId
        self.amount = float(self.amount)

    def __eq__(self, other: object) -> bool:
        return self.transactionId == other.transactionId

    def __hash__(self) -> int:
        return hash(self.transactionId)


@dataclass(kw_only=True)
class Order:
    tipDetails: dict[str, Any]
    order_id: int
    delivery_address: DeliveryAddress
    order_items: list[OrderItem] = field(default_factory=list)
    charges: dict[str, str]
    is_coupon_applied: bool
    offers_data: list[Offer] = field(default_factory=list)
    order_time: datetime
    customer_id: str
    order_status: str
    post_status: str
    order_type: str
    order_placement_status: str
    sla_time: int
    delivery_boy: dict[str, Optional[Union[int, str]]]
    restaurant: Restaurant
    payment_method: str
    payment_method_involved: str
    payment_transaction: list[Payment] = field(default_factory=list)
    order_delivery_status: str
    ordered_time_in_seconds: int
    delivered_time_in_seconds: int
    delivery_time_in_seconds: int
    order_total: int
    order_total_with_tip: float
    # net_total: float
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
    rating_meta: dict[str, Union[int, str]]
    order_restaurant_bill: float
    order_notes: Optional[str] = None
    customer_user_agent: str
    #! coordinates from where the order was placed?
    billing_lat: float
    billing_lng: float
    payment_txn_id: str
    order_payment_method: str
    is_refund_initiated: int
    cust_lat_lng: dict[str, float]
    delayed_placing: int
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
    base_order_id: Optional[int] = None
    is_replicated: bool
    cloning_reason: Optional[str] = None
    cancellation_fee_collected: int
    cancellation_fee_applied: int
    cancellation_fee_collected_total: int
    is_cancellation_fee_already_reverted: bool
    previous_cancellation_fee: int
    is_select: bool
    is_first_order_delivered: bool
    first_order: bool
    is_bank_discount: Optional[bool] = None
    coupon_type: str
    coupon_description: str
    cashback_source: str
    mCancellationTime: int
    configurations: dict[str, bool]
    success_message_info: str
    success_title: str
    success_message_type: str
    savings_shown_to_customer: str
    threshold_fee: int
    distance_fee: int
    time_fee: int
    special_fee: int
    threshold_fee_effective: int
    distance_fee_effective: int
    time_fee_effective: int
    special_fee_effective: int
    free_del_break_up: dict[str, Union[int, bool]]
    order_tags: tuple[str]
    cancellation_source: str
    updated_at: str
    conservative_last_mile_distance: float
    # selected_sla_option: str
    address_changed_post_order: str
    post_order_address_change_attempted_at: int

    def __post_init__(self):
        self.charges = {key: float(self.charges[key]) for key in self.charges}
        self.delivered_time_in_seconds = int(self.delivered_time_in_seconds)
        self.delivery_time_in_seconds = int(self.delivery_time_in_seconds)
        self.order_restaurant_bill = float(self.order_restaurant_bill)
        self.billing_lat = float(self.billing_lat)
        self.billing_lng = float(self.billing_lng)
        self.cust_lat_lng = {
            key: float(self.cust_lat_lng[key]) for key in self.cust_lat_lng
        }
        self.order_tags = tuple(self.order_tags)
        # on_time should be True if sla_difference is positive
        self.sla_time = int(self.sla_time)
        self.actual_sla_time = int(self.actual_sla_time)
        self.sla_difference = int(self.sla_difference)
        self.on_time = True if self.sla_difference >= 0 else False
        self.order_time = datetime.strptime(self.order_time, "%Y-%m-%d %H:%M:%S")

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)
