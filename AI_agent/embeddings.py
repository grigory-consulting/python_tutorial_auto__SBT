

from openai import OpenAI 
import json 


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio" 
)


def embeddings():

    # Embedding model text -> vector; 
    texts = ["The car is broke down.", "The automobile stopped working.", "I ate a banana."]

    result = client.embeddings.create(model="text-embedding-nomic-embed-text-v1.5", input=texts)
    vectors = [d.embedding for d in result.data]

    def cosine(a,b):
        import math
        dot = sum(x*y for x,y in zip(a,b))
        return dot / (math.hypot(*a) * math.hypot(*b))

    
    #print(vectors)
    print("car vs automobile", cosine(vectors[0], vectors[1]))
    print("car vs banana", cosine(vectors[0], vectors[2]))
    print("automobile vs banana", cosine(vectors[1], vectors[2])) 

    #print(vectors[0])

embeddings()