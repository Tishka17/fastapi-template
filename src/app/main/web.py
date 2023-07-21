from fastapi import FastAPI

from app.presentation.index import index_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(index_router)
    return app


app = create_app()
