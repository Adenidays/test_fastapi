from uuid import uuid4, UUID
from datetime import datetime

from app.domains.tasks.abstraction import ITasksRepository
from app.domains.tasks.model import Tasks
from app.dto.task import TaskCreateDTO, TaskUpdateDTO


class TasksService:
    def __init__(self, repo: ITasksRepository):
        self.repo = repo

    async def create_task(self, dto: TaskCreateDTO) -> Tasks:
        challenge = Tasks(
            id=uuid4(),
            title=dto.title,
            description=dto.description,
            created_at=datetime.utcnow(),
            status=dto.status,
        )
        return await self.repo.create_tasks(challenge)

    async def list(self) -> list[Tasks]:
        return await self.repo.list()

    async def get_by_id(self, tasks_id: UUID) -> Tasks | None:
        return await self.repo.get_by_id(tasks_id)

    async def update(self, tasks_id: UUID, dto: TaskUpdateDTO) -> Tasks | None:
        return await self.repo.update(tasks_id, dto)

    async def delete(self, tasks_id: UUID):
        await self.repo.delete(tasks_id)
