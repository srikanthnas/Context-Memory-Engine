from sqlalchemy.orm import Session

from memory.memory_engine import MemoryEngine
from schemas.conversation import ConversationCreate
from schemas.message import MessageCreate
from services.conversation_service import ConversationService
from services.message_service import MessageService


class ChatService:
    """
    Coordinates the complete chat workflow.

    Responsibilities:
    - Create a conversation (if needed)
    - Save user messages
    - Call the Memory Engine
    - Save AI responses
    """

    def __init__(self):
        self.memory_engine = MemoryEngine()

    def chat(
        self,
        db: Session,
        user_id: int,
        prompt: str,
        conversation_id: int = None,
    ):

        # ------------------------------------
        # Create conversation if one doesn't exist
        # ------------------------------------

        if conversation_id is None:

            conversation = ConversationService.create_conversation(
                db=db,
                conversation=ConversationCreate(
                    user_id=user_id,
                    title=prompt[:50],
                ),
            )

            conversation_id = conversation.id

        # ------------------------------------
        # Save user message
        # ------------------------------------

        MessageService.create_message(
            db=db,
            message=MessageCreate(
                conversation_id=conversation_id,
                role="user",
                content=prompt,
            ),
        )

        # ------------------------------------
        # Generate AI response
        # ------------------------------------

        result = self.memory_engine.process_prompt(
            db=db,
            user_id=user_id,
            prompt=prompt,
        )

        # ------------------------------------
        # Save AI response
        # ------------------------------------

        MessageService.create_message(
            db=db,
            message=MessageCreate(
                conversation_id=conversation_id,
                role="assistant",
                content=result["ai_response"],
            ),
        )

        return result