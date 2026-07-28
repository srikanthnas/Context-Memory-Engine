import faiss
import numpy as np


class VectorStore:
    """
    Stores document embeddings using FAISS and performs
    nearest-neighbour similarity search.
    """

    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):
        """
        Add embeddings to the FAISS index.

        embeddings:
            numpy array of shape (n, dimension)
        """

        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=3):
        """
        Search for the nearest embeddings.
        """

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        return distances[0], indices[0]

    def size(self):
        """
        Number of vectors currently stored.
        """
        return self.index.ntotal