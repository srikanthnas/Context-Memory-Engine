from memory.memory_conflict_detector import (
    MemoryConflictDetector,
)


def main():

    detector = MemoryConflictDetector()

    print("\n" + "=" * 60)
    print("PHASE 27 - FACT CONFLICT DETECTION TEST")
    print("=" * 60)

    messages = [
        {
            "id": 1,
            "role": "user",
            "content": (
                "My project backend uses Flask."
            ),
        },
        {
            "id": 2,
            "role": "user",
            "content": (
                "My project backend now uses FastAPI."
            ),
        },
        {
            "id": 3,
            "role": "user",
            "content": (
                "I prefer concise responses."
            ),
        },
    ]

    memory = {
        "messages": messages,
    }

    result = detector.detect(memory)

    conflicts = result["message_conflicts"]

    print("\nDETECTED CONFLICTS")
    print("-" * 60)

    for conflict in conflicts:

        print("\nFirst:")
        print(
            conflict["first"]["content"]
        )

        print("Second:")
        print(
            conflict["second"]["content"]
        )

        print(
            "Shared terms:",
            conflict["shared_terms"],
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert len(conflicts) >= 1, (
        "Expected factual conflict was not detected."
    )

    expected_found = False

    for conflict in conflicts:

        ids = {
            conflict["first"]["id"],
            conflict["second"]["id"],
        }

        if ids == {1, 2}:
            expected_found = True
            break

    assert expected_found, (
        "Flask/FastAPI conflict was not detected."
    )

    print(
        "\nPotential factual conflict detected."
    )

    print(
        "Unrelated memory was not required "
        "for the conflict."
    )

    print(
        "\nFACT CONFLICT DETECTION TEST PASSED"
    )


if __name__ == "__main__":
    main()