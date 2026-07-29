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

                # -------------------------------
        # Conversation Memory Collection
        # -------------------------------

        self.conversation_collection = (
            self.client.get_or_create_collection(
                name="conversation_memory"
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

        # ======================================================
    # CONVERSATION MEMORY
    # ======================================================

    def add_conversations(
        self,
        embedded_conversations,
    ):
        """
        Store embedded conversations.
        """

        ids = [
            str(uuid.uuid4())
            for _ in embedded_conversations
        ]

        self.conversation_collection.add(
            ids=ids,
            documents=[
                item["text"]
                for item in embedded_conversations
            ],
            embeddings=[
                item["embedding"].tolist()
                for item in embedded_conversations
            ],
            metadatas=[
                item["metadata"]
                for item in embedded_conversations
            ],
        )

    def search_conversations(
        self,
        query_embedding,
        top_k=5,
        where=None,
    ):
        """
        Search conversation memory.
        """

        return self.conversation_collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
            where=where,
        )

    def conversation_count(
        self,
    ):
        """
        Number of stored conversations.
        """

        return self.conversation_collection.count()

        return self.message_collection.count()