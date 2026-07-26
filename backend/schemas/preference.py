from pydantic import BaseModel


class PreferenceCreate(BaseModel):
    user_id: int
    key: str
    value: str


class PreferenceResponse(BaseModel):
    id: int
    user_id: int
    key: str
    value: str

    model_config = {
        "from_attributes": True
    }