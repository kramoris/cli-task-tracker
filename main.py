class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.title}"

tasks = []

def main():
    task = Task("Finish building CLI Task Tracker")
    tasks.append(task)

    print("Tasks:")
    for t in tasks:
        print(t)

if __name__ == "__main__":
    main()
