from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.generator import generate
from app.application.protocols.database import DatabaseGateway, UoW

generator_router = APIRouter()


@dataclass
class GeneratorResult:
    user_id: int


@generator_router.get("/generate")
def generator(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> GeneratorResult:
    user = generate(database, uow, "tishka17")
    return GeneratorResult(
        user_id=user.id,
    )
