"""
Memory Selector

Selects the highest-ranked memories for the LLM context.
"""

from memory.memory_config import (
    MAX_CONVERSATIONS,
    MAX_DOCUMENTS,
    MAX_MEMORY_ITEMS,
    MAX_MESSAGES,
    MAX_PREFERENCES,
)


class MemorySelector:
    """
    Selects the best memories after ranking.
    """

    @classmethod
    def select(
        cls,
        unified_memory,
    ):
        """
        Select the highest-ranked memories while maintaining
        a balanced mix of memory types.
        """

        ranked_memory = sorted(
            unified_memory,
            key=lambda memory: memory["score"],
            reverse=True,
        )

        selected = []

        counts = {
            "document": 0,
            "conversation": 0,
            "message": 0,
            "preference": 0,
        }

        limits = {
            "document": MAX_DOCUMENTS,
            "conversation": MAX_CONVERSATIONS,
            "message": MAX_MESSAGES,
            "preference": MAX_PREFERENCES,
        }

        for memory in ranked_memory:

            memory_type = memory["memory_type"]

            if memory_type not in counts:
                continue

            if counts[memory_type] >= limits[memory_type]:
                continue

            selected.append(memory)
            counts[memory_type] += 1

            if len(selected) >= MAX_MEMORY_ITEMS:
                break

        return selected