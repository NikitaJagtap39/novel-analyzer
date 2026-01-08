import os
from dotenv import load_dotenv
import cohere

# Import your existing query function
from query_vector_db import query_novel

# ----------------------------
# Load env variables
# ----------------------------
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# ----------------------------
# Initialize Cohere client
# ----------------------------
co = cohere.Client(COHERE_API_KEY)

def generate_answer(question: str, top_n: int = 5):
    """
    RAG pipeline:
    1. Query Chroma DB for top relevant pages using the imported query_novel().
    2. Use Cohere Chat API to generate an answer based on retrieved context.
    """

    # 1) Retrieve context
    results = query_novel(question, n_results=top_n)
    context_docs = results["documents"][0]

    # Combine top results into a single context string
    context_text = "\n\n".join(
        [f"Page {results['metadatas'][0][i]['page']}: {doc}"
         for i, doc in enumerate(context_docs)]
    )

    # 2) Create prompt
    prompt = f"""
You are a helpful assistant. Use the context below to answer the question.

CONTEXT:
{context_text}

QUESTION:
{question}

ANSWER:
"""

    # 3) Call Cohere Chat (old SDK signature)
    response = co.chat(
        model="command-a-03-2025",  # a chat-capable Cohere model
        message=prompt
    )

    # Get the generated answer text
    answer_text = response.text.strip()
    return answer_text

# ----------------------------
# Test run
# ----------------------------
if __name__ == "__main__":
    question = "Which tribes are described in the book?"
    answer = generate_answer(question)
    print("\nFINAL ANSWER:\n")
    print(answer)
