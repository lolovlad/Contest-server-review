from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from .settings import settings

name_data_base = f'sqlite:///{settings.database_name.strip()}'
name_data_base_async = f'sqlite+aiosqlite:///{settings.database_name.strip()}'

engine = create_engine(name_data_base, echo=False)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

async_engine = create_async_engine(name_data_base_async, echo=False)
AsySession = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def get_session():
    return Session()
