

# Retrieval Augmented Generation (RAG) 


from openai import OpenAI
from pathlib import Path 

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

CHAT_MODEL = "qwen3-0.6b"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5" # LM Studio standard embedding 
CHUNK_SIZE = 1500 # characters, approx. 350 tokens 
TOP_K = 10 # best 3 chunks 

# nomic requires prefixes
DOC_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "

#QUESTION = "Who predicted that the next era of information technology will be dominated by IoT devices?"
QUESTION2 = "Who forecast in 2004 that connected devices would take over the next generation of IT?"
#QUESTION3 = "What are protocols and industry standards in building automation systems?"
#QUESTION4 = "Which book is doi:10.1007/978-3-031-21343-4 ?"
QUESTION5 = "What is the difference between Asian and European temperature control methods?"


CORPUS_DIR = Path(__file__).resolve().parent / "wiki_corpus_smart_building"

# Pipeline
# 1. Take the documents and chunk them 
# 2. Retrieve the most relevant chunks 
# 3. Build context
# 4. Generate + ground the answer with sources (cite)


def chunk_file(path):
    chunks = [] 
    current = "" # current chunk 
    for paragraph in path.read_text().split("\n\n"): 
        if len(current) + len(paragraph) > CHUNK_SIZE and current:
            chunks.append(current)
            current = ""
        current += paragraph + "\n\n"

    chunks.append(current)

    return [{"file": path.name, "text": c} for c in chunks]

def embed(corpus):
    chunks = []
    for doc in sorted(corpus.glob("*.txt")): # all text files 
        chunks.extend(chunk_file(doc)) # add new chunks to existing chunks 

    print("Embedding of chunks")

    for chunk in chunks:
        result = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input = DOC_PREFIX + chunk["text"]
        )
        chunk["vector"] = result.data[0].embedding

    return chunks

def cosine(a,b):
        import math
        dot = sum(x*y for x,y in zip(a,b))
        return dot / (math.hypot(*a) * math.hypot(*b))

def retrieve(embeddings, question):
    question_vector = client.embeddings.create(
         model=EMBEDDING_MODEL,
         input=QUERY_PREFIX + question
    )
    ranked = sorted(
         embeddings,
                    key= lambda c: cosine(question_vector.data[0].embedding, c["vector"]),
                    reverse=True
                )
    return ranked[:TOP_K] # first three 

def answer(question, corpus):
    embeddings = embed(corpus=corpus)
    hits = retrieve(embeddings=embeddings,question=question)

    context = "\n\n---\n\n".join(f"[{h['file']}]\n{h['text']}" for h in hits) # Augmentation 

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system",
            "content": "Answer using only the provided context. If the "
                        "context does not contain the answer, say so. "},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.0,
    )
    print(f"\n{response.choices[0].message.content.strip()}")

answer(QUESTION5,CORPUS_DIR)