from datetime import datetime
from uuid import UUID

from models import Task, TaskRepository, TaskStatus
from views import ConsoleView


class TaskController:
    def __init__(self, repository: TaskRepository, view: ConsoleView) -> None:
        self.repository = repository
        self.view = view

    @staticmethod
    def parse_datetime(date_str: str) -> datetime:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M")

    @staticmethod
    def parse_uuid(id_str: str) -> UUID:
        return UUID(id_str.strip())

    @staticmethod
    def parse_status(status_str: str) -> TaskStatus:
        normalized = status_str.strip().lower()
        mapping = {
            "todo": TaskStatus.TODO,
            "inprogress": TaskStatus.IN_PROGRESS,
            "done": TaskStatus.DONE,
        }
        if normalized not in mapping:
            raise ValueError("Невідомий статус")
        return mapping[normalized]

    def create_task(self, description: str, schedule_str: str) -> Task | None:
        desc = description.strip()
        if not desc:
            self.view.show_message("Помилка: опис не може бути порожнім.")
            return None
        try:
            schedule_for = self.parse_datetime(schedule_str)
        except ValueError:
            self.view.show_message(
                "Помилка: некоректний формат дати. Використовуйте YYYY-MM-DD HH:MM"
            )
            return None

        task = Task(description=desc, schedule_for=schedule_for)
        self.repository.add(task)
        self.view.show_message(f"Задачу створено з ID: {task.id}")
        return task

    def change_status(self, id_str: str, status_str: str) -> bool:
        try:
            task_id = self.parse_uuid(id_str)
            status = self.parse_status(status_str)
        except ValueError:
            self.view.show_message(
                "Помилка: некоректний ID або статус (дозволено: InProgress, Done)."
            )
            return False

        if status == TaskStatus.TODO:
            self.view.show_message(
                "Помилка: статус можна змінити лише на InProgress або Done."
            )
            return False

        updated = self.repository.change_status(task_id, status)
        if not updated:
            self.view.show_message("Задачу з таким ID не знайдено.")
            return False

        self.view.show_message(f"Статус змінено на {status.value}.")
        return True

    def delete_task(self, id_str: str) -> bool:
        try:
            task_id = self.parse_uuid(id_str)
        except ValueError:
            self.view.show_message("Помилка: некоректний формат UUID.")
            return False

        if self.repository.delete(task_id):
            self.view.show_message("Задачу видалено.")
            return True

        self.view.show_message("Задачу з таким ID не знайдено.")
        return False

    def edit_task(
        self, id_str: str, new_description: str, new_schedule_str: str
    ) -> bool:
        try:
            task_id = self.parse_uuid(id_str)
        except ValueError:
            self.view.show_message("Помилка: некоректний формат UUID.")
            return False

        desc = new_description.strip() if new_description.strip() else None
        schedule_for = None
        if new_schedule_str.strip():
            try:
                schedule_for = self.parse_datetime(new_schedule_str)
            except ValueError:
                self.view.show_message(
                    "Помилка: некоректний формат дати (YYYY-MM-DD HH:MM)."
                )
                return False

        updated = self.repository.update(task_id, desc, schedule_for)
        if not updated:
            self.view.show_message("Задачу з таким ID не знайдено.")
            return False

        self.view.show_message("Задачу оновлено.")
        return True

    def list_all_tasks(self) -> None:
        tasks = self.repository.get_all()
        self.view.show_tasks(tasks)

    def filter_tasks(self, status_str: str) -> None:
        try:
            status = self.parse_status(status_str)
        except ValueError:
            self.view.show_message(
                "Помилка: некоректний статус (ToDo, InProgress, Done)."
            )
            return

        tasks = self.repository.filter_by_status(status)
        self.view.show_tasks(tasks)

    def show_task_by_id(self, id_str: str) -> None:
        try:
            task_id = self.parse_uuid(id_str)
        except ValueError:
            self.view.show_message("Помилка: некоректний формат UUID.")
            return

        task = self.repository.get_by_id(task_id)
        if not task:
            self.view.show_message("Задачу з таким ID не знайдено.")
            return

        self.view.show_tasks([task])