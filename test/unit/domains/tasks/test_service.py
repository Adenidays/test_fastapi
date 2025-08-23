import uuid
import pytest
from typing import Optional, List
from datetime import timedelta

from app.domains.tasks.service import TasksService
from app.domains.tasks.abstraction import ITasksRepository
from app.domains.tasks.model import Tasks, TaskStatus
from app.dto.task import TaskCreateDTO, TaskUpdateDTO

pytestmark = pytest.mark.asyncio


class InMemoryTasksRepo(ITasksRepository):
    def __init__(self):
        self._store: dict[uuid.UUID, Tasks] = {}

    async def create_tasks(self, tasks: Tasks) -> Tasks:
        self._store[tasks.id] = tasks
        return tasks

    async def get_by_id(self, tasks_id: uuid.UUID) -> Optional[Tasks]:
        return self._store.get(tasks_id)

    async def list(self) -> List[Tasks]:
        return list(self._store.values())

    async def delete(self, tasks_id: uuid.UUID):
        self._store.pop(tasks_id, None)

    async def update(self, tasks_id: uuid.UUID, dto: TaskUpdateDTO) -> Optional[Tasks]:
        task = self._store.get(tasks_id)
        if task is None:
            return None
        payload = (
            dto.model_dump(exclude_unset=True)
            if hasattr(dto, "model_dump")
            else dto.dict(exclude_unset=True)
        )
        payload.pop("id", None)
        payload.pop("created_at", None)
        for k, v in payload.items():
            setattr(task, k, v)
        self._store[tasks_id] = task
        return task

    async def save(self, tasks: Tasks) -> Tasks:
        self._store[tasks.id] = tasks
        return tasks


@pytest.fixture()
def service() -> TasksService:
    return TasksService(repo=InMemoryTasksRepo())


async def test_create_and_get(service: TasksService):
    dto = TaskCreateDTO(title="T", description="D", status=TaskStatus.created)
    created = await service.create_task(dto)
    got = await service.get_by_id(created.id)
    assert got is not None and got.id == created.id


async def test_list_and_delete(service: TasksService):
    dto = TaskCreateDTO(title="A", description="", status=TaskStatus.created)
    t = await service.create_task(dto)
    items = await service.list()
    assert any(x.id == t.id for x in items)
    await service.delete(t.id)
    assert await service.get_by_id(t.id) is None


async def test_update_partial(service: TasksService):
    dto = TaskCreateDTO(title="Old", description="Desc", status=TaskStatus.created)
    created = await service.create_task(dto)

    patch = TaskUpdateDTO(title="New")
    updated = await service.update(created.id, patch)
    assert updated is not None
    assert updated.title == "New"
    assert updated.description == "Desc"
    assert updated.status is TaskStatus.created


async def test_update_404(service: TasksService):
    assert await service.update(uuid.uuid4(), TaskUpdateDTO(title="X")) is None


@pytest.mark.skip(reason="")
async def test_created_at_not_changed(service: TasksService):
    dto = TaskCreateDTO(title="A", description="B", status=TaskStatus.created)
    created = await service.create_task(dto)
    old = created.created_at - timedelta(days=2)
    created.created_at = old
    await service.repo.save(created)

    updated = await service.update(created.id, TaskUpdateDTO(description="B2"))
    assert updated is not None
    assert updated.created_at == old
