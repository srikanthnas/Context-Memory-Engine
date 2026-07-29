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
    ):
        """
        Generate an embedding for a single conversation message.
        """

        embedding = self.embed_text(message)

        return {
            "text": message,
            "embedding": embedding,
            "metadata": {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": role,
            },
        }
        # =====================================================
    # CONVERSATION EMBEDDINGS
    # =====================================================

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