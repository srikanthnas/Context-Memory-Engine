class ContextOptimizer:
    """
    Optimizes memory before sending it to an LLM.
    """

    @staticmethod
    def optimize(
        conversations: list,
        messages: list,
        max_conversations: int = 3,
        max_messages: int = 5,
    ):
        optimized_conversations = conversations[:max_conversations]

        optimized_messages = messages[-max_messages:]

        return {
            "conversations": optimized_conversations,
            "messages": optimized_messages,
        }