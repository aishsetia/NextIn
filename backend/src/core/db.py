import json
import math
from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from pydantic_core import to_jsonable_python
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import CONFIG


class PydanticType(sa.types.TypeDecorator):
    """
    Pydantic type.
    SAVING:
    - Uses SQLAlchemy JSON type under the hood.
    - Acceps the pydantic model and converts it to a dict on save.
    - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
    - Pulls the string from the database.
    - SQLAlchemy engine JSON-decodes the string to a dict.
    - Uses the dict to create a pydantic model.
    """

    impl = sa.types.JSON

    def __init__(self, pydantic_type=None):
        super().__init__()
        self.pydantic_type = pydantic_type

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(sa.JSON())

    def process_bind_param(self, value, dialect):
        return jsonable_encoder(value) if value else None

    def process_result_value(self, value, dialect):
        return TypeAdapter(self.pydantic_type).validate_python(value) if value else None

    @staticmethod
    def json_serializer(*args, **kwargs) -> str:
        return json.dumps(*args, default=to_jsonable_python, **kwargs)


def local_db_url_factory(
    user: str, password: str, name: str, host: str, port: int, is_async: bool = True
):
    protocol = "postgresql+asyncpg" if is_async else "postgresql"
    return f"{protocol}://{user}:{password}@/{name}?host={host}&port={port}"


url_primary = local_db_url_factory(
    CONFIG.DB.USER, CONFIG.DB.PASSWORD, CONFIG.DB.NAME, CONFIG.DB.HOST, CONFIG.DB.PORT
)

url_primary_sync = local_db_url_factory(
    CONFIG.DB.USER,
    CONFIG.DB.PASSWORD,
    CONFIG.DB.NAME,
    CONFIG.DB.HOST,
    CONFIG.DB.PORT,
    is_async=False,
)

engine = None
engine_sync = None


def create_engine_async():
    global engine
    engine = create_async_engine(
        url_primary,
        future=True,
        echo_pool=True,
        pool_timeout=180,
        pool_size=max(1, math.floor(CONFIG.DB.POOL_SIZE / CONFIG.UVICORN.WORKERS)),
        json_serializer=PydanticType.json_serializer,
    )


def create_engine_sync():
    global engine_sync
    engine_sync = create_engine(
        url_primary_sync,
        future=True,
        echo_pool=True,
        pool_timeout=180,
        pool_size=max(1, math.floor(CONFIG.DB.POOL_SIZE / CONFIG.UVICORN.WORKERS)),
        json_serializer=PydanticType.json_serializer,
    )


async def get_session():
    global engine
    if engine is None:
        create_engine_async()

    async with AsyncSession(engine) as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_session)]
