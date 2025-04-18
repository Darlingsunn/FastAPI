from fastapi import Query, Body, APIRouter
from src.schemas.Hotels import Hotel, HotelPatch
from src.api.dependences import PaginationDEP

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDEP,
        id: int | None = Query(None, description='Айди отеля'),
        title: str | None = Query(None, description='Название отеля'),

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page

    return hotels_[start:end]


@router.post("/hotels")
def create_hotel(hotel_data: Hotel = Body(openapi_examples=
                                          {'1': {'summary': "Сочи", "value": {
                                              "title": "Отель 5 звезд у моря", "name": "sochi_u_morya",
                                          }}, '2': {'summary': "Dubai", "value": {
                                              "title": "Отель 5 звезд у fountain", "name": "Dubai_fountain",
                                          }},
                                           })
                 ):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })


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
