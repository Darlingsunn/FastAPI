from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.like(f"%{location.strip().title()}%"))
        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title.strip().title()}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

