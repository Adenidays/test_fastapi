from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
import uuid

from app.config import Base
from app.domains.tasks.model import TaskStatus


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.created, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
