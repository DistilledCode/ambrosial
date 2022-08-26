from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class Restaurant:
    id: int
    name: str
    address: str
    locality: str
    type: str
    city_code: int
    city_name: str
    area_code: int
    area_name: str
    cuisine: tuple[str]
    coordinates: str  # restaurant_lat_lng: "xx.xxxxxxx,xx.xxxxxxx"
    customer_distance: tuple[float, str]
    new_slug: str
    cover_url: str
    taxation_type: str
    gst_category: str

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.name}, {self.area_name}, {self.city_name}"

    def __hash__(self) -> int:
        return hash(self.id)
