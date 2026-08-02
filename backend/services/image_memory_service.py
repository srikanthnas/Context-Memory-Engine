from datetime import datetime

from sqlalchemy.orm import Session

from database.models import ImageMemory


class ImageMemoryService:
    """
    Handles persistent image-memory operations.

    Responsibilities:
    - Register original uploaded images
    - Register edited image versions
    - Retrieve individual image memories
    - Retrieve complete edit history
    """

    @staticmethod
    def register_image(
        db: Session,
        user_id: int,
        filename: str,
        filepath: str,
        conversation_id: int = None,
        description: str = None,
        importance: float = 1.0,
    ) -> ImageMemory:
        """
        Register a new original image.

        Original images always begin at version 1
        and have no parent image.
        """

        image = ImageMemory(
            user_id=user_id,
            conversation_id=conversation_id,
            filename=filename,
            filepath=filepath,
            description=description,
            parent_image_id=None,
            edit_instruction=None,
            edit_version=1,
            importance=importance,
        )

        db.add(image)
        db.commit()
        db.refresh(image)

        return image

    @staticmethod
    def create_edited_version(
        db: Session,
        parent_image_id: int,
        filename: str,
        filepath: str,
        edit_instruction: str,
        description: str = None,
    ) -> ImageMemory:
        """
        Register an edited version of an existing image.

        The new image becomes a child of the supplied
        parent image and inherits the user and
        conversation association.
        """

        parent = (
            db.query(ImageMemory)
            .filter(
                ImageMemory.id == parent_image_id
            )
            .first()
        )

        if parent is None:
            raise ValueError(
                "Parent image memory not found."
            )

        edited_image = ImageMemory(
            user_id=parent.user_id,
            conversation_id=parent.conversation_id,
            filename=filename,
            filepath=filepath,
            description=description,
            parent_image_id=parent.id,
            edit_instruction=edit_instruction,
            edit_version=(
                parent.edit_version + 1
            ),
            importance=parent.importance,
        )

        db.add(edited_image)
        db.commit()
        db.refresh(edited_image)

        return edited_image

    @staticmethod
    def get_image(
        db: Session,
        image_id: int,
    ):
        """
        Retrieve an image-memory record.
        """

        return (
            db.query(ImageMemory)
            .filter(
                ImageMemory.id == image_id
            )
            .first()
        )

    @staticmethod
    def get_user_images(
        db: Session,
        user_id: int,
    ):
        """
        Retrieve all image memories belonging
        to a user.
        """

        return (
            db.query(ImageMemory)
            .filter(
                ImageMemory.user_id == user_id
            )
            .order_by(
                ImageMemory.created_at.asc()
            )
            .all()
        )

    @staticmethod
    def get_edit_history(
        db: Session,
        image_id: int,
    ):
        """
        Retrieve the edit lineage ending at image_id.

        Example:

        Original v1
            ↓
        Edit v2
            ↓
        Edit v3

        Calling this with v3 returns:
        [v1, v2, v3]
        """

        current = (
            db.query(ImageMemory)
            .filter(
                ImageMemory.id == image_id
            )
            .first()
        )

        if current is None:
            return []

        history = []

        visited = set()

        while current is not None:

            # Protect against accidental circular
            # parent relationships.
            if current.id in visited:
                break

            visited.add(current.id)

            history.append(current)

            if current.parent_image_id is None:
                break

            current = (
                db.query(ImageMemory)
                .filter(
                    ImageMemory.id
                    == current.parent_image_id
                )
                .first()
            )

        history.reverse()

        return history

    @staticmethod
    def mark_accessed(
        db: Session,
        image_id: int,
    ):
        """
        Update adaptive-memory usage metadata
        when an image memory is accessed.
        """

        image = (
            db.query(ImageMemory)
            .filter(
                ImageMemory.id == image_id
            )
            .first()
        )

        if image is None:
            return None

        image.access_count += 1
        image.last_accessed = datetime.utcnow()

        db.commit()
        db.refresh(image)

        return image