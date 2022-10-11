from pydantic import BaseModel


class Address(BaseModel):
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
    address_id: int
    address_line1: str
    address_line2: str
    alternate_mobile: str
    flat_no: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return NotImplemented
        return (
            self.address_id == other.address_id and self.version == other.version
            if self.ddav
            else self.address_id == other.address_id
        )

    def __hash__(self) -> int:
        return (
            hash(str(self.address_id) + str(self.version))
            if self.ddav
            else hash(str(self.address_id))
        )
