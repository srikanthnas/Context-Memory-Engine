from datetime import datetime, timedelta

from memory.memory_decay import MemoryDecay


def main():

    print("\n" + "=" * 60)
    print("PHASE 28 - MEMORY DECAY TEST")
    print("=" * 60)

    decay = MemoryDecay()

    now = datetime.utcnow()

    recent_memory = {
        "importance": 1.0,
        "access_count": 0,
        "last_accessed": now,
    }

    old_memory = {
        "importance": 1.0,
        "access_count": 0,
        "last_accessed": (
            now - timedelta(days=30)
        ),
    }

    frequently_used_memory = {
        "importance": 1.0,
        "access_count": 10,
        "last_accessed": (
            now - timedelta(days=30)
        ),
    }

    recent_score = decay.score_memory(
        recent_memory,
        now=now,
    )

    old_score = decay.score_memory(
        old_memory,
        now=now,
    )

    frequent_score = decay.score_memory(
        frequently_used_memory,
        now=now,
    )

    print("\nRECENT MEMORY")
    print("-" * 60)
    print(f"Strength: {recent_score:.4f}")

    print("\nOLD MEMORY")
    print("-" * 60)
    print(f"Strength: {old_score:.4f}")

    print("\nOLD BUT FREQUENTLY USED MEMORY")
    print("-" * 60)
    print(f"Strength: {frequent_score:.4f}")

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert recent_score > old_score, (
        "Old memory did not decay."
    )

    assert frequent_score > old_score, (
        "Access frequency did not strengthen memory."
    )

    assert old_score > 0, (
        "Memory strength reached zero."
    )

    print("\nRecent memory is stronger than old memory.")
    print("Frequently accessed memory resists decay.")
    print("Memory strength remains above zero.")

    print("\nMEMORY DECAY TEST PASSED")


if __name__ == "__main__":
    main()