"""
Memory Selector

Selects the highest-ranked memories for the LLM context.
"""

from memory.memory_ranker import MemoryRanker


class MemorySelector:
    """
    Selects the best memories after ranking.
    """

    DEFAULT_LIMIT = 10

    @classmethod
    def select(
        cls,
        unified_memory,
        limit=None,
    ):
        """
        Rank memories and return the best ones.
        """

        if limit is None:
            limit = cls.DEFAULT_LIMIT

        for memory in unified_memory:

            metadata = memory.get("metadata", {})

            memory["score"] = MemoryRanker.rank(
                memory_type=memory["memory_type"],
                semantic_score=memory.get("score", 1.0),
                timestamp=metadata.get("last_accessed"),
                memory=metadata,
            )

        ranked_memory = sorted(
            unified_memory,
            key=lambda x: x["score"],
            reverse=True,
        )

        return ranked_memory[:limit]