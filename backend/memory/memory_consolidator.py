from memory.memory_lifecycle import MemoryLifecycle


class MemoryConsolidator:
    """
    Consolidates redundant memories before they enter
    active context.

    Phase 29 behavior:
    - Historical memories are never deleted.
    - Exact duplicate memories are consolidated.
    - Stronger memories are preferred.
    - Lifecycle state influences which duplicate survives.
    """

    def __init__(self):
        self.lifecycle = MemoryLifecycle()

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for duplicate comparison.
        """

        if not text:
            return ""

        return " ".join(
            text.lower().strip().split()
        )

    def _get_content(
        self,
        memory: dict,
    ) -> str:
        """
        Extract comparable textual content from
        different memory structures.
        """

        return (
            memory.get("content")
            or memory.get("summary")
            or memory.get("text")
            or ""
        )

    def _prepare_memory(
        self,
        memory: dict,
        now=None,
    ) -> dict:
        """
        Add lifecycle information to a memory.
        """

        return self.lifecycle.classify_with_score(
            memory=memory,
            now=now,
        )

    @staticmethod
    def _choose_stronger(
        first: dict,
        second: dict,
    ) -> dict:
        """
        Choose the stronger duplicate memory.

        If strengths are equal, prefer the memory
        with the higher database ID because it is
        normally the newer record.
        """

        first_strength = first.get(
            "memory_strength",
            0.0,
        )

        second_strength = second.get(
            "memory_strength",
            0.0,
        )

        if second_strength > first_strength:
            return second

        if first_strength > second_strength:
            return first

        first_id = first.get("id", 0) or 0
        second_id = second.get("id", 0) or 0

        if second_id > first_id:
            return second

        return first

    def consolidate(
        self,
        memories: list,
        now=None,
    ) -> list:
        """
        Consolidate exact duplicate memories.

        Only one active-context copy of identical
        information survives.

        The underlying historical memories are
        not modified or deleted.
        """

        if not memories:
            return []

        unique_memories = {}
        order = []

        for memory in memories:

            content = self.normalize(
                self._get_content(memory)
            )

            # Memories without usable text cannot be
            # safely consolidated.
            if not content:

                prepared = self._prepare_memory(
                    memory,
                    now=now,
                )

                unique_key = (
                    "__memory_id__",
                    memory.get("id"),
                )

                unique_memories[
                    unique_key
                ] = prepared

                order.append(
                    unique_key
                )

                continue

            prepared = self._prepare_memory(
                memory,
                now=now,
            )

            if content not in unique_memories:

                unique_memories[
                    content
                ] = prepared

                order.append(
                    content
                )

                continue

            existing = unique_memories[
                content
            ]

            winner = self._choose_stronger(
                first=existing,
                second=prepared,
            )

            unique_memories[
                content
            ] = winner

        return [
            unique_memories[key]
            for key in order
        ]