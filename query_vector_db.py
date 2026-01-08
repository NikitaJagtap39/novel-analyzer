import chromadb
import os
import json
from sentence_transformers import SentenceTransformer

# Chroma persistence directory (must match ingestion)
PERSIST_DIR = r"D:\Novel Analyzer Project\chroma_db"

# Initialize Chroma Persistent Client
chroma_client = chromadb.PersistentClient(
    path=PERSIST_DIR
)

# Load existing collection
collection = chroma_client.get_collection(name="novel_pages")

# Load Hugging Face SentenceTransformer (must match document embeddings)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_query(text: str):
    """
    Generate embedding for a user query using Hugging Face SentenceTransformer.
    """
    embedding = model.encode([text], show_progress_bar=False)
    return embedding[0].tolist()  # convert numpy array to list

def query_novel(question: str, n_results: int = 5):
    """
    Query the Chroma vector database for relevant novel pages.
    """
    query_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    return results

# Test query
if __name__ == "__main__":
    question = "Which tribes are described in the book?"

    results = query_novel(question)

    print("\nTOP MATCHING PAGES:\n")

    for i, doc in enumerate(results["documents"][0], 1):
        page_num = results["metadatas"][0][i - 1]["page"]
        distance = results["distances"][0][i - 1]

        print(f"\n--- Result {i} (Page {page_num}, score={distance:.4f}) ---")
        print(doc[:500])  # Print first 500 characters
