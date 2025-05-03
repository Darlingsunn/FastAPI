from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, Query, HTTPException, Request

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationPARAMS(BaseModel):
    page: Annotated[int, Query(default=1, description="Страница", gt=0)]
    per_page: Annotated[int | None, Query(default=5, description="Количество Отелей на странице", gt=0, lt=30)]


PaginationDEP = Annotated[PaginationPARAMS, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


GetToken = Annotated[get_token, Depends()]


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]





async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
