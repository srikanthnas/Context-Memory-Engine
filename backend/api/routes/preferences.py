from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.preference import (
    PreferenceCreate,
    PreferenceResponse,
)
from services.preference_service import PreferenceService

router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"],
)


@router.post("/", response_model=PreferenceResponse)
def create_preference(
    preference: PreferenceCreate,
    db: Session = Depends(get_db),
):
    return PreferenceService.create_preference(
        db,
        preference,
    )


@router.get(
    "/user/{user_id}",
    response_model=List[PreferenceResponse],
)
def get_preferences(
    user_id: int,
    db: Session = Depends(get_db),
):
    return PreferenceService.get_preferences(
        db,
        user_id,
    )