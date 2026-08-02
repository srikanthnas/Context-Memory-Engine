import re


class UserProfileExtractor:
    """
    Extracts stable user-profile information from
    user messages.

    Phase 32 uses conservative deterministic rules.

    Only explicit first-person statements are stored.
    """

    PATTERNS = [
        # --------------------------------------------------
        # Name
        # --------------------------------------------------
        (
            "name",
            re.compile(
                r"\bmy name is\s+([a-zA-Z][a-zA-Z ]{1,50})",
                re.IGNORECASE,
            ),
        ),

        # --------------------------------------------------
        # Location
        # --------------------------------------------------
        (
            "location",
            re.compile(
                r"\bi live in\s+([a-zA-Z][a-zA-Z ,]{1,80})",
                re.IGNORECASE,
            ),
        ),

        # --------------------------------------------------
        # Occupation / role
        # --------------------------------------------------
        (
            "occupation",
            re.compile(
                r"\bi am an?\s+([a-zA-Z][a-zA-Z ]{1,80})",
                re.IGNORECASE,
            ),
        ),

        # --------------------------------------------------
        # Preferred programming language
        # --------------------------------------------------
        (
            "preferred_programming_language",
            re.compile(
                r"\bi prefer\s+([a-zA-Z0-9+#.]+)"
                r"\s+(?:for\s+)?programming",
                re.IGNORECASE,
            ),
        ),

        # --------------------------------------------------
        # General preference
        # Example:
        # I prefer concise responses
        # --------------------------------------------------
        (
            "preference",
            re.compile(
                r"\bi prefer\s+(.{2,100})",
                re.IGNORECASE,
            ),
        ),
    ]

    @staticmethod
    def _clean_value(
        value: str,
    ) -> str:
        """
        Normalize extracted profile values.
        """

        value = value.strip()

        value = value.rstrip(
            ".,!?;:"
        )

        return value.strip()

    def extract(
        self,
        text: str,
    ):
        """
        Extract stable user-profile facts.

        Returns:

        [
            {
                "key": "...",
                "value": "..."
            }
        ]
        """

        if not text:
            return []

        extracted = []

        used_keys = set()

        for key, pattern in self.PATTERNS:

            match = pattern.search(
                text
            )

            if not match:
                continue

            value = self._clean_value(
                match.group(1)
            )

            if not value:
                continue

            # Avoid storing the same key twice
            # from a single message.

            if key in used_keys:
                continue

            extracted.append(
                {
                    "key": key,
                    "value": value,
                }
            )

            used_keys.add(
                key
            )

        return extracted