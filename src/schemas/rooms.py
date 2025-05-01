from pydantic import BaseModel, Field


class RoomPatch(BaseModel):

    title: str| None = Field(default=None)
    description: str | None = Field(default=None)
    price: int
    quantity: int


class RoomAdd(BaseModel):
    title: str
    description: str
    price: int
    quantity: int

class Room(RoomAdd):
    hotel_id: int
