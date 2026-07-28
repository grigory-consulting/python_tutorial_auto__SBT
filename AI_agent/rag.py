"""Simple RAG over the wiki_corpus folders, all local via LM Studio.

Pipeline:
  1. chunk   - split each .txt into ~1500-char chunks at paragraph borders
  2. embed   - one vector per chunk (cached in <corpus>/embeddings.json,
               so the corpus is embedded only once)
  3. retrieve - embed the question, cosine similarity, take top 3 chunks
  4. generate - answer with the chat model, grounded in those chunks only

Run:
  python rag.py "Who invented the CAN bus?"
  python rag.py "Who predicted IoT would dominate IT?" wiki_corpus_smart_building
"""

import json
import math
import sys
from pathlib import Path

from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

CHAT_MODEL = "qwen3-0.6b"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
CHUNK_SIZE = 1500  # characters; roughly 350 tokens
TOP_K = 3

# nomic-embed models are trained with task prefixes; retrieval quality
# collapses without them (documents and queries land in different regions).
DOC_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "
CACHE_VERSION = 2  # bump when chunking or embedding parameters change


def chunk_file(path: Path) -> list:
    """Split into chunks of up to CHUNK_SIZE chars, cutting only between
    paragraphs so no sentence is torn apart."""
    chunks, current = [], ""
    for paragraph in path.read_text(encoding="utf-8").split("\n\n"):
        if len(current) + len(paragraph) > CHUNK_SIZE and current:
            chunks.append(current.strip())
            current = ""
        current += paragraph + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    return [{"file": path.name, "text": c} for c in chunks]


def build_index(corpus_dir: Path) -> list:
    """Chunk + embed the whole corpus; reuse embeddings.json if present."""
    cache = corpus_dir / "embeddings.json"
    chunks = []
    for path in sorted(corpus_dir.glob("*.txt")):
        chunks.extend(chunk_file(path))

    if cache.exists():
        stored = json.loads(cache.read_text(encoding="utf-8"))
        if not isinstance(stored, dict):
            stored = {}  # cache from an older script version, re-embed
        if (stored.get("version") == CACHE_VERSION
                and [c["text"] for c in stored["chunks"]] == [c["text"] for c in chunks]):
            return stored["chunks"]  # corpus unchanged, embeddings still valid

    print(f"embedding {len(chunks)} chunks (one-time)...")
    for start in range(0, len(chunks), 32):  # batches of 32
        batch = chunks[start:start + 32]
        result = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[DOC_PREFIX + c["text"] for c in batch])
        for chunk, data in zip(batch, result.data):
            chunk["vector"] = data.embedding
    cache.write_text(json.dumps({"version": CACHE_VERSION, "chunks": chunks}),
                     encoding="utf-8")
    return chunks


def cosine(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.hypot(*a) * math.hypot(*b))


def retrieve(index: list, question: str) -> list:
    question_vector = client.embeddings.create(
        model=EMBEDDING_MODEL, input=[QUERY_PREFIX + question]).data[0].embedding
    ranked = sorted(index, key=lambda c: cosine(question_vector, c["vector"]),
                    reverse=True)
    return ranked[:TOP_K]


def answer(question: str, corpus_dir: Path) -> None:
    index = build_index(corpus_dir)
    hits = retrieve(index, question)

    context = "\n\n---\n\n".join(f"[{h['file']}]\n{h['text']}" for h in hits)
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system",
             "content": "Answer using only the provided context. If the "
                        "context does not contain the answer, say so. /no_think"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.0,
        max_tokens=300,
    )
    print(f"\nretrieved: {', '.join(h['file'] for h in hits)}")
    print(f"\n{response.choices[0].message.content.strip()}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Usage: python rag.py "<question>" [corpus_dir]')
    question = sys.argv[1]
    corpus = Path(__file__).resolve().parent / (
        sys.argv[2] if len(sys.argv) > 2 else "wiki_corpus")
    if not corpus.is_dir():
        sys.exit(f"No corpus folder: {corpus}")
    answer(question, corpus)


if __name__ == "__main__":
    main()
