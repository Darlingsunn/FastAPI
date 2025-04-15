from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationPARAMS(BaseModel):
    page: Annotated[int, Query(default=1, description="Страница", gt=0)]
    per_page: Annotated[int, Query(default=3, description="Количество Отелей на странице", gt=1, lt=30)]


PaginationDEP = Annotated[PaginationPARAMS, Depends()]
