from dataclasses import dataclass, field
from typing import Any, Optional, Union

from swiggy.address import DeliveryAddress
from swiggy.orderitem import OrderItem
from swiggy.restaurant import Restaurant


@dataclass(kw_only=True, frozen=True)
class OffersData:
    id: str
    super_type: str
    total_offer_discount: float
    discount_share: dict[str, Union[int, float]]
    discount_type: str
    description: str
    fixed_charges: dict[str, dict[str, Union[int, str]]]


@dataclass(kw_only=True, frozen=True)
class Payment:
    paymentMethod: str
    paymentMethodDisplayName: str
    transactionId: str
    amount: str  # could be int
    paymentMeta: dict[str, Optional[Union[str, dict]]]
    transactionStatus: str
    swiggyTransactionId: str
    pgTransactionId: str
    couponApplied: str
    paymentGateway: Optional[str]
    pgResponseTime: str


@dataclass(kw_only=True, frozen=True)
class Order:
    sharedOrder: bool
    previousOrderId: int
    tipDetails: dict[str, Any]
    deliveryFeeCouponBreakup: dict[str, Union[int, dict[str, int]]]
    order_id: int
    delivery_address: DeliveryAddress
    order_items: list[OrderItem] = field(default_factory=list)
    old_order_items: list[Any] = field(default_factory=list)
    order_meals: list[Any] = field(default_factory=list)
    old_order_meals: list[Any] = field(default_factory=list)
    order_subscriptions: list[Any] = field(default_factory=list)
    # TODO: create a separate dataclass if `charges` eases out the maths calculation
    charges: dict[str, str]
    free_gifts: list[Any] = field(default_factory=list)
    is_coupon_applied: bool
    # is_coupon_auto_applied: bool !! Skipped, only 3 occurrences in 400+ orders
    coupon_applied: str
    #! offers_data can also be empty string (`""`), convert that to empty list.
    # TODO: check if an attr value can conditionally depend on other attr value
    offers_data: list[OffersData] = field(default_factory=list)
    order_time: str
    customer_id: str
    order_status: str
    post_status: str
    order_type: str
    post_type: str
    post_name: str
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
    subscription_total: float
    subscription_tax: float
    subscription_total_without_tax: float
    original_order_total: int
    swiggy_money: float
    order_tax: float
    free_shipping: str  # either "" or "0"
    order_discount_without_freebie: float
    order_discount: float
    coupon_discount: float
    trade_discount: float
    order_discount_effective: float
    coupon_discount_effective: float
    trade_discount_effective: float
    batch_opt_in_discount: int
    batch_opt_in: str
    free_delivery_discount_hit: int
    delivery_discount_hit: int
    freebie_discount_hit: int
    super_specific_discount: float
    has_rating: str
    show_rate_us: bool
    restaurant_order_rating: int
    delivery_rating: Optional[int] = None  # rating_meta['delivert_rating']['rating']
    order_spending: str
    order_incoming: str
    waive_off_amount: int
    edit_refund_amount: int
    order_restaurant_bill: str
    order_notes: Optional[str] = None
    customer_care_number: str
    pg_response_time: str
    converted_to_cod: bool
    last_failed_order_id: int
    order_delivery_charge: int
    convenience_fee: str
    discounted_total_delivery_charge_actual: str
    customer_user_agent: str
    overbooking: str
    # coordinates from where the order was placed?
    billing_lat: str
    billing_lng: str
    payment_txn_id: str
    coupon_code: str
    payment_partner_order_id: Optional[str]
    with_de: bool
    order_payment_method: str
    pay_by_system_value: bool
    de_pickedup_refund: int
    agreement_type: str
    is_ivr_enabled: str
    is_refund_initiated: int
    cust_lat_lng: dict[str, str]
    key: str
    is_assured: int
    delayed_placing: int
    cod_verification_threshold: Optional[int] = None
    is_long_distance: bool
    on_time: bool
    sla_difference: str
    actual_sla_time: str
    payment_txn_status: str
    rain_mode: str
    promise_id: str
    is_super_long_distance: bool
    payment: str
    device_id: str
    swuid: str
    sid: str
    cancellation_policy_promise_id: str
    base_order_id: Optional[int]
    is_replicated: bool
    is_cancellable: bool
    cloning_reason: Optional[str]
    cancellation_fee_collected: int
    cancellation_fee_applied: int
    cancellation_fee_collected_total: int
    is_cancellation_fee_already_reverted: bool
    previous_cancellation_fee: int
    is_select: bool
    is_first_order_delivered: bool
    first_order: bool
    is_bank_discount: Optional[bool]
    coupon_type: str
    coupon_description: str
    cashback_source: str
    rendering_details: list[dict[str, Any]] = field(default_factory=list)
    mCancellationTime: int  # epoch
    configurations: dict[str, bool]
    GST_on_discounted_total_delivery_fee: dict
    GST_on_subscription: dict
    discounted_total_delivery_charge_gst_expression: str
    subscription_gst_expression: str
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
    delivery_fee_details: dict[str, dict]
    total_tax: float
    delivery_fee_reversal_breakup: dict[str, int]
    delivery_fee_reversal: int
    discounted_total_delivery_fee: int
    free_del_break_up: dict[str, Union[int, bool]]
    initiation_source: int
    order_tags: list[str] = field(default_factory=list)
    juspay_meta: dict
    cancellation_source: str
    tip_detail_list: list[dict[str, Any]] = field(default_factory=list)
    default_delivery_text: str
    additional_payment_details: list = field(default_factory=list)
    group_tag_details: list[dict[str, str]] = field(default_factory=list)
    updated_at: str
    category_info: Optional[str] = None
    user_flow_info: dict
    conservative_last_mile_distance: float
    selected_sla_option: str
    priority_delivery_fee: int
    is_gourmet: bool
    address_changed_post_order: str
    post_order_address_change_attempted_at: int
