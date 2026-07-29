"""Simple RAG over the wiki_corpus folder, all local via LM Studio.

Pipeline:
  1. chunk    - split each .txt into ~1500-char chunks at paragraph borders
  2. embed    - one vector per chunk
  3. retrieve - embed the question, cosine similarity, take top 3 chunks
                (plus a hand-made BM25 lexical retriever for comparison)
  4. generate - answer with the chat model, grounded in those chunks only
"""

import math
import re
from collections import Counter
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

QUESTION = "Who built a clockwork-driven carriage?"
CORPUS_DIR = Path(__file__).resolve().parent / "wiki_corpus"


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
    """Chunk + embed the whole corpus."""
    chunks = []
    for path in sorted(corpus_dir.glob("*.txt")):
        chunks.extend(chunk_file(path))

    print(f"embedding {len(chunks)} chunks...")
    for start in range(0, len(chunks), 32):  # batches of 32
        batch = chunks[start:start + 32]
        result = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[DOC_PREFIX + c["text"] for c in batch])
        for chunk, data in zip(batch, result.data):
            chunk["vector"] = data.embedding
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


def tokenize(text: str) -> list:
    return re.findall(r"[a-z0-9]+", text.lower())


def retrieve_bm25(index: list, question: str, k1: float = 1.5, b: float = 0.75) -> list:
    """Classic lexical retrieval, no embeddings involved.

    Score of a chunk = sum over question words of
        idf(word) * saturated_tf(word)
    idf: rare words count more than common ones ("clockwork" >> "the")
    saturated_tf: 2nd occurrence of a word adds less than the 1st (k1),
    and long chunks are penalized so they don't win by sheer size (b)."""
    docs = [tokenize(c["text"]) for c in index]
    n = len(docs)
    average_length = sum(len(d) for d in docs) / n

    document_frequency = Counter()  # in how many chunks does each word occur?
    for d in docs:
        document_frequency.update(set(d))

    scored = []
    for chunk, doc in zip(index, docs):
        term_frequency = Counter(doc)
        score = 0.0
        for word in set(tokenize(question)):
            tf = term_frequency[word]
            if tf == 0:
                continue
            df = document_frequency[word]
            idf = math.log((n - df + 0.5) / (df + 0.5) + 1)
            score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(doc) / average_length))
        scored.append((score, chunk))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:TOP_K]]


def answer(question: str, corpus_dir: Path) -> None:
    index = build_index(corpus_dir)
    hits = retrieve(index, question)
    bm25_hits = retrieve_bm25(index, question)
    print(f"\nretrieved (embeddings): {', '.join(h['file'] for h in hits)}")
    print(f"retrieved (bm25):       {', '.join(h['file'] for h in bm25_hits)}")

    context = "\n\n---\n\n".join(f"[{h['file']}]\n{h['text']}" for h in hits)
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system",
             "content": "Answer using only the provided context. If the "
                        "context does not contain the answer, say so. "},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.0,
        max_tokens=300,
    )
    print(f"\n{response.choices[0].message.content.strip()}")


if __name__ == "__main__":
    answer(QUESTION, CORPUS_DIR)
