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
    # TODO: start from "order_spending": "0",
