from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import select  # ⬅ вместо sqlalchemy.future.select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.tasks.abstraction import ITasksRepository
from app.domains.tasks.model import Tasks
from app.infrastructure.task.orm import TaskORM
from app.dto.task import TaskUpdateDTO


class TaskRepository(ITasksRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    def _to_domain(self, row: TaskORM) -> Tasks:
        return Tasks(
            id=row.id,
            title=row.title,
            description=row.description,
            status=row.status,
            created_at=row.created_at,
        )

    async def create_tasks(self, task: Tasks) -> Tasks:
        # избегаем task.__dict__ чтобы не протащить лишние атрибуты
        db_task = TaskORM(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return self._to_domain(db_task)

    async def get_by_id(self, task_id: UUID) -> Optional[Tasks]:
        result = await self.db.execute(select(TaskORM).where(TaskORM.id == task_id))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def list(self) -> List[Tasks]:
        result = await self.db.execute(select(TaskORM))
        return [self._to_domain(row) for row in result.scalars().all()]

    async def delete(self, task_id: UUID) -> None:
        obj = await self.db.get(TaskORM, task_id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()

    async def update(self, tasks_id: UUID, dto: TaskUpdateDTO) -> Optional[Tasks]:
        obj: TaskORM | None = await self.db.get(TaskORM, tasks_id)
        if obj is None:
            return None

        payload = dto.model_dump(exclude_unset=True)

        payload.pop("id", None)
        payload.pop("created_at", None)

        for field, value in payload.items():
            setattr(obj, field, value)

        if hasattr(obj, "updated_at"):
            setattr(obj, "updated_at", datetime.utcnow())

        await self.db.commit()
        await self.db.refresh(obj)
        return self._to_domain(obj)

    async def save(self, task: Tasks) -> Tasks:
        obj: TaskORM | None = await self.db.get(TaskORM, task.id)
        if obj is None:
            obj = TaskORM(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at,
            )
            self.db.add(obj)
        else:
            obj.title = task.title
            obj.description = task.description
            obj.status = task.status

        if hasattr(obj, "updated_at"):
            setattr(obj, "updated_at", datetime.utcnow())

        await self.db.commit()
        await self.db.refresh(obj)
        return self._to_domain(obj)
