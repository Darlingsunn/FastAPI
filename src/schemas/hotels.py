from pydantic import BaseModel, Field


class HotelPatch(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int
