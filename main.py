import json

class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.title}"

    def to_dict(self):
        return {"title": self.title, "completed": self.completed}

    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["completed"])

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

def main():
    global tasks
    tasks = load_tasks()

    list_tasks()

    print("\nOptions:")
    print("1. Add a task")
    print("2. Mark a task as complete")

    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        title = input("Enter a new task: ")
        task = Task(title)
        tasks.append(task)
        save_tasks()
        print("Task added.")
    elif choice == "2":
        if not tasks:
            print("No tasks to mark.")
            return
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
    else:
        print("Invalid option.")

    print()
    list_tasks()

if __name__ == "__main__":
    main()
