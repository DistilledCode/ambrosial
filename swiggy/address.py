from dataclasses import dataclass


@dataclass(kw_only=True)
class DeliveryAddress:
    ddav: bool
    version: int
    name: str
    address: str
    landmark: str
    area: str
    mobile: str
    annotation: str
    instructions: str
    email: str
    city: str
    lat: float
    lng: float
    id: str
    address_line1: str
    address_line2: str
    alternate_mobile: str
    voice_directions_s3_uri: str
    flat_no: str

    def __post_init__(self):
        self.lat = float(self.lat)
        self.lng = float(self.lng)

    def __eq__(self, other):
        return (
            self.id == other.id and self.version == other.version
            if self.ddav
            else self.id == other.id
        )

    def __hash__(self) -> int:
        return hash(str(self.id) + str(self.version))
