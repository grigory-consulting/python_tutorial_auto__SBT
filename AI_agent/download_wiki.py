"""Download Wikipedia articles as plain text for the RAG corpus.

Uses the official Wikipedia API (no scraping): action=query&prop=extracts
returns the article body as plain text, without markup, infoboxes or
references. Each article lands in wiki_corpus/<name>.txt with a small
attribution header (Wikipedia text is licensed CC BY-SA 4.0).

Run:  python download_wiki.py                 (all topics)
      python download_wiki.py smart_building  (one topic)
Only the standard library is needed.
"""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

TOPICS = {
    "auto": [
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
    ],
    "smart_building": [
        "Building automation",
        "Home automation",
        "Heating, ventilation, and air conditioning",
        "Internet of things",
        "Smart meter",
        "Smart grid",
        "Smart thermostat",
        "BACnet",
        "KNX",
        "Digital twin",
    ],
}

# topic -> output directory ("auto" keeps its original folder name)
CORPUS_DIRS = {
    "auto": "wiki_corpus",
    "smart_building": "wiki_corpus_smart_building",
}

API = "https://en.wikipedia.org/w/api.php"
ROOT = Path(__file__).resolve().parent


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


def download_topic(topic: str) -> None:
    out = ROOT / CORPUS_DIRS[topic]
    out.mkdir(exist_ok=True)
    print(f"[{topic}] -> {out.name}/")
    for title in TOPICS[topic]:
        text = fetch_plain_text(title)
        url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
        header = (
            f"{title}\n"
            f"Source: {url}\n"
            f"License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)\n"
            f"{'=' * 70}\n\n"
        )
        filename = (title.lower().replace(",", "").replace(" ", "_")
                    .replace("-", "_") + ".txt")
        (out / filename).write_text(header + text, encoding="utf-8")
        print(f"  {filename}: {len(text):,} chars")


def main() -> None:
    requested = sys.argv[1:] or list(TOPICS)
    for topic in requested:
        if topic not in TOPICS:
            sys.exit(f"Unknown topic '{topic}'. Available: {', '.join(TOPICS)}")
        download_topic(topic)


if __name__ == "__main__":
    main()
