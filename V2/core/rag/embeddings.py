from sentence_transformers import SentenceTransformer

def embed_texts(texts, model_name="all-MiniLM-L6-v2"):
    """
    Encodes list of texts as embeddings using sentence transformers.
    """
    model = SentenceTransformer(model_name)
    return model.encode(texts, show_progress_bar=True)
