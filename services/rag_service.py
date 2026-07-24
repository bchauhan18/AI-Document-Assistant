from utils.pdf_reader import extract_text
from utils.chunker import chunk_text
from utils.embeddings import create_embeddings
from utils.vector_store import create_vector_store, search_vector_store
from utils.gemini import ask_gemini


def process_pdf(pdf_path):

    text = extract_text(pdf_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    index = create_vector_store(embeddings)

    return chunks, embeddings, index

def search_chunks(question, chunks, index):

    question_embedding = create_embeddings([question])

    indices = search_vector_store(index, question_embedding[0])

    results = [chunks[i] for i in indices]

    context = "\n\n".join(results)

    answer = ask_gemini(question, context)

    return answer