from memory.factual_conflict_resolver import (
    FactualConflictResolver,
)


def main():

    resolver = FactualConflictResolver()

    print("\n" + "=" * 60)
    print("PHASE 27 - FACTUAL CONFLICT RESOLUTION TEST")
    print("=" * 60)

    old_message = {
        "id": 101,
        "role": "user",
        "content": "My project backend uses Flask.",
        "timestamp": "2026-07-01T10:00:00",
    }

    new_message = {
        "id": 102,
        "role": "user",
        "content": (
            "My project backend now uses FastAPI."
        ),
        "timestamp": "2026-08-01T10:00:00",
    }

    unrelated_message = {
        "id": 103,
        "role": "user",
        "content": "I prefer concise responses.",
        "timestamp": "2026-08-01T11:00:00",
    }

    messages = [
        old_message,
        new_message,
        unrelated_message,
    ]

    confirmed_conflicts = [
        {
            "first": old_message,
            "second": new_message,
        }
    ]

    print("\nBEFORE")
    print("-" * 60)

    for message in messages:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    resolved = resolver.resolve(
        messages=messages,
        confirmed_conflicts=confirmed_conflicts,
    )

    print("\nAFTER")
    print("-" * 60)

    for message in resolved:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    remaining_ids = {
        message["id"]
        for message in resolved
    }

    assert 101 not in remaining_ids, (
        "Older conflicting memory survived."
    )

    assert 102 in remaining_ids, (
        "Newer conflicting memory was removed."
    )

    assert 103 in remaining_ids, (
        "Unrelated memory was incorrectly removed."
    )

    # Original history must remain untouched.
    assert len(messages) == 3, (
        "Original message history was modified."
    )

    print(
        "\nOlder conflicting memory removed "
        "from active context."
    )

    print(
        "Newer factual memory preserved."
    )

    print(
        "Unrelated memory preserved."
    )

    print(
        "Original history remains unchanged."
    )

    print(
        "\nFACTUAL CONFLICT RESOLUTION TEST PASSED"
    )


if __name__ == "__main__":
    main()