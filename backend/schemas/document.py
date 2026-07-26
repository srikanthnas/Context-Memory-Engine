from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    filepath: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }