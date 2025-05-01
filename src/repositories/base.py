from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)

        result = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)

        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.schema.model_validate(res, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stat = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stat)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_data = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_data)

    async def delete(self, **filter_by):
        del_data = delete(self.model).filter_by(**filter_by)
        await self.session.execute(del_data)
