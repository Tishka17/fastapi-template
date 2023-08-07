from app.application.models import User
from app.application.protocols.database import DatabaseGateway


class StubDatabaseGateway(DatabaseGateway):
    def add_user(self, name: str) -> User:
        return User(
            id=0,
            name=name,
        )

    def get_int(self) -> int:
        return 100
