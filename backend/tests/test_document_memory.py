from database.connection import SessionLocal
from memory.document_memory import DocumentMemory

db = SessionLocal()

documents = DocumentMemory.get_documents(
    db=db,
    user_id=1,
)

print("\n===== DOCUMENT MEMORY =====\n")

for document in documents:
    print(document)

db.close()