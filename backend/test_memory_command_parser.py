from memory.memory_command_parser import (
    MemoryCommandParser,
)


def main():

    print("\n" + "=" * 60)
    print("PHASE 33.1 - MEMORY COMMAND PARSER TEST")
    print("=" * 60)

    parser = MemoryCommandParser()

    # ==============================================
    # TEST 1 — REMEMBER
    # ==============================================

    result = parser.parse(
        "Remember that my preferred IDE is VS Code."
    )

    print("\nREMEMBER")
    print(result)

    assert result == {
        "action": "remember",
        "key": "preferred_ide",
        "value": "VS Code",
    }

    # ==============================================
    # TEST 2 — REMEMBER ALTERNATE FORM
    # ==============================================

    result = parser.parse(
        "Remember my favorite language is Python."
    )

    print("\nREMEMBER ALTERNATE")
    print(result)

    assert result == {
        "action": "remember",
        "key": "favorite_language",
        "value": "Python",
    }

    # ==============================================
    # TEST 3 — FORGET
    # ==============================================

    result = parser.parse(
        "Forget my preferred IDE."
    )

    print("\nFORGET")
    print(result)

    assert result == {
        "action": "forget",
        "key": "preferred_ide",
    }

    # ==============================================
    # TEST 4 — NORMAL MESSAGE
    # ==============================================

    result = parser.parse(
        "Explain inheritance in Java."
    )

    print("\nNORMAL MESSAGE")
    print(result)

    assert result is None

    # ==============================================
    # VALIDATION
    # ==============================================

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    print("\nRemember command detected.")
    print("Memory key normalized.")
    print("Memory value preserved.")
    print("Forget command detected.")
    print("Normal prompt ignored.")

    print(
        "\nMEMORY COMMAND PARSER TEST PASSED"
    )


if __name__ == "__main__":
    main()