"""
Memory Engine

Coordinates all memory components.
"""

from sqlalchemy.orm import Session

from memory.prompt_manager import PromptManager
from memory.conversation_memory import ConversationMemory
from memory.message_memory import MessageMemory


class MemoryEngine:
    """Main orchestrator for the Context Memory Engine."""

    def __init__(self):
        self.prompt_manager = PromptManager()
        self.conversation_memory = ConversationMemory()
        self.message_memory = MessageMemory()

    def process_prompt(
        self,
        db: Session,
        user_id: int,
        prompt: str,
    ):
        prepared_prompt = self.prompt_manager.prepare_prompt(
            user_id=user_id,
            prompt=prompt,
        )

        conversations = self.conversation_memory.get_recent_conversations(
            db=db,
            user_id=user_id,
        )

        latest_messages = []

        if conversations:
            latest_conversation = conversations[0]

            latest_messages = self.message_memory.get_recent_messages(
                db=db,
                conversation_id=latest_conversation["id"],
            )

        return {
            "prompt": prepared_prompt,
            "conversation_memory": conversations,
            "message_memory": latest_messages,
        }