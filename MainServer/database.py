from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

name_data_base = f'sqlite:///{settings.database_name.strip()}'

engine = create_engine(name_data_base, echo=False)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    return Session()
