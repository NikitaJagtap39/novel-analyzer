import json
from pdf_parser import pages_data  # PDF extraction module

OUTPUT_JSON = r"D:\Novel Analyzer Project\novel_pages_cleaned.json"

# Front-matter / TOC keywords
FRONT_KEYWORDS = [
    "table of contents",
    "contents",
    "title page",
    "copyright",
    "dedication"
]

# Hard stop keywords (true ending)
END_KEYWORDS = [
    "about the author",
    "what’s next",
    "whats next"
]


def is_front_page(text: str) -> bool:
    """Detect front-matter pages like TOC, copyright, dedication."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in FRONT_KEYWORDS)


def is_end_page(text: str) -> bool:
    """Detect true ending pages where story is definitely over."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in END_KEYWORDS)


def looks_like_acknowledgments(text: str) -> bool:
    """
    Heuristic detector for acknowledgments pages.
    Works even if the word 'Acknowledgments' is not present.
    """

    text_lower = text.lower()
    words = text.split()

    if len(words) < 80:
        return False  # too short to be acknowledgments

    # Gratitude language
    thank_words = [
        "thank",
        "thanks",
        "grateful",
        "gratitude",
        "owe",
        "indebted"
    ]

    # Proper-name density (many capitalized words)
    title_case_words = sum(1 for w in words if w.istitle())
    name_density = title_case_words / max(len(words), 1)

    return (
        any(w in text_lower for w in thank_words)
        and name_density > 0.25
    )


def clean_pages(pages):
    """
    Clean PDF pages for a novel pipeline:
    - Skip empty pages
    - Skip front-matter pages
    - Skip acknowledgments pages (heuristic)
    - Stop at true ending pages
    - Normalize line breaks (one paragraph per page)
    """

    cleaned = []

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        if is_front_page(text):
            continue

        if looks_like_acknowledgments(text):
            continue

        if is_end_page(text):
            break

        # Normalize line breaks and extra whitespace
        normalized_text = " ".join(text.split())

        cleaned.append({
            "page": page["page"],
            "text": normalized_text
        })

    return cleaned


def save_to_json(data, path):
    """Save cleaned pages to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(data)} cleaned pages to {path}")


if __name__ == "__main__":
    cleaned_pages = clean_pages(pages_data)
    save_to_json(cleaned_pages, OUTPUT_JSON)
