import json
import os
import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File paths
CLEAN_JSON = r"D:\Novel Analyzer Project\novel_pages_cleaned.json"
EMBEDDINGS_JSON = r"D:\Novel Analyzer Project\novel_pages_embeddings.json"

# Initialize Cohere client with API key from environment variable
# Make sure you have COHERE_API_KEY in your .env
client = cohere.Client(os.getenv("COHERE_API_KEY"))


def embed_text_batch(texts: list):
    """
    Generate embeddings for a batch of texts using Cohere.
    
    Args:
        texts (list[str]): List of text strings to embed.
        
    Returns:
        list[list[float]]: List of embedding vectors.
    """
    response = client.embed(
        model="small",  # lightweight embedding model
        texts=texts
    )
    return response.embeddings  # returns a list of vectors


def create_embeddings(json_path: str, batch_size=20):
    """
    Read cleaned pages and generate embeddings in batches.
    
    Args:
        json_path (str): Path to cleaned JSON file of pages.
        batch_size (int): Number of pages to embed per API call.
    
    Returns:
        list[dict]: Pages with added "embedding" key.
    """
    # Load cleaned pages
    with open(json_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    # Process in batches to avoid hitting rate limits
    for i in range(0, len(pages), batch_size):
        batch_pages = pages[i:i + batch_size]
        batch_texts = [p["text"] for p in batch_pages]

        # Get embeddings for the batch
        batch_embeddings = embed_text_batch(batch_texts)

        # Assign embeddings back to pages
        for page, emb in zip(batch_pages, batch_embeddings):
            page["embedding"] = emb

        print(f"Embedded pages {i+1} to {i+len(batch_pages)}")

    return pages


def save_embeddings(data, path: str):
    """
    Save the list of pages with embeddings to a JSON file.
    
    Args:
        data (list[dict]): List of pages with embeddings.
        path (str): Path to save JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} pages with embeddings to {path}")


if __name__ == "__main__":
    # Generate embeddings for cleaned pages
    pages_with_embeddings = create_embeddings(CLEAN_JSON, batch_size=20)

    # Save embeddings to JSON
    save_embeddings(pages_with_embeddings, EMBEDDINGS_JSON)
