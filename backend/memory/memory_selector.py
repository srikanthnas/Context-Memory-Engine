"""
Memory Selector

Selects the highest-ranked memories for the LLM context.
"""


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
        Select the top-ranked memories.
        """

        if limit is None:
            limit = cls.DEFAULT_LIMIT

        return unified_memory[:limit]