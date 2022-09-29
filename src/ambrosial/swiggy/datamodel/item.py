from pydantic import BaseModel, HttpUrl


class Item(BaseModel):
    rewardType: str
    item_key: str
    has_variantv2: bool
    order_id: int
    restaurant_id: str
    item_id: int
    external_item_id: str
    name: str
    is_veg: bool
    variants: tuple
    addons: tuple
    image: HttpUrl
    quantity: int
    free_item_quantity: int
    total: float
    subtotal: float
    final_price: float
    base_price: float
    effective_item_price: float
    packing_charges: float
    category_details: dict[str, str]
    item_charges: dict[str, float]
    item_total_discount: float

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)
