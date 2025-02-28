# test.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add current directory to path
from vector_store import VectorStore

cdps = ["Segment", "mParticle", "Lytics"]
vs = VectorStore(cdps)

queries = [
    "How do I set up a new source in Segment?",
    "How can I create a user profile in mParticle?",
    "How do I build an audience segment in Lytics?"
]

for query in queries:
    print(f"Query: {query}")
    results = vs.search(query)
    for cdp, chunk, distance in results:
        print(f"CDP: {cdp}, Distance: {distance:.4f}")
        print(f"Chunk: {chunk}\n")
