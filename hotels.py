from fastapi import Query,Body,APIRouter

router=APIRouter(prefix="/hotels", tags=["Отели"])




hotels = [
    {"id": 1, "title": "Sochi", "name": "Отель в Сочи"},
    {"id": 2, "title": "Дубай", "name": "Отель в Дубае"},
]


@router.get("/hotels")
def get_hotels(
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
    return hotels_
    # return [hotel for hotel in hotels if hotel["title"]==title and hotel["id"]==id]


# body, request body
@router.post('/hotels')
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })


@router.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}

@router.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int,
                title: str | None = Body(default=None),
                name: str | None = Body(default=None),
                ):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title is not None:
        hotel["title"] = title
    if name is not None:
        hotel["name"] = name
    return {"status": "OK"}