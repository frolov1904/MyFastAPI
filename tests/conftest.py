import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.dao import base as base_dao_module
from app.database import Base
from app.main import app
from app.students.models import Major, Student
from app.users.models import User


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5433/myfastapi_test"
)

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True)
async def prepare_test_database(monkeypatch):
    """
    Перед каждым тестом пересоздаём таблицы в тестовой БД.
    Также подменяем async_session_maker, чтобы DAO работал с myfastapi_test.
    """
    monkeypatch.setattr(
        base_dao_module,
        "async_session_maker",
        TestSessionLocal,
    )

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def client():
    """
    Асинхронный клиент для тестирования FastAPI.
    """
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as async_client:
        yield async_client