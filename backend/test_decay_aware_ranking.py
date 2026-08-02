from datetime import datetime, timedelta

from memory.context_optimizer import ContextOptimizer


def main():

    print("\n" + "=" * 60)
    print("PHASE 28 - DECAY AWARE RANKING TEST")
    print("=" * 60)

    optimizer = ContextOptimizer()

    now = datetime.utcnow()

    messages = [
        {
            "id": 3001,
            "role": "user",
            "content": "Very old unused memory",
            "similarity": 0.80,
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": (
                now - timedelta(days=100)
            ).isoformat(),
        },
        {
            "id": 3002,
            "role": "user",
            "content": "Recent relevant memory",
            "similarity": 0.80,
            "importance": 1.0,
            "access_count": 0,
            "last_accessed": now.isoformat(),
        },
        {
            "id": 3003,
            "role": "user",
            "content": "Older frequently used memory",
            "similarity": 0.80,
            "importance": 1.0,
            "access_count": 15,
            "last_accessed": (
                now - timedelta(days=30)
            ).isoformat(),
        },
    ]

    print("\nINPUT MEMORIES")
    print("-" * 60)

    for message in messages:
        print(
            f"ID={message['id']} | "
            f"{message['content']}"
        )

    optimized = optimizer.optimize(
        conversations=[],
        messages=messages,
        preferences=[],
        documents=[],
    )

    optimized_messages = (
        optimized["messages"]
    )

    print("\nRANKED MEMORY SCORES")
    print("-" * 60)

    score_map = {}

    for message in optimized_messages:

        score_map[message["id"]] = (
            message["ranking_score"]
        )

        print(
            f"ID={message['id']} | "
            f"Strength="
            f"{message['memory_strength']:.4f} | "
            f"Ranking="
            f"{message['ranking_score']:.4f}"
        )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert (
        score_map[3002]
        > score_map[3001]
    ), (
        "Recent memory did not outrank "
        "old unused memory."
    )

    assert (
        score_map[3003]
        > score_map[3001]
    ), (
        "Frequently accessed memory did not "
        "resist decay."
    )

    print(
        "\nRecent memory outranks old unused memory."
    )

    print(
        "Frequently accessed memory resists decay."
    )

    print(
        "\nDECAY AWARE RANKING TEST PASSED"
    )


if __name__ == "__main__":
    main()