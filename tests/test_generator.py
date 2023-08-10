from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from app.application.models import User
from app.application.protocols.database import DatabaseGateway, UoW
from app.main.web import init_routers


class MockDatabase(DatabaseGateway):
    def add_user(self, user: User) -> None:
        user.id = 42


@fixture
def mock_uow() -> UoW:
    uow = Mock()
    uow.commit = Mock()
    uow.flush = Mock()
    return uow


@fixture
def client(mock_uow):
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[DatabaseGateway] = MockDatabase
    app.dependency_overrides[UoW] = lambda: mock_uow
    return TestClient(app)


def test_generator(client, mock_uow):
    response = client.get("/users")
    mock_uow.commit.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() == {"user_id": 42}
