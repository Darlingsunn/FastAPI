from fastapi import APIRouter, HTTPException, Response
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from passlib.context import CryptContext
from datetime import timezone, timedelta, datetime
import jwt

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
async def register_user(
        data: UserRequestAdd,

):
    hashed_password = pwd_context.hash(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользлватель с таким email не существует")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access token", access_token)
        return {"access_token": access_token}
