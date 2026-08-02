from memory.memory_conflict_detector import (
    MemoryConflictDetector,
)

from memory.memory_conflict_confirmer import (
    MemoryConflictConfirmer,
)


def main():

    detector = MemoryConflictDetector()
    confirmer = MemoryConflictConfirmer()

    print("\n" + "=" * 60)
    print("PHASE 27 - CONFLICT CONFIRMATION TEST")
    print("=" * 60)

    messages = [
        {
            "id": 1,
            "role": "user",
            "content":
                "My project backend uses Flask.",
        },
        {
            "id": 2,
            "role": "user",
            "content":
                "My project backend now uses FastAPI.",
        },
        {
            "id": 3,
            "role": "user",
            "content":
                "My project backend handles API requests.",
        },
        {
            "id": 4,
            "role": "user",
            "content":
                "I prefer concise responses.",
        },
    ]

    memory = {
        "messages": messages,
    }

    detected = detector.detect(memory)

    candidates = detected[
        "message_conflicts"
    ]

    print("\nCANDIDATES")
    print("-" * 60)

    for candidate in candidates:

        print(
            candidate["first"]["id"],
            "<->",
            candidate["second"]["id"],
        )

    confirmed = confirmer.confirm(
        candidates
    )

    print("\nCONFIRMED")
    print("-" * 60)

    for conflict in confirmed:

        print(
            conflict["first"]["id"],
            "<->",
            conflict["second"]["id"],
        )

        print(
            conflict["first"]["content"]
        )

        print(
            conflict["second"]["content"]
        )

        print("-" * 60)

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    confirmed_pairs = {
        frozenset(
            {
                conflict["first"]["id"],
                conflict["second"]["id"],
            }
        )
        for conflict in confirmed
    }

    assert frozenset({1, 2}) in confirmed_pairs, (
        "Expected Flask/FastAPI update "
        "was not confirmed."
    )

    assert frozenset({1, 3}) not in confirmed_pairs, (
        "Related but non-conflicting messages "
        "were incorrectly confirmed."
    )

    print(
        "\nExplicit factual update confirmed."
    )

    print(
        "Related non-update memory was not "
        "treated as a confirmed conflict."
    )

    print(
        "\nCONFLICT CONFIRMATION TEST PASSED"
    )


if __name__ == "__main__":
    main()