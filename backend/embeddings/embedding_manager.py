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

    def embed_document_chunks(self, chunks):
        """
        Generate embeddings for all document chunks.
        """

        embeddings = self.model.encode(chunks)

        results = []

        for chunk, embedding in zip(chunks, embeddings):
            results.append({
                "text": chunk,
                "embedding": embedding
            })

        return results