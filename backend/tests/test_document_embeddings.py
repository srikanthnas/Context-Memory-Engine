from embeddings.embedding_manager import EmbeddingManager

manager = EmbeddingManager()

chunks = [
    "Python is a programming language.",
    "Machine learning uses data.",
    "FastAPI is used for backend APIs."
]

embedded_chunks = manager.embed_document_chunks(chunks)

for i, chunk in enumerate(embedded_chunks):
    print(f"\nChunk {i+1}")

    print("Text:")
    print(chunk["text"])

    print("Embedding Dimension:")
    print(len(chunk["embedding"]))