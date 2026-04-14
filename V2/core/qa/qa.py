import requests
import os
import numpy as np

LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LMSTUDIO_MODEL", "mistral")

def answer_question(question, chunks, index, embed_fn, url=LMSTUDIO_URL, model=MODEL_NAME, top_k=5):
    """
    Q&A with retrieval: embeds question, fetches top-k chunks, answers via LLM.
    Returns answer and citations.
    - question: str
    - chunks: list[str]
    - index: faiss index built over chunk embeddings
    - embed_fn: function (list[str]) -> np.array
    """
    q_emb = embed_fn([question])
    neighbors = index.search(np.array(q_emb), top_k)[1][0]
    cited_chunks = [chunks[i] for i in neighbors]
    context = "\n---\n".join([f"[{i}] {c}" for i, c in zip(neighbors, cited_chunks)])
    prompt = f"""You are a legal contract expert. Using ONLY the context below, answer the user's question. Always cite section indices ([index]) that support your answer.

CONTEXT:
{context}

Q: {question}
A (with citations):"""
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 500,
    }
    resp = requests.post(url, json=body)
    if not resp.ok:
        return {"answer": "LLM error", "citations": []}
    answer = resp.json()["choices"][0]["message"]["content"].strip()
    citations = [{"index": int(i), "text": chunks[int(i)]} for i in neighbors]
    return {"answer": answer, "citations": citations}
