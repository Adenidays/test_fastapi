import os
import sys
import pathlib
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from app.gateway.routers.task import router as task_router
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import MetaData
from fastapi import FastAPI
from httpx import AsyncClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv()


def build_test_app() -> FastAPI:
    application = FastAPI(title="Project8 API (tests)")
    application.include_router(task_router)
    return application


fastapi_app = build_test_app()

try:
    from app.config import get_db as _get_db
except Exception:

    async def _get_db():
        raise RuntimeError("get_db not found; adjust imports in tests/conftest.py")


try:
    from app.infrastructure.task.orm import Base

    METADATA: MetaData = Base.metadata
except Exception:
    from app.infrastructure.task.orm import TaskORM

    METADATA: MetaData = TaskORM.__table__.metadata

TEST_DATABASE_URL = (
    os.getenv("TEST_DATABASE_URL")
    or os.getenv("DATABASE_URL")
    or "sqlite+aiosqlite:///:memory:"
)


@pytest_asyncio.fixture()
async def engine():
    eng = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        future=True,
        echo=False,
    )
    async with eng.begin() as conn:
        await conn.run_sync(METADATA.create_all)
    try:
        yield eng
    finally:
        async with eng.begin() as conn:
            await conn.run_sync(METADATA.drop_all)
        await eng.dispose()


@pytest_asyncio.fixture()
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    Session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        trans = await session.begin()
        try:
            yield session
        finally:
            if trans.is_active:
                await trans.rollback()


@pytest.fixture()
def app(db_session: AsyncSession) -> FastAPI:
    application = fastapi_app

    async def _override_get_db():
        yield db_session

    application.dependency_overrides[_get_db] = _override_get_db
    return application


@pytest_asyncio.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
