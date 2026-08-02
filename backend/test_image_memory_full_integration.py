from database.connection import SessionLocal
from database.models import ImageMemory, User
from memory.memory_engine import MemoryEngine
from services.image_memory_service import ImageMemoryService


def main():

    print("\n" + "=" * 60)
    print("PHASE 31 - FULL IMAGE MEMORY INTEGRATION TEST")
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
            "No user available for test."
        )

        service = ImageMemoryService()

        # ==================================================
        # CREATE IMAGE HISTORY
        # ==================================================

        original = service.register_image(
            db=db,
            user_id=user.id,
            filename="phase31_car_original.jpg",
            filepath=(
                "test_images/"
                "phase31_car_original.jpg"
            ),
            description="Original photo of a car.",
        )

        created_ids.append(
            original.id
        )

        edit_1 = service.create_edited_version(
            db=db,
            parent_image_id=original.id,
            filename="phase31_car_edit1.jpg",
            filepath=(
                "test_images/"
                "phase31_car_edit1.jpg"
            ),
            edit_instruction=(
                "Make the background darker."
            ),
            description=(
                "Car with darker background."
            ),
        )

        created_ids.append(
            edit_1.id
        )

        edit_2 = service.create_edited_version(
            db=db,
            parent_image_id=edit_1.id,
            filename="phase31_car_edit2.jpg",
            filepath=(
                "test_images/"
                "phase31_car_edit2.jpg"
            ),
            edit_instruction=(
                "Remove the person in the background."
            ),
            description=(
                "Car with cleaned background."
            ),
        )

        created_ids.append(
            edit_2.id
        )

        # ==================================================
        # RUN MEMORY ENGINE
        # ==================================================

        engine = MemoryEngine()

        # Do not consume Gemini quota.
        engine._generate_response = (
            lambda context:
            "[TEST IMAGE MEMORY RESPONSE]"
        )

        prompt = (
            "What edits did I make "
            "to my image earlier?"
        )

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt=prompt,
        )

        # ==================================================
        # RAW IMAGE MEMORY
        # ==================================================

        images = result.get(
            "image_memory",
            [],
        )

        print("\nRAW IMAGE MEMORY")
        print("-" * 60)

        for image in images:

            print(
                f"ID={image['id']} | "
                f"v{image['edit_version']} | "
                f"{image['filename']}"
            )

        image_ids = {
            image["id"]
            for image in images
        }

        assert original.id in image_ids
        assert edit_1.id in image_ids
        assert edit_2.id in image_ids

        # ==================================================
        # OPTIMIZED MEMORY
        # ==================================================

        optimized_images = (
            result["optimized_memory"].get(
                "images",
                [],
            )
        )

        assert optimized_images, (
            "Images disappeared during optimization."
        )

        # ==================================================
        # UNIFIED MEMORY
        # ==================================================

        unified_images = [
            memory
            for memory
            in result["unified_memory"]
            if memory.get("memory_type")
            == "image"
        ]

        assert unified_images, (
            "Images did not reach unified memory."
        )

        # ==================================================
        # SELECTED MEMORY
        # ==================================================

        selected_images = [
            memory
            for memory
            in result["selected_memory"]
            if memory.get("memory_type")
            == "image"
        ]

        assert selected_images, (
            "No image memory reached selection."
        )

        # ==================================================
        # FINAL CONTEXT
        # ==================================================

        context = result["context"]

        print("\nFINAL CONTEXT")
        print("-" * 60)

        print(context)

        assert "Image" in context, (
            "Image memory missing from context."
        )

        assert (
            "Make the background darker."
            in context
            or
            "Remove the person in the background."
            in context
        ), (
            "Image edit history missing from context."
        )

        assert (
            "phase31_car_" in context
        ), (
            "Image identity missing from context."
        )

        # ==================================================
        # LLM BOUNDARY
        # ==================================================

        assert (
            result["ai_response"]
            == "[TEST IMAGE MEMORY RESPONSE]"
        )

        # ==================================================
        # VALIDATION
        # ==================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nImage history retrieved.")
        print("Images survived optimization.")
        print("Images entered unified memory.")
        print("Image memory was selected.")
        print("Edit history reached final context.")
        print("LLM boundary reached without Gemini.")

        print(
            "\nFULL IMAGE MEMORY INTEGRATION "
            "TEST PASSED"
        )

    finally:

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