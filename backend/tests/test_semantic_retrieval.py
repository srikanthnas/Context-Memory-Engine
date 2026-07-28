from retrieval.chroma_vector_store import ChromaVectorStore
from embeddings.embedding_manager import EmbeddingManager

embedding_manager = EmbeddingManager()
store = ChromaVectorStore()

query = "What programming languages are mentioned in my resume?"

query_embedding = embedding_manager.embed_text(query)

results = store.search(
    query_embedding=query_embedding,
    top_k=3,
    where={"user_id": 1},
)

print("\n===== RESULTS =====\n")

print(results["documents"])
print()
print(results["metadatas"])