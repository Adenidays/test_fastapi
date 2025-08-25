import uuid
from datetime import datetime
import pytest

from app.domains.tasks.model import Tasks, TaskStatus

pytestmark = pytest.mark.unit


def test_status_enum_values():
    assert {s.value for s in TaskStatus} == {"created", "in_progress", "completed"}


def test_tasks_dataclass_fields_types():
    t = Tasks(
        id=uuid.uuid4(),
        title="Title",
        description="Desc",
        status=TaskStatus.created,
    )
    assert isinstance(t.id, uuid.UUID)
    assert t.title == "Title"
    assert t.description == "Desc"
    assert t.status is TaskStatus.created
    assert isinstance(t.created_at, datetime)


@pytest.mark.skip(reason="")
def test_created_at_should_be_dynamic():
    import uuid as _uuid

    a = Tasks(id=_uuid.uuid4(), title="A", description="", status=TaskStatus.created)
    b = Tasks(id=_uuid.uuid4(), title="B", description="", status=TaskStatus.created)
    assert a.created_at != b.created_at
