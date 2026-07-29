from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from database.connection import get_db
from schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from services.conversation_service import ConversationService
conversation_service = ConversationService()

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "/",
    response_model=ConversationResponse,
)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    return conversation_service.create_conversation(
        db,
        conversation,
    )


@router.get(
    "/",
    response_model=List[ConversationResponse],
)
def get_conversations(
    db: Session = Depends(get_db),
):
   return conversation_service.get_all_conversations(db)