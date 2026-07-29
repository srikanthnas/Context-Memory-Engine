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

    def _retrieve_memories(
        self,
        db: Session,
        user_id: int,
        prepared_prompt: dict,
    ):
        """
        Retrieve all memories required for response generation.
        """

        conversations = self.conversation_memory.get_recent_conversations(
            db=db,
            user_id=user_id,
        )

        preferences = self.preference_memory.get_preferences(
            db=db,
            user_id=user_id,
        )

        documents = self.document_memory.get_documents(
            db=db,
            user_id=user_id,
            query=prepared_prompt["prompt"],
        )

        recent_messages = []

        if conversations:
            recent_messages = self.message_memory.get_recent_messages(
                db=db,
                conversation_id=conversations[0]["id"],
            )

        semantic_messages = self.message_memory.search_relevant_messages(
            query=prepared_prompt["prompt"],
            user_id=user_id,
        )

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

        return {
            "conversations": conversations,
            "preferences": preferences,
            "documents": documents,
            "messages": latest_messages,
        }

    def _optimize_memory(
        self,
        memory: dict,
    ):
        """
        Optimize retrieved memories before building unified memory.
        """

        return self.context_optimizer.optimize(
            conversations=memory["conversations"],
            messages=memory["messages"],
            preferences=memory["preferences"],
            documents=memory["documents"],
        )
    def _build_unified_memory(
        self,
        optimized_memory: dict,
    ):
        """
        Build a unified memory from the optimized memory sources.
        """

        return self.unified_context_manager.build(
            conversations=optimized_memory["conversations"],
            messages=optimized_memory["messages"],
            preferences=optimized_memory["preferences"],
            documents=optimized_memory["documents"],
        )
    def _select_memory(
        self,
        unified_memory: dict,
    ):
        """
        Rank and select the most relevant memories.
        """

        return self.memory_selector.select(
            unified_memory
        )
    def _build_context(
        self,
        prepared_prompt: dict,
        selected_memory: dict,
    ):
        """
        Build the final prompt context for the LLM.
        """

        return self.context_builder.build(
            prompt=prepared_prompt["prompt"],
            selected_memory=selected_memory,
        )
    def _generate_response(
        self,
        context: str,
    ):
        """
        Generate the final AI response from the constructed context.
        """

        return self.llm_manager.generate(context)

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

        memory = self._retrieve_memories(
            db=db,
            user_id=user_id,
            prepared_prompt=prepared_prompt,
        )

        optimized_memory = self._optimize_memory(
            memory=memory,
        )

        unified_memory = self._build_unified_memory(
            optimized_memory=optimized_memory,
        )

        selected_memory = self._select_memory(
            unified_memory=unified_memory,
        )

        context = self._build_context(
            prepared_prompt=prepared_prompt,
            selected_memory=selected_memory,
        )

        ai_response = self._generate_response(
            context=context,
        )

        return {
            "prompt": prepared_prompt,
            "conversation_memory": memory["conversations"],
            "message_memory": memory["messages"],
            "preference_memory": memory["preferences"],
            "document_memory": memory["documents"],
            "optimized_memory": optimized_memory,
            "unified_memory": unified_memory,
            "selected_memory": selected_memory,
            "context": context,
            "ai_response": ai_response,
        }