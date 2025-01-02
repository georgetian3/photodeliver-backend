import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import nest_asyncio
from fastapi import Depends
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import config
from models.photo import *
from models.user import User

nest_asyncio.apply()


class Database:

    def __init__(self):
        self._url = URL.create(
            drivername=config.DATABASE_DRIVERNAME,
            username=config.DATABASE_USERNAME,
            password=config.DATABASE_PASSWORD,
            host=config.DATABASE_HOST,
            port=config.DATABASE_PORT,
            database=config.DATABASE_NAME,
        )
        self._engine = create_async_engine(self._url)
        self._async_session_maker = async_sessionmaker(
            self._engine, expire_on_commit=False
        )

    async def create(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def reset(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await self.create()

    def get_session(self) -> AsyncSession:
        return self._async_session_maker()


_DATABASE = Database()
asyncio.run(_DATABASE.create())


@asynccontextmanager
async def get_session():
    session = _DATABASE.get_session()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with _DATABASE._async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLModelUserDatabaseAsync(session, User)
