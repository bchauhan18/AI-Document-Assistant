import faiss
import numpy as np


def create_vector_store(embeddings):
    """
    Create a FAISS index from embeddings.
    """

    # Convert embeddings to float32 (required by FAISS)
    embeddings = np.array(embeddings).astype("float32")

    # Get embedding dimension (384 for all-MiniLM-L6-v2)
    dimension = embeddings.shape[1]

    # Create a flat L2 index
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to the index
    index.add(embeddings)

    return index

def search_vector_store(index, query_embedding, top_k=3):

    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    return indices[0]