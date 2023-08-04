from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.generator import generate
from app.application.protocols.database import DatabaseGateway

generator_router = APIRouter()


@dataclass
class GeneratorResult:
    value: int


@generator_router.get("/generate")
def generator(
        database: Annotated[DatabaseGateway, Depends()],
) -> GeneratorResult:
    value = generate(database)
    return GeneratorResult(
        value=value,
    )
