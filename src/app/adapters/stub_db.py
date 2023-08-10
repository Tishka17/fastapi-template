from app.application.models import User
from app.application.protocols.database import DatabaseGateway


class StubDatabaseGateway(DatabaseGateway):
    def add_user(self, user: User) -> None:
        pass
