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


# alternative implementation using classes
class NewUser:
    def __init__(
            self,
            database: DatabaseGateway,
            uow: UoW,
    ):
        self.database = database
        self.uow = uow

    def __call__(
            self, name: str,
    ) -> int:
        user = User(name=name)
        self.database.add_user(user)
        self.uow.commit()
        return user.id
