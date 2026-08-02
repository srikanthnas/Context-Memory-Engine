from database.connection import SessionLocal
from services.chat_service import ChatService


def main():

    print("\n" + "=" * 60)
    print("PHASE 30 - FULL ORCHESTRATION TEST")
    print("=" * 60)

    db = SessionLocal()

    try:
        chat = ChatService()

        # --------------------------------------------------
        # MOCK ONLY THE EXTERNAL LLM CALL
        # --------------------------------------------------
        #
        # Everything else runs normally:
        #
        # ChatService
        # -> MemoryEngine
        # -> retrieval
        # -> conflict resolution
        # -> consolidation
        # -> optimization
        # -> unified memory
        # -> selection
        # -> context construction
        #
        # Gemini is replaced only at the final boundary.
        # --------------------------------------------------

        chat.memory_engine._generate_response = (
            lambda context: "[TEST LLM RESPONSE]"
        )

        result = chat.chat(
            db=db,
            user_id=2,
            prompt=(
                "Explain my programming skills "
                "from my resume."
            ),
        )

        # ==================================================
        # SELECTED MEMORY
        # ==================================================

        print("\n" + "=" * 60)
        print("SELECTED MEMORY")
        print("=" * 60)

        selected_memory = result.get(
            "selected_memory",
            [],
        )

        for item in selected_memory:

            print(
                item.get("memory_type"),
                "->",
                item.get("score"),
            )

            if item.get(
                "memory_type"
            ) == "preference":

                print(
                    "PREFERENCE:",
                    item.get("key"),
                    "=",
                    item.get("value"),
                )

            elif item.get(
                "memory_type"
            ) == "document":

                print(
                    "FILE:",
                    item.get("filename"),
                )

                print(
                    "CHUNK:\n",
                    item.get("chunk"),
                )

            print("-" * 60)

        # ==================================================
        # FINAL CONTEXT
        # ==================================================

        context = result.get(
            "context",
            "",
        )

        print("\n" + "=" * 60)
        print("FINAL CONTEXT")
        print("=" * 60)

        print(context)

        # ==================================================
        # AI RESPONSE
        # ==================================================

        ai_response = result.get(
            "ai_response"
        )

        print("\n" + "=" * 60)
        print("CONTROLLED LLM RESPONSE")
        print("=" * 60)

        print(ai_response)

        # ==================================================
        # VALIDATION
        # ==================================================

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        assert result.get("prompt"), (
            "Prepared prompt was not returned."
        )

        assert (
            "resolved_memory" in result
        ), (
            "Conflict-resolution stage missing."
        )

        assert (
            "consolidated_memory" in result
        ), (
            "Consolidation stage missing."
        )

        assert (
            "optimized_memory" in result
        ), (
            "Optimization stage missing."
        )

        assert (
            "unified_memory" in result
        ), (
            "Unified-memory stage missing."
        )

        assert (
            "selected_memory" in result
        ), (
            "Memory-selection stage missing."
        )

        assert selected_memory, (
            "No memory was selected."
        )

        assert context, (
            "Final context was empty."
        )

        assert (
            "Explain my programming skills"
            in context
        ), (
            "Current user question did not "
            "reach final context."
        )

        assert (
            ai_response
            == "[TEST LLM RESPONSE]"
        ), (
            "Controlled LLM boundary failed."
        )

        print(
            "\nPrompt preparation passed."
        )

        print(
            "Memory retrieval passed."
        )

        print(
            "Conflict resolution passed."
        )

        print(
            "Memory consolidation passed."
        )

        print(
            "Decay-aware optimization passed."
        )

        print(
            "Unified memory construction passed."
        )

        print(
            "Memory selection passed."
        )

        print(
            "Final context construction passed."
        )

        print(
            "Controlled LLM boundary passed."
        )

        print(
            "\nFULL ORCHESTRATION TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()