from typing import Literal, Optional, Union


class OrderTypes:
    TIP_DETAILS = dict[Literal["amount", "optIn", "type"], Union[float, str]]
    ORDER_STATUS = Literal["Delivered", "cancelled"]
    POST_STATUS = Literal["completed", "cancelled"]
    ORDER_DELIVERY_STATUS = Literal["", "delivered"]
    CUST_LAT_LNG = dict[Literal["lat", "lng"], float]
    PAYMENT_TXN_STATUS = Literal["refund-initiated", "success"]
    COUPON_TYPE = Literal["", "Discount"]
    RATING_META = dict[
        Literal["restaurant_rating", "delivery_rating"],
        dict[Literal["rating", "title"], Union[int, str]],
    ]
    CONFIGURATIONS = dict[
        Literal[
            "cancel_not_allowed",
            "edit_not_allowed",
            "external_relay_info",
            "no_delivery_notification",
            "reorder_not_allowed",
            "self_delivery",
        ],
        bool,
    ]
    FREE_DEL_BREAK_UP = dict[
        Literal[
            "thresholdFee",
            "distanceFee",
            "timeFee",
            "specialFee",
            "rainFee",
        ],
        int,
    ]
    DELIVERY_BOY = dict[
        Literal[
            "trackable",
            "id",
            "name",
            "mobile",
            "image_url",
        ],
        Optional[Union[int, str]],
    ]
    CHARGES = dict[
        Literal[
            "Cancellation Fee",
            "Convenience Fee",
            "Delivery Charges",
            "GST",
            "Packing Charges",
            "Service Charges",
            "Service Tax",
            "Total Delivery Fees",
            "Vat",
        ],
        float,
    ]


class ItemTypes:
    VARIANTS = tuple[dict[str, Union[int, float, str, dict[str, str]]], ...]
    ADDONS = tuple[dict[str, Union[str, dict[str, str]]], ...]
    CATEGORY_DETAILS = dict[Literal["category", "sub_category"], str]
    ITEM_CHARGES = dict[Literal["GST", "Service Charges", "Service Tax", "Vat"], float]


class RestaurantTypes:
    COORDINATES = dict[Literal["lat", "lng"], float]
    GST_CATEGORY = Literal["RESTAURANT", "NONRESTAURANT", "HYBRID", ""]


class OfferTypes:
    DISCOUNT_SHARE = dict[
        Literal[
            "alliance_discount",
            "store_discount",
            "swiggy_discount",
        ],
        float,
    ]
