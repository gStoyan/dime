import requests

from datetime import datetime
from rich.console import Console
from rich.table import Table

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"


def show_tech_news():
    response = requests.get(HN_TOP_STORIES_URL, timeout=10)
    response.raise_for_status()

    story_ids = response.json()[:5]

    console = Console()
    table = Table(title="Tech News")
    table.add_column("#")
    table.add_column("Title")
    table.add_column("Score")
    table.add_column("Time")

    for index, story_id in enumerate(story_ids, start=1):
        story_response = requests.get(
            HN_ITEM_URL.format(item_id=story_id),
            timeout=10,
        )
        story_response.raise_for_status()

        story = story_response.json()

        title = story.get("title", "No title")
        url = story.get(
            "url",
            f"https://news.ycombinator.com/item?id={story_id}",
        )
        score = story.get("score", "No score")
        time = datetime.fromtimestamp(story.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")

        table.add_row(str(index), f"[link={url}]{title}[/link]", str(score), time)


    console.print(table)
    print()
