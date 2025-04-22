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

def main():
    global tasks
    tasks = load_tasks()

    title = input("Enter a new task: ")
    task = Task(title)
    tasks.append(task)

    save_tasks()

    print("\nTasks:")
    for t in tasks:
        print(t)

if __name__ == "__main__":
    main()
