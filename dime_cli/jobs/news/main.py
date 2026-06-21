from dime_cli.jobs.news.tech import show_tech_news
from dime_cli.jobs.news.world import show_world_news

def run(category: str):
    if category == "tech":
        show_tech_news()
    elif category == "world":
        show_world_news()
    else:
        print("Unknown news category.")
        print("Use:")
        print("  dime news tech")
        print("  dime news world")
        print("  dime news business")