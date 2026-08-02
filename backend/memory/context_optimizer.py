from memory.memory_decay import MemoryDecay


class ContextOptimizer:
    """
    Optimizes memory before context construction.

    Message memories are ranked using:
    - Retrieval relevance
    - Decay-adjusted memory strength

    Image memories are preserved when image retrieval
    determines that they are relevant to the query.
    """

    def __init__(self):
        self.memory_decay = MemoryDecay()

    def _score_message(
        self,
        message: dict,
    ) -> float:
        """
        Calculate a final ranking score for a message.
        """

        similarity = message.get(
            "similarity",
            1.0,
        )

        try:
            similarity = float(similarity)
        except (TypeError, ValueError):
            similarity = 1.0

        decay_strength = (
            self.memory_decay.score_memory(
                message
            )
        )

        final_score = (
            0.70 * similarity
            + 0.30 * decay_strength
        )

        return final_score

    def _optimize_messages(
        self,
        messages: list,
        limit: int = 5,
    ):
        """
        Rank messages using relevance + memory decay.
        """

        if not messages:
            return []

        scored_messages = []

        for index, message in enumerate(messages):

            score = self._score_message(
                message
            )

            enriched_message = dict(
                message
            )

            enriched_message[
                "memory_strength"
            ] = self.memory_decay.score_memory(
                message
            )

            enriched_message[
                "ranking_score"
            ] = score

            scored_messages.append(
                (
                    index,
                    enriched_message,
                )
            )

        ranked = sorted(
            scored_messages,
            key=lambda item: item[1][
                "ranking_score"
            ],
            reverse=True,
        )

        selected = ranked[:limit]

        selected = sorted(
            selected,
            key=lambda item: item[0],
        )

        return [
            message
            for _, message in selected
        ]

    def optimize(
        self,
        conversations: list,
        messages: list,
        preferences: list,
        documents: list,
        images: list = None,
    ):
        """
        Optimize retrieved memory before unified
        context construction.
        """

        optimized_conversations = (
            conversations[:3]
        )

        optimized_messages = (
            self._optimize_messages(
                messages=messages,
                limit=5,
            )
        )

        optimized_preferences = (
            preferences
        )

        optimized_documents = (
            documents
        )

        # ImageMemoryManager already limits image
        # retrieval. Keep the most recent five here.
        optimized_images = (
            (images or [])[:5]
        )

        return {
            "conversations":
                optimized_conversations,

            "messages":
                optimized_messages,

            "preferences":
                optimized_preferences,

            "documents":
                optimized_documents,

            "images":
                optimized_images,
        }