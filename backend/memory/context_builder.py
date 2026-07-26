class ContextBuilder:
    """
    Builds a single context string from all memory sources.
    """

    @staticmethod
    def build(prompt: dict, conversations: list, messages: list) -> str:
        context = []

        if conversations:
            context.append("Previous Conversations:")
            for conversation in conversations:
                context.append(f"- {conversation['title']}")

        if messages:
            context.append("")
            context.append("Recent Messages:")
            for message in messages:
                context.append(
                    f"{message['role'].capitalize()}: {message['content']}"
                )

        context.append("")
        context.append("Current User Prompt:")
        context.append(prompt["prompt"])

        return "\n".join(context)