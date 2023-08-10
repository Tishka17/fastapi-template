from fastapi import APIRouter

from .index import index_router
from .users import users_router

root_router = APIRouter()
root_router.include_router(
    users_router,
    prefix="/users",
)
root_router.include_router(
    index_router,
)
