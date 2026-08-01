import sqlite3


DB_PATH = "context_memory.db"


def get_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def add_column_if_missing(
    cursor,
    table_name,
    column_name,
    definition,
):
    columns = get_columns(cursor, table_name)

    if column_name in columns:
        print(
            f"SKIPPED: {table_name}.{column_name} "
            f"already exists"
        )
        return

    cursor.execute(
        f"""
        ALTER TABLE {table_name}
        ADD COLUMN {column_name} {definition}
        """
    )

    print(
        f"ADDED: {table_name}.{column_name}"
    )


def main():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        tables = [
            "conversations",
            "messages",
            "preferences",
        ]

        for table in tables:

            print(f"\nMigrating {table}...")

            add_column_if_missing(
                cursor,
                table,
                "last_accessed",
                "DATETIME",
            )

            add_column_if_missing(
                cursor,
                table,
                "access_count",
                "INTEGER NOT NULL DEFAULT 0",
            )

            add_column_if_missing(
                cursor,
                table,
                "importance",
                "FLOAT NOT NULL DEFAULT 1.0",
            )

        # Populate last_accessed for existing rows.
        #
        # SQLite cannot use a dynamic CURRENT_TIMESTAMP
        # default through ALTER TABLE in every situation,
        # so existing rows are initialized here.

        cursor.execute(
            """
            UPDATE conversations
            SET last_accessed = COALESCE(
                last_accessed,
                created_at,
                CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            UPDATE messages
            SET last_accessed = COALESCE(
                last_accessed,
                timestamp,
                CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            UPDATE preferences
            SET last_accessed = COALESCE(
                last_accessed,
                CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

        print("\n================================")
        print("MIGRATION COMPLETE")
        print("================================")

        # Verify resulting schema
        for table in tables:

            columns = get_columns(
                cursor,
                table,
            )

            print(
                f"{table}:",
                sorted(columns),
            )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
    