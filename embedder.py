import json
from sentence_transformers import SentenceTransformer

# File paths
CLEAN_JSON = r"D:\Novel Analyzer Project\novel_pages_cleaned.json"
EMBEDDINGS_JSON = r"D:\Novel Analyzer Project\novel_pages_embeddings.json"

# Load a free Hugging Face sentence transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def create_embeddings(json_path):
    """
    Read cleaned pages and generate embeddings for each page.
    
    Args:
        json_path (str): Path to cleaned JSON file of pages.
    
    Returns:
        list[dict]: Pages with added "embedding" key.
    """
    # Load cleaned pages
    with open(json_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    for i, page in enumerate(pages, start=1):
        # Generate embedding for a single page
        embedding = model.encode(page["text"], show_progress_bar=False).tolist()
        page["embedding"] = embedding

        print(f"Embedded page {i} / {len(pages)}")

    return pages

def save_embeddings(data, path):
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
    pages_with_embeddings = create_embeddings(CLEAN_JSON)
    save_embeddings(pages_with_embeddings, EMBEDDINGS_JSON)
