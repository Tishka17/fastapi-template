from .models import User
from .protocols.database import DatabaseGateway, UoW


def new_user(
        database: DatabaseGateway,
        uow: UoW,
        name: str,
) -> User:
    user = database.add_user(name)
    uow.commit()
    return user
