from sqlalchemy.orm import Session

from app.application.models import User
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, user: User) -> None:
        self.session.add(user)
        return
