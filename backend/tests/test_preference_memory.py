from database.connection import SessionLocal
from memory.preference_memory import PreferenceMemory


db = SessionLocal()

preferences = PreferenceMemory.get_preferences(db, 1)

print(preferences)

db.close()