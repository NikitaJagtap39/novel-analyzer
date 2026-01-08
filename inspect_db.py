import chromadb

CHROMA_PATH = r"D:\Novel Analyzer Project\chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection("novel_pages")

print("Stored vectors:", collection.count())
