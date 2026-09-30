import argparse
import sys

from dime_cli.jobs.news.main import run as run_news
from dime_cli.jobs.focus.focus import run as run_focus
from dime_cli.jobs.todo.todo import run as run_todo

ASCII_LOGO = r"""
██████╗ ██╗███╗   ███╗███████╗
██╔══██╗██║████╗ ████║██╔════╝
██║  ██║██║██╔████╔██║█████╗
██║  ██║██║██║╚██╔╝██║██╔══╝
██████╔╝██║██║ ╚═╝ ██║███████╗
╚═════╝ ╚═╝╚═╝     ╚═╝╚══════╝
"""
def main():
    
    parser = argparse.ArgumentParser(description="dime CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    news_parser = subparsers.add_parser("news",
                                        help="Display current news headlines",
                                        description="Fetches the latest headlines from public news sources.")
    news_parser.add_argument("category", 
                             choices=["tech", "world"], 
                             help="Choose which category of news to display")
    
    focus_parser = subparsers.add_parser("focus",
                                          help="Start focus timer")
    focus_parser.add_argument("mode", 
                               choices=["start", "stop", "reset"],
                               help="Choose focus or break mode")
    
    todo_parser = subparsers.add_parser("todo",
                                        help="Manage your todo list")
    todo_parser.add_argument("param",
                             choices=["add", "list", "complete", "reset"],
                             help="Add a new task, list existing tasks, mark a task as completed, or reset the todo list")
    todo_parser.add_argument("task",
                             nargs="*",
                             help="Task description (required for 'add' command)")


    if len(sys.argv) == 1:
        print(ASCII_LOGO)
        parser.print_help()
        return

    args = parser.parse_args()

    commands = {
        "news": lambda: run_news(args.category),
        "focus": lambda: run_focus(args.mode),
        "todo": lambda: run_todo(args.param, " ".join(args.task) if args.task else None)
    }
    
    commands[args.command]()    



if __name__ == "__main__":
    main()