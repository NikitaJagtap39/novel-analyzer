import chromadb
import json
import os

EMBEDDINGS_JSON = r"D:\Novel Analyzer Project\novel_pages_embeddings.json"
PERSIST_DIR = r"D:\Novel Analyzer Project\chroma_db"

#Ensure persist directory exists
os.makedirs(PERSIST_DIR, exist_ok=True)

#Initialize Chroma Client
client = chromadb.PersistentClient(
    path= PERSIST_DIR
)

print("Chroma DB path:", os.path.abspath(PERSIST_DIR))

#Creating a collection
collection = client.get_or_create_collection(name="novel_pages") #collection where novel's pages and embeddings will be stored

#Reads the JSON file containing cleaned and embedded pages and also returns list of dictionaries.
def load_embeddings(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
#Adding pages to the vector database
def add_to_vector_db(pages):
    for page in pages:
        collection.add(
            documents=[page["text"]], #The actual text content
            metadatas=[{"page":page["page"]}], #Metadata associated with the doc i.e. here its the page number
            ids=[str(page["page"])], #unique ID for each doc in the collection(page number= ID)
            embeddings=[page["embedding"]] #Vector representation of the text
        )
    print(f"Added {len(pages)} pages to vector DB")

if __name__ == "__main__":
    pages = load_embeddings(EMBEDDINGS_JSON)
    add_to_vector_db(pages)

