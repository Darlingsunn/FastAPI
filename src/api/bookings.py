from fastapi import APIRouter,Body
from src.api.dependences import DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.rooms import Room

router=APIRouter(prefix="/users", tags=["Бронирования"])

@router.post("/{user_id}/bookings")
async def create_booking(
        user_id: int,
        db: DBDep,
        booking_data: BookingAddRequest = Body()

):

    _booking_data = BookingAdd(user_id=user_id ,**booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}