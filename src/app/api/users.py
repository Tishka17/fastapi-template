from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import new_user, NewUser
from .depends_stub import Stub

users_router = APIRouter()


@dataclass
class SomeResult:
    user_id: int


@users_router.get("/")
def add_users(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> SomeResult:
    user_id = new_user(database, uow, "tishka17")
    return SomeResult(
        user_id=user_id,
    )


@users_router.get("/alternative")
def add_users_alternative(
        new_user: Annotated[NewUser, Depends(Stub(NewUser))],
) -> SomeResult:
    user_id = new_user("tishka17")
    return SomeResult(
        user_id=user_id,
    )
