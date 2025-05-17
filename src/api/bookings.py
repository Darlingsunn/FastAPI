from fastapi import APIRouter, Body
from src.api.dependences import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.models.bookings import BookingsOrm

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get("/me")
async def current_user_booking(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


# @router.post("/{user_id}/bookings")
# async def create_booking(
#         user_id: UserIdDep,
#         db: DBDep,
#         booking_data: BookingAddRequest = Body()
#
# ):
#     room = await db.rooms.get_one_or_none(id=booking_data.room_id)
#     room_price: int = room.price
#     total_booking_price = BookingsOrm(price=room_price, **booking_data.model_dump()).total_cost
#     _booking_data = BookingAdd(user_id=user_id, price=total_booking_price, **booking_data.model_dump())
#     booking = await db.bookings.add(_booking_data)
#     await db.commit()
#     return {"status": "OK", "data": booking}


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
       **booking_data.dict(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}