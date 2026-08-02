from embeddings.embedding_manager import EmbeddingManager


def main():
    embedding_manager = EmbeddingManager()

    text1 = "Explain my programming skills from my resume."
    text2 = "What coding skills do I have according to my resume?"

    embedding1 = embedding_manager.embed_text(text1)
    embedding2 = embedding_manager.embed_text(text2)

    similarity = embedding_manager.model.similarity(
        embedding1,
        embedding2,
    )

    similarity_score = float(similarity[0][0])

    print("\n" + "=" * 60)
    print("PHASE 26 - SEMANTIC SIMILARITY TEST")
    print("=" * 60)

    print("\nText 1:")
    print(text1)

    print("\nText 2:")
    print(text2)

    print("\nSimilarity:")
    print(round(similarity_score, 4))

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()