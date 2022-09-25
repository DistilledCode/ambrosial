from dataclasses import dataclass

URL = "https://res.cloudinary.com/swiggy/image/upload/"


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
    cuisine: list[str]
    coordinates: dict[str, float]
    customer_distance: tuple[str, float]
    cover_image: str
    taxation_type: str
    gst_category: str

    def __post_init__(self) -> None:
        _lat_lng = [float(i) for i in self.coordinates.split(",")]  # type:ignore
        self.coordinates = dict(zip(["lat", "lng"], _lat_lng))
        self.image = URL + self.cover_image

    def __eq__(self, other: object) -> bool:
        return self.id == other.id  # type:ignore

    def __hash__(self) -> int:
        return hash(self.id)
