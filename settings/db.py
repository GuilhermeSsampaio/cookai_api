from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

from settings.settings import DATABASE_URL, RESET_DB
from settings.models import setup_models

connect_args = {}
if "postgres" in DATABASE_URL:
    connect_args = {"client_encoding": "utf8"}
elif "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args,
    pool_pre_ping=True,
)


def create_db_and_tables() -> None:
    setup_models()

    if RESET_DB:
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
