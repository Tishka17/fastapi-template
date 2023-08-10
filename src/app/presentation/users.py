from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import new_user

users_router = APIRouter()


@dataclass
class SomeResult:
    user_id: int


@users_router.get("/")
def get_users(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> SomeResult:
    user = new_user(database, uow, "tishka17")
    return SomeResult(
        user_id=user.id,
    )
