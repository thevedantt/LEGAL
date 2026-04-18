import re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import time

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

    def embed(self, query):
        return self.model.encode([query])

    def retrieve(self, query_embedding, context):
        chunks = self.chunk_text(context)
        chunk_embeddings = self.embed_texts(chunks)
        index = self.build_faiss_index(np.array(chunk_embeddings))
        distances, indices = index.search(query_embedding.astype('float32'), 1)
        return [chunks[i] for i in indices[0]]

    def generate_answer(self, query, docs, llm_client):
        context_str = "\n".join(docs)
        prompt = f"Context: {context_str}\n\nQuestion: {query}\n\nAnswer the question based ONLY on the context."
        return llm_client.generate(prompt)

    def rag_pipeline(self, query, context, llm_client):
        start_total = time.time()

        # ---- Embedding ----
        start_embed = time.time()
        query_embedding = self.embed(query)
        embed_time = time.time() - start_embed

        # ---- Retrieval ----
        start_retrieval = time.time()
        docs = self.retrieve(query_embedding, context)
        retrieval_time = time.time() - start_retrieval

        # ---- LLM ----
        start_llm = time.time()
        response = self.generate_answer(query, docs, llm_client)
        llm_time = time.time() - start_llm

        total_time = time.time() - start_total

        print(f"\nLatency Breakdown:")
        print(f"Embedding: {embed_time:.2f}s")
        print(f"Retrieval: {retrieval_time:.2f}s")
        print(f"LLM: {llm_time:.2f}s")
        print(f"Total: {total_time:.2f}s")

        return response
