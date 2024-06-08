from datetime import datetime
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    cutename = Column(String, nullable=True)
    registered_at = Column(
        TIMESTAMP, default=datetime.now())
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)



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


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)