import chromadb
from chromadb.config import Settings
import uuid


class ChromaVectorStore:
    """
    Stores and searches document embeddings using ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.Client(
            Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name="document_memory"
        )

    def add_documents(self, embedded_chunks):
        """
        embedded_chunks:
        [
            {
                "text": "...",
                "embedding": [...]
            }
        ]
        """

        ids = [str(uuid.uuid4()) for _ in embedded_chunks]

        self.collection.add(
            ids=ids,
            documents=[item["text"] for item in embedded_chunks],
            embeddings=[
                item["embedding"].tolist()
                for item in embedded_chunks
            ],
        )

    def search(self, query_embedding, top_k=3):

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
        )

        return results

    def size(self):
        return self.collection.count()