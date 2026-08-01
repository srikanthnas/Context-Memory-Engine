from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    vector_store = ChromaVectorStore()

    results = vector_store.message_collection.get(
        include=[
            "documents",
            "metadatas",
        ]
    )

    print("\n" + "=" * 60)
    print("MESSAGE METADATA TEST")
    print("=" * 60)

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    print(f"\nTotal messages: {len(metadatas)}")

    print("\nFirst 5 messages:\n")

    for document, metadata in zip(
        documents[:5],
        metadatas[:5],
    ):
        print("Metadata:", metadata)
        print("Text:", document[:150])
        print("-" * 60)


if __name__ == "__main__":
    main()
    