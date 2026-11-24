from controllers import TaskController
from models import TaskRepository
from views import ConsoleView


def run() -> None:
    repository = TaskRepository()
    view = ConsoleView()
    controller = TaskController(repository, view)

    while True:
        view.show_menu()
        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            desc = input("Опис задачі: ")
            sched = input("Запланувати на (YYYY-MM-DD HH:MM): ")
            controller.create_task(desc, sched)
        elif choice == "2":
            task_id = input("Введіть ID задачі: ")
            status = input("Новий статус (InProgress / Done): ")
            controller.change_status(task_id, status)
        elif choice == "3":
            task_id = input("Введіть ID задачі: ")
            controller.delete_task(task_id)
        elif choice == "4":
            task_id = input("Введіть ID задачі: ")
            desc = input("Новий опис (Enter, щоб залишити без змін): ")
            sched = input("Нова дата (YYYY-MM-DD HH:MM, або Enter): ")
            controller.edit_task(task_id, desc, sched)
        elif choice == "5":
            controller.list_all_tasks()
        elif choice == "6":
            status = input("Введіть статус (ToDo / InProgress / Done): ")
            controller.filter_tasks(status)
        elif choice == "7":
            task_id = input("Введіть ID задачі: ")
            controller.show_task_by_id(task_id)
        elif choice == "0":
            view.show_message("Роботу завершено.")
            break
        else:
            view.show_message("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    run()