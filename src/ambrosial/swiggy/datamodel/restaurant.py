from pydantic import BaseModel, HttpUrl


class Restaurant(BaseModel):
    rest_id: int
    name: str
    address: str
    locality: str
    rest_type: str
    city_code: int
    city_name: str
    area_code: int
    area_name: str
    cuisine: list
    coordinates: dict[str, float]
    customer_distance: tuple[str, float]
    cover_image: HttpUrl
    taxation_type: str
    gst_category: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Restaurant):
            return NotImplemented
        return self.rest_id == other.rest_id

    def __hash__(self) -> int:
        return hash(self.rest_id)
