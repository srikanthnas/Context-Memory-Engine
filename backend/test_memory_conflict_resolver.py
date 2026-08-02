from memory.memory_conflict_resolver import (
    MemoryConflictResolver,
)


def main():

    resolver = MemoryConflictResolver()

    print("\n" + "=" * 60)
    print("PHASE 27 - MEMORY CONFLICT RESOLUTION TEST")
    print("=" * 60)

    memory = {
        "conversations": [],
        "messages": [],
        "documents": [],
        "preferences": [
            {
                "id": 1,
                "key": "response_style",
                "value": "detailed",
                "last_accessed": "2026-07-20T10:00:00",
            },
            {
                "id": 2,
                "key": "response_style",
                "value": "concise",
                "last_accessed": "2026-08-01T16:42:33",
            },
            {
                "id": 3,
                "key": "language",
                "value": "English",
                "last_accessed": "2026-08-01T12:00:00",
            },
        ],
    }

    resolved = resolver.resolve(memory)

    preferences = resolved["preferences"]

    print("\nBEFORE")
    print("-" * 60)

    for preference in memory["preferences"]:
        print(
            preference["key"],
            "=",
            preference["value"],
        )

    print("\nAFTER")
    print("-" * 60)

    for preference in preferences:
        print(
            preference["key"],
            "=",
            preference["value"],
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    response_styles = [
        preference
        for preference in preferences
        if preference["key"] == "response_style"
    ]

    assert len(response_styles) == 1, (
        "Conflicting preference was not resolved."
    )

    assert (
        response_styles[0]["value"]
        == "concise"
    ), (
        "Newest preference was not selected."
    )

    language_preferences = [
        preference
        for preference in preferences
        if preference["key"] == "language"
    ]

    assert len(language_preferences) == 1

    assert (
        language_preferences[0]["value"]
        == "English"
    )

    print(
        "\nNewest conflicting preference selected."
    )

    print(
        "Unrelated preference preserved."
    )

    print(
        "\nMEMORY CONFLICT RESOLUTION TEST PASSED"
    )


if __name__ == "__main__":
    main()