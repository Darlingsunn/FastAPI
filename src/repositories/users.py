from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword
from sqlalchemy import select
from pydantic import EmailStr


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)

        result = await self.session.execute(query)
        res = result.scalars().one()
        if res is None:
            return None
        return UserWithHashedPassword.model_validate(res)
