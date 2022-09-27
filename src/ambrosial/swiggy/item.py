from dataclasses import dataclass, field

URL = "https://res.cloudinary.com/swiggy/image/upload/"


@dataclass(kw_only=True, frozen=False, order=True)
class Item:
    rewardType: str
    item_key: str
    has_variantv2: bool
    order_id: int
    restaurant_id: str
    item_id: int
    external_item_id: str
    name: str
    is_veg: bool
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
    item_charges: dict[str, float]
    item_total_discount: float
    single_variant: bool

    def __post_init__(self) -> None:
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
        self.packing_charges = float(self.packing_charges)
        for key in self.item_charges:
            self.item_charges[key] = float(self.item_charges[key])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)