from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


@dataclass
class Tasks:
    id: UUID
    title: str
    description: str
    status: TaskStatus
    created_at: datetime = datetime.utcnow()
