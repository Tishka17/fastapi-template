from sqlalchemy.orm import Session

from app.application.models import User
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, name: str) -> User:
        user = User(name=name)
        self.session.add(user)
        return user

    def get_int(self) -> int:
        return 101

