from database.connection import SessionLocal
from database.models import ImageMemory, User
from memory.image_memory import ImageMemoryManager
from services.image_memory_service import ImageMemoryService


def main():

    print("\n" + "=" * 60)
    print("PHASE 31 - IMAGE MEMORY RETRIEVAL TEST")
    print("=" * 60)

    db = SessionLocal()

    created_ids = []

    try:

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None

        service = ImageMemoryService()
        image_memory = ImageMemoryManager()

        # ==============================================
        # CREATE TEST IMAGE HISTORY
        # ==============================================

        original = service.register_image(
            db=db,
            user_id=user.id,
            filename="car_original.jpg",
            filepath="test_images/car_original.jpg",
            description="Photo of a car.",
        )

        created_ids.append(original.id)

        edited = service.create_edited_version(
            db=db,
            parent_image_id=original.id,
            filename="car_edited.jpg",
            filepath="test_images/car_edited.jpg",
            edit_instruction="Make the background darker.",
            description="Edited photo of a car.",
        )

        created_ids.append(edited.id)

        # ==============================================
        # IMAGE-RELATED QUERY
        # ==============================================

        query = (
            "What edits did I make "
            "to my image earlier?"
        )

        results = image_memory.get_images(
            db=db,
            user_id=user.id,
            query=query,
        )

        print("\nIMAGE QUERY")
        print("-" * 60)
        print(query)

        print("\nRETRIEVED IMAGE MEMORY")
        print("-" * 60)

        for image in results:

            print(
                f"ID={image['id']} | "
                f"v{image['edit_version']} | "
                f"{image['filename']}"
            )

            if image["edit_instruction"]:
                print(
                    "Edit:",
                    image["edit_instruction"],
                )

        result_ids = {
            image["id"]
            for image in results
        }

        assert original.id in result_ids, (
            "Original image was not retrieved."
        )

        assert edited.id in result_ids, (
            "Edited image was not retrieved."
        )

        assert any(
            image["edit_instruction"]
            == "Make the background darker."
            for image in results
        ), (
            "Edit instruction was not retrieved."
        )

        # ==============================================
        # NON-IMAGE QUERY
        # ==============================================

        normal_results = (
            image_memory.get_images(
                db=db,
                user_id=user.id,
                query=(
                    "Explain my programming skills."
                ),
            )
        )

        assert normal_results == [], (
            "Image memory polluted a normal text query."
        )

        # ==============================================
        # MEMORY ENGINE RETRIEVAL
        # ==============================================

        from memory.memory_engine import MemoryEngine

        engine = MemoryEngine()

        prepared = engine._prepare_prompt(
            user_id=user.id,
            prompt=query,
        )

        memory = engine._retrieve_memories(
            db=db,
            user_id=user.id,
            prepared_prompt=prepared,
        )

        assert "images" in memory, (
            "Image memory source missing from MemoryEngine."
        )

        engine_image_ids = {
            image["id"]
            for image in memory["images"]
        }

        assert edited.id in engine_image_ids, (
            "MemoryEngine did not retrieve edited image."
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nImage-related query detected.")
        print("Original image retrieved.")
        print("Edited image retrieved.")
        print("Edit instruction preserved.")
        print("Normal text query ignored image memory.")
        print("MemoryEngine image retrieval connected.")

        print(
            "\nIMAGE MEMORY RETRIEVAL TEST PASSED"
        )

    finally:

        if created_ids:

            (
                db.query(ImageMemory)
                .filter(
                    ImageMemory.id.in_(created_ids)
                )
                .delete(
                    synchronize_session=False
                )
            )

            db.commit()

        db.close()


if __name__ == "__main__":
    main()