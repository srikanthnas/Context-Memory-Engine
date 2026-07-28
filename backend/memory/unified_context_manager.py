"""
Unified Context Manager

Combines memories from all memory sources into a single ranked list.
"""

from memory.memory_ranker import MemoryRanker


class UnifiedContextManager:
    """
    Builds a unified ranked memory list.
    """

    def build(
        self,
        conversations,
        messages,
        preferences,
        documents,
    ):

        unified_memory = []

        # -------------------------------
        # Preferences
        # -------------------------------

        for preference in preferences:

            preference["memory_type"] = "preference"

            preference["score"] = MemoryRanker.rank(
                memory_type="preference",
                memory=preference,
            )

            unified_memory.append(preference)

        # -------------------------------
        # Conversations
        # -------------------------------

        for conversation in conversations:

            conversation["memory_type"] = "conversation"

            conversation["score"] = MemoryRanker.rank(
                memory_type="conversation",
                timestamp=conversation.get("created_at"),
                memory=conversation,
            )

            unified_memory.append(conversation)

        # -------------------------------
        # Messages
        # -------------------------------

        for message in messages:

            message["memory_type"] = "message"

            message["score"] = MemoryRanker.rank(
            memory_type="message",
            timestamp=message.get("created_at"),
            memory=message,
        )

            unified_memory.append(message)

        # -------------------------------
        # Documents
        # -------------------------------

        for document in documents:

            document["memory_type"] = "document"

            semantic = document.get("similarity", 1.0)

            document["score"] = MemoryRanker.rank(
                memory_type="document",
                semantic_score=semantic,
                timestamp=document.get("created_at"),
                memory=document,
)

            unified_memory.append(document)

        # -------------------------------
        # Highest score first
        # -------------------------------

        unified_memory.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return unified_memory