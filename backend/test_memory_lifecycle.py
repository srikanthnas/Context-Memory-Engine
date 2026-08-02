from datetime import datetime, timedelta

from memory.memory_lifecycle import MemoryLifecycle


def main():

    print("\n" + "=" * 60)
    print("PHASE 29 - MEMORY LIFECYCLE TEST")
    print("=" * 60)

    lifecycle = MemoryLifecycle()

    now = datetime.utcnow()

    memories = [
        {
            "id": 5001,
            "content": "Recent active memory",
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": now.isoformat(),
        },
        {
            "id": 5002,
            "content": "Older aging memory",
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": (
                now - timedelta(days=20)
            ).isoformat(),
        },
        {
            "id": 5003,
            "content": "Very old dormant memory",
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": (
                now - timedelta(days=100)
            ).isoformat(),
        },
        {
            "id": 5004,
            "content": "Old but frequently accessed memory",
            "importance": 1.0,
            "access_count": 15,
            "last_accessed": (
                now - timedelta(days=20)
            ).isoformat(),
        },
    ]

    classified = (
        lifecycle.classify_memories(
            memories,
            now=now,
        )
    )

    print("\nCLASSIFIED MEMORIES")
    print("-" * 60)

    states = {}

    for memory in classified:

        states[memory["id"]] = (
            memory["lifecycle_state"]
        )

        print(
            f"ID={memory['id']} | "
            f"Strength="
            f"{memory['memory_strength']:.4f} | "
            f"State="
            f"{memory['lifecycle_state']}"
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert states[5001] == "active", (
        "Recent memory should be active."
    )

    assert states[5002] == "aging", (
        "Older memory should be aging."
    )

    assert states[5003] == "dormant", (
        "Very old unused memory should be dormant."
    )

    assert states[5004] == "active", (
        "Frequently accessed memory should remain active."
    )

    assert len(classified) == 4, (
        "Lifecycle classification must not delete memories."
    )

    print("\nRecent memory classified as ACTIVE.")
    print("Older memory classified as AGING.")
    print("Very old memory classified as DORMANT.")
    print("Frequently accessed memory remains ACTIVE.")
    print("No memories were deleted.")

    print("\nMEMORY LIFECYCLE TEST PASSED")


if __name__ == "__main__":
    main()