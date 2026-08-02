from memory.memory_engine import MemoryEngine


def main():

    print("\n" + "=" * 60)
    print("PHASE 29 - CONSOLIDATION INTEGRATION TEST")
    print("=" * 60)

    engine = MemoryEngine()

    memory = {
        "conversations": [],
        "preferences": [],
        "documents": [],
        "messages": [
            {
                "id": 7001,
                "role": "user",
                "content": "My project uses FastAPI.",
                "importance": 1.0,
                "access_count": 0,
                "last_accessed": "2026-01-01T10:00:00",
            },
            {
                "id": 7002,
                "role": "user",
                "content": "  my PROJECT uses FastAPI.  ",
                "importance": 2.0,
                "access_count": 5,
                "last_accessed": "2026-08-01T10:00:00",
            },
            {
                "id": 7003,
                "role": "user",
                "content": "My database uses PostgreSQL.",
                "importance": 1.0,
                "access_count": 0,
                "last_accessed": "2026-08-01T10:00:00",
            },
        ],
    }

    print("\nBEFORE")
    print("-" * 60)

    for message in memory["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    consolidated = engine._consolidate_memory(
        memory=memory
    )

    print("\nAFTER")
    print("-" * 60)

    for message in consolidated["messages"]:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    ids = {
        message["id"]
        for message in consolidated["messages"]
    }

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert len(memory["messages"]) == 3, (
        "Original memory history was modified."
    )

    assert len(
        consolidated["messages"]
    ) == 2, (
        "Duplicate active memories were not consolidated."
    )

    assert 7002 in ids, (
        "Stronger duplicate was not preserved."
    )

    assert 7001 not in ids, (
        "Weaker duplicate survived."
    )

    assert 7003 in ids, (
        "Unrelated memory was removed."
    )

    print("\nConsolidator integrated successfully.")
    print("Stronger duplicate preserved.")
    print("Unrelated memory preserved.")
    print("Original memory remained unchanged.")

    print(
        "\nCONSOLIDATION INTEGRATION TEST PASSED"
    )


if __name__ == "__main__":
    main()