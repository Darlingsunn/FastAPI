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

    async def get_one_or_none(self, id, location, title):
        query = select(HotelsOrm)
        if id:
            query = query.filter(id==HotelsOrm.id)
        if location:
            query = query.filter(location.title()==HotelsOrm.location)
        if title:
            query = query.filter(title.title()==HotelsOrm.title)
        result = await self.session.execute(query)

        return result.scalars().all()
