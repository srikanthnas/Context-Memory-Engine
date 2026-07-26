class ContextOptimizer:
    """
    Optimizes memory before context construction.
    """

    @staticmethod
    def optimize(
        conversations: list,
        messages: list,
        preferences: list,
    ):
        optimized_conversations = conversations[:3]
        optimized_messages = messages[-5:]
        optimized_preferences = preferences

        return {
            "conversations": optimized_conversations,
            "messages": optimized_messages,
            "preferences": optimized_preferences,
        }