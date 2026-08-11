from langchain_huggingface import HuggingFaceEmbeddings


embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_embeddings(texts):

    embeddings = embeddings_model.embed_documents(texts)

    return embeddings