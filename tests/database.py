from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
from alembic import command

# SQLALCHENY_DATABASE_URL= 'postgresql://postgres:Hathi8120@localhost:5432/FastApi_test'
# SQLALCHENY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'
# SQLALCHENY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME_TEST}'
SQLALCHENY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHENY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# Base.metadata.create_all(bind=engine)


# # We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
# # Dependency
# def overrid_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# client = TestClient(app)


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)   

    
# @pytest.fixture
# def client():
#     Base.metadata.drop_all(bind=engine)
#     #run our code before we run out test
#     Base.metadata.create_all(bind=engine)
#     yield  TestClient(app)
#     #run our code after our test finishes

#*OR using alembic
# @pytest.fixture
# def client():
#     #run our code before we run out test
#     command.upgrade("head")
#     yield  TestClient(app)
#     #run our code after our test finishes
#     command.downgrade("base")