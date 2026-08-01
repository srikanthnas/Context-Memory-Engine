from database.connection import SessionLocal
from services.conversation_summary_service import ConversationSummaryService


def main():
    db = SessionLocal()

    try:
        service = ConversationSummaryService()

        conversation_id = 2

        # Check whether the current summary is stale
        stale = service.is_summary_stale(
            db=db,
            conversation_id=conversation_id,
        )

        print("\nSummary stale:", stale)

        # Generate a new summary only when necessary
        summary = service.get_or_refresh_summary(
            db=db,
            conversation_id=conversation_id,
        )

        print("\nGenerated / Retrieved Summary:\n")
        print(summary)

        # Check again after refresh
        stale_after = service.is_summary_stale(
            db=db,
            conversation_id=conversation_id,
        )

        print("\nSummary stale after retrieval:", stale_after)

    finally:
        db.close()


if __name__ == "__main__":
    main()