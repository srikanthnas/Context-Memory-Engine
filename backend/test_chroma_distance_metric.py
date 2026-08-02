from retrieval.chroma_vector_store import ChromaVectorStore


def main():

    vector_store = ChromaVectorStore()

    collection = vector_store.message_collection

    print("\n" + "=" * 60)
    print("PHASE 27 - CHROMA DISTANCE METRIC CHECK")
    print("=" * 60)

    print("\nCollection:")
    print(collection.name)

    print("\nMetadata:")
    print(collection.metadata)

    print("\nCount:")
    print(collection.count())

    print("\n" + "=" * 60)

    metadata = collection.metadata or {}

    distance_metric = metadata.get(
        "hnsw:space",
        "NOT EXPLICITLY CONFIGURED",
    )

    print("\nConfigured distance metric:")
    print(distance_metric)

    print("\nInterpretation:")

    if distance_metric == "cosine":
        print(
            "Collection explicitly uses cosine distance."
        )

    elif distance_metric == "l2":
        print(
            "Collection explicitly uses L2 distance."
        )

    elif distance_metric == "ip":
        print(
            "Collection explicitly uses inner product."
        )

    else:
        print(
            "No explicit distance metric is stored "
            "in the collection metadata."
        )

    print("\nDISTANCE METRIC CHECK COMPLETE")


if __name__ == "__main__":
    main()
    