import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from rich.console import Console
from rich.table import Table

REDDIT_WORLD_RSS = "https://www.reddit.com/r/worldnews/top/.rss?t=day"

def show_world_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    response = requests.get(
        REDDIT_WORLD_RSS,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    
    # Reddit RSS uses Atom format
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = root.findall('atom:entry', namespace)[:5]

    console = Console()
    table = Table(title="Top 5 World News (Reddit r/worldnews)")
    table.add_column("#")
    table.add_column("Title")
    table.add_column("Updated")


    for index, entry in enumerate(entries, start=1):
        title = entry.find('atom:title', namespace)
        link = entry.find('atom:link', namespace)
        updated = entry.find('atom:updated', namespace)
        
        title_text = title.text if title is not None else "No title"
        link_url = link.get('href') if link is not None else "No link"
        updated_text = updated.text[:10] if updated is not None else "No date"
        
        table.add_row(
            str(index), 
            f"[link={link_url}]{title_text}[/link]", 
            updated_text
        )

    console.print(table)
    print()