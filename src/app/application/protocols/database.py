from abc import ABC, abstractmethod

from app.application.models import User


class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError


class DatabaseGateway(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError
