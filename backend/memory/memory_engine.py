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
from memory.memory_selector import MemorySelector
from llm.llm_manager import LLMManager


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
        self.llm_manager = LLMManager()
        self.memory_selector = MemorySelector()

    def _prepare_prompt(
        self,
        user_id: int,
        prompt: str,
    ):
        """
        Prepare and normalize the incoming prompt.
        """

        print("RAW prompt:", repr(prompt))

        prepared_prompt = self.prompt_manager.prepare_prompt(
            user_id=user_id,
            prompt=prompt,
        )

        print("prepared_prompt:", prepared_prompt)

        return prepared_prompt

    def process_prompt(
        self,
        db: Session,
        user_id: int,
        prompt: str,
    ):
        prepared_prompt = self._prepare_prompt(
            user_id=user_id,
            prompt=prompt,
        )

        # ---------------------------------------------------
        # Retrieve conversation memory
        # ---------------------------------------------------

        conversations = self.conversation_memory.get_recent_conversations(
            db=db,
            user_id=user_id,
        )

        # ---------------------------------------------------
        # Retrieve user preferences
        # ---------------------------------------------------

        preferences = self.preference_memory.get_preferences(
            db=db,
            user_id=user_id,
        )

        # ---------------------------------------------------
        # Retrieve relevant documents
        # ---------------------------------------------------

        documents = self.document_memory.get_documents(
            db=db,
            user_id=user_id,
            query=prepared_prompt["prompt"],
        )

        # ---------------------------------------------------
        # Retrieve recent conversation messages
        # ---------------------------------------------------

        recent_messages = []

        if conversations:
            recent_messages = self.message_memory.get_recent_messages(
                db=db,
                conversation_id=conversations[0]["id"],
            )

        # ---------------------------------------------------
        # Retrieve semantic message memories
        # ---------------------------------------------------

        semantic_messages = self.message_memory.search_relevant_messages(
            query=prepared_prompt["prompt"],
            user_id=user_id,
        )

        # ---------------------------------------------------
        # Merge both message sources
        # ---------------------------------------------------

        message_map = {}

        for message in recent_messages:
            key = (
                message.get("id")
                if message.get("id") is not None
                else (
                    message.get("role"),
                    message.get("content"),
                )
            )
            message_map[key] = message

        for message in semantic_messages:
            key = (
                message.get("id")
                if message.get("id") is not None
                else (
                    message.get("role"),
                    message.get("content"),
                )
            )
            message_map[key] = message

        latest_messages = list(message_map.values())

        # ---------------------------------------------------
        # Optimize memory
        # ---------------------------------------------------

        optimized_memory = self.context_optimizer.optimize(
            conversations=conversations,
            messages=latest_messages,
            preferences=preferences,
            documents=documents,
        )

        # ---------------------------------------------------
        # Build unified memory
        # ---------------------------------------------------

        unified_memory = self.unified_context_manager.build(
            conversations=optimized_memory["conversations"],
            messages=optimized_memory["messages"],
            preferences=optimized_memory["preferences"],
            documents=optimized_memory["documents"],
        )

        # ---------------------------------------------------
        # Rank and select memories
        # ---------------------------------------------------

        selected_memory = self.memory_selector.select(
            unified_memory
        )

        # ---------------------------------------------------
        # Build context
        # ---------------------------------------------------

        context = self.context_builder.build(
            prompt=prepared_prompt["prompt"],
            selected_memory=selected_memory,
        )

        # ---------------------------------------------------
        # Generate response
        # ---------------------------------------------------

        ai_response = self.llm_manager.generate(context)

        return {
            "prompt": prepared_prompt,
            "conversation_memory": conversations,
            "message_memory": latest_messages,
            "preference_memory": preferences,
            "document_memory": documents,
            "optimized_memory": optimized_memory,
            "unified_memory": unified_memory,
            "selected_memory": selected_memory,
            "context": context,
            "ai_response": ai_response,
        }