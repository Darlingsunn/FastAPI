from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomWithRel
from datetime import date
from src.repositories.utils import rooms_ids_for_booking
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)



        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRel.model_validate(model) for model in result.unique().scalars().all()]


    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        res_s = result.unique().scalars().one_or_none()
        if res_s is None:
            return None
        return RoomWithRel.model_validate(res_s)

