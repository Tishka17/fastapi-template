from app.application.protocols.database import DatabaseGateway
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from app.main.web import init_routers, init_dependencies


class MockDatabase(DatabaseGateway):

    def get_int(self) -> int:
        return 0


@fixture
def client():
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[DatabaseGateway] = MockDatabase
    return TestClient(app)


def test_generator(client):
    response = client.get("/generate")
    assert response.status_code == 200
    assert response.json() == {"value": 0}
