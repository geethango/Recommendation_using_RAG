import chromadb
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the ChromaDB vector store
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("transcriptions")

# Input query
query = "How does flexbox work in CSS?"

# Create embedding for query
query_embedding = model.encode([query], convert_to_numpy=True).tolist()

# Search
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

# Print top matches
for i, doc in enumerate(results['documents'][0]):
    print(f"\nMatch {i+1}:\n{doc}")
