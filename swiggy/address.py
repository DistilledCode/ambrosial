from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class DeliveryAddress:
    version: int
    address: str
    landmark: str
    area: str
    mobile: str
    annotation: str
    instructions: str
    email: str
    city: str
    lat: str
    lng: str
    id: str
    address_line1: str
    address_line2: str
    alternate_mobile: str
    voice_directions_s3_uri: str
    flat_no: str
    is_verified: bool
    reverse_geo_code_failed: bool

    def __eq__(self, other):
        return self.id == other.id
