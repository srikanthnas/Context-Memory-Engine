class MemoryConflictDetector:
    """
    Detects potential conflicts between memory items.

    This component does NOT delete or modify memories.

    It identifies memories that may refer to the same
    subject while containing different information.
    """

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for lightweight comparison.
        """

        if not text:
            return ""

        return " ".join(
            text.lower().strip().split()
        )

    def detect_message_conflicts(
        self,
        messages: list,
    ):
        """
        Detect possible conflicts between messages.

        For Phase 27 we use a conservative rule:
        messages must share important subject terms
        before being considered possible conflicts.

        Actual semantic contradiction handling can
        later be extended with embeddings or an LLM.
        """

        conflicts = []

        for index, first in enumerate(messages):

            first_content = self.normalize(
                first.get("content", "")
            )

            if not first_content:
                continue

            first_words = set(
                first_content.split()
            )

            for second in messages[index + 1:]:

                second_content = self.normalize(
                    second.get("content", "")
                )

                if not second_content:
                    continue

                # Identical memories are duplicates,
                # not conflicts.
                if first_content == second_content:
                    continue

                second_words = set(
                    second_content.split()
                )

                shared_words = (
                    first_words
                    & second_words
                )

                # Conservative threshold to avoid
                # treating unrelated messages as conflicts.
                if len(shared_words) < 2:
                    continue

                conflicts.append(
                    {
                        "first": first,
                        "second": second,
                        "shared_terms": sorted(
                            shared_words
                        ),
                    }
                )

        return conflicts

    def detect(
        self,
        memory: dict,
    ):
        """
        Detect potential conflicts across memory sources.
        """

        return {
            "message_conflicts":
                self.detect_message_conflicts(
                    memory.get(
                        "messages",
                        []
                    )
                )
        }