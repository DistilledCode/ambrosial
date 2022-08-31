from dataclasses import dataclass, field
from typing import Union

URL = "https://res.cloudinary.com/swiggy/image/upload/"


@dataclass(kw_only=True, frozen=False, order=True)
class OrderItem:
    rewardType: str
    item_key: str
    has_variantv2: bool
    order_id: int
    restaurant_id: str
    item_id: int
    external_item_id: str
    name: str
    is_veg: bool  # 1 (True) or 0 (False)
    variants: list[dict] = field(default_factory=list)
    addons: list[dict] = field(default_factory=list)
    image_id: str
    quantity: int
    free_item_quantity: int
    total: float
    subtotal: float
    final_price: float
    base_price: float
    effective_item_price: float
    packing_charges: float
    category_details: dict[str, str]
    item_charges: Union[dict[str, float], dict[str, int]]
    item_total_discount: float
    single_variant: bool

    def __post_init__(self):
        self.is_veg = bool(self.is_veg)
        self.image = URL + self.image_id
        self.quantity = int(self.quantity)
        self.free_item_quantity = (
            int(self.free_item_quantity) if self.free_item_quantity else 0
        )
        self.total = float(self.total)
        self.subtotal = float(self.subtotal)
        self.final_price = float(self.final_price)
        self.base_price = float(self.base_price)
        self.effective_item_price = float(self.effective_item_price)
        self.item_total_discount = float(self.item_total_discount)
        for key in self.item_charges:
            self.item_charges[key] = float(self.item_charges[key])

    def __eq__(self, other):
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)

    def __str__(self) -> str:
        return f"{self.name}"
