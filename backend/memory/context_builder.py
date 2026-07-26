class ContextBuilder:
    """
    Builds a single context string from all memory sources.
    """

    @staticmethod
    def build(
        prompt,
        preferences,
        conversations,
        messages,
        documents,
    ):

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
        context.append("Relevant Documents:")

        if documents:
            for document in documents:
                context.append(f"- {document['filename']}:")

                for chunk in document.get("chunks", [])[:2]:
                    context.append(f"  {chunk}")

        else:
            context.append("- None")

        context.append("")
        context.append("Current User Prompt:")
        context.append(prompt["prompt"])

        return "\n".join(context)