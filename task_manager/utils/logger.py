def log_task_creation(task_title: str, username: str):
    with open("task_log.txt", "a") as f:
        f.write(f"{username} created task: {task_title}\n")
