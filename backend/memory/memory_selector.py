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

    Supported memory types:
    - Documents
    - Conversations
    - Messages
    - Preferences
    - Images
    """

    # Phase 31:
    # Keep image-memory configuration local for now
    # so existing memory_config.py does not need to change.
    MAX_IMAGES = 3

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
        4. Reserved image slot when image memories exist
        5. Global memory limit
        """

        ranked_memory = sorted(
            unified_memory,
            key=lambda memory: memory.get(
                "score",
                0,
            ),
            reverse=True,
        )

        # ---------------------------------------
        # Remove memories below minimum score
        # ---------------------------------------

        ranked_memory = [
            memory
            for memory in ranked_memory
            if memory.get(
                "score",
                0,
            ) >= MIN_MEMORY_SCORE
        ]

        selected = []

        counts = {
            "document": 0,
            "conversation": 0,
            "message": 0,
            "preference": 0,
            "image": 0,
        }

        limits = {
            "document": MAX_DOCUMENTS,
            "conversation": MAX_CONVERSATIONS,
            "message": MAX_MESSAGES,
            "preference": MAX_PREFERENCES,
            "image": cls.MAX_IMAGES,
        }

        # ==================================================
        # STEP 1 — Reserve preference memory
        # ==================================================

        preferences = [
            memory
            for memory in ranked_memory
            if memory.get(
                "memory_type"
            ) == "preference"
        ]

        if (
            preferences
            and MAX_PREFERENCES > 0
            and len(selected) < MAX_MEMORY_ITEMS
        ):

            best_preference = (
                preferences[0]
            )

            selected.append(
                best_preference
            )

            counts["preference"] += 1

        # ==================================================
        # STEP 2 — Reserve image memory
        # ==================================================
        #
        # ImageMemoryManager only returns images for
        # image-related prompts.
        #
        # Therefore, if image memories reach this stage,
        # at least one should survive final selection.
        # ==================================================

        images = [
            memory
            for memory in ranked_memory
            if memory.get(
                "memory_type"
            ) == "image"
        ]

        if (
            images
            and cls.MAX_IMAGES > 0
            and len(selected) < MAX_MEMORY_ITEMS
        ):

            best_image = images[0]

            selected.append(
                best_image
            )

            counts["image"] += 1

        # ==================================================
        # STEP 3 — Fill remaining slots by ranking
        # ==================================================

        for memory in ranked_memory:

            memory_type = memory.get(
                "memory_type"
            )

            if memory_type not in counts:
                continue

            # Already selected through a reserved slot.
            if memory in selected:
                continue

            if (
                counts[memory_type]
                >= limits[memory_type]
            ):
                continue

            if (
                len(selected)
                >= MAX_MEMORY_ITEMS
            ):
                break

            selected.append(
                memory
            )

            counts[memory_type] += 1

        # ==================================================
        # STEP 4 — Final ranking
        # ==================================================

        selected.sort(
            key=lambda memory: memory.get(
                "score",
                0,
            ),
            reverse=True,
        )

        return selected