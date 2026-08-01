from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


def main():
    vector_store = ChromaVectorStore()
    embedding_manager = EmbeddingManager()

    print("\n========================================")
    print("DOCUMENT COLLECTION")
    print("========================================")

    print("Total document chunks:", vector_store.size())

    stored = vector_store.document_collection.get(
        include=["documents", "metadatas"]
    )

    print("\n=== STORED DOCUMENT METADATA ===")

    for document, metadata in zip(
        stored.get("documents", []),
        stored.get("metadatas", []),
    ):
        print("\nMetadata:", metadata)
        print("Text:", document[:200])

    print("\n========================================")
    print("SEARCH TEST")
    print("========================================")

    query = "What programming languages are mentioned in my resume?"

    query_embedding = embedding_manager.embed_text(query)

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
        where={"user_id": 2},
    )

    print("\nSearch results:")
    print(results)


if __name__ == "__main__":
    main()