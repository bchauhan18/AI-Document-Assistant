from flask import Flask, request

from services.rag_service import process_pdf, search_chunks


app = Flask(__name__)

chunks = None
embeddings = None
index = None


@app.route("/", methods=["GET", "POST"])
def home():

    global chunks, embeddings, index

    answer = ""

    if request.method == "POST":

        pdf = request.files.get("pdf")
        question = request.form.get("question")

        # Process PDF only when a new PDF is uploaded
        if pdf and pdf.filename:

            pdf_path = "uploads/" + pdf.filename
            pdf.save(pdf_path)

            chunks, embeddings, index = process_pdf(pdf_path)

        # Ask question using the already processed PDF
        if question and index is not None:

            answer = search_chunks(
                question,
                chunks,
                index
            )

    return f"""
    <h1>AI Document Assistant</h1>

    <form method="POST" enctype="multipart/form-data">

        <h3>Upload PDF</h3>

        <input
            type="file"
            name="pdf"
            accept=".pdf"
        >

        <br><br>

        <h3>Ask a question</h3>

        <input
            type="text"
            name="question"
            placeholder="Ask something about the PDF"
            style="width: 500px; padding: 10px;"
        >

        <br><br>

        <button type="submit">
            Ask
        </button>

    </form>

    <h2>Answer:</h2>

    <p>{answer}</p>
    """


if __name__ == "__main__":
    app.run(debug=True)