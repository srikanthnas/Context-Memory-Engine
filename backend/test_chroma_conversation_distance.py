from embeddings.embedding_manager import EmbeddingManager
from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    embedding_manager = EmbeddingManager()
    vector_store = ChromaVectorStore()

    query = "What coding skills do I have according to my resume?"

    print("\n" + "=" * 60)
    print("PHASE 26 - CHROMA DISTANCE DEBUG")
    print("=" * 60)

    print("\nQuery:")
    print(query)

    query_embedding = embedding_manager.embed_text(query)

    results = vector_store.search_conversations(
        query_embedding=query_embedding,
        top_k=10,
        where={"user_id": 2},
    )

    print("\nRAW RESULTS")
    print("=" * 60)

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for index, (
        chroma_id,
        document,
        metadata,
        distance,
    ) in enumerate(
        zip(
            ids,
            documents,
            metadatas,
            distances,
        ),
        start=1,
    ):

        print(f"\nRESULT {index}")
        print("-" * 60)

        print("Chroma ID:", chroma_id)
        print(
            "Conversation ID:",
            metadata.get("conversation_id"),
        )

        print("Distance:", distance)
        print("1 - Distance:", 1 - distance)

        print("\nStored text:")
        print(document)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()