class MemoryConflictConfirmer:
    """
    Confirms whether candidate message conflicts are
    strong enough to be resolved.

    The detector finds POSSIBLE conflicts.

    This confirmer uses conservative rules so that
    related messages are not automatically treated
    as contradictions.
    """

    UPDATE_MARKERS = {
        "now",
        "instead",
        "changed",
        "updated",
        "currently",
        "replaced",
    }

    UPDATE_PHRASES = {
        "no longer",
        "used to",
        "changed to",
        "switched to",
        "moved to",
    }

    IGNORE_WORDS = {
        "my",
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "uses",
        "use",
        "using",
        "now",
        "currently",
        "changed",
        "updated",
        "instead",
        "to",
        "from",
        "project",
        "backend",
        "database",
    }

    # =====================================================
    # FACTUAL SUBJECTS
    # =====================================================
    #
    # Two messages should only replace each other when
    # they refer to the same factual slot.
    #
    # Example:
    #
    # backend = Flask
    # backend = FastAPI
    #
    # These conflict.
    #
    # backend = FastAPI
    # database = PostgreSQL
    #
    # These do NOT conflict.
    # =====================================================

    SUBJECT_TERMS = {
        "backend",
        "database",
        "frontend",
        "framework",
        "language",
        "hosting",
        "deployment",
        "cloud",
        "library",
    }

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for comparison.
        """

        if not text:
            return ""

        return " ".join(
            text.lower().strip().split()
        )

    @staticmethod
    def tokenize(text: str):
        """
        Create simple normalized tokens.
        """

        cleaned = (
            text.replace(".", " ")
            .replace(",", " ")
            .replace(":", " ")
            .replace(";", " ")
            .replace("!", " ")
            .replace("?", " ")
        )

        return {
            word
            for word in cleaned.split()
            if word
        }

    def contains_update_marker(
        self,
        text: str,
    ) -> bool:
        """
        Check whether text explicitly indicates
        that previous information changed.
        """

        normalized = self.normalize(text)

        words = self.tokenize(normalized)

        if words & self.UPDATE_MARKERS:
            return True

        for phrase in self.UPDATE_PHRASES:
            if phrase in normalized:
                return True

        return False

    def extract_fact_terms(
        self,
        text: str,
    ):
        """
        Extract possible factual-value terms.

        Example:

        My project backend uses Flask.
            -> {'flask'}

        My project backend now uses FastAPI.
            -> {'fastapi'}
        """

        words = self.tokenize(
            self.normalize(text)
        )

        return {
            word
            for word in words
            if word not in self.IGNORE_WORDS
        }

    def extract_subject_terms(
        self,
        text: str,
    ):
        """
        Extract the factual subject or slot.

        Example:

        My project backend uses Flask.
            -> {'backend'}

        My project database uses PostgreSQL.
            -> {'database'}
        """

        words = self.tokenize(
            self.normalize(text)
        )

        return (
            words
            & self.SUBJECT_TERMS
        )

    def confirm_candidate(
        self,
        candidate: dict,
    ) -> bool:
        """
        Confirm a candidate factual update.

        Conservative rules:

        1. Messages must be different.
        2. They must share enough terms.
        3. At least one must contain an update marker.
        4. Both must describe the same factual subject.
        5. Both must contain factual values.
        6. Both must use the same relationship type.
        7. Their factual values must differ.
        """

        first = candidate.get("first")
        second = candidate.get("second")

        if not first or not second:
            return False

        first_content = self.normalize(
            first.get("content", "")
        )

        second_content = self.normalize(
            second.get("content", "")
        )

        if not first_content or not second_content:
            return False

        if first_content == second_content:
            return False

        shared_terms = candidate.get(
            "shared_terms",
            [],
        )

        if len(shared_terms) < 2:
            return False

        # =================================================
        # REQUIRE EXPLICIT UPDATE
        # =================================================

        first_has_update = (
            self.contains_update_marker(
                first_content
            )
        )

        second_has_update = (
            self.contains_update_marker(
                second_content
            )
        )

        if not (
            first_has_update
            or second_has_update
        ):
            return False

        # =================================================
        # REQUIRE SAME FACTUAL SUBJECT
        # =================================================

        first_subjects = (
            self.extract_subject_terms(
                first_content
            )
        )

        second_subjects = (
            self.extract_subject_terms(
                second_content
            )
        )

        # If we cannot identify a subject safely,
        # do not resolve the candidate automatically.

        if not first_subjects:
            return False

        if not second_subjects:
            return False

        # Backend vs database must NOT conflict.

        if not (
            first_subjects
            & second_subjects
        ):
            return False

        # =================================================
        # EXTRACT FACTUAL VALUES
        # =================================================

        first_facts = self.extract_fact_terms(
            first_content
        )

        second_facts = self.extract_fact_terms(
            second_content
        )

        if not first_facts:
            return False

        if not second_facts:
            return False

        # =================================================
        # REQUIRE SAME RELATIONSHIP TYPE
        # =================================================

        usage_terms = {
            "uses",
            "use",
            "using",
        }

        first_words = self.tokenize(
            first_content
        )

        second_words = self.tokenize(
            second_content
        )

        first_is_usage_fact = bool(
            first_words & usage_terms
        )

        second_is_usage_fact = bool(
            second_words & usage_terms
        )

        if (
            first_is_usage_fact
            != second_is_usage_fact
        ):
            return False

        # =================================================
        # FACTUAL VALUES MUST DIFFER
        # =================================================

        if first_facts == second_facts:
            return False

        return True

    def confirm(
        self,
        candidates: list,
    ):
        """
        Return only safely confirmed conflicts.
        """

        confirmed = []

        for candidate in candidates:

            if self.confirm_candidate(
                candidate
            ):
                confirmed.append(
                    candidate
                )

        return confirmed