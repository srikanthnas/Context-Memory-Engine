from database.connection import SessionLocal
from memory.memory_engine import MemoryEngine


def main():
    db = SessionLocal()

    try:
        engine = MemoryEngine()

        user_id = 2
        prompt = "What programming languages are mentioned in my resume?"

        # ---------------------------------------
        # Prepare prompt
        # ---------------------------------------

        prepared_prompt = engine._prepare_prompt(
            user_id=user_id,
            prompt=prompt,
        )

        # ---------------------------------------
        # Retrieve memories
        # ---------------------------------------

        memory = engine._retrieve_memories(
            db=db,
            user_id=user_id,
            prepared_prompt=prepared_prompt,
        )

        # ---------------------------------------
        # Optimize memories
        # ---------------------------------------

        optimized_memory = engine._optimize_memory(
            memory=memory,
        )

        # ---------------------------------------
        # Build unified memory
        # ---------------------------------------

        unified_memory = engine._build_unified_memory(
            optimized_memory=optimized_memory,
        )

        # ---------------------------------------
        # Select memories
        # ---------------------------------------

        selected_memory = engine._select_memory(
            unified_memory=unified_memory,
        )

        # ---------------------------------------
        # Build final context
        # ---------------------------------------

        context = engine._build_context(
            prepared_prompt=prepared_prompt,
            selected_memory=selected_memory,
        )

        print("\n" + "=" * 60)
        print("SELECTED MEMORY")
        print("=" * 60)

        for item in selected_memory:
            print(
                item["memory_type"],
                "->",
                item["score"],
            )

            if item["memory_type"] == "document":
                print("FILE:", item["filename"])
                print("CHUNK:")
                print(item["chunk"])
                print("-" * 60)

        print("\n" + "=" * 60)
        print("FINAL CONTEXT")
        print("=" * 60)
        print(context)

        print("\n" + "=" * 60)
        print("GEMINI CALL SKIPPED")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()