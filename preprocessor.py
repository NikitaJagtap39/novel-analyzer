import json
from pdf_parser import pages_data  # your PDF extraction module

OUTPUT_JSON = r"D:\Novel Analyzer Project\novel_pages.json"

# Front-matter / TOC keywords
FRONT_KEYWORDS = ["table of contents", "contents", "title page", "copyright", "dedication"]

# Ending / back-matter keywords
END_KEYWORDS = ["about the author", "acknowledgments", "what’s next"]

def is_front_page(text):
    """Check if page contains front-matter keywords"""
    text_lower = text.lower()
    return any(kw in text_lower for kw in FRONT_KEYWORDS)

def is_end_page(text):
    """Check if page contains end keywords"""
    text_lower = text.lower()
    return any(kw in text_lower for kw in END_KEYWORDS)

def clean_pages(pages):
    """
    Clean PDF pages for novel pipeline:
    - Skip empty pages
    - Skip front-matter pages with specific keywords
    - Skip ending pages
    - Normalize line breaks to make each page one paragraph
    """
    cleaned = []

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue  # skip empty pages

        if is_front_page(text):
            continue  # skip front-matter / TOC pages

        if is_end_page(text):
            break  # stop at ending pages

        # Normalize line breaks and extra spaces
        normalized_text = " ".join(text.split())

        cleaned.append({
            "page": page["page"],
            "text": normalized_text
        })

    return cleaned

def save_to_json(data, path):
    """Save cleaned pages to JSON file"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} cleaned pages to {path}")


if __name__ == "__main__":
    cleaned_pages = clean_pages(pages_data)
    save_to_json(cleaned_pages, OUTPUT_JSON)
