from langchain_community.vectorstores import FAISS

from utils.embeddings import embeddings_model


def create_vector_store(chunks, embeddings):

    text_embeddings = list(zip(chunks, embeddings))

    vectorstore = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embeddings_model
    )

    return vectorstore