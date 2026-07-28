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
        Placeholder implementation.

        Returns 1.0 for now.
        We'll replace this with
        time-decay scoring later.
        """

        return 1.0

    @classmethod
    def calculate_importance_score(
        cls,
        memory,
    ):
        """
        Placeholder implementation.

        Future versions can use:
        - bookmarks
        - user pins
        - access frequency
        """

        return memory.get("importance", 1.0)

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