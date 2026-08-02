from sentence_transformers import SentenceTransformer
import numpy as np


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

    # =====================================================
    # DOCUMENT EMBEDDINGS
    # =====================================================

    def embed_document_chunks(
        self,
        chunks,
        document_id=None,
        user_id=None,
        filename=None,
    ):
        """
        Generate embeddings for document chunks.
        """

        embeddings = self.embed_chunks(chunks)

        results = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            results.append(
                {
                    "text": chunk,
                    "embedding": embedding,
                    "metadata": {
                        "document_id": document_id,
                        "user_id": user_id,
                        "filename": filename,
                        "chunk_index": index,
                    },
                }
            )

        return results

    # =====================================================
    # MESSAGE EMBEDDINGS
    # =====================================================

    def embed_message(
        self,
        message,
        conversation_id,
        user_id,
        role,
        message_id=None,
    ):
        """
        Generate an embedding for a single conversation message.

        Stores the SQLite message ID in ChromaDB metadata
        so semantic memories can be mapped back to the
        original database record.
        """

        embedding = self.embed_text(message)

        return {
            "text": message,
            "embedding": embedding,
            "metadata": {
                "message_id": message_id,
                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": role,
            },
        }

    def embed_conversation(
        self,
        title,
        summary,
        conversation_id,
        user_id,
    ):
        """
        Generate an embedding for a conversation.
        """

        text = f"{title}\n\n{summary}"

        embedding = self.embed_text(text)

        return {
            "text": text,
            "embedding": embedding,
            "metadata": {
                "conversation_id": conversation_id,
                "user_id": user_id,
            },
        }

    def cosine_similarity(
        self,
        embedding_a,
        embedding_b,
    ):
        """
        Calculate cosine similarity between two embeddings.
        """

        embedding_a = np.asarray(embedding_a)
        embedding_b = np.asarray(embedding_b)

        denominator = (
            np.linalg.norm(embedding_a)
            * np.linalg.norm(embedding_b)
        )

        if denominator == 0:
            return 0.0

        return float(
            np.dot(embedding_a, embedding_b)
            / denominator
        )