from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from app.domains.tasks.model import Tasks
from app.dto.task import TaskUpdateDTO


class ITasksRepository(ABC):
    @abstractmethod
    async def create_tasks(self, tasks: Tasks) -> Tasks:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, tasks_id: UUID) -> Tasks | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Tasks]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, tasks_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def update(self, tasks_id: UUID, dto: TaskUpdateDTO) -> Tasks | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, challenges: Tasks) -> Tasks:
        raise NotImplementedError
