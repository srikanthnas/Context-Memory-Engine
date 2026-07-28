from embeddings.embedding_manager import EmbeddingManager
from backend.retrieval.vector_store_faiss import VectorStore


manager = EmbeddingManager()

store = VectorStore()


documents = [
    "Python is a programming language.",
    "FastAPI is used to build APIs.",
    "Machine learning uses data.",
    "Artificial intelligence is changing software.",
    "Football is a popular sport."
]


embeddings = manager.embed_chunks(documents)

store.add_embeddings(embeddings)

print("Vectors stored:", store.size())


query = "How do I create an API?"

query_embedding = manager.embed_text(query)

distances, indices = store.search(query_embedding, top_k=3)

print("\nTop Results")

for rank, idx in enumerate(indices):
    print(f"{rank+1}. {documents[idx]}")
