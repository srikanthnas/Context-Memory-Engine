from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    """
    Generates embeddings for text.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str):
        return self.model.encode(text)

    def embed_chunks(self, chunks):
        return self.model.encode(chunks)