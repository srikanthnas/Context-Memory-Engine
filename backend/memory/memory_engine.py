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
from memory.memory_usage_tracker import MemoryUsageTracker
from memory.memory_conflict_resolver import MemoryConflictResolver
from memory.memory_conflict_detector import MemoryConflictDetector
from memory.memory_conflict_confirmer import MemoryConflictConfirmer
from memory.factual_conflict_resolver import FactualConflictResolver


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
        self.memory_selector = MemorySelector()
        self.llm_manager = LLMManager()
        self.memory_usage_tracker = MemoryUsageTracker()
        self.memory_conflict_resolver = MemoryConflictResolver()
        self.memory_conflict_detector = MemoryConflictDetector()
        self.memory_conflict_confirmer = MemoryConflictConfirmer()
        self.factual_conflict_resolver = FactualConflictResolver()

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

        semantic_conversations = (
            self.conversation_memory.get_recent_conversations(
                db=db,
                user_id=user_id,
                prompt=prepared_prompt["prompt"],
            )
        )

        recent_conversations = (
            self.conversation_memory.get_latest_conversations(
                db=db,
                user_id=user_id,
            )
        )

        conversations = self._deduplicate_conversations(
            recent_conversations=recent_conversations,
            semantic_conversations=semantic_conversations,
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

        latest_messages = self._deduplicate_messages(
            recent_messages=recent_messages,
            semantic_messages=semantic_messages,
        )

        return {
            "conversations": conversations,
            "preferences": preferences,
            "documents": documents,
            "messages": latest_messages,
        }

    def _deduplicate_messages(
        self,
        recent_messages: list,
        semantic_messages: list,
    ):
        """
        Merge and remove duplicate messages.

        Messages are deduplicated using:
        (role, normalized content)
        """

        message_map = {}

        for message in recent_messages + semantic_messages:

            key = (
                message.get("role"),
                message.get("content", "").strip().lower(),
            )

            if key not in message_map:
                message_map[key] = message

        return list(message_map.values())
    
    def _deduplicate_conversations(
        self,
        recent_conversations: list,
        semantic_conversations: list,
    ):
        """
        Merge and remove duplicate conversations.

        Conversations are deduplicated using:
        conversation id
        """

        conversation_map = {}

        for conversation in (
            semantic_conversations + recent_conversations
        ):
            key = conversation.get("id")

            if key not in conversation_map:
                conversation_map[key] = conversation

        return list(conversation_map.values())

    def _resolve_memory_conflicts(
        self,
        memory: dict,
    ):
        """
        Resolve conflicts before memory optimization.

        Handles:
        1. Preference conflicts.
        2. Candidate factual conflict detection.
        3. Conservative conflict confirmation.
        4. Recency-aware factual resolution.

        Historical memories remain unchanged in storage.
        Only the active context is modified.
        """

        # ---------------------------------------------
        # Resolve structured preference conflicts
        # ---------------------------------------------

        resolved_memory = (
            self.memory_conflict_resolver.resolve(
                memory
            )
        )

        # ---------------------------------------------
        # Detect possible factual conflicts
        # ---------------------------------------------

        detected = (
            self.memory_conflict_detector.detect(
                resolved_memory
            )
        )

        candidate_conflicts = detected.get(
            "message_conflicts",
            [],
        )

        # ---------------------------------------------
        # Confirm safe conflicts
        # ---------------------------------------------

        confirmed_conflicts = (
            self.memory_conflict_confirmer.confirm(
                candidate_conflicts
            )
        )

        print("\n" + "=" * 60)
        print("DEBUG - CANDIDATE CONFLICTS")
        print("=" * 60)

        for conflict in candidate_conflicts:
            print(
                conflict["first"].get("id"),
                "->",
                conflict["first"].get("content"),
            )
            print(
                conflict["second"].get("id"),
                "->",
                conflict["second"].get("content"),
            )
            print(
                "Shared:",
                conflict.get("shared_terms"),
            )
            print("-" * 60)


        print("\n" + "=" * 60)
        print("DEBUG - CONFIRMED CONFLICTS")
        print("=" * 60)

        for conflict in confirmed_conflicts:
            print(
                conflict["first"].get("id"),
                "->",
                conflict["first"].get("content"),
            )
            print(
                conflict["second"].get("id"),
                "->",
                conflict["second"].get("content"),
            )
            print("-" * 60)

        # ---------------------------------------------
        # Resolve confirmed conflicts
        # ---------------------------------------------

        resolved_messages = (
            self.factual_conflict_resolver.resolve(
                messages=resolved_memory.get(
                    "messages",
                    [],
                ),
                confirmed_conflicts=confirmed_conflicts,
            )
        )

        resolved_memory["messages"] = (
            resolved_messages
        )

        return resolved_memory

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
        """
        Main orchestration pipeline for the Context Memory Engine.
        """

        prepared_prompt = self._prepare_prompt(
            user_id=user_id,
            prompt=prompt,
        )

        memory = self._retrieve_memories(
            db=db,
            user_id=user_id,
            prepared_prompt=prepared_prompt,
        )

        resolved_memory = self._resolve_memory_conflicts(
            memory=memory,
        )

        optimized_memory = self._optimize_memory(
            memory=resolved_memory,
        )

        unified_memory = self._build_unified_memory(
            optimized_memory=optimized_memory,
        )

        selected_memory = self._select_memory(
            unified_memory=unified_memory,
        )

        # Track only memories actually selected for the final context
        self.memory_usage_tracker.track(
            db=db,
            selected_memory=selected_memory,
        )

        context = self._build_context(
            prepared_prompt=prepared_prompt,
            selected_memory=selected_memory,
        )

        # TEMPORARY: Skip Gemini during memory pipeline testing
        ai_response = "[GEMINI CALL SKIPPED]"

        return {
            "prompt": prepared_prompt,
            "conversation_memory": memory["conversations"],
            "message_memory": memory["messages"],
            "preference_memory": memory["preferences"],
            "document_memory": memory["documents"],
            "resolved_memory": resolved_memory,
            "optimized_memory": optimized_memory,
            "unified_memory": unified_memory,
            "selected_memory": selected_memory,
            "context": context,
            "ai_response": ai_response,
        }