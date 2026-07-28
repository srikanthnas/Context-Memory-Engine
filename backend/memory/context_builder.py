"""
Context Builder

Builds the final LLM prompt from selected memories.
"""


class ContextBuilder:
    """
    Builds the final prompt sent to the LLM.
    """

    def build(
        self,
        prompt: str,
        selected_memory,
    ):

        context = []

        context.append(
            "You have access to the following memories.\n"
        )

        # ---------------------------------------
        # Ranked memories
        # ---------------------------------------

        for memory in selected_memory:

            memory_type = memory["memory_type"]

            if memory_type == "preference":

                context.append(
                    f"[Preference | Score={memory['score']}]"
                )

                context.append(
                    f"{memory['key']} = {memory['value']}"
                )

            elif memory_type == "conversation":

                context.append(
                    f"[Conversation | Score={memory['score']}]"
                )

                context.append(
                    memory["title"]
                )

            elif memory_type == "message":

                context.append(
                    f"[Message | Score={memory['score']}]"
                )

                context.append(
                    f"{memory['role']}: {memory['content']}"
                )

            elif memory_type == "document":

                context.append(
                    f"[Document | Score={memory['score']}]"
                )

                context.append(
                    f"File: {memory['filename']}"
                )

                context.append(
                    memory["chunk"]
                )

            context.append("")

        # ---------------------------------------
        # User Prompt
        # ---------------------------------------

        context.append(
            "Current User Question:"
        )

        context.append(prompt)

        return "\n".join(context)