from database.connection import SessionLocal
from database.models import (
    Conversation,
    ImageMemory,
    User,
)


def main():

    print("\n" + "=" * 60)
    print("PHASE 31 - IMAGE MEMORY MODEL TEST")
    print("=" * 60)

    db = SessionLocal()

    original = None
    edited = None

    try:

        # --------------------------------------------------
        # FIND EXISTING USER
        # --------------------------------------------------

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None, (
            "No existing user found."
        )

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.user_id
                == user.id
            )
            .order_by(
                Conversation.id.asc()
            )
            .first()
        )

        print(
            f"\nUsing User ID: {user.id}"
        )

        if conversation:
            print(
                f"Using Conversation ID: "
                f"{conversation.id}"
            )

        # --------------------------------------------------
        # ORIGINAL IMAGE
        # --------------------------------------------------

        original = ImageMemory(
            user_id=user.id,
            conversation_id=(
                conversation.id
                if conversation
                else None
            ),
            filename="phase31_original.jpg",
            filepath=(
                "test_images/"
                "phase31_original.jpg"
            ),
            description=(
                "Temporary Phase 31 test image."
            ),
            edit_version=1,
        )

        db.add(original)
        db.commit()
        db.refresh(original)

        print("\nORIGINAL IMAGE")
        print("-" * 60)

        print(
            f"ID: {original.id}"
        )
        print(
            f"Version: {original.edit_version}"
        )
        print(
            f"Parent: {original.parent_image_id}"
        )

        # --------------------------------------------------
        # EDITED VERSION
        # --------------------------------------------------

        edited = ImageMemory(
            user_id=user.id,
            conversation_id=(
                conversation.id
                if conversation
                else None
            ),
            filename="phase31_edited.jpg",
            filepath=(
                "test_images/"
                "phase31_edited.jpg"
            ),
            description=(
                "Edited Phase 31 test image."
            ),
            parent_image_id=original.id,
            edit_instruction=(
                "Make the background darker."
            ),
            edit_version=2,
        )

        db.add(edited)
        db.commit()
        db.refresh(edited)

        print("\nEDITED IMAGE")
        print("-" * 60)

        print(
            f"ID: {edited.id}"
        )
        print(
            f"Version: {edited.edit_version}"
        )
        print(
            f"Parent: {edited.parent_image_id}"
        )
        print(
            f"Instruction: "
            f"{edited.edit_instruction}"
        )

        # --------------------------------------------------
        # RELATIONSHIP TEST
        # --------------------------------------------------

        db.refresh(original)

        print("\nEDIT HISTORY")
        print("-" * 60)

        for version in original.edited_versions:
            print(
                f"v{version.edit_version} -> "
                f"{version.edit_instruction}"
            )

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        assert original.parent_image_id is None

        assert edited.parent_image_id == original.id

        assert edited.parent_image.id == original.id

        assert edited in original.edited_versions

        assert edited.edit_version == 2

        assert (
            edited.edit_instruction
            == "Make the background darker."
        )

        print(
            "\nOriginal image stored successfully."
        )

        print(
            "Edited version stored successfully."
        )

        print(
            "Parent-child relationship works."
        )

        print(
            "Edit instruction preserved."
        )

        print(
            "Image version history works."
        )

        print(
            "\nIMAGE MEMORY MODEL TEST PASSED"
        )

    finally:

        # --------------------------------------------------
        # CLEAN UP ONLY TEST RECORDS
        # --------------------------------------------------

        db.rollback()

        if edited is not None:
            test_edited = (
                db.query(ImageMemory)
                .filter(
                    ImageMemory.id == edited.id
                )
                .first()
            )

            if test_edited:
                db.delete(test_edited)
                db.commit()

        if original is not None:
            test_original = (
                db.query(ImageMemory)
                .filter(
                    ImageMemory.id == original.id
                )
                .first()
            )

            if test_original:
                db.delete(test_original)
                db.commit()

        db.close()


if __name__ == "__main__":
    main()