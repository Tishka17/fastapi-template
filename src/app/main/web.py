from fastapi import FastAPI

from app.adapters.db import StubDatabaseGateway
from app.application.protocols.database import DatabaseGateway
from app.presentation.index import index_router
from app.presentation.generator import generator_router


def init_dependencies(app: FastAPI):
    app.dependency_overrides[DatabaseGateway] = StubDatabaseGateway


def init_routers(app: FastAPI):
    app.include_router(index_router)
    app.include_router(generator_router)


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_dependencies(app)
    return app


app = create_app()
