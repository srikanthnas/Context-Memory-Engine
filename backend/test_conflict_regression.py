from datetime import datetime, timedelta

from memory.memory_engine import MemoryEngine


def main():

    engine = MemoryEngine()

    print("\n" + "=" * 60)
    print("PHASE 27 - CONFLICT REGRESSION TEST")
    print("=" * 60)

    # =====================================================
    # TEST MEMORY
    # =====================================================

    base_time = datetime.now()

    messages = [
        {
            "id": 2001,
            "role": "user",
            "content": "My project backend uses Flask.",
            "timestamp": (
                base_time - timedelta(days=3)
            ).isoformat(),
            "memory_type": "message",
            "score": 0.80,
        },
        {
            "id": 2002,
            "role": "user",
            "content": "My project backend uses Django.",
            "timestamp": (
                base_time - timedelta(days=2)
            ).isoformat(),
            "memory_type": "message",
            "score": 0.82,
        },
        {
            "id": 2003,
            "role": "user",
            "content": "My project backend now uses FastAPI.",
            "timestamp": (
                base_time - timedelta(days=1)
            ).isoformat(),
            "memory_type": "message",
            "score": 0.85,
        },
        {
            "id": 2004,
            "role": "user",
            "content": "My project database uses PostgreSQL.",
            "timestamp": base_time.isoformat(),
            "memory_type": "message",
            "score": 0.78,
        },
        {
            "id": 2005,
            "role": "user",
            "content": "I prefer concise replies.",
            "timestamp": base_time.isoformat(),
            "memory_type": "message",
            "score": 0.75,
        },
    ]

    memory = {
        "conversations": [],
        "documents": [],
        "preferences": [],
        "messages": messages,
    }

    # =====================================================
    # BEFORE
    # =====================================================

    print("\nBEFORE CONFLICT RESOLUTION")
    print("-" * 60)

    for message in memory["messages"]:

        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    # =====================================================
    # RUN REAL CONFLICT PIPELINE
    # =====================================================

    resolved = engine._resolve_memory_conflicts(
        memory=memory
    )

    # =====================================================
    # AFTER
    # =====================================================

    print("\nAFTER CONFLICT RESOLUTION")
    print("-" * 60)

    for message in resolved["messages"]:

        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    remaining_ids = {
        message["id"]
        for message in resolved["messages"]
    }

    # =====================================================
    # VALIDATE UPDATE CHAIN
    # =====================================================

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert 2001 not in remaining_ids, (
        "Oldest Flask fact survived."
    )

    assert 2002 not in remaining_ids, (
        "Intermediate Django fact survived."
    )

    assert 2003 in remaining_ids, (
        "Newest FastAPI fact was removed."
    )

    print(
        "\nBackend update chain resolved correctly."
    )

    # =====================================================
    # VALIDATE UNRELATED FACTS
    # =====================================================

    assert 2004 in remaining_ids, (
        "Unrelated PostgreSQL fact was removed."
    )

    assert 2005 in remaining_ids, (
        "Unrelated response preference was removed."
    )

    print(
        "PostgreSQL memory preserved."
    )

    print(
        "Concise-reply memory preserved."
    )

    # =====================================================
    # MAKE SURE ONLY EXPECTED MEMORIES REMAIN
    # =====================================================

    expected_ids = {
        2003,
        2004,
        2005,
    }

    assert remaining_ids == expected_ids, (
        "Unexpected memories remained after "
        "conflict resolution."
    )

    print(
        "No unexpected memories survived."
    )

    # =====================================================
    # ORIGINAL MEMORY HISTORY CHECK
    # =====================================================

    original_ids = {
        message["id"]
        for message in messages
    }

    assert original_ids == {
        2001,
        2002,
        2003,
        2004,
        2005,
    }, (
        "Original historical memory was modified."
    )

    print(
        "Original memory history remained unchanged."
    )

    # =====================================================
    # SUCCESS
    # =====================================================

    print(
        "\nCONFLICT REGRESSION TEST PASSED"
    )


if __name__ == "__main__":
    main()