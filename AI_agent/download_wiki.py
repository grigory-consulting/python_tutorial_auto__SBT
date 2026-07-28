"""Download Wikipedia articles as plain text for the RAG corpus.

Uses the official Wikipedia API (no scraping): action=query&prop=extracts
returns the article body as plain text, without markup, infoboxes or
references. Each article lands in wiki_corpus/<name>.txt with a small
attribution header (Wikipedia text is licensed CC BY-SA 4.0).

Run:  python download_wiki.py
Only the standard library is needed.
"""

import json
import urllib.parse
import urllib.request
from pathlib import Path

TITLES = [
    "Automotive industry",
    "Car",
    "Electric vehicle",
    "Hybrid electric vehicle",
    "Internal combustion engine",
    "Self-driving car",
    "Automotive safety",
    "Automotive engineering",
    "CAN bus",
    "Charging station",
]

API = "https://en.wikipedia.org/w/api.php"
OUT = Path(__file__).resolve().parent / "wiki_corpus"


def fetch_plain_text(title: str) -> str:
    params = urllib.parse.urlencode({
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "format": "json",
        "redirects": 1,
        "titles": title,
    })
    request = urllib.request.Request(
        f"{API}?{params}",
        headers={"User-Agent": "python-tutorial-corpus-builder/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    page = next(iter(data["query"]["pages"].values()))
    if "extract" not in page:
        raise ValueError(f"No article found for '{title}'")
    return page["extract"]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for title in TITLES:
        text = fetch_plain_text(title)
        url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
        header = (
            f"{title}\n"
            f"Source: {url}\n"
            f"License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)\n"
            f"{'=' * 70}\n\n"
        )
        filename = title.lower().replace(" ", "_").replace("-", "_") + ".txt"
        path = OUT / filename
        path.write_text(header + text, encoding="utf-8")
        print(f"{filename}: {len(text):,} chars")


if __name__ == "__main__":
    main()
