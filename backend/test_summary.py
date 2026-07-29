from database.connection import SessionLocal
from services.conversation_summary_service import ConversationSummaryService

db = SessionLocal()

try:
    service = ConversationSummaryService()

    summary = service.generate_summary(
        db=db,
        conversation_id=2   # Change this if your conversation ID is different
    )

    print("\nGenerated Summary:\n")
    print(summary)

finally:
    db.close()