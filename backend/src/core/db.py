import math
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from core.config import CONFIG


def local_db_url_factory(
    user: str, password: str, name: str, host: str, port: int, is_async: bool = True
):
    protocol = "postgresql+asyncpg" if is_async else "postgresql"
    return f"{protocol}://{user}:{password}@/{name}?host={host}&port={port}"


url_primary = local_db_url_factory(
    CONFIG.DB.USER, CONFIG.DB.PASSWORD, CONFIG.DB.NAME, CONFIG.DB.HOST, CONFIG.DB.PORT
)

engine = None


def create_engine_async():
    global engine
    engine = create_async_engine(
        url_primary,
        future=True,
        echo_pool=True,
        pool_timeout=180,
        pool_size=max(1, math.floor(CONFIG.DB.POOL_SIZE / CONFIG.UVICORN.WORKERS)),
    )


async def get_session():
    global engine
    if engine is None:
        create_engine_async()

    async with AsyncSession(engine) as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_session)]
