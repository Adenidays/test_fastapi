from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.domains.tasks.model import TaskStatus


class TaskCreateDTO(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.created


class TaskReadDTO(BaseModel):
    id: UUID
    title: str
    description: str
    status: TaskStatus
    created_at: datetime


class TaskUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
