from sqlalchemy.orm import Session

from database.models import ImageMemory


class ImageMemoryManager:
    """
    Retrieves persistent image memories for the
    Context Memory Engine.
    """

    IMAGE_TERMS = {
        "image",
        "images",
        "photo",
        "photos",
        "picture",
        "pictures",
        "edit",
        "edited",
        "editing",
        "background",
        "version",
    }

    @staticmethod
    def _is_image_related(query: str) -> bool:
        """
        Determine whether the current prompt appears
        to refer to image memory.
        """

        if not query:
            return False

        normalized = (
            query.lower()
            .replace(".", " ")
            .replace(",", " ")
            .replace("?", " ")
            .replace("!", " ")
        )

        words = set(normalized.split())

        return bool(
            words
            & ImageMemoryManager.IMAGE_TERMS
        )

    @classmethod
    def get_images(
        cls,
        db: Session,
        user_id: int,
        query: str,
        limit: int = 5,
    ):
        """
        Retrieve recent image memories when the prompt
        appears to reference an image.

        Non-image prompts return an empty list so image
        history does not pollute normal text context.
        """

        if not cls._is_image_related(query):
            return []

        images = (
            db.query(ImageMemory)
            .filter(
                ImageMemory.user_id == user_id
            )
            .order_by(
                ImageMemory.created_at.desc(),
                ImageMemory.id.desc(),
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "id": image.id,
                "user_id": image.user_id,
                "conversation_id": (
                    image.conversation_id
                ),
                "filename": image.filename,
                "filepath": image.filepath,
                "description": image.description,
                "parent_image_id": (
                    image.parent_image_id
                ),
                "edit_instruction": (
                    image.edit_instruction
                ),
                "edit_version": (
                    image.edit_version
                ),
                "created_at": (
                    image.created_at.isoformat()
                    if image.created_at
                    else None
                ),
                "last_accessed": (
                    image.last_accessed.isoformat()
                    if image.last_accessed
                    else None
                ),
                "access_count": (
                    image.access_count
                ),
                "importance": (
                    image.importance
                ),
                "memory_type": "image",
            }
            for image in images
        ]