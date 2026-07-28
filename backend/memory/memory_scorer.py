"""
Memory Scorer

Calculates relevance scores for different memory types.
"""


class MemoryScorer:
    """
    Scores memories based on type.
    """

    BASE_SCORES = {
        "document": 0.90,
        "message": 0.80,
        "conversation": 0.70,
        "preference": 0.60,
    }

    @classmethod
    def score(cls, memory_type):
        """
        Return the base score for a memory type.
        """

        return cls.BASE_SCORES.get(memory_type, 0.50)