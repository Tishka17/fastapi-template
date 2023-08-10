from app.application.models import User
from app.application.protocols.database import DatabaseGateway


class StubDatabaseGateway(DatabaseGateway):
    def add_user(self, name: str) -> User:
        user = User(
            name=name,
        )
        user.id = 0
        return user
