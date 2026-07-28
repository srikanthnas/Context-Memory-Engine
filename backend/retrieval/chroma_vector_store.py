import uuid

import chromadb


class ChromaVectorStore:
    """
    Stores and searches embeddings using ChromaDB.

    Collections:
    - document_memory : Document chunks
    - message_memory  : Conversation messages
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        # -------------------------------
        # Document Memory Collection
        # -------------------------------
        self.document_collection = (
            self.client.get_or_create_collection(
                name="document_memory"
            )
        )

        # -------------------------------
        # Message Memory Collection
        # -------------------------------
        self.message_collection = (
            self.client.get_or_create_collection(
                name="message_memory"
            )
        )

    # ======================================================
    # DOCUMENT MEMORY
    # ======================================================

    def add_documents(self, embedded_chunks):
        """
        Store embedded document chunks.
        """

        ids = [
            str(uuid.uuid4())
            for _ in embedded_chunks
        ]

        self.document_collection.add(
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

    def search(
        self,
        query_embedding,
        top_k=3,
        where=None,
    ):
        """
        Search document memory.
        """

        return self.document_collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
            where=where,
        )

    def size(self):
        """
        Number of stored document chunks.
        """

        return self.document_collection.count()

    # ======================================================
    # MESSAGE MEMORY
    # ======================================================

    def add_messages(self, embedded_messages):
        """
        Store embedded conversation messages.
        """

        ids = [
            str(uuid.uuid4())
            for _ in embedded_messages
        ]

        self.message_collection.add(
            ids=ids,
            documents=[
                item["text"]
                for item in embedded_messages
            ],
            embeddings=[
                item["embedding"].tolist()
                for item in embedded_messages
            ],
            metadatas=[
                item["metadata"]
                for item in embedded_messages
            ],
        )

    def search_messages(
        self,
        query_embedding,
        top_k=5,
        where=None,
    ):
        """
        Search conversation memory.
        """

        return self.message_collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
            where=where,
        )

    def message_count(self):
        """
        Number of stored conversation messages.
        """

        return self.message_collection.count()