from datetime import datetime


class FactualConflictResolver:
    """
    Resolves confirmed factual conflicts between messages.

    Important:
    - Historical messages are never deleted.
    - Resolution only affects active context.
    - Newer memories are preferred over older memories.
    - Conflict chains are resolved as a group.
    """

    @staticmethod
    def _parse_datetime(value):
        """
        Convert timestamps into datetime objects.
        """

        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass

        return datetime.min

    def _get_timestamp(
        self,
        message: dict,
    ):
        """
        Extract a usable timestamp from a message.
        """

        return self._parse_datetime(
            message.get("timestamp")
            or message.get("created_at")
            or message.get("last_accessed")
        )

    def choose_newer(
        self,
        first: dict,
        second: dict,
    ):
        """
        Choose the newer memory.

        If timestamps are equal or unavailable,
        prefer the message with the larger database ID.
        """

        first_time = self._get_timestamp(first)
        second_time = self._get_timestamp(second)

        if second_time > first_time:
            return second

        if first_time > second_time:
            return first

        first_id = first.get("id", 0) or 0
        second_id = second.get("id", 0) or 0

        if second_id > first_id:
            return second

        return first

    def _find(
        self,
        parent: dict,
        node,
    ):
        """
        Find the root of a conflict group.
        """

        if parent[node] != node:
            parent[node] = self._find(
                parent,
                parent[node],
            )

        return parent[node]

    def _union(
        self,
        parent: dict,
        first_id,
        second_id,
    ):
        """
        Join two memories into the same
        factual-conflict group.
        """

        first_root = self._find(
            parent,
            first_id,
        )

        second_root = self._find(
            parent,
            second_id,
        )

        if first_root != second_root:
            parent[second_root] = first_root

    def resolve(
        self,
        messages: list,
        confirmed_conflicts: list,
    ):
        """
        Remove superseded memories from active context.

        Confirmed conflicts may contain simple pairs or
        chains of related conflicting facts.

        Example:

        Flask <-> Django
        Django <-> FastAPI

        These form one conflict group:

        Flask -> Django -> FastAPI

        Only the newest memory in that group survives.
        """

        if not confirmed_conflicts:
            return list(messages)

        # =================================================
        # MAP ACTIVE MESSAGES BY ID
        # =================================================

        message_map = {
            message.get("id"): message
            for message in messages
            if message.get("id") is not None
        }

        # =================================================
        # BUILD CONFLICT GRAPH
        # =================================================

        parent = {}

        for conflict in confirmed_conflicts:

            first = conflict.get("first")
            second = conflict.get("second")

            if not first or not second:
                continue

            first_id = first.get("id")
            second_id = second.get("id")

            if (
                first_id is None
                or second_id is None
            ):
                continue

            # Only resolve memories that are actually
            # present in the active message collection.

            if (
                first_id not in message_map
                or second_id not in message_map
            ):
                continue

            if first_id not in parent:
                parent[first_id] = first_id

            if second_id not in parent:
                parent[second_id] = second_id

            self._union(
                parent=parent,
                first_id=first_id,
                second_id=second_id,
            )

        # No usable conflicts
        if not parent:
            return list(messages)

        # =================================================
        # CREATE CONNECTED CONFLICT GROUPS
        # =================================================

        groups = {}

        for message_id in parent:

            root = self._find(
                parent,
                message_id,
            )

            groups.setdefault(
                root,
                [],
            ).append(
                message_id
            )

        # =================================================
        # SELECT NEWEST MEMORY IN EACH GROUP
        # =================================================

        superseded_ids = set()

        for group_ids in groups.values():

            if len(group_ids) < 2:
                continue

            winner = message_map[
                group_ids[0]
            ]

            for message_id in group_ids[1:]:

                candidate = message_map[
                    message_id
                ]

                winner = self.choose_newer(
                    first=winner,
                    second=candidate,
                )

            winner_id = winner.get("id")

            # Every member except the newest winner
            # becomes superseded in active context.

            for message_id in group_ids:

                if message_id != winner_id:
                    superseded_ids.add(
                        message_id
                    )

        # =================================================
        # BUILD RESOLVED ACTIVE MEMORY
        # =================================================

        resolved_messages = []

        for message in messages:

            message_id = message.get("id")

            if message_id in superseded_ids:
                continue

            resolved_messages.append(
                message
            )

        return resolved_messages