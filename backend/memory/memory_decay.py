from datetime import datetime, timezone
import math


class MemoryDecay:
    """
    Calculates the current strength of a memory.

    Memory strength depends on:
    - Base importance
    - Access frequency
    - Time since last access

    This class does NOT delete or modify memories.
    It only calculates a decay-adjusted score.
    """

    def __init__(
        self,
        decay_rate: float = 0.03,
        access_boost: float = 0.05,
        minimum_strength: float = 0.10,
    ):
        self.decay_rate = decay_rate
        self.access_boost = access_boost
        self.minimum_strength = minimum_strength

    @staticmethod
    def _parse_datetime(value):
        """
        Convert supported timestamp values to datetime.
        """

        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None

        return None

    @staticmethod
    def _make_naive(value):
        """
        Normalize timezone-aware datetimes so they can
        safely be compared with SQLite timestamps.
        """

        if value is None:
            return None

        if value.tzinfo is not None:
            return value.astimezone(
                timezone.utc
            ).replace(
                tzinfo=None
            )

        return value

    def calculate_age_days(
        self,
        last_accessed,
        now=None,
    ) -> float:
        """
        Calculate memory age in days.
        """

        timestamp = self._parse_datetime(
            last_accessed
        )

        if timestamp is None:
            return 0.0

        timestamp = self._make_naive(
            timestamp
        )

        if now is None:
            now = datetime.utcnow()
        else:
            now = self._parse_datetime(now)
            now = self._make_naive(now)

        if now is None:
            now = datetime.utcnow()

        age = now - timestamp

        return max(
            age.total_seconds() / 86400,
            0.0,
        )

    def calculate_strength(
        self,
        importance: float = 1.0,
        access_count: int = 0,
        last_accessed=None,
        now=None,
    ) -> float:
        """
        Calculate decay-adjusted memory strength.

        Formula:

        base_strength =
            importance + access boost

        decay =
            exponential time decay

        final_strength =
            base_strength * decay

        A minimum floor prevents a memory from
        reaching absolute zero.
        """

        importance = max(
            float(importance or 0),
            0.0,
        )

        access_count = max(
            int(access_count or 0),
            0,
        )

        age_days = self.calculate_age_days(
            last_accessed=last_accessed,
            now=now,
        )

        access_bonus = (
            access_count
            * self.access_boost
        )

        base_strength = (
            importance
            + access_bonus
        )

        decay_factor = math.exp(
            -self.decay_rate
            * age_days
        )

        strength = (
            base_strength
            * decay_factor
        )

        return max(
            strength,
            self.minimum_strength,
        )

    def score_memory(
        self,
        memory: dict,
        now=None,
    ) -> float:
        """
        Calculate strength directly from a memory dict.
        """

        return self.calculate_strength(
            importance=memory.get(
                "importance",
                1.0,
            ),
            access_count=memory.get(
                "access_count",
                0,
            ),
            last_accessed=memory.get(
                "last_accessed"
            ),
            now=now,
        )