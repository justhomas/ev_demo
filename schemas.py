from pydantic import BaseModel

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    class Config:
        orm_mode = True