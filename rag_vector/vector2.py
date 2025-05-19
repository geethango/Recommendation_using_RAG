from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import logging

# Step 1: Connect to MongoDB Atlas
username = "dbgeet"
password = "dbgeet"
cluster_url = "cluster0.azme6ia.mongodb.net"
uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)
    db = client["mydatabase"]
    mongo_collection = db["mycollection"]
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    logging.error("❌ Failed to connect to MongoDB: %s", str(e))
    raise

# Step 2: Load all non-empty field values (excluding _id)
docs = list(mongo_collection.find({}))
texts = []
ids = []

for doc in docs:
    base_id = str(doc["_id"])
    for key, value in doc.items():
        if key == "_id":
            continue
        if isinstance(value, str) and value.strip():  # Non-empty string
            texts.append(value.strip())
            ids.append(f"{base_id}_{key}")  # Unique ID per field

print(f"📄 Loaded {len(texts)} non-empty text entries from MongoDB")

# Step 3: Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
print("🔍 Generating embeddings...")
embeddings = model.encode(texts, convert_to_numpy=True).tolist()
print("✅ Embeddings generated")

# Step 4: Store in ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("transcriptions")

print("💾 Storing in ChromaDB...")
chroma_collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=[{"video_id": vid.split('_')[-1]} for vid in ids]
)

print("✅ Data stored in ChromaDB successfully")
