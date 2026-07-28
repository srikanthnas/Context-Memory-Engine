"""
Memory Ranker

Ranks memories using semantic relevance,
recency, importance and memory type.
"""

from datetime import datetime


class MemoryRanker:

    WEIGHTS = {
        "semantic": 0.45,
        "recency": 0.25,
        "importance": 0.20,
        "type": 0.10,
    }

    MEMORY_TYPE_SCORE = {
        "document": 1.00,
        "message": 0.90,
        "conversation": 0.80,
        "preference": 0.70,
    }

    @classmethod
    def calculate_recency_score(
        cls,
        timestamp,
    ):
        """
        More recent memories receive higher scores.
        Older memories gradually decay.
        """

        if timestamp is None:
            return 0.5

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        hours_old = (
            datetime.utcnow() - timestamp
        ).total_seconds() / 3600

        if hours_old < 1:
            return 1.0
        elif hours_old < 24:
            return 0.8
        elif hours_old < 24 * 7:
            return 0.6
        elif hours_old < 24 * 30:
            return 0.4

        return 0.2

    @classmethod
    def calculate_importance_score(
        cls,
        memory,
    ):
        """
        Calculates normalized importance score.

        Importance is stored between 1.0 and 5.0,
        so we normalize it to 0.0–1.0.
        """

        importance = memory.get("importance", 1.0)

        return min(importance / 5.0, 1.0)

    @classmethod
    def rank(
        cls,
        memory_type,
        semantic_score=1.0,
        timestamp=None,
        memory=None,
    ):

        if memory is None:
            memory = {}

        recency = cls.calculate_recency_score(timestamp)

        importance = cls.calculate_importance_score(memory)

        type_score = cls.MEMORY_TYPE_SCORE.get(
            memory_type,
            0.5,
        )

        final = (
            cls.WEIGHTS["semantic"] * semantic_score
            + cls.WEIGHTS["recency"] * recency
            + cls.WEIGHTS["importance"] * importance
            + cls.WEIGHTS["type"] * type_score
        )

        return round(final, 4)