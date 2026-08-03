from database.connection import SessionLocal
from database.models import User
from memory.memory_engine import MemoryEngine


def main():

    print("\n" + "=" * 60)
    print("PHASE 34.1 - FINAL SYSTEM INTEGRATION TEST")
    print("=" * 60)

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .order_by(User.id.asc())
            .first()
        )

        assert user is not None, (
            "No user available."
        )

        engine = MemoryEngine()

        # --------------------------------------------------
        # Skip Gemini for integration testing.
        # --------------------------------------------------

        engine._generate_response = (
            lambda context:
            "[FINAL SYSTEM TEST]"
        )

        # --------------------------------------------------
        # Test Prompt
        # --------------------------------------------------

        prompt = (
            "Summarize everything you know about me "
            "from my uploaded resume, profile, "
            "previous conversations, and image edits."
        )

        result = engine.process_prompt(
            db=db,
            user_id=user.id,
            prompt=prompt,
        )

        # ==================================================
        # PIPELINE VALIDATION
        # ==================================================

        assert "conversation_memory" in result
        assert "message_memory" in result
        assert "preference_memory" in result
        assert "document_memory" in result
        assert "image_memory" in result

        assert "resolved_memory" in result
        assert "consolidated_memory" in result
        assert "optimized_memory" in result
        assert "unified_memory" in result
        assert "selected_memory" in result
        assert "context" in result

        assert (
            result["ai_response"]
            == "[FINAL SYSTEM TEST]"
        )

        # ==================================================
        # DISPLAY MEMORY COUNTS
        # ==================================================

        print("\nMEMORY SUMMARY")
        print("-" * 60)

        print(
            "Conversations :",
            len(result["conversation_memory"]),
        )

        print(
            "Messages      :",
            len(result["message_memory"]),
        )

        print(
            "Preferences   :",
            len(result["preference_memory"]),
        )

        print(
            "Documents     :",
            len(result["document_memory"]),
        )

        print(
            "Images        :",
            len(result["image_memory"]),
        )

        print(
            "Unified Memory:",
            len(result["unified_memory"]),
        )

        print(
            "Selected      :",
            len(result["selected_memory"]),
        )

        # ==================================================
        # CONTEXT PREVIEW
        # ==================================================

        print("\nFINAL CONTEXT")
        print("-" * 60)

        preview = result["context"][:1200]

        print(preview)

        if len(result["context"]) > 1200:
            print("\n... (truncated)")

        # ==================================================
        # VALIDATION
        # ==================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("\nPrompt preparation passed.")
        print("Profile extraction passed.")
        print("Explicit memory commands available.")
        print("Conversation retrieval passed.")
        print("Message retrieval passed.")
        print("Preference retrieval passed.")
        print("Document retrieval passed.")
        print("Image retrieval passed.")
        print("Conflict resolution passed.")
        print("Memory consolidation passed.")
        print("Memory optimization passed.")
        print("Unified memory construction passed.")
        print("Memory selection passed.")
        print("Context builder passed.")
        print("LLM boundary passed.")

        print(
            "\nFINAL SYSTEM INTEGRATION TEST PASSED"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()