class ContextOptimizer:
    """
    Optimizes memory before context construction.
    """

    @staticmethod
    def optimize(
        conversations: list,
        messages: list,
        preferences: list,
        documents: list,
    ):
        optimized_conversations = conversations[:3]
        optimized_messages = messages[-5:]
        optimized_preferences = preferences

        # For now, keep all documents.
        # Later this will retrieve only relevant chunks.
        optimized_documents = documents

        return {
            "conversations": optimized_conversations,
            "messages": optimized_messages,
            "preferences": optimized_preferences,
            "documents": optimized_documents,
        }