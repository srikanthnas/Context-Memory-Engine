from database.connection import SessionLocal
from database.models import Conversation
from services.conversation_summary_service import (
    ConversationSummaryService,
)


def main():
    db = SessionLocal()

    try:
        conversation_id = 13

        service = ConversationSummaryService()

        print("\n" + "=" * 60)
        print("PHASE 26 - SUMMARY GENERATION TEST")
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

        print("\nBEFORE")
        print("-" * 60)

        print("Conversation ID:", conversation.id)
        print("Title:", conversation.title)
        print("Summary:", conversation.summary)
        print(
            "Summary Updated:",
            conversation.summary_updated,
        )

        # -------------------------------------------------
        # Generate / refresh summary
        # -------------------------------------------------

        summary = service.get_or_refresh_summary(
            db=db,
            conversation_id=conversation_id,
        )

        # Reload from SQLite
        db.refresh(conversation)

        print("\nAFTER")
        print("-" * 60)

        print("Summary:")
        print(conversation.summary)

        print(
            "\nSummary Updated:",
            conversation.summary_updated,
        )

        # -------------------------------------------------
        # Validate SQLite
        # -------------------------------------------------

        assert conversation.summary, (
            "Summary was not stored in SQLite."
        )

        assert conversation.summary_updated is not None, (
            "summary_updated was not set."
        )

        assert summary == conversation.summary, (
            "Returned summary does not match "
            "the stored summary."
        )

        # -------------------------------------------------
        # Validate summary freshness
        # -------------------------------------------------

        stale = service.is_summary_stale(
            db=db,
            conversation_id=conversation_id,
        )

        print("\nSummary stale after generation:", stale)

        assert stale is False, (
            "Summary should be fresh immediately "
            "after generation."
        )

        # -------------------------------------------------
        # Validate Chroma
        # -------------------------------------------------

        result = (
            service.vector_store
            .conversation_collection
            .get(
                ids=[
                    f"conversation_{conversation_id}"
                ],
                include=[
                    "documents",
                    "metadatas",
                ],
            )
        )

        print("\nCHROMA")
        print("-" * 60)

        print("IDs:", result["ids"])

        if result["documents"]:
            print(
                "Stored text:",
                result["documents"][0],
            )

        assert result["ids"], (
            "Conversation embedding was not found "
            "in ChromaDB."
        )

        stored_text = result["documents"][0]

        assert conversation.summary in stored_text, (
            "Updated summary was not written "
            "into the Chroma conversation memory."
        )

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        print("Summary generated successfully.")
        print("Summary stored in SQLite.")
        print("Summary marked fresh.")
        print("Chroma conversation embedding updated.")

        print(
            "\nSUMMARY GENERATION TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()