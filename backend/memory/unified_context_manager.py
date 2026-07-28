"""
Unified Context Manager

Ranks and combines memories from different sources.
"""
from memory.memory_scorer import MemoryScorer


class UnifiedContextManager:

    def build(
        self,
        conversations,
        messages,
        preferences,
        documents,
    ):

        memories = []

        for conversation in conversations:
            memories.append(
                {
                    "type": "conversation",
                    "score": MemoryScorer.score("conversation"),
                    "content": conversation,
                }
            )

        for message in messages:
            memories.append(
                {
                    "type": "message",
                    "score": MemoryScorer.score("conversation"),
                    "content": message,
                }
            )

        for preference in preferences:
            memories.append(
                {
                    "type": "preference",
                    "score": MemoryScorer.score("preference"),
                    "content": preference,
                }
            )

        for document in documents:
            memories.append(
                {
                    "type": "document",
                    "score": MemoryScorer.score("document"),
                    "content": document,
                }
            )

        memories.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return memories