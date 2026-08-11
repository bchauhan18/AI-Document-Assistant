from flask import Flask, request, render_template

from services.rag_service import process_pdf, search_chunks


app = Flask(__name__)


chunks = None
embeddings = None
index = None


@app.route("/", methods=["GET", "POST"])
def home():

    global chunks, embeddings, index

    answer = ""
    message = ""

    if request.method == "POST":

        pdf = request.files.get("pdf")
        question = request.form.get("question", "").strip()

        # Process PDF when a new PDF is uploaded
        if pdf and pdf.filename:

            if not pdf.filename.lower().endswith(".pdf"):
                message = "Please upload a PDF file."

                return render_template(
                    "index.html",
                    answer=answer,
                    message=message
                )

            pdf_path = "uploads/" + pdf.filename

            pdf.save(pdf_path)

            chunks, embeddings, index = process_pdf(pdf_path)

            message = "PDF uploaded and processed successfully."

        # Check whether a PDF has been processed
        if question:

            if index is None:

                message = "Please upload a PDF before asking a question."

            else:

                answer = search_chunks(
                    question,
                    chunks,
                    index
                )

        else:

            if not message:
                message = "Please enter a question."

    return render_template(
        "index.html",
        answer=answer,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)