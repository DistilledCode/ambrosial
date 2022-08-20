from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass(kw_only=True, frozen=True)
class Restaurant:
    id: int
    name: str
    address: str
    locality: str
    type: str
    coverage_area: str
    city_code: int
    city_name: str
    area_code: int
    cuisine: list[str] = field(default_factory=list)
    closing_in_min: int
    closed: bool
    fulfilment_charges: int
    order_rating: int
    rating: Optional[int] = None  # rating_meta['restaurant_rating']['rating']
    coordinates: dict[str, float]  # restaurant_lat_lng: [xx.xxxxxxx, xx.xxxxxxx]
    customer_distance: float
    new_slug: str
    has_inventory: Union[str, int]
    cover_image: str
    cover_url: str = "https://res.cloudinary.com/swiggy/image/upload/" + cover_image
    area_name: str
    taxation_type: str
    gst_category: str
    order_bill: float
    packing_charges: int

    def __eq__(self, other):
        return self.id == other.id
