from dataclasses import make_dataclass

order_useless_attrs = [
    "sharedOrder",
    "old_order_items",
    "previousOrderId",
    "old_order_meals",
    "deliveryFeeCouponBreakup",
    "free_gifts",
    "order_meals",
    "post_name",
    "order_subscriptions",
    "subscription_total",
    "post_type",
    "subscription_total_without_tax",
    "restaurant_fulfilment_charges",
    "order_tax",
    "subscription_tax",
    "batch_opt_in_discount",
    "original_order_total",
    "delivery_discount_hit",
    "free_shipping",
    "show_rate_us",
    "batch_opt_in",
    "order_spending",
    "has_rating",
    "waive_off_amount",
    "restaurant_order_rating",
    "customer_care_number",
    "order_incoming",
    "last_failed_order_id",
    "edit_refund_amount",
    "convenience_fee",
    "converted_to_cod",
    "overbooking",
    "order_delivery_charge",
    "with_de",
    "discounted_total_delivery_charge_actual",
    "de_pickedup_refund",
    "coupon_code",
    "is_ivr_enabled",
    "pay_by_system_value",
    "is_assured",
    "agreement_type",
    "payment",
    "key",
    "cancellation_policy_promise_id",
    "promise_id",
    "rendering_details",
    "is_cancellable",
    "td_gp_data",
    "rest_bear_amount",
    "defaulting_lat",
    "restaurant_has_inventory",
    "GST_on_discounted_total_delivery_fee",
    "defaulting_type",
    "discounted_total_delivery_charge_gst_expression",
    "defaulting_lng",
    "delivery_fee_details",
    "GST_on_subscription",
    "delivery_fee_reversal_breakup",
    "subscription_gst_expression",
    "discounted_total_delivery_fee",
    "total_tax",
    "juspay_meta",
    "delivery_fee_reversal",
    "default_delivery_text",
    "initiation_source",
    "group_tag_details",
    "tip_detail_list",
    "is_gourmet",
    "additional_payment_details",
    "paymentTransactions",
    "priority_delivery_fee",
    "cod_verification_threshold",
    "restaurant_packing_charges",
    "user_flow_info",
    "restaurant_coverage_area",
    "pg_response_time",
    "is_coupon_auto_applied",
    "billing_address_id",
]
order_item_useless_attrs = [
    "item_group_tag_id",
    "added_by_user_id",
    "added_by_username",
    "group_user_item_map",
    "item_key",
    "item_delivery_fee_reversal",
    "item_type",
    "meal_id",
    "meal_name",
    "meal_quantity",
    "in_stock",
]


def dict2dataclass(name: str, dict_to_conv: dict, **kwargs: dict) -> type:
    if any(
        not isinstance((x := key), str) or not x.replace(" ", "_").isidentifier()
        for key in dict_to_conv
    ):
        raise TypeError(f"Field names must be valid identifiers: {x!r}")
    field_list = []
    for key, val in dict_to_conv.items():
        new_key = key.replace(" ", "_").lower()
        if val.__class__ in [list, set, tuple]:
            value_list = []
            for ind, i in enumerate(val):
                if i.__class__ is dict:
                    value_list.append(dict2dataclass(f"{new_key}{ind}", i, **kwargs))
                else:
                    value_list.append(i)
            val = tuple(value_list)
        if val.__class__ is dict:
            val = dict2dataclass(new_key, val, **kwargs)
        field_list.append((new_key, val.__class__, val))
    DataClass = make_dataclass(name, field_list, **kwargs)
    return DataClass()
