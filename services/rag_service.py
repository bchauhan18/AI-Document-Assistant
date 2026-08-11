from utils.pdf_reader import extract_text
from utils.chunker import chunk_text
from utils.embeddings import create_embeddings
from utils.vector_store import create_vector_store
from utils.gemini import ask_gemini


def process_pdf(pdf_path):

    text = extract_text(pdf_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    index = create_vector_store(chunks, embeddings)

    return chunks, embeddings, index


def search_chunks(question, chunks, index):

    retriever = index.as_retriever(
        search_kwargs={"k": 6}
    )

    documents = retriever.invoke(question)

    print("QUESTION:", question)

    print("=" * 50)
    print("Retrieved Chunks")
    print("=" * 50)

    for document in documents:
        print(document.page_content)
        print("-" * 50)

    context = "\n\n".join(
        document.page_content for document in documents
    )

    answer = ask_gemini(question, context)

    return answer