from flask import Flask
from services.rag_service import process_pdf, search_chunks

app = Flask(__name__)

chunks, embeddings, index = process_pdf("uploads/sample.pdf")


@app.route("/")
def home():

    question = "What are the HR and opinion-based topics?"

    answer = search_chunks(question, chunks, index)

    print("=" * 50)
    print("Relevant Chunks")
    print("=" * 50)
    print(answer)

    return f"<h1>{answer}</h1>"


if __name__ == "__main__":
    app.run(debug=True)