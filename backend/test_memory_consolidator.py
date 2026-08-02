from datetime import datetime, timedelta

from memory.memory_consolidator import MemoryConsolidator


def main():

    print("\n" + "=" * 60)
    print("PHASE 29 - MEMORY CONSOLIDATION TEST")
    print("=" * 60)

    consolidator = MemoryConsolidator()

    now = datetime.utcnow()

    memories = [
        {
            "id": 6001,
            "content": "My project uses FastAPI.",
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": (
                now - timedelta(days=30)
            ).isoformat(),
        },
        {
            "id": 6002,
            "content": "  my PROJECT uses FastAPI.  ",
            "importance": 1.0,
            "access_count": 5,
            "last_accessed": now.isoformat(),
        },
        {
            "id": 6003,
            "content": "My project database uses PostgreSQL.",
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": now.isoformat(),
        },
    ]

    print("\nBEFORE CONSOLIDATION")
    print("-" * 60)

    for memory in memories:
        print(
            f"ID={memory['id']} | "
            f"{memory['content']}"
        )

    consolidated = consolidator.consolidate(
        memories=memories,
        now=now,
    )

    print("\nAFTER CONSOLIDATION")
    print("-" * 60)

    for memory in consolidated:
        print(
            f"ID={memory['id']} | "
            f"State={memory['lifecycle_state']} | "
            f"Strength={memory['memory_strength']:.4f} | "
            f"{memory['content']}"
        )

    ids = {
        memory["id"]
        for memory in consolidated
    }

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert len(memories) == 3, (
        "Original memory history was modified."
    )

    assert len(consolidated) == 2, (
        "Duplicate memories were not consolidated."
    )

    assert 6002 in ids, (
        "Stronger duplicate memory was not preserved."
    )

    assert 6001 not in ids, (
        "Weaker duplicate survived consolidation."
    )

    assert 6003 in ids, (
        "Unrelated memory was incorrectly removed."
    )

    print("\nDuplicate memory consolidated.")
    print("Stronger duplicate preserved.")
    print("Unrelated memory preserved.")
    print("Historical input remained unchanged.")

    print(
        "\nMEMORY CONSOLIDATION TEST PASSED"
    )


if __name__ == "__main__":
    main()