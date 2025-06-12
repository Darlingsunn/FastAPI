from pydantic import BaseModel, ConfigDict


class FacilitiesTitle(BaseModel):
    title: str
    model_config = ConfigDict(from_attributes=True)


class Facilities(FacilitiesTitle):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int



class RoomFacility(RoomFacilityAdd):
    id: int
