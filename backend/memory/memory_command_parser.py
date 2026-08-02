import re


class MemoryCommandParser:
    """
    Detects explicit user commands for controlling
    persistent memory.

    Supported Phase 33 commands:

    - remember
    - forget
    """

    REMEMBER_PATTERNS = [
        re.compile(
            r"^\s*remember that my\s+(.+?)\s+is\s+(.+?)"
            r"[.!?]?\s*$",
            re.IGNORECASE,
        ),
        re.compile(
            r"^\s*remember my\s+(.+?)\s+is\s+(.+?)"
            r"[.!?]?\s*$",
            re.IGNORECASE,
        ),
    ]

    FORGET_PATTERNS = [
        re.compile(
            r"^\s*forget my\s+(.+?)"
            r"[.!?]?\s*$",
            re.IGNORECASE,
        ),
        re.compile(
            r"^\s*forget that my\s+(.+?)"
            r"[.!?]?\s*$",
            re.IGNORECASE,
        ),
    ]

    @staticmethod
    def _normalize_key(
        value: str,
    ) -> str:
        """
        Convert a natural-language profile key into
        a consistent storage key.

        Example:

        preferred IDE
            ->
        preferred_ide
        """

        value = value.strip().lower()

        value = re.sub(
            r"[^a-z0-9]+",
            "_",
            value,
        )

        return value.strip("_")

    @staticmethod
    def _clean_value(
        value: str,
    ) -> str:
        """
        Clean a memory value without changing its
        meaningful casing.
        """

        return value.strip().rstrip(
            ".,!?;:"
        ).strip()

    def parse(
        self,
        text: str,
    ):
        """
        Parse an explicit memory-control command.

        Returns None when the message is not a
        memory command.
        """

        if not text:
            return None

        # ==============================================
        # REMEMBER
        # ==============================================

        for pattern in self.REMEMBER_PATTERNS:

            match = pattern.match(text)

            if not match:
                continue

            key = self._normalize_key(
                match.group(1)
            )

            value = self._clean_value(
                match.group(2)
            )

            if not key or not value:
                return None

            return {
                "action": "remember",
                "key": key,
                "value": value,
            }

        # ==============================================
        # FORGET
        # ==============================================

        for pattern in self.FORGET_PATTERNS:

            match = pattern.match(text)

            if not match:
                continue

            key = self._normalize_key(
                match.group(1)
            )

            if not key:
                return None

            return {
                "action": "forget",
                "key": key,
            }

        return None