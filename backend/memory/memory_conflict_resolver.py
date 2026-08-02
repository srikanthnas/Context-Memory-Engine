from datetime import datetime


class MemoryConflictResolver:
    """
    Resolves conflicts between retrieved memories.

    Current responsibilities:
    1. Detect duplicate preference keys.
    2. Prefer the most recently updated/accessed value.
    3. Preserve unrelated memories.
    """

    @staticmethod
    def _parse_datetime(value):
        """
        Convert ISO datetime strings into datetime objects.

        Invalid or missing timestamps are treated as the
        oldest possible timestamp.
        """

        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass

        return datetime.min

    def resolve_preferences(
        self,
        preferences: list,
    ):
        """
        Resolve conflicting preferences.

        When multiple memories contain the same preference
        key, keep the newest one.
        """

        resolved = {}

        for preference in preferences:

            key = preference.get("key")

            if not key:
                continue

            existing = resolved.get(key)

            if existing is None:
                resolved[key] = preference
                continue

            current_time = self._parse_datetime(
                preference.get("last_accessed")
            )

            existing_time = self._parse_datetime(
                existing.get("last_accessed")
            )

            if current_time > existing_time:
                resolved[key] = preference

        return list(resolved.values())

    def resolve(
        self,
        memory: dict,
    ):
        """
        Resolve conflicts across retrieved memory.

        Additional conflict-resolution strategies can
        be added here in later steps.
        """

        resolved_memory = {
            "conversations": memory.get(
                "conversations",
                [],
            ),
            "messages": memory.get(
                "messages",
                [],
            ),
            "documents": memory.get(
                "documents",
                [],
            ),
            "preferences": self.resolve_preferences(
                memory.get(
                    "preferences",
                    [],
                )
            ),
        }

        return resolved_memory