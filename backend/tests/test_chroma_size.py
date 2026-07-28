from retrieval.chroma_vector_store import ChromaVectorStore

store = ChromaVectorStore()

print("Total vectors:", store.size())