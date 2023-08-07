from fastapi import FastAPI

from app.main.di_stub import init_dependencies_stub as init_dependencies
# or:
# from app.main.ioc import init_dependencies_ioc as init_dependencies
from app.presentation.generator import generator_router
from app.presentation.index import index_router


def init_routers(app: FastAPI):
    app.include_router(index_router)
    app.include_router(generator_router)


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_dependencies(app)
    return app


app = create_app()
