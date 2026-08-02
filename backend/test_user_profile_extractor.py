from memory.user_profile_extractor import (
    UserProfileExtractor,
)


def main():

    print("\n" + "=" * 60)
    print("PHASE 32.1 - USER PROFILE EXTRACTOR TEST")
    print("=" * 60)

    extractor = UserProfileExtractor()

    # ==================================================
    # TEST 1 — NAME
    # ==================================================

    result = extractor.extract(
        "My name is Alex."
    )

    print("\nNAME")
    print(result)

    assert any(
        item["key"] == "name"
        and item["value"] == "Alex"
        for item in result
    )

    # ==================================================
    # TEST 2 — LOCATION
    # ==================================================

    result = extractor.extract(
        "I live in Bengaluru."
    )

    print("\nLOCATION")
    print(result)

    assert any(
        item["key"] == "location"
        and item["value"] == "Bengaluru"
        for item in result
    )

    # ==================================================
    # TEST 3 — OCCUPATION
    # ==================================================

    result = extractor.extract(
        "I am an engineering student."
    )

    print("\nOCCUPATION")
    print(result)

    assert any(
        item["key"] == "occupation"
        and item["value"]
        == "engineering student"
        for item in result
    )

    # ==================================================
    # TEST 4 — GENERAL PREFERENCE
    # ==================================================

    result = extractor.extract(
        "I prefer concise responses."
    )

    print("\nPREFERENCE")
    print(result)

    assert any(
        item["key"] == "preference"
        and item["value"]
        == "concise responses"
        for item in result
    )

    # ==================================================
    # TEST 5 — NON-PROFILE MESSAGE
    # ==================================================

    result = extractor.extract(
        "Explain binary search to me."
    )

    print("\nNON-PROFILE MESSAGE")
    print(result)

    assert result == []

    # ==================================================
    # VALIDATION
    # ==================================================

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    print("\nName extraction passed.")
    print("Location extraction passed.")
    print("Occupation extraction passed.")
    print("Preference extraction passed.")
    print("Non-profile message ignored.")

    print(
        "\nUSER PROFILE EXTRACTOR TEST PASSED"
    )


if __name__ == "__main__":
    main()