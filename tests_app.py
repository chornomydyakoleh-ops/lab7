import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch
from uuid import uuid4

from controllers import TaskController
from main import run
from models import TaskRepository, TaskStatus
from views import ConsoleView


class TestToDoApp(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = TaskRepository()
        self.view = ConsoleView()
        self.controller = TaskController(self.repo, self.view)

    def test_create_task_success(self) -> None:
        task = self.controller.create_task("Зробити лабу", "2026-12-01 18:00")
        self.assertIsNotNone(task)
        self.assertEqual(task.description, "Зробити лабу")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(len(self.repo.get_all()), 1)

    def test_create_task_invalid_inputs(self) -> None:
        self.assertIsNone(self.controller.create_task("   ", "2026-12-01 18:00"))
        self.assertIsNone(self.controller.create_task("Тест", "невірна-дата"))

    def test_change_status(self) -> None:
        task = self.controller.create_task("Задача 1", "2026-12-01 12:00")
        task_id = str(task.id)

        self.assertTrue(self.controller.change_status(task_id, "InProgress"))
        self.assertEqual(self.repo.get_by_id(task.id).status, TaskStatus.IN_PROGRESS)

        self.assertTrue(self.controller.change_status(task_id, "Done"))
        self.assertEqual(self.repo.get_by_id(task.id).status, TaskStatus.DONE)

        self.assertFalse(self.controller.change_status(task_id, "ToDo"))
        self.assertFalse(self.controller.change_status(task_id, "Unknown"))
        self.assertFalse(self.controller.change_status("bad-uuid", "Done"))
        self.assertFalse(self.controller.change_status(str(uuid4()), "Done"))

    def test_edit_task(self) -> None:
        task = self.controller.create_task("Старий опис", "2026-12-01 10:00")
        task_id = str(task.id)

        self.assertTrue(
            self.controller.edit_task(task_id, "Новий опис", "2026-12-05 15:30")
        )
        updated = self.repo.get_by_id(task.id)
        self.assertEqual(updated.description, "Новий опис")
        self.assertEqual(updated.schedule_for, datetime(2026, 12, 5, 15, 30))

        self.assertFalse(self.controller.edit_task("invalid-uuid", "Опис", ""))
        self.assertFalse(self.controller.edit_task(task_id, "", "bad-date"))
        self.assertFalse(self.controller.edit_task(str(uuid4()), "Опис", ""))

    def test_delete_task(self) -> None:
        task = self.controller.create_task("На видалення", "2026-12-01 10:00")
        self.assertTrue(self.controller.delete_task(str(task.id)))
        self.assertEqual(len(self.repo.get_all()), 0)

        self.assertFalse(self.controller.delete_task(str(task.id)))
        self.assertFalse(self.controller.delete_task("bad-uuid"))

    def test_filter_and_view_output(self) -> None:
        t1 = self.controller.create_task(
            "Дуже довгий опис задачі понад 25 символів", "2026-12-01 10:00"
        )
        t2 = self.controller.create_task("Друга задача", "2026-12-02 10:00")
        self.controller.change_status(str(t2.id), "Done")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.controller.list_all_tasks()
            self.controller.filter_tasks("Done")
            self.controller.filter_tasks("InvalidStatus")
            self.controller.show_task_by_id(str(t1.id))
            self.controller.show_task_by_id(str(uuid4()))
            self.controller.show_task_by_id("bad-uuid")
            output = fake_out.getvalue()

        self.assertIn("Друга задача", output)
        self.assertIn("...", output)
        self.assertIn("Помилка", output)

    def test_empty_view(self) -> None:
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.view.show_tasks([])
            self.assertIn("Список задач порожній.", fake_out.getvalue())

    def test_main_loop(self) -> None:
        user_inputs = [
            "1", "Тест меню", "2026-12-10 14:00",
            "5",
            "6", "ToDo",
            "2", "wrong-id", "Done",
            "4", "wrong-id", "", "",
            "7", "wrong-id",
            "3", "wrong-id",
            "99",
            "0",
        ]
        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                run()
                output = fake_out.getvalue()

        self.assertIn("Тест меню", output)
        self.assertIn("Невідома команда", output)
        self.assertIn("Роботу завершено.", output)


if __name__ == "__main__":
    unittest.main()