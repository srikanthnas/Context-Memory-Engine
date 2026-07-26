from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.message import MessageCreate, MessageResponse
from services.message_service import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("/", response_model=MessageResponse)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    return MessageService.create_message(db, message)


@router.get(
    "/conversation/{conversation_id}",
    response_model=List[MessageResponse],
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    return MessageService.get_messages(db, conversation_id)