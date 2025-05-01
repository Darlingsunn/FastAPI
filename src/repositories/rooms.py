from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from sqlalchemy import select

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
    async def get_all(
            self,
            hotel_id,
            title,
            description,
            price,
            quantity
    ) -> list[Room]:
        query = select(RoomsOrm)
        result = await self.session.execute(query)
        return [Room.model_validate(room,from_attributes=True) for room in result.scalars().all()]