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
    MIN_MEMORY_SCORE,
)


class MemorySelector:
    """
    Selects the best memories after ranking while maintaining
    a balanced mix of memory types.
    """

    @classmethod
    def select(
        cls,
        unified_memory,
    ):
        """
        Select memories using:

        1. Minimum relevance threshold
        2. Per-memory-type limits
        3. Reserved preference slot when preferences exist
        4. Global memory limit
        """

        ranked_memory = sorted(
            unified_memory,
            key=lambda memory: memory["score"],
            reverse=True,
        )

        # ---------------------------------------
        # Remove memories below minimum score
        # ---------------------------------------

        ranked_memory = [
            memory
            for memory in ranked_memory
            if memory.get("score", 0) >= MIN_MEMORY_SCORE
        ]

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

        # ==================================================
        # STEP 1 — Reserve preference memory
        # ==================================================

        preferences = [
            memory
            for memory in ranked_memory
            if memory.get("memory_type") == "preference"
        ]

        if preferences and MAX_PREFERENCES > 0:

            best_preference = preferences[0]

            selected.append(best_preference)

            counts["preference"] += 1

        # ==================================================
        # STEP 2 — Fill remaining slots by ranking
        # ==================================================

        for memory in ranked_memory:

            memory_type = memory.get("memory_type")

            if memory_type not in counts:
                continue

            # Preference already selected above
            if (
                memory_type == "preference"
                and memory in selected
            ):
                continue

            if counts[memory_type] >= limits[memory_type]:
                continue

            if len(selected) >= MAX_MEMORY_ITEMS:
                break

            selected.append(memory)

            counts[memory_type] += 1

        # ==================================================
        # STEP 3 — Final ranking
        # ==================================================

        selected.sort(
            key=lambda memory: memory["score"],
            reverse=True,
        )

        return selected