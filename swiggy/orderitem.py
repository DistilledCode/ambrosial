from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass(kw_only=True, frozen=True)
class OrderItemAddons:
    pass


@dataclass(kw_only=True, frozen=True)
class OrderItemVariants:
    variation_id: int
    group_id: int
    name: str
    price: float
    external_choice_id: str
    external_group_id: str
    variant_tax_charges: dict[str, Union(Union[int, float], str)]


@dataclass(kw_only=True, frozen=True)
class OrderItem:
    rewardType: Any
    item_key: str
    has_variantv2: bool
    item_group_tag_id: str
    added_by_user_id: int
    added_by_username: str
    group_user_item_map: dict
    item_id: int
    external_item_id: str
    name: str
    is_veg: bool  # 1 (True) or 0 (False)
    variants: list[OrderItemVariants] = field(default_factory=list)
    addons: list[OrderItemAddons] = field(default_factory=list)
    image_id: str
    image_url: str = "https://res.cloudinary.com/swiggy/image/upload/" + image_id
    quantity: int
    free_item_quantity: int
    total: float
    subtotal: float
    final_price: float
    base_price: float
    effective_item_price: float
    packing_charges: float
    category_details: dict[str, str]
    item_charges: dict[str, Union(int, float)]
    item_total_discount: float
    item_delivery_fee_reversal: int
    single_variant: bool
    in_stock: int
    meal_quantity: str
    # if meal_quantity == "1" then bottom three are None
    item_type: Optional[str] = None
    meal_id: Optional[str] = None
    meal_name: Optional[str] = None
