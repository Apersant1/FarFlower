from datetime import datetime
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.models import Plant, Base
from sqlalchemy.orm import sessionmaker,Session


class DatabaseInitializer():
    def __init__(self) -> None:
        self.engine = None
        self.async_session_maker = None

    def init_database(self, postgres_dsn):
        self.engine = create_async_engine(postgres_dsn)
        self.async_session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False)


DB_INITIALIZER = DatabaseInitializer()


async def create_db_and_tables():
    async with DB_INITIALIZER.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with DB_INITIALIZER.async_session_maker() as session:
        yield session
