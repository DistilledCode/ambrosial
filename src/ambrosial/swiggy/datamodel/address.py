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
    add_id: int
    address_line1: str
    address_line2: str
    alternate_mobile: str
    flat_no: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return NotImplemented
        return (
            self.add_id == other.add_id and self.version == other.version
            if self.ddav
            else self.add_id == other.add_id
        )

    def __hash__(self) -> int:
        return hash(str(self.add_id) + str(self.version))
