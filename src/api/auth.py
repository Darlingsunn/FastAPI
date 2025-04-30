from fastapi import APIRouter, HTTPException,Response,Request
from src.config import settings
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from datetime import timezone, timedelta, datetime
from src.services.auth import AuthService
import jwt
from fastapi import APIRouter, HTTPException, Response

from src.api.dependences import UserIdDep, GetToken

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=AuthService().ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


@router.post("/register")
async def register_user(
        data: UserRequestAdd,

):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_hashed_password(email=data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Пользлватель с таким email не существует")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.patch("/logout")
async def logout_user(
        data: UserRequestAdd,
        response: Response
):
    response.delete_cookie("access_token", "/login")
    return {"status": "Done"}
@router.get("/me")
async def get_me(
         user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user