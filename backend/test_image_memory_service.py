from database.connection import SessionLocal
from database.models import ImageMemory, User
from services.image_memory_service import ImageMemoryService


def main():

    print("\n" + "=" * 60)
    print("PHASE 31 - IMAGE MEMORY SERVICE TEST")
    print("=" * 60)

    db = SessionLocal()

    created_ids = []

    try:

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None, (
            "No user exists for image-memory test."
        )

        service = ImageMemoryService()

        # ==================================================
        # ORIGINAL
        # ==================================================

        original = service.register_image(
            db=db,
            user_id=user.id,
            filename="phase31_original.jpg",
            filepath="test_images/phase31_original.jpg",
            description="Original test image.",
        )

        created_ids.append(original.id)

        print("\nORIGINAL")
        print("-" * 60)

        print(
            f"ID={original.id} | "
            f"Version={original.edit_version}"
        )

        assert original.edit_version == 1
        assert original.parent_image_id is None

        # ==================================================
        # EDIT 1
        # ==================================================

        edit_1 = service.create_edited_version(
            db=db,
            parent_image_id=original.id,
            filename="phase31_edit_1.jpg",
            filepath="test_images/phase31_edit_1.jpg",
            edit_instruction="Make the background darker.",
        )

        created_ids.append(edit_1.id)

        # ==================================================
        # EDIT 2
        # ==================================================

        edit_2 = service.create_edited_version(
            db=db,
            parent_image_id=edit_1.id,
            filename="phase31_edit_2.jpg",
            filepath="test_images/phase31_edit_2.jpg",
            edit_instruction=(
                "Remove the person in the background."
            ),
        )

        created_ids.append(edit_2.id)

        print("\nEDITED VERSIONS")
        print("-" * 60)

        print(
            f"ID={edit_1.id} | "
            f"Version={edit_1.edit_version} | "
            f"Parent={edit_1.parent_image_id}"
        )

        print(
            f"ID={edit_2.id} | "
            f"Version={edit_2.edit_version} | "
            f"Parent={edit_2.parent_image_id}"
        )

        # ==================================================
        # HISTORY
        # ==================================================

        history = service.get_edit_history(
            db=db,
            image_id=edit_2.id,
        )

        print("\nEDIT HISTORY")
        print("-" * 60)

        for image in history:

            print(
                f"v{image.edit_version} | "
                f"ID={image.id} | "
                f"{image.edit_instruction}"
            )

        assert len(history) == 3, (
            "Complete edit history was not returned."
        )

        assert history[0].id == original.id
        assert history[1].id == edit_1.id
        assert history[2].id == edit_2.id

        assert [
            image.edit_version
            for image in history
        ] == [1, 2, 3]

        # ==================================================
        # ACCESS TRACKING
        # ==================================================

        before_access = edit_2.access_count

        accessed = service.mark_accessed(
            db=db,
            image_id=edit_2.id,
        )

        assert (
            accessed.access_count
            == before_access + 1
        ), (
            "Image access count was not updated."
        )

        # ==================================================
        # VALIDATION
        # ==================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nOriginal image registered.")
        print("Edited versions registered.")
        print("Version numbers increment correctly.")
        print("Complete edit lineage retrieved.")
        print("Image access tracking works.")

        print(
            "\nIMAGE MEMORY SERVICE TEST PASSED"
        )

    finally:

        # Delete only temporary Phase 31 records.
        if created_ids:

            (
                db.query(ImageMemory)
                .filter(
                    ImageMemory.id.in_(
                        created_ids
                    )
                )
                .delete(
                    synchronize_session=False
                )
            )

            db.commit()

        db.close()


if __name__ == "__main__":
    main()