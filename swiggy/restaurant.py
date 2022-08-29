from dataclasses import dataclass


@dataclass(kw_only=True)
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
    coordinates: dict[str, float]
    customer_distance: tuple[float, str]
    new_slug: str
    cover_image: str
    taxation_type: str
    gst_category: str

    def __post_init__(self):
        _lat_lng = [float(i) for i in self.coordinates.split(",")]
        self.coordinates = dict(zip(["lat", "lng"], _lat_lng))
        self.cuisine = tuple(self.cuisine)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self):
        return f"{self.name}, {self.area_name}, {self.city_name}"
