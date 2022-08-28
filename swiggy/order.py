from dataclasses import dataclass, field
from typing import Any, Optional, Union

from swiggy.address import DeliveryAddress
from swiggy.orderitem import OrderItem
from swiggy.restaurant import Restaurant


@dataclass(kw_only=True, frozen=True)
class Payment:
    paymentMethod: str
    paymentMethodDisplayName: str
    transactionId: str
    amount: str  #! could be int
    paymentMeta: dict[str, Optional[Union[str, dict]]]
    transactionStatus: str
    swiggyTransactionId: str
    pgTransactionId: str
    couponApplied: str
    paymentGateway: Optional[str] = None
    pgResponseTime: str


@dataclass(kw_only=True, frozen=True)
class Order:
    tipDetails: dict[str, Any]
    order_id: int
    delivery_address: DeliveryAddress
    order_items: list[OrderItem] = field(default_factory=list)
    old_order_items: list[Any] = field(default_factory=list)
    order_meals: list[Any] = field(default_factory=list)
    old_order_meals: list[Any] = field(default_factory=list)
    order_subscriptions: list[Any] = field(default_factory=list)
    charges: dict[str, str]
    is_coupon_applied: bool
    #! is_coupon_auto_applied: bool !! Skipped, only 3 occurrences in 400+ orders
    coupon_applied: str
    #! offers_data can also be empty string (`""`), convert that to empty list.
    # TODO: check if an attr value can conditionally depend on other attr value
    offers_data: tuple[dict]
    order_time: str
    customer_id: str
    order_status: str
    post_status: str
    order_type: str
    order_placement_status: str
    billing_address_id: str  # refers to the id of DeliveryAddress
    sla_time: str
    delivery_boy: dict[str, Optional[Union[int, str]]]
    restaurant_id: str
    restaurant: Restaurant
    payment_method: str
    payment_method_involved: str
    payment_transaction: list[Payment] = field(default_factory=list)
    order_delivery_status: str
    ordered_time_in_seconds: int  # epoch
    delivered_time_in_seconds: str  # epoch string
    delivery_time_in_seconds: str
    order_total: int
    order_total_with_tip: float
    net_total: float
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
    delivery_discount_hit: int
    freebie_discount_hit: int
    super_specific_discount: float
    delivery_rating: Optional[int] = None  # rating_meta['delivert_rating']['rating']
    order_restaurant_bill: str
    order_notes: Optional[str] = None
    pg_response_time: str
    customer_user_agent: str
    overbooking: str
    #! coordinates from where the order was placed?
    billing_lat: str
    billing_lng: str
    payment_txn_id: str
    order_payment_method: str
    is_refund_initiated: int
    cust_lat_lng: dict[str, str]
    delayed_placing: int
    cod_verification_threshold: Optional[int] = None
    is_long_distance: bool
    on_time: bool
    sla_difference: str
    actual_sla_time: str
    payment_txn_status: str
    rain_mode: str
    is_super_long_distance: bool
    payment: str
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
    mCancellationTime: int  #! epoch
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
    total_tax: float
    delivery_fee_reversal_breakup: dict[str, int]
    delivery_fee_reversal: int
    discounted_total_delivery_fee: int
    free_del_break_up: dict[str, Union[int, bool]]
    order_tags: list[str] = field(default_factory=list)
    cancellation_source: str
    default_delivery_text: str
    additional_payment_details: list = field(default_factory=list)
    group_tag_details: list[dict[str, str]] = field(default_factory=list)
    updated_at: str
    user_flow_info: dict
    conservative_last_mile_distance: float
    selected_sla_option: str
    address_changed_post_order: str
    post_order_address_change_attempted_at: int
