from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_url = os.getenv("MONGO_CLUSTER")

# Build MongoDB URI
uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)

# Choose database and collection
db = client["mydatabase"]
collection = db["mycollection"]

# Load JSON data
with open("video_data_by_id.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Insert into MongoDB
if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("✅ JSON data inserted into MongoDB Atlas successfully.")
