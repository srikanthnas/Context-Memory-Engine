import os
import shutil
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from database.models import Document

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


class DocumentService:

    @staticmethod
    def upload_document(
        db: Session,
        user_id: int,
        file: UploadFile,
    ):

        file_path = UPLOAD_FOLDER / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            user_id=user_id,
            filename=file.filename,
            filepath=str(file_path),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document