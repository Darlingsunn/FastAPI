from fastapi import Query, Body, APIRouter
from src.schemas.rooms import RoomPatch, RoomAdd
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Номера"])


# @router.get("/{hotel_id}")
# async def get_rooms(title: str
#
# ):
#     async with (async_session_maker() as session):
#         return await RoomsRepository(session).get_all(*args,**kwargs)
#

@router.post("/{hotel_id}")
async def create_room(
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "VIP",
                "value": {
                    "hotel_id":2,
                    "title": "VIP комнаты на 2-х",
                    "description": "Номера ЛЮКС-класса с видом на море",
                    "price": 15000,
                    "quantity": 2
                }
            },
            "2": {
                "summary": "MEDIUM",
                "value": {
                    "hotel_id":3,
                    "title": "Уютные комнаты на 4-х",
                    "description": "Номера -класса с видом на море",
                    "price": 7000,
                    "quantity": 4
                }
            } 
        })
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "Done", "data": room}
