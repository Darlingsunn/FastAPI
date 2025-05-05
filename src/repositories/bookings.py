from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking
from sqlalchemy import select
from src.models.bookings import BookingsOrm

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_all(
            self,
            booking_id,
            user_id,
            room_id,
            date_from,
            date_to,
            price
    ) -> list[Booking]:
        query = select(BookingsOrm)

        result = await self.session.execute(query)
        return [Booking.model_validate(booking,from_attributes=True) for booking in result.scalars().all()]
