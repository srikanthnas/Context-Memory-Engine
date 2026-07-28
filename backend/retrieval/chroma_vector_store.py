import chromadb
import uuid


class ChromaVectorStore:
    """
    Stores and searches document embeddings using ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
        path="./chroma_db"
    )

        self.collection = self.client.get_or_create_collection(
            name="document_memory"
        )

    def add_documents(self, embedded_chunks):
        """
        Store embedded document chunks in ChromaDB.
        """

        ids = [str(uuid.uuid4()) for _ in embedded_chunks]

        self.collection.add(
            ids=ids,
            documents=[
                item["text"]
                for item in embedded_chunks
            ],
            embeddings=[
                item["embedding"].tolist()
                for item in embedded_chunks
            ],
            metadatas=[
                item["metadata"]
                for item in embedded_chunks
            ],
        )

    def search(self, query_embedding, top_k=3, where=None):
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where,
        )

    
        return results

    def size(self):
        return self.collection.count()