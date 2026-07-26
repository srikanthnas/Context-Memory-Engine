from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: int
    role: str
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }