from sqlalchemy import inspect

from database.base import Base
from database.connection import engine

# Important:
# Import models so SQLAlchemy registers all models
# with Base.metadata.
from database.models import ImageMemory


def main():

    print("\n" + "=" * 60)
    print("PHASE 31 - IMAGE MEMORY TABLE CREATION")
    print("=" * 60)

    inspector = inspect(engine)

    tables_before = inspector.get_table_names()

    print("\nTables before:")
    for table in tables_before:
        print("-", table)

    # --------------------------------------------------
    # CREATE MISSING TABLES ONLY
    # --------------------------------------------------

    Base.metadata.create_all(
        bind=engine
    )

    # Refresh inspector after table creation.
    inspector = inspect(engine)

    tables_after = inspector.get_table_names()

    print("\nTables after:")
    for table in tables_after:
        print("-", table)

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    assert "image_memories" in tables_after, (
        "image_memories table was not created."
    )

    print("\nimage_memories table exists.")

    # Existing important tables must still exist.

    expected_existing_tables = {
        "users",
        "conversations",
        "messages",
        "documents",
        "preferences",
    }

    missing_tables = (
        expected_existing_tables
        - set(tables_after)
    )

    assert not missing_tables, (
        f"Existing tables missing: {missing_tables}"
    )

    print(
        "Existing memory tables preserved."
    )

    print(
        "\nIMAGE MEMORY TABLE CREATION PASSED"
    )


if __name__ == "__main__":
    main()