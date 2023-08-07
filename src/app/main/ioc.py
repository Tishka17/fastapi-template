import os
from contextlib import ExitStack
from typing import NewType

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.adapters.sqlalchemy_db.models import metadata_obj
from app.application.protocols.database import DatabaseGateway, UoW

Context = NewType("Context", dict)


class IoC:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def provide_context(self):
        stack = ExitStack()
        context = {
            "stack": stack,
        }
        with stack:
            yield context

    def __getattr__(self, item: str):
        if not item.startswith("provide_"):
            super().__getattr__(item)
        item = item[len("provide_"):]

        def provide_item(context: Context = Depends()):
            if item in context:
                return context[item]
            res = getattr(self, f"_create_{item}")(context)
            context[item] = res
            if hasattr(res, "__exit__"):
                context["stack"].enter_context(res)
            return res

        return provide_item

    def _create_gateway(self, context: Context):
        return SqlaGateway(
            self.provide_session(context),
        )

    def _create_uow(self, context: Context):
        return self.provide_session(context)

    def _create_session(self, context: Context):
        return self.session_factory()


def init_dependencies_ioc(app: FastAPI):
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
    ioc = IoC(sessionmaker(engine, autoflush=False, expire_on_commit=False))

    app.dependency_overrides[Context] = ioc.provide_context
    app.dependency_overrides[Session] = ioc.provide_session
    app.dependency_overrides[DatabaseGateway] = ioc.provide_gateway
    app.dependency_overrides[UoW] = ioc.provide_uow
