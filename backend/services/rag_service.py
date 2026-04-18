import re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class RAGService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def chunk_text(self, text, size=500, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), size - overlap):
            chunk = " ".join(words[i:i + size])
            chunks.append(chunk)
            if i + size >= len(words):
                break
        return chunks

    def embed_texts(self, texts):
        return self.model.encode(texts)

    def build_faiss_index(self, embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings.astype('float32'))
        return index

    def query_index(self, index, query, k=3):
        query_embedding = self.model.encode([query])
        distances, indices = index.search(query_embedding.astype('float32'), k)
        return indices[0]
