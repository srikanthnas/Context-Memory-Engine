from memory.memory_engine import MemoryEngine


def main():

    print("\n" + "=" * 60)
    print("PHASE 30 - CORE MEMORY INTEGRATION TEST")
    print("=" * 60)

    engine = MemoryEngine()

    # Disable the external LLM only for this test.
    # We want to validate the memory pipeline without
    # consuming Gemini quota.
    engine._generate_response = (
        lambda context: "[TEST RESPONSE]"
    )

    # --------------------------------------------------
    # TEST MEMORY
    # --------------------------------------------------

    memory = {
        "conversations": [
            {
                "id": 8001,
                "title": "Backend Development",
                "summary": "Discussion about project backend.",
                "score": 0.90,
            }
        ],

        "messages": [
            {
                "id": 8002,
                "role": "user",
                "content": "My project backend uses Flask.",
                "importance": 1.0,
                "access_count": 0,
                "last_accessed": "2026-01-01T10:00:00",
                "similarity": 0.80,
            },
            {
                "id": 8003,
                "role": "user",
                "content": "My project backend now uses FastAPI.",
                "importance": 1.0,
                "access_count": 5,
                "last_accessed": "2026-08-01T10:00:00",
                "similarity": 0.90,
            },
            {
                "id": 8004,
                "role": "user",
                "content": "  my project backend now uses FastAPI.  ",
                "importance": 2.0,
                "access_count": 10,
                "last_accessed": "2026-08-02T10:00:00",
                "similarity": 0.90,
            },
            {
                "id": 8005,
                "role": "user",
                "content": "My project database uses PostgreSQL.",
                "importance": 1.0,
                "access_count": 0,
                "last_accessed": "2026-08-01T10:00:00",
                "similarity": 0.80,
            },
        ],

        "preferences": [
            {
                "id": 8006,
                "key": "response_style",
                "value": "concise",
                "importance": 1.0,
                "access_count": 0,
            }
        ],

        "documents": [],
    }

    print("\nINITIAL MEMORY")
    print("-" * 60)

    for message in memory["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    # ==================================================
    # 1. CONFLICT RESOLUTION
    # ==================================================

    resolved = engine._resolve_memory_conflicts(
        memory=memory
    )

    print("\nAFTER CONFLICT RESOLUTION")
    print("-" * 60)

    for message in resolved["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    resolved_ids = {
        message["id"]
        for message in resolved["messages"]
    }

    assert 8002 not in resolved_ids, (
        "Outdated Flask fact survived conflict resolution."
    )

    assert 8003 in resolved_ids or 8004 in resolved_ids, (
        "Current FastAPI fact was removed."
    )

    assert 8005 in resolved_ids, (
        "Unrelated PostgreSQL fact was removed."
    )

    # ==================================================
    # 2. CONSOLIDATION
    # ==================================================

    consolidated = engine._consolidate_memory(
        memory=resolved
    )

    print("\nAFTER CONSOLIDATION")
    print("-" * 60)

    for message in consolidated["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    consolidated_ids = {
        message["id"]
        for message in consolidated["messages"]
    }

    assert 8004 in consolidated_ids, (
        "Stronger FastAPI duplicate was not preserved."
    )

    assert 8003 not in consolidated_ids, (
        "Weaker FastAPI duplicate survived consolidation."
    )

    assert 8005 in consolidated_ids, (
        "Unrelated memory disappeared during consolidation."
    )

    # ==================================================
    # 3. DECAY-AWARE OPTIMIZATION
    # ==================================================

    optimized = engine._optimize_memory(
        memory=consolidated
    )

    print("\nAFTER OPTIMIZATION")
    print("-" * 60)

    for message in optimized["messages"]:
        print(
            f"ID={message['id']} | "
            f"Strength="
            f"{message.get('memory_strength', 0):.4f} | "
            f"Ranking="
            f"{message.get('ranking_score', 0):.4f}"
        )

    assert optimized["messages"], (
        "Optimization removed every message."
    )

    # ==================================================
    # 4. UNIFIED MEMORY
    # ==================================================

    unified = engine._build_unified_memory(
        optimized_memory=optimized
    )

    assert unified is not None, (
        "Unified memory was not created."
    )

    print("\nUnified memory created.")

    # ==================================================
    # 5. MEMORY SELECTION
    # ==================================================

    selected = engine._select_memory(
        unified_memory=unified
    )

    assert selected is not None, (
        "Memory selection failed."
    )

    print("Memory selection completed.")

    # ==================================================
    # 6. CONTEXT CONSTRUCTION
    # ==================================================

    prepared_prompt = {
        "user_id": 1,
        "prompt": (
            "What backend technology "
            "does my project use?"
        ),
    }

    context = engine._build_context(
        prepared_prompt=prepared_prompt,
        selected_memory=selected,
    )

    assert context, (
        "Final context was empty."
    )

    print("Final context constructed.")

    # ==================================================
    # 7. LLM BOUNDARY
    # ==================================================

    response = engine._generate_response(
        context=context
    )

    assert response == "[TEST RESPONSE]", (
        "Controlled LLM boundary failed."
    )

    print("LLM boundary reached successfully.")

    # ==================================================
    # FINAL VALIDATION
    # ==================================================

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert "Flask" not in context, (
        "Outdated Flask fact reached final context."
    )

    assert "FastAPI" in context, (
        "Current FastAPI fact did not reach final context."
    )

    assert "PostgreSQL" in context, (
        "Non-conflicting database memory was lost."
    )

    print("\nOutdated fact removed.")
    print("Current fact preserved.")
    print("Duplicate memory consolidated.")
    print("Decay-aware optimization completed.")
    print("Unified memory constructed.")
    print("Memory selection completed.")
    print("Final context contains correct memories.")
    print("LLM boundary validated without Gemini call.")

    print(
        "\nCORE MEMORY INTEGRATION TEST PASSED"
    )


if __name__ == "__main__":
    main()