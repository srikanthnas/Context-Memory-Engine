"""
Context Builder

Builds the final context that is sent to the LLM.
"""


class ContextBuilder:
    """
    Builds a single context string from all memory sources.
    """

    def build(
        self,
        prompt: str,
        preferences,
        conversations,
        messages,
        documents,
    ):
        context = []

        # =====================================================
        # User Preferences
        # =====================================================

        context.append("User Preferences:")

        if preferences:
            for preference in preferences:
                context.append(
                    f"- {preference['key']}: {preference['value']}"
                )
        else:
            context.append("- None")

        context.append("")

        # =====================================================
        # Previous Conversations
        # =====================================================

        context.append("Previous Conversations:")

        if conversations:
            for conversation in conversations:
                context.append(
                    f"- {conversation['title']}"
                )
        else:
            context.append("- None")

        context.append("")

        # =====================================================
        # Recent Messages
        # =====================================================

        context.append("Recent Messages:")

        if messages:
            for message in messages:
                context.append(
                    f"{message['role'].capitalize()}: {message['content']}"
                )
        else:
            context.append("- None")

        context.append("")

        # =====================================================
        # Relevant Document Chunks
        # =====================================================

        context.append("Relevant Documents:")

        if documents:
            for document in documents:
                context.append(f"- {document['filename']}")

                chunk = document.get("chunk")

                if chunk:
                    context.append(chunk)
                    context.append("")
                else:
                    context.append("(No text retrieved)")
                    context.append("")
        else:
            context.append("- None")

        # =====================================================
        # Current Prompt
        # =====================================================

        print("DEBUG PROMPT:", repr(prompt))
        context.append("Current User Prompt:")
        context.append(prompt)

        return "\n".join(context)