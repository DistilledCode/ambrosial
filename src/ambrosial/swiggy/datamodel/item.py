from typing import Optional

from pydantic import BaseModel, HttpUrl, NonNegativeFloat, NonNegativeInt

from ambrosial.swiggy.datamodel.typealiases import ItemTypeHint


class Item(BaseModel):
    rewardType: Optional[str] = None
    has_variantv2: bool
    order_id: int
    restaurant_id: int
    item_id: int
    external_item_id: str
    name: str
    is_veg: bool
    variants: ItemTypeHint.VARIANTS
    addons: ItemTypeHint.ADDONS
    image: HttpUrl
    quantity: NonNegativeInt
    free_item_quantity: NonNegativeInt
    total: NonNegativeFloat
    subtotal: NonNegativeFloat
    final_price: NonNegativeFloat
    base_price: NonNegativeFloat
    effective_item_price: NonNegativeFloat
    packing_charges: NonNegativeFloat
    category_details: ItemTypeHint.CATEGORY_DETAILS
    item_charges: ItemTypeHint.ITEM_CHARGES
    item_total_discount: NonNegativeFloat

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)
