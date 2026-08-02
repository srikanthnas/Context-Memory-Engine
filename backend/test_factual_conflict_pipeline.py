from memory.memory_engine import MemoryEngine


def main():

    engine = MemoryEngine()

    print("\n" + "=" * 60)
    print("PHASE 27 - FACTUAL CONFLICT PIPELINE TEST")
    print("=" * 60)

    old_message = {
        "id": 1001,
        "role": "user",
        "content": (
            "My project backend uses Flask."
        ),
        "timestamp": "2026-07-01T10:00:00",
    }

    new_message = {
        "id": 1002,
        "role": "user",
        "content": (
            "My project backend now uses FastAPI."
        ),
        "timestamp": "2026-08-01T10:00:00",
    }

    related_message = {
        "id": 1003,
        "role": "user",
        "content": (
            "My project backend handles API requests."
        ),
        "timestamp": "2026-08-01T11:00:00",
    }

    unrelated_message = {
        "id": 1004,
        "role": "user",
        "content": (
            "I prefer concise responses."
        ),
        "timestamp": "2026-08-01T12:00:00",
    }

    memory = {
        "conversations": [],
        "documents": [],
        "preferences": [],
        "messages": [
            old_message,
            new_message,
            related_message,
            unrelated_message,
        ],
    }

    print("\nBEFORE")
    print("-" * 60)

    for message in memory["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    resolved = (
        engine._resolve_memory_conflicts(
            memory=memory,
        )
    )

    print("\nAFTER")
    print("-" * 60)

    for message in resolved["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    remaining_ids = {
        message["id"]
        for message in resolved["messages"]
    }

    # Old Flask fact should be superseded.
    assert 1001 not in remaining_ids, (
        "Older Flask memory survived "
        "factual conflict resolution."
    )

    # New FastAPI fact must remain.
    assert 1002 in remaining_ids, (
        "Newer FastAPI memory was removed."
    )

    # Related but non-conflicting information
    # must remain.
    assert 1003 in remaining_ids, (
        "Related non-conflicting memory "
        "was incorrectly removed."
    )

    # Completely unrelated memory must remain.
    assert 1004 in remaining_ids, (
        "Unrelated memory was incorrectly removed."
    )

    # Original input must remain untouched.
    original_ids = {
        message["id"]
        for message in memory["messages"]
    }

    assert original_ids == {
        1001,
        1002,
        1003,
        1004,
    }, (
        "Original historical memory was modified."
    )

    print(
        "\nOld factual memory removed "
        "from active context."
    )

    print(
        "New factual memory preserved."
    )

    print(
        "Related information preserved."
    )

    print(
        "Unrelated information preserved."
    )

    print(
        "Historical memory remained unchanged."
    )

    print(
        "\nFACTUAL CONFLICT PIPELINE TEST PASSED"
    )


if __name__ == "__main__":
    main()