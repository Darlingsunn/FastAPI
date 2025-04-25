from sqlalchemy import select, func, insert
from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
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
        return result.scalars().all()



