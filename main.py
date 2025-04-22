class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.title}"

tasks = []

def main():
    title = input("Enter a new task: ")
    task = Task(title)
    tasks.append(task)

    print("\nTasks:")
    for t in tasks:
        print(t)

if __name__ == "__main__":
    main()
