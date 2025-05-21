import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, create_engine
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from app.core.config import settings

from app.core.db import init_db,  engine
from app.main import app
from app.models import Item, User
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


engine_2 = create_engine(str(settings.SQLALCHEMY_TEST_2_DATABASE_URI))
@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    """Create a new database session for the test suite."""
    
    # 1. Run migrations using Alembic
    # Construct the path to alembic.ini relative to conftest.py
    alembic_ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini"))
    if not os.path.exists(alembic_ini_path):
        print(f"Error: alembic.ini not found at {alembic_ini_path}. Cannot run migrations.")
    else:
        alembic_cfg = AlembicConfig(alembic_ini_path)
        # Set the database URL for Alembic to use the test database
        alembic_cfg.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))
        alembic_command.upgrade(alembic_cfg, "head")
    
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Item)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()
    
    
@pytest.fixture(scope="function")
def db_2() -> Generator[Session, None, None]:
    """Create a new database session for the test suite."""
    
    # 1. Run migrations using Alembic
    # Construct the path to alembic.ini relative to conftest.py
    alembic_ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini"))
    if not os.path.exists(alembic_ini_path):
        print(f"Error: alembic.ini not found at {alembic_ini_path}. Cannot run migrations.")
    else:
        alembic_cfg = AlembicConfig(alembic_ini_path)
        # Set the database URL for Alembic to use the test database
        alembic_cfg.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_TEST_2_DATABASE_URI))
        alembic_command.upgrade(alembic_cfg, "head")
    
    with Session(engine_2) as session_2:
        init_db(session_2)
        yield session_2
        statement = delete(Item)
        session_2.execute(statement)
        statement = delete(User)
        session_2.execute(statement)
        session_2.commit()
      

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
