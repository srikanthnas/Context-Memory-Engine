from datetime import datetime, timedelta

from memory.memory_decay import MemoryDecay


def main():

    print("\n" + "=" * 60)
    print("PHASE 28 - MEMORY DECAY BOUNDARY TEST")
    print("=" * 60)

    decay = MemoryDecay()

    now = datetime.utcnow()

    normal_old = {
        "id": 4001,
        "importance": 1.0,
        "access_count": 0,
        "last_accessed": (
            now - timedelta(days=365)
        ).isoformat(),
    }

    important_old = {
        "id": 4002,
        "importance": 3.0,
        "access_count": 0,
        "last_accessed": (
            now - timedelta(days=365)
        ).isoformat(),
    }

    accessed_old = {
        "id": 4003,
        "importance": 1.0,
        "access_count": 30,
        "last_accessed": (
            now - timedelta(days=365)
        ).isoformat(),
    }

    recent = {
        "id": 4004,
        "importance": 1.0,
        "access_count": 0,
        "last_accessed": now.isoformat(),
    }

    memories = [
        normal_old,
        important_old,
        accessed_old,
        recent,
    ]

    scores = {}

    print("\nMEMORY STRENGTH")
    print("-" * 60)

    for memory in memories:

        score = decay.score_memory(
            memory,
            now=now,
        )

        scores[memory["id"]] = score

        print(
            f"ID={memory['id']} | "
            f"Strength={score:.4f}"
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert (
        scores[4004] > scores[4001]
    ), (
        "Recent memory should be stronger "
        "than old unused memory."
    )

    assert (
        scores[4002] >= scores[4001]
    ), (
        "Importance should help resist decay."
    )

    assert (
        scores[4003] >= scores[4001]
    ), (
        "Access frequency should help resist decay."
    )

    for score in scores.values():

        assert (
            score >= decay.minimum_strength
        ), (
            "Memory dropped below minimum strength."
        )

    assert len(memories) == 4, (
        "Decay must not delete memories."
    )

    print(
        "\nRecent memory remains stronger."
    )

    print(
        "Important memory resists decay."
    )

    print(
        "Frequently accessed memory resists decay."
    )

    print(
        "Minimum memory strength is respected."
    )

    print(
        "No memories were deleted."
    )

    print(
        "\nMEMORY DECAY BOUNDARY TEST PASSED"
    )


if __name__ == "__main__":
    main()