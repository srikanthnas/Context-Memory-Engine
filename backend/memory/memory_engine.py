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
from memory.memory_consolidator import MemoryConsolidator
from memory.image_memory import ImageMemoryManager
from memory.user_profile_extractor import UserProfileExtractor
from services.preference_service import PreferenceService


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
        self.image_memory = ImageMemoryManager()
        self.unified_context_manager = UnifiedContextManager()
        self.memory_selector = MemorySelector()
        self.llm_manager = LLMManager()
        self.memory_usage_tracker = MemoryUsageTracker()
        self.memory_conflict_resolver = MemoryConflictResolver()
        self.memory_conflict_detector = MemoryConflictDetector()
        self.memory_conflict_confirmer = MemoryConflictConfirmer()
        self.factual_conflict_resolver = FactualConflictResolver()
        self.memory_consolidator = MemoryConsolidator()
        self.user_profile_extractor = UserProfileExtractor()
        self.preference_service = PreferenceService()

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

    def _update_user_profile(
        self,
        db: Session,
        user_id: int,
        prompt: str,
    ):
        """
        Extract and persist stable user-profile facts
        from the current user prompt.

        Existing facts with the same key are updated
        instead of duplicated.
        """

        facts = self.user_profile_extractor.extract(
            prompt
        )

        if not facts:
            return []

        saved_facts = (
            self.preference_service.save_profile_facts(
                db=db,
                user_id=user_id,
                facts=facts,
            )
        )

        return saved_facts

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

        images = self.image_memory.get_images(
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
            "images": images,
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

        Conflict resolution may modify supported memory
        categories, but unrelated memory sources such as
        images must remain preserved.
        """

        # ==================================================
        # PRESERVE ALL RETRIEVED MEMORY SOURCES
        # ==================================================

        original_memory = dict(memory)

        # ==================================================
        # STRUCTURED MEMORY CONFLICT RESOLUTION
        # ==================================================

        conflict_result = (
            self.memory_conflict_resolver.resolve(
                memory
            )
        )

        # Start from the original complete memory dictionary
        # so newly added memory types such as images cannot
        # disappear during conflict resolution.

        resolved_memory = dict(
            original_memory
        )

        # Merge whatever categories the conflict resolver
        # actually changed.

        if conflict_result:
            resolved_memory.update(
                conflict_result
            )

        # ==================================================
        # DETECT POSSIBLE FACTUAL MESSAGE CONFLICTS
        # ==================================================

        detected = (
            self.memory_conflict_detector.detect(
                resolved_memory
            )
        )

        candidate_conflicts = detected.get(
            "message_conflicts",
            [],
        )

        # ==================================================
        # CONFIRM SAFE CONFLICTS
        # ==================================================

        confirmed_conflicts = (
            self.memory_conflict_confirmer.confirm(
                candidate_conflicts
            )
        )

        # ==================================================
        # RESOLVE CONFIRMED MESSAGE CONFLICTS
        # ==================================================

        resolved_messages = (
            self.factual_conflict_resolver.resolve(
                messages=resolved_memory.get(
                    "messages",
                    [],
                ),
                confirmed_conflicts=(
                    confirmed_conflicts
                ),
            )
        )

        resolved_memory["messages"] = (
            resolved_messages
        )

        return resolved_memory

    def _consolidate_memory(
        self,
        memory: dict,
    ):
        """
        Consolidate redundant active-context memories.
        """

        consolidated_memory = dict(memory)

        consolidated_messages = (
            self.memory_consolidator.consolidate(
                memories=memory.get(
                    "messages",
                    [],
                )
            )
        )

        consolidated_memory["messages"] = (
            consolidated_messages
        )

        return consolidated_memory

    def _optimize_memory(
        self,
        memory: dict,
    ):
        """
        Optimize retrieved memory before unified
        context construction.
        """

        return self.context_optimizer.optimize(
            conversations=memory.get(
                "conversations",
                [],
            ),
            messages=memory.get(
                "messages",
                [],
            ),
            preferences=memory.get(
                "preferences",
                [],
            ),
            documents=memory.get(
                "documents",
                [],
            ),
            images=memory.get(
                "images",
                [],
            ),
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
            images=optimized_memory.get("images", []),
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

        Pipeline:
        1. Prepare prompt
        2. Retrieve memories
        3. Resolve factual conflicts
        4. Consolidate duplicate memories
        5. Optimize memories
        6. Build unified memory
        7. Select relevant memories
        8. Track memory usage
        9. Build final context
        10. Generate LLM response
        """

        # ==================================================
        # 1. PREPARE PROMPT
        # ==================================================

        prepared_prompt = self._prepare_prompt(
    user_id=user_id,
    prompt=prompt,
)

# ==================================================
# PERSIST STABLE USER PROFILE FACTS
# ==================================================

        profile_updates = self._update_user_profile(
            db=db,
            user_id=user_id,
            prompt=prepared_prompt["prompt"],
        )

        # ==================================================
        # RETRIEVE MEMORY
        # ==================================================

        memory = self._retrieve_memories(
            db=db,
            user_id=user_id,
            prepared_prompt=prepared_prompt,
        )

        # ==================================================
        # 3. RESOLVE FACTUAL CONFLICTS
        # ==================================================

        resolved_memory = self._resolve_memory_conflicts(
            memory=memory,
        )

        # ==================================================
        # 4. CONSOLIDATE MEMORY
        # ==================================================

        consolidated_memory = self._consolidate_memory(
            memory=resolved_memory,
        )

        # ==================================================
        # 5. OPTIMIZE MEMORY
        # ==================================================

        optimized_memory = self._optimize_memory(
            memory=consolidated_memory,
        )

        # ==================================================
        # 6. BUILD UNIFIED MEMORY
        # ==================================================

        unified_memory = self._build_unified_memory(
            optimized_memory=optimized_memory,
        )

        # ==================================================
        # 7. SELECT MEMORY
        # ==================================================

        selected_memory = self._select_memory(
            unified_memory=unified_memory,
        )

        # ==================================================
        # 8. TRACK MEMORY USAGE
        # ==================================================

        self.memory_usage_tracker.track(
            db=db,
            selected_memory=selected_memory,
        )

        # ==================================================
        # 9. BUILD FINAL CONTEXT
        # ==================================================

        context = self._build_context(
            prepared_prompt=prepared_prompt,
            selected_memory=selected_memory,
        )

        # ==================================================
        # 10. GENERATE RESPONSE
        # ==================================================

        ai_response = self._generate_response(
            context=context,
        )

        # ==================================================
        # RETURN PIPELINE RESULT
        # ==================================================

        return {
            "prompt": prepared_prompt,

            "profile_updates": [
                {
                    "id": item.id,
                    "key": item.key,
                    "value": item.value,
                }
                for item in profile_updates
            ],

                "conversation_memory": memory.get(
                    "conversations",
                    [],
                ),

            "message_memory": memory.get(
                "messages",
                [],
            ),

            "preference_memory": memory.get(
                "preferences",
                [],
            ),

            "document_memory": memory.get(
                "documents",
                [],
            ),

            "image_memory": memory.get(
                "images",
                [],
            ),

            "resolved_memory": resolved_memory,

            "consolidated_memory": consolidated_memory,

            "optimized_memory": optimized_memory,

            "unified_memory": unified_memory,

            "selected_memory": selected_memory,

            "context": context,

            "ai_response": ai_response,
        }