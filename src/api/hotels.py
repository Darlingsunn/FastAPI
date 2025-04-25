from fastapi import Query, Body, APIRouter
from src.schemas.Hotels import Hotel, HotelPatch
from src.api.dependences import PaginationDEP
from sqlalchemy import insert, select
from src.models.hotels import HotelsOrm
from src.database import async_session_maker
from repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDEP,
        location: str | None = Query(None, description='Адрес отеля'),
        title: str | None = Query(None, description='Название отеля'),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("")
async def create_hotel(
        title: str = Body(embed=True),
        location: str = Body(embed=True),

):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(
            title=title,
            location=location
        )
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int,
                hotel_data: HotelPatch
                ):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title is not None:
        hotel["title"] = hotel_data.title
    if hotel_data.name is not None:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}
