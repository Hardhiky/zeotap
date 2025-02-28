# vector_store.py
from annoy import AnnoyIndex
from sentence_transformers import SentenceTransformer
import os

class VectorStore:
    def __init__(self, cdps):
        self.indices = {}
        self.chunks = {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Load the embedding model
        for cdp in cdps:
            # Load the Annoy index
            index_path = f'indices/{cdp}.ann'
            chunks_path = f'indices/{cdp}_chunks.txt'
            if not os.path.exists(index_path) or not os.path.exists(chunks_path):
                raise FileNotFoundError(f"Index or chunks file for {cdp} not found. Ensure scraping is complete.")
            
            embedding_dim = self.model.get_sentence_embedding_dimension()
            index = AnnoyIndex(embedding_dim, 'angular')
            index.load(index_path)
            
            with open(chunks_path, 'r') as f:
                chunks = f.read().split('\n')
            
            self.indices[cdp] = index
            self.chunks[cdp] = chunks
    
    def search(self, query, cdps=None, k=3):
        query_embed = self.model.encode([query])  # Encode the query
        results = []
        if cdps is None:
            cdps = self.indices.keys()  # Search across all CDPs if none specified
        
        for cdp in cdps:
            index = self.indices[cdp]
            chunk_list = self.chunks[cdp]
            
            # Get nearest neighbors
            indices, distances = index.get_nns_by_vector(query_embed[0], k, include_distances=True)
            
            for i, distance in zip(indices, distances):
                if i < len(chunk_list):  # Ensure the index is valid
                    results.append((cdp, chunk_list[i], distance))
        
        # Sort results by distance (lower is better)
        results.sort(key=lambda x: x[2])
        return results[:k]
