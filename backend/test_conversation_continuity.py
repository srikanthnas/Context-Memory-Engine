from database.connection import SessionLocal
from database.models import Conversation, Message
from schemas.conversation import ConversationCreate
from schemas.message import MessageCreate
from services.conversation_service import ConversationService
from services.message_service import MessageService


def main():
    db = SessionLocal()

    try:
        conversation_service = ConversationService()

        user_id = 2

        # Semantically equivalent to the existing
        # programming-skills conversation.
        new_prompt = (
            "Tell me about the coding abilities "
            "shown in my resume."
        )

        print("\n" + "=" * 60)
        print("PHASE 26 - CONVERSATION CONTINUITY TEST")
        print("=" * 60)

        # -------------------------------------------------
        # Find/create conversation
        # -------------------------------------------------

        request = ConversationCreate(
            user_id=user_id,
            title=new_prompt,
        )

        conversation = (
            conversation_service.create_conversation(
                db=db,
                conversation=request,
            )
        )

        print("\nConversation selected:")
        print("ID:", conversation.id)
        print("Title:", conversation.title)

        # -------------------------------------------------
        # Count messages before
        # -------------------------------------------------

        before_count = (
            db.query(Message)
            .filter(
                Message.conversation_id
                == conversation.id
            )
            .count()
        )

        print(
            "\nMessages before:",
            before_count,
        )

        # -------------------------------------------------
        # Store new message
        # -------------------------------------------------

        message_request = MessageCreate(
            conversation_id=conversation.id,
            role="user",
            content=new_prompt,
        )

        new_message = MessageService.create_message(
            db=db,
            message=message_request,
        )

        # -------------------------------------------------
        # Count messages after
        # -------------------------------------------------

        after_count = (
            db.query(Message)
            .filter(
                Message.conversation_id
                == conversation.id
            )
            .count()
        )

        print(
            "Messages after:",
            after_count,
        )

        print("\nStored message:")
        print("ID:", new_message.id)
        print(
            "Conversation ID:",
            new_message.conversation_id,
        )
        print("Content:", new_message.content)

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)

        assert (
            new_message.conversation_id
            == conversation.id
        ), (
            "Message was attached to the wrong "
            "conversation."
        )

        assert after_count == before_count + 1, (
            "Message count did not increase correctly."
        )

        # We expect semantic consolidation to reuse
        # the existing programming-skills conversation,
        # not create a conversation with new_prompt.
        newly_created = (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id,
                Conversation.title == new_prompt,
            )
            .first()
        )

        assert newly_created is None, (
            "A duplicate conversation was created "
            "instead of reusing the existing one."
        )

        print(
            "\nExisting conversation reused."
        )

        print(
            "New message attached successfully."
        )

        print(
            "No duplicate conversation created."
        )

        print(
            "\nCONVERSATION CONTINUITY TEST PASSED"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()