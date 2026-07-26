from database.connection import SessionLocal
from database.models import Document

db = SessionLocal()

print("\n===== ALL DOCUMENTS =====\n")

documents = db.query(Document).all()

for doc in documents:
    print(
        f"id={doc.id}, "
        f"user_id={doc.user_id}, "
        f"filename={doc.filename}, "
        f"filepath={doc.filepath}"
    )

db.close()