import faiss
import numpy as np

def build_faiss_index(embeddings):
    """
    Input: numpy array [n_chunks, dim]
    Output: faiss.IndexFlatL2 object
    """
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

def search_index(index, query_embedding, top_k=5):
    D, I = index.search(query_embedding, top_k)
    return I[0]  # indices of top_k nearest neighbors
