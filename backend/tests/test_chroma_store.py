from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore

manager = EmbeddingManager()
store = ChromaVectorStore()

documents = [
    "Python is a programming language.",
    "FastAPI is used to build APIs.",
    "Machine learning uses data.",
    "Artificial intelligence is changing software.",
    "Football is a popular sport."
]

embedded = manager.embed_document_chunks(
    documents,
    document_id=1,
    filename="resume.pdf"
)
store.add_documents(embedded)

print("Stored:", store.size())

query = "How can I build a REST API?"

query_embedding = manager.embed_text(query)

results = store.search(query_embedding)

print("\nTop Matches:\n")

for doc, metadata in zip(
    results["documents"][0],
    results["metadatas"][0]
):
    print("Document:")
    print(doc)

    print("Metadata:")
    print(metadata)

    print("-" * 40)