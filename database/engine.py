# --------------------------------------------------------------------------------
# Движок БД
# --------------------------------------------------------------------------------
# Импорты
# --------------------------------------------------------------------------------


import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base
from database.orm_query import orm_create_db


# --------------------------------------------------------------------------------
# Настройки и константы
# --------------------------------------------------------------------------------


engine = create_async_engine(os.getenv("DB_URL"), echo=True)

session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# --------------------------------------------------------------------------------
# Команды
# --------------------------------------------------------------------------------



async def create_db(): # создание таблиц БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with session_maker() as session: # заполнение таблиц БД
        await orm_create_db(session)


async def drop_db(): # удаление БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
