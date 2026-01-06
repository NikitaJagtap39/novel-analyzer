#Importing necessary libraries
import pymupdf
import json

#Path to novel
novel_path = r"D:\Novel Analyzer Project\born-a-crime-trevor-noah.pdf"

#Path to save the JSON output
json_path = r"D:\Novel Analyzer Project\novel_pages.json"

#Opening the PDF
doc = pymupdf.open(novel_path)

#List to hold all pages
pages_data = []

#Loop through each page
for page_number, page in enumerate(doc, start=1):
    text = page.get_text()

    #Create dictionary
    page_dict ={
        
        "page": page_number,
        "text": text.strip() #Text of the page, stripped of leading/trailing spaces
    }

    #Add to the list of pages
    pages_data.append(page_dict)

#Save all pages to a JSON file
with open(json_path, "w", encoding="utf-8") as f:
    #ensure_ascii= False allows non-English characters to be saved correctly
    #indent=2 makes the JSON file readable
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print(f"PDF text extracted and saved to {json_path}")
