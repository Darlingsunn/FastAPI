from fastapi import Query, Body, APIRouter
from src.schemas.Hotels import HotelPatch, HotelAdd
from src.api.dependences import PaginationDEP
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDEP,
        location: str | None = Query(None, description='Адрес отеля'),
        title: str | None = Query(None, description='Название отеля'),

):
    per_page = pagination.per_page or 5
    async with (async_session_maker() as session):
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)

        )


@router.get("/{hotel_id}")
async def get_hotel(
        hotel_id: int


):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "location": "ул. Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete('/hotels/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/hotels/{hotel_id}")
async def put_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/hotels/{hotel_id}")
async def patch_hotel(hotel_id: int,
                      hotel_data: HotelPatch
                      ):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
    return {"status": "OK"}
