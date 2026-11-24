from models import Task


class ConsoleView:
    @staticmethod
    def show_menu() -> None:
        print("\nToDo List")
        print("1. Створити задачу")
        print("2. Змінити статус задачі")
        print("3. Видалити задачу")
        print("4. Змінити задачу")
        print("5. Показати всі задачі")
        print("6. Відфільтрувати задачі за статусом")
        print("7. Показати задачу за ID")
        print("0. Вихід")

    @staticmethod
    def show_tasks(tasks: list[Task]) -> None:
        if not tasks:
            print("Список задач порожній.")
            return

        header = (
            f"{'ID':<36} | {'Description':<25} | "
            f"{'Created At':<16} | {'Schedule For':<16} | {'Status':<10}"
        )
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)
        for task in tasks:
            created = task.created_at.strftime("%Y-%m-%d %H:%M")
            scheduled = task.schedule_for.strftime("%Y-%m-%d %H:%M")
            desc = (
                task.description[:22] + "..."
                if len(task.description) > 25
                else task.description
            )
            print(
                f"{str(task.id):<36} | {desc:<25} | "
                f"{created:<16} | {scheduled:<16} | {task.status.value:<10}"
            )
        print(separator)

    @staticmethod
    def show_message(message: str) -> None:
        print(message)