import os
from functools import partial
from logging import getLogger
from typing import Iterable

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.adapters.sqlalchemy_db.models import metadata_obj
from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import NewUser
from app.api.depends_stub import Stub

logger = getLogger(__name__)


def all_depends(cls: type) -> None:
    """
    Adds `Depends()` to the class `__init__` methods, so it can be used
    a fastapi dependency having own dependencies
    """
    init = cls.__init__
    total_ars = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(total_ars)
    )


def new_gateway(session: Session = Depends(Stub(Session))):
    yield SqlaGateway(session)


def new_uow(session: Session = Depends(Stub(Session))):
    return session


def create_session_maker():
    db_uri = os.getenv("DB_URI")
    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return sessionmaker(engine, autoflush=False, expire_on_commit=False)


def new_session(session_maker: sessionmaker) -> Iterable[Session]:
    with session_maker() as session:
        yield session


def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()

    app.dependency_overrides[Session] = partial(new_session, session_maker)
    app.dependency_overrides[DatabaseGateway] = new_gateway
    app.dependency_overrides[UoW] = new_uow
    app.dependency_overrides[NewUser] = NewUser
    all_depends(NewUser)
