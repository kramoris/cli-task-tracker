import json
from datetime import datetime

CATEGORIES = ["work", "personal", "errands", "study", "other"]

class Task:
    def __init__(self, title, completed=False, category="other", due_date=None):
        self.title = title
        self.completed = completed
        self.category = category
        self.due_date = due_date  # format: "YYYY-MM-DD"

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        due = f" due {self.due_date}" if self.due_date else ""
        return f"{status} ({self.category}) {self.title.strip().capitalize()}{due}"

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed,
            "category": self.category,
            "due_date": self.due_date
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data["completed"],
            data.get("category", "other"),
            data.get("due_date")
        )

tasks = []

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data]
    except FileNotFoundError:
        return []

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=2)

def list_tasks():
    if not tasks:
        print("No tasks yet.")
        return
    print("\nTasks:")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task}")

def choose_category():
    print("\nChoose a category:")
    for i, cat in enumerate(CATEGORIES):
        print(f"{i + 1}. {cat}")
    try:
        choice = int(input("Enter the number: "))
        if 1 <= choice <= len(CATEGORIES):
            return CATEGORIES[choice - 1]
    except ValueError:
        pass
    print("Invalid choice. Defaulting to 'other'.")
    return "other"

def ask_due_date():
    date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    if date_input == "":
        return None
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
        return date_input
    except ValueError:
        print("Invalid date format. Skipping due date.")
        return None

def main():
    global tasks
    tasks = load_tasks()

    while True:
        print("\nOptions:")
        print("1. Show all tasks")
        print("2. Add a task")
        print("3. Mark a task as complete")
        print("4. Edit or delete a task")
        print("5. View tasks by category")
        print("6. View tasks due before a date")
        print("7. Delete all completed tasks")
        print("8. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            list_tasks()

        elif choice == "2":
            title = input("Enter a new task: ").strip().lower()
            category = choose_category()
            due_date = ask_due_date()
            task = Task(title, category=category, due_date=due_date)
            tasks.append(task)
            save_tasks()
            print("Task added.")

        elif choice == "3":
            if not tasks:
                print("No tasks to mark.")
                continue
            try:
                index = int(input("Enter the number of the task to mark as complete: ")) - 1
                if 0 <= index < len(tasks):
                    tasks[index].completed = True
                    save_tasks()
                    print("Task marked as complete.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            if not tasks:
                print("No tasks to edit or delete.")
                continue
            list_tasks()
            try:
                index = int(input("Enter the task number to edit or delete: ")) - 1
                if 0 <= index < len(tasks):
                    print("\nWhat would you like to do?")
                    print("1. Edit task")
                    print("2. Delete task")
                    sub_choice = input("Choose 1 or 2: ")
                    if sub_choice == "1":
                        new_title = input("Enter new title (or leave blank to keep current): ").strip()
                        new_category = choose_category()
                        new_due = ask_due_date()
                        if new_title:
                            tasks[index].title = new_title
                        tasks[index].category = new_category
                        tasks[index].due_date = new_due
                        save_tasks()
                        print("Task updated.")
                    elif sub_choice == "2":
                        del tasks[index]
                        save_tasks()
                        print("Task deleted.")
                    else:
                        print("Invalid choice.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            selected = choose_category()
            filtered = [task for task in tasks if task.category == selected]
            if not filtered:
                print(f"No tasks in category '{selected}'.")
            else:
                print(f"\nTasks in category '{selected}':")
                for i, task in enumerate(filtered):
                    print(f"{i + 1}. {task}")

        elif choice == "6":
            date_input = input("Enter the cutoff date (YYYY-MM-DD): ").strip()
            try:
                cutoff = datetime.strptime(date_input, "%Y-%m-%d")
                filtered = []
                for task in tasks:
                    if task.due_date:
                        try:
                            task_date = datetime.strptime(task.due_date, "%Y-%m-%d")
                            if task_date < cutoff:
                                filtered.append(task)
                        except ValueError:
                            pass
                if not filtered:
                    print(f"No tasks due before {date_input}.")
                else:
                    print(f"\nTasks due before {date_input}:")
                    for i, task in enumerate(filtered):
                        print(f"{i + 1}. {task}")
            except ValueError:
                print("Invalid date format.")

        elif choice == "7":
            tasks = [task for task in tasks if not task.completed]
            save_tasks()
            print("All completed tasks have been deleted.")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

        print()

if __name__ == "__main__":
    main()
