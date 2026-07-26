class ContextBuilder:
    """
    Builds a single context string from all memory sources.
    """

    @staticmethod
    def build(
        prompt: dict,
        preferences: list,
        conversations: list,
        messages: list,
    ) -> str:

        context = []

        # User Preferences
        context.append("User Preferences:")

        if preferences:
            for preference in preferences:
                context.append(
                    f"- {preference['key']}: {preference['value']}"
                )
        else:
            context.append("- None")

        context.append("")

        # Previous Conversations
        context.append("Previous Conversations:")
        if conversations:
            for conversation in conversations:
                context.append(f"- {conversation['title']}")
        else:
            context.append("- None")

        context.append("")

        # Recent Messages
        context.append("Recent Messages:")
        if messages:
            for message in messages:
                context.append(
                    f"{message['role'].capitalize()}: {message['content']}"
                )
        else:
            context.append("- None")

        context.append("")
        context.append("Current User Prompt:")
        context.append(prompt["prompt"])

        return "\n".join(context)