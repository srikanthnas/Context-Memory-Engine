import uuid

import chromadb


class ChromaVectorStore:
    """
    Stores and searches embeddings using ChromaDB.

    Collections:
    - document_memory
    - message_memory
    - conversation_memory
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        # ==================================================
        # DOCUMENT MEMORY COLLECTION
        # ==================================================

        self.document_collection = (
            self.client.get_or_create_collection(
                name="document_memory"
            )
        )

        # ==================================================
        # MESSAGE MEMORY COLLECTION
        # ==================================================

        self.message_collection = (
            self.client.get_or_create_collection(
                name="message_memory"
            )
        )

        # ==================================================
        # CONVERSATION MEMORY COLLECTION
        # ==================================================

        self.conversation_collection = (
            self.client.get_or_create_collection(
                name="conversation_memory"
            )
        )

    # ======================================================
    # DOCUMENT MEMORY
    # ======================================================

    def add_documents(
        self,
        embedded_chunks,
    ):
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

    def add_messages(
        self,
        embedded_messages,
    ):
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
        Search message memory.
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

    def delete_messages_by_message_ids(
        self,
        message_ids,
    ):
        """
        Delete message embeddings using their
        SQLite message IDs.

        This keeps ChromaDB synchronized when
        messages are removed from SQLite.
        """

        for message_id in message_ids:

            self.message_collection.delete(
                where={
                    "message_id": message_id
                }
            )

    def reset_message_collection(self):
        """
        Delete and recreate only the message-memory
        collection.

        Document and conversation collections
        are not affected.
        """

        try:
            self.client.delete_collection(
                name="message_memory"
            )
        except Exception:
            pass

        self.message_collection = (
            self.client.get_or_create_collection(
                name="message_memory"
            )
        )

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
            (
                f"conversation_"
                f"{item['metadata']['conversation_id']}"
            )
            for item in embedded_conversations
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

    def conversation_count(self):
        """
        Number of stored conversations.
        """

        return self.conversation_collection.count()

    def update_conversation(
        self,
        embedded_conversation,
    ):
        """
        Replace an existing conversation embedding.
        """

        conversation_id = (
            embedded_conversation[
                "metadata"
            ][
                "conversation_id"
            ]
        )

        vector_id = (
            f"conversation_{conversation_id}"
        )

        # Remove previous embedding if it exists
        try:
            self.conversation_collection.delete(
                ids=[vector_id]
            )
        except Exception:
            pass

        self.conversation_collection.add(
            ids=[vector_id],
            documents=[
                embedded_conversation["text"]
            ],
            embeddings=[
                embedded_conversation[
                    "embedding"
                ].tolist()
            ],
            metadatas=[
                embedded_conversation["metadata"]
            ],
        )

    def delete_conversation(
        self,
        conversation_id: int,
    ):
        """
        Delete a conversation embedding
        from ChromaDB.
        """

        vector_id = (
            f"conversation_{conversation_id}"
        )

        self.conversation_collection.delete(
            ids=[vector_id]
        )