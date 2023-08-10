from .models import User
from .protocols.database import DatabaseGateway, UoW


def new_user(
        database: DatabaseGateway,
        uow: UoW,
        name: str,
) -> int:
    user = User(name=name)
    database.add_user(user)
    uow.commit()
    return user.id
