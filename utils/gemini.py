import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API Key not found. Check your .env file."
    )


client = genai.Client(api_key=api_key)


def ask_gemini(question, context):

    prompt = f"""
You are an AI Document Assistant.

Answer the user's question ONLY using the information provided in the context.

If the context contains only part of the answer, answer only that part.

If the answer is not available in the context, respond:
"I couldn't find information related to your question in the provided document."

Do not guess.
Do not make up information.
Keep your response clear, accurate, and easy to understand.

Context:
{context}

Question:
{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"