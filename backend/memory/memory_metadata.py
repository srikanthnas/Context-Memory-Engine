"""
Memory Metadata

Creates and updates metadata for memory items.
"""

from datetime import datetime


class MemoryMetadata:
    """
    Utility methods for memory metadata.
    """

    @staticmethod
    def create():
        """
        Metadata for a newly created memory.
        """

        now = datetime.utcnow().isoformat()

        return {
            "created_at": now,
            "last_accessed": now,
            "access_count": 0,
            "importance": 1.0,
        }

    @staticmethod
    def touch(memory: dict):
        """
        Update metadata whenever a memory is accessed.
        """

        memory["last_accessed"] = datetime.utcnow().isoformat()

        memory["access_count"] = (
            memory.get("access_count", 0) + 1
        )

        return memory