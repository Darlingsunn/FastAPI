from fastapi import Query, Body, APIRouter
from src.schemas.Hotels import Hotel, HotelPatch
from src.api.dependences import PaginationDEP
from sqlalchemy import insert, select
from src.models.hotels import HotelsOrm
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDEP,
        location: str | None = Query(None, description='Адрес отеля'),
        title: str | None = Query(None, description='Название отеля'),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:

        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.like(f"%{location.strip().title()}%"))
        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title.strip().title()}%"))
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]


@router.post("/hotels")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples=
                                                {'1': {'summary': "Сочи", "value": {
                                                    "title": "Отель 5 звезд у моря", "name": "sochi_u_morya",
                                                }}, '2': {'summary': "Dubai", "value": {
                                                    "title": "Отель 5 звезд у fountain", "name": "Dubai_fountain",
                                                }},
                                                 })
                       ):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


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
