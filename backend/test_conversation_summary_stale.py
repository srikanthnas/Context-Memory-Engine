from database.connection import SessionLocal
from database.models import Conversation, Message
from services.conversation_summary_service import (
    ConversationSummaryService,
)


def main():
    db = SessionLocal()

    try:
        conversation_id = 13

        service = ConversationSummaryService()

        print("\n" + "=" * 60)
        print("PHASE 26 - SUMMARY STALENESS TEST")
        print("=" * 60)

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if conversation is None:
            raise ValueError(
                f"Conversation {conversation_id} not found."
            )

        latest_message = (
            db.query(Message)
            .filter(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                Message.timestamp.desc()
            )
            .first()
        )

        print("\nConversation:")
        print("ID:", conversation.id)
        print("Title:", conversation.title)

        print("\nCurrent summary:")
        print(conversation.summary)

        print("\nSummary updated:")
        print(conversation.summary_updated)

        if latest_message:
            print("\nLatest message:")
            print("ID:", latest_message.id)
            print("Timestamp:", latest_message.timestamp)
            print("Content:", latest_message.content)

        stale = service.is_summary_stale(
            db=db,
            conversation_id=conversation_id,
        )

        print("\n" + "=" * 60)
        print("RESULT")
        print("=" * 60)

        print("\nSummary stale:", stale)

        assert stale is True, (
            "Summary should be stale after a new "
            "message was added."
        )

        if (
            latest_message
            and conversation.summary_updated
        ):
            assert (
                latest_message.timestamp
                > conversation.summary_updated
            ), (
                "Latest message should be newer "
                "than the summary."
            )

        print(
            "\nNew message correctly invalidated "
            "the existing summary."
        )

        print(
            "\nSUMMARY STALENESS TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()