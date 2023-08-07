from sqlalchemy import Integer, String, Column, MetaData, Table
from sqlalchemy.orm import registry

from app.application.models import User

metadata_obj = MetaData()
mapper_registry = registry()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String()),
)

mapper_registry.map_imperatively(User, user)
