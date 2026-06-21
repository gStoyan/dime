import argparse

from dime_cli.jobs.news.main import run as run_news
from dime_cli.jobs.focus.focus import run as run_focus

def main():
    parser = argparse.ArgumentParser(description="My CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    news_parser = subparsers.add_parser("news",help="Display current news headlines",description="Fetches the latest headlines from public news sources.")
    news_parser.add_argument("category", choices=["tech", "world"], help="Choose which category of news to display")
    
    focus_parser = subparsers.add_parser("focus", help="Start focus timer")
    focus_parser.add_argument("mode", choices=["start", "stop", "reset"], help="Choose focus or break mode")
    
    args = parser.parse_args()

    if args.command == "news":
        run_news(args.category)
    elif args.command == "focus":
        run_focus(args.mode)    



if __name__ == "__main__":
    main()