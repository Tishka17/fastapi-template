import os
from typing import Callable

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.adapters.sqlalchemy_db.models import metadata_obj
from app.application.protocols.database import DatabaseGateway, UoW


class Stub:
    def __init__(self, dependency: Callable, **kwargs):
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        if isinstance(other, Stub):
            return (
                    self._dependency == other._dependency
                    and self._kwargs == other._kwargs
            )
        else:
            if not self._kwargs:
                return self._dependency == other
            return False

    def __hash__(self):
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)


def new_gateway(session: Session = Depends(Stub(Session))):
    yield SqlaGateway(session)


def new_uow(session: Session = Depends(Stub(Session))):
    return session


def init_dependencies_stub(app: FastAPI):
    db_uri = os.getenv("DB_URI")
    engine = create_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    metadata_obj.create_all(bind=engine)  # TODO migrations
    sm = sessionmaker(engine, autoflush=False, expire_on_commit=False)

    def new_session():
        with sm() as session:
            yield session

    app.dependency_overrides[Session] = new_session
    app.dependency_overrides[DatabaseGateway] = new_gateway
    app.dependency_overrides[UoW] = new_uow
