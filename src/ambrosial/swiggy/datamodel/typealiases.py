from typing import Literal, Optional, Union

from typing_extensions import TypeAlias


class OrderTypeHint:
    TIP_DETAILS: TypeAlias = dict[Literal["amount", "optIn", "type"], Union[float, str]]
    ORDER_STATUS: TypeAlias = Literal["Delivered", "cancelled"]
    POST_STATUS: TypeAlias = Literal["completed", "cancelled"]
    ORDER_DELIVERY_STATUS: TypeAlias = Literal["", "delivered"]
    CUST_LAT_LNG: TypeAlias = dict[Literal["lat", "lng"], float]
    PAYMENT_TXN_STATUS: TypeAlias = Literal["refund-initiated", "success"]
    COUPON_TYPE: TypeAlias = Literal["", "Discount"]
    RATING_META: TypeAlias = dict[
        Literal["restaurant_rating", "delivery_rating"],
        dict[Literal["rating", "title"], Union[int, str]],
    ]
    CONFIGURATIONS: TypeAlias = dict[
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
    FREE_DEL_BREAK_UP: TypeAlias = dict[
        Literal[
            "thresholdFee",
            "distanceFee",
            "timeFee",
            "specialFee",
            "rainFee",
        ],
        int,
    ]
    DELIVERY_BOY: TypeAlias = dict[
        Literal[
            "trackable",
            "id",
            "name",
            "mobile",
            "image_url",
        ],
        Optional[Union[int, str]],
    ]
    CHARGES: TypeAlias = dict[
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


class ItemTypeHint:
    VARIANTS: TypeAlias = tuple[dict[str, Union[int, float, str, dict[str, str]]], ...]
    ADDONS: TypeAlias = tuple[dict[str, Union[str, dict[str, str]]], ...]
    CATEGORY_DETAILS: TypeAlias = dict[Literal["category", "sub_category"], str]
    ITEM_CHARGES: TypeAlias = dict[
        Literal["GST", "Service Charges", "Service Tax", "Vat"], float
    ]


class RestaurantTypeHint:
    COORDINATES: TypeAlias = dict[Literal["lat", "lng"], float]
    GST_CATEGORY: TypeAlias = Literal["RESTAURANT", "NONRESTAURANT", "HYBRID", ""]


class OfferTypeHint:
    DISCOUNT_SHARE: TypeAlias = dict[
        Literal[
            "alliance_discount",
            "store_discount",
            "swiggy_discount",
        ],
        float,
    ]
