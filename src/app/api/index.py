from fastapi import APIRouter, Request

index_router = APIRouter()


@index_router.get("/")
def index(
        request: Request,
) -> dict:
    return {}
