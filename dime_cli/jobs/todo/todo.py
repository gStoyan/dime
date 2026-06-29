
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

TODO_LIST_FILE = BASE_DIR / "todo_list.json"

def load_todo_list():
    if TODO_LIST_FILE.exists():
        try:
            with open(TODO_LIST_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []

def save_todo_list(todo_list):
    try:
        with open(TODO_LIST_FILE, 'w') as f:
            json.dump(todo_list, f)
    except IOError as e:
        print(f"Warning: Could not save todo list: {e}")

def add_task(task):
    todo_list = load_todo_list()
    todo_list.append({"task": task, "completed": False})
    save_todo_list(todo_list)
    print(f"Task added: {task}")

def list_tasks():
    todo_list = load_todo_list()
    if not todo_list:
        print("No tasks in the todo list.")
    else:
        for idx, item in enumerate(todo_list, start=1):
            status = "✓" if item["completed"] else "✗"
            print(f"{idx}. [{status}] {item['task']}")
            
def mark_task_completed(index):
    todo_list = load_todo_list()
    if 0 <= index < len(todo_list):
        todo_list[index]["completed"] = True
        save_todo_list(todo_list)
        print(f"Task marked as completed: {todo_list[index]['task']}")
    else:
        print("Invalid task index.")

def reset_todo_list():
    save_todo_list([])
    print("Todo list has been reset.")

def run (param: str, task: str = None):
    if param == "add":
        if task:
            add_task(task)
        else:
            print("Error: No task provided to add.")
    elif param == "list":
        list_tasks()
    elif param == "complete":
        if task and task.isdigit():
            mark_task_completed(int(task) - 1)
        else:
            print("Error: Please provide a valid task number to mark as completed.")
    elif param == "reset":
        reset_todo_list()
    else:
        print(f"Unknown command: {param}. Use 'add', 'list', 'complete', or 'reset'.\n")

