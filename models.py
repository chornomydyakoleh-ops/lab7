from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class TaskStatus(Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


@dataclass
class Task:
    description: str
    schedule_for: datetime
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.TODO


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: UUID) -> Task | None:
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def filter_by_status(self, status: TaskStatus) -> list[Task]:
        return [task for task in self._tasks.values() if task.status == status]

    def update(
        self,
        task_id: UUID,
        description: str | None = None,
        schedule_for: datetime | None = None,
    ) -> Task | None:
        task = self._tasks.get(task_id)
        if not task:
            return None
        if description is not None:
            task.description = description
        if schedule_for is not None:
            task.schedule_for = schedule_for
        return task

    def change_status(self, task_id: UUID, status: TaskStatus) -> Task | None:
        task = self._tasks.get(task_id)
        if not task:
            return None
        task.status = status
        return task

    def delete(self, task_id: UUID) -> bool:
        return self._tasks.pop(task_id, None) is not None