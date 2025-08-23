import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.task import TaskRepository
from app.domains.tasks.model import Tasks, TaskStatus
from app.dto.task import TaskUpdateDTO

pytestmark = pytest.mark.asyncio


async def test_create_and_get(db_session: AsyncSession):
    repo = TaskRepository(db_session)
    created_at = datetime.utcnow() - timedelta(days=1)
    t = Tasks(
        id=uuid4(),
        title="Hello",
        description="World",
        status=TaskStatus.created,
        created_at=created_at,
    )
    created = await repo.create_tasks(t)
    assert created.id == t.id

    got = await repo.get_by_id(t.id)
    assert got is not None
    assert got.id == t.id
    assert got.created_at == created_at


async def test_list_returns_all(db_session: AsyncSession):
    repo = TaskRepository(db_session)
    for i in range(3):
        await repo.create_tasks(
            Tasks(id=uuid4(), title=f"T{i}", description="", status=TaskStatus.created)
        )
    items = await repo.list()
    assert len(items) == 3
    assert {x.title for x in items} == {"T0", "T1", "T2"}


async def test_update_partial(db_session: AsyncSession):
    repo = TaskRepository(db_session)
    t = await repo.create_tasks(
        Tasks(id=uuid4(), title="A", description="B", status=TaskStatus.created)
    )

    dto = TaskUpdateDTO(description="B2")
    updated = await repo.update(t.id, dto)
    assert updated is not None
    assert updated.id == t.id
    assert updated.description == "B2"
    assert updated.title == "A"
    assert updated.status == TaskStatus.created


async def test_update_404(db_session: AsyncSession):
    repo = TaskRepository(db_session)
    dto = TaskUpdateDTO(title="X")
    res = await repo.update(uuid4(), dto)
    assert res is None


async def test_delete_removes(db_session: AsyncSession):
    repo = TaskRepository(db_session)
    t = await repo.create_tasks(
        Tasks(id=uuid4(), title="Del", description="", status=TaskStatus.created)
    )
    assert await repo.get_by_id(t.id) is not None
    await repo.delete(t.id)
    assert await repo.get_by_id(t.id) is None
