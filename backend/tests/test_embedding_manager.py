from embeddings.embedding_manager import EmbeddingManager

manager = EmbeddingManager()

print("Loading model...")

embedding = manager.embed_text("Hello World")

print("\n===== EMBEDDING INFO =====")

print("Type:", type(embedding))
print("Dimensions:", len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])