"""
Memory Engine

Coordinates all memory components.
"""

from sqlalchemy.orm import Session

from memory.prompt_manager import PromptManager
from memory.conversation_memory import ConversationMemory
from memory.message_memory import MessageMemory
from memory.preference_memory import PreferenceMemory
from memory.context_builder import ContextBuilder
from memory.context_optimizer import ContextOptimizer
from memory.document_memory import DocumentMemory
from memory.unified_context_manager import UnifiedContextManager


class MemoryEngine:
    """Main orchestrator for the Context Memory Engine."""

    def __init__(self):
        self.prompt_manager = PromptManager()
        self.conversation_memory = ConversationMemory()
        self.message_memory = MessageMemory()
        self.preference_memory = PreferenceMemory()
        self.context_builder = ContextBuilder()
        self.context_optimizer = ContextOptimizer()
        self.document_memory = DocumentMemory()
        self.unified_context_manager = UnifiedContextManager()

    def process_prompt(
        self,
        db: Session,
        user_id: int,
        prompt: str,
    ):
        # Prepare prompt
        prepared_prompt = self.prompt_manager.prepare_prompt(
            user_id=user_id,
            prompt=prompt,
        )

        # Retrieve recent conversations
        conversations = self.conversation_memory.get_recent_conversations(
            db=db,
            user_id=user_id,
        )

        # Retrieve user preferences
        preferences = self.preference_memory.get_preferences(
            db=db,
            user_id=user_id,
        )
        documents = self.document_memory.get_documents(
            db=db,
            user_id=user_id,
            query=prepared_prompt,
        )

        # Retrieve latest messages from the newest conversation
        latest_messages = []

        if conversations:
            latest_messages = self.message_memory.get_recent_messages(
                db=db,
                conversation_id=conversations[0]["id"],
            )

        # Optimize retrieved memory
        optimized_memory = self.context_optimizer.optimize(
            conversations=conversations,
            messages=latest_messages,
            preferences=preferences,
            documents=documents,
        )
        unified_memory = self.unified_context_manager.build(
        conversations=optimized_memory["conversations"],
        messages=optimized_memory["messages"],
        preferences=optimized_memory["preferences"],
        documents=optimized_memory["documents"],
    )

        # Build final LLM context
        context = self.context_builder.build(
            prompt=prepared_prompt,
            preferences=optimized_memory["preferences"],
            conversations=optimized_memory["conversations"],
            messages=optimized_memory["messages"],
            documents=optimized_memory["documents"],
        )

        return {
            "prompt": prepared_prompt,
            "conversation_memory": conversations,
            "message_memory": latest_messages,
            "preference_memory": preferences,
            "document_memory": documents,
            "optimized_memory": optimized_memory,
            "unified_memory": unified_memory,
            "context": context,
        }