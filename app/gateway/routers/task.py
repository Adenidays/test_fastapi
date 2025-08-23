from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_db
from app.domains.tasks.service import TasksService
from app.dto.task import TaskCreateDTO, TaskReadDTO, TaskUpdateDTO
from app.repository.task import TaskRepository

router = APIRouter(prefix="/task", tags=["Task"])


def get_service(db: AsyncSession = Depends(get_db)) -> TasksService:
    return TasksService(repo=TaskRepository(db))


@router.post("/", response_model=TaskReadDTO, status_code=status.HTTP_201_CREATED)
async def create_task(
    dto: TaskCreateDTO,
    service: TasksService = Depends(get_service),
):
    created = await service.create_task(dto)
    return created


@router.get("/", response_model=list[TaskReadDTO])
async def list_tasks(service: TasksService = Depends(get_service)):
    return await service.list()


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(
    task_id: UUID,
    service: TasksService = Depends(get_service),
):
    task = await service.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskReadDTO)
async def update_task(
    task_id: UUID,
    dto: TaskUpdateDTO,
    service: TasksService = Depends(get_service),
):
    updated = await service.update(task_id, dto)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    service: TasksService = Depends(get_service),
):
    task = await service.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await service.delete(task_id)
