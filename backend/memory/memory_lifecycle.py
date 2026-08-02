from memory.memory_decay import MemoryDecay


class MemoryLifecycle:
    """
    Classifies memories according to their
    decay-adjusted strength.

    Lifecycle states:

    ACTIVE
        Strong memory that should normally remain
        available for active context.

    AGING
        Memory that has weakened but may still be useful.

    DORMANT
        Weak memory that should normally have low
        priority in active context.

    This component does NOT delete memories.
    """

    ACTIVE = "active"
    AGING = "aging"
    DORMANT = "dormant"

    def __init__(
        self,
        active_threshold: float = 0.75,
        dormant_threshold: float = 0.30,
    ):
        self.memory_decay = MemoryDecay()

        self.active_threshold = (
            active_threshold
        )

        self.dormant_threshold = (
            dormant_threshold
        )

    def classify(
        self,
        memory: dict,
        now=None,
    ) -> str:
        """
        Classify a single memory according to
        its decay-adjusted strength.
        """

        strength = (
            self.memory_decay.score_memory(
                memory,
                now=now,
            )
        )

        if strength >= self.active_threshold:
            return self.ACTIVE

        if strength >= self.dormant_threshold:
            return self.AGING

        return self.DORMANT

    def classify_with_score(
        self,
        memory: dict,
        now=None,
    ) -> dict:
        """
        Return the memory together with its
        calculated strength and lifecycle state.
        """

        strength = (
            self.memory_decay.score_memory(
                memory,
                now=now,
            )
        )

        if strength >= self.active_threshold:
            state = self.ACTIVE

        elif strength >= self.dormant_threshold:
            state = self.AGING

        else:
            state = self.DORMANT

        result = dict(memory)

        result["memory_strength"] = strength
        result["lifecycle_state"] = state

        return result

    def classify_memories(
        self,
        memories: list,
        now=None,
    ) -> list:
        """
        Classify multiple memories.
        """

        return [
            self.classify_with_score(
                memory,
                now=now,
            )
            for memory in memories
        ]