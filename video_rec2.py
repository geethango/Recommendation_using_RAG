import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# === Paths ===
json_path = "D:/audio_rec/transcriptions/all_transcriptions.json"
output_path = "D:/audio_rec/recommendations/top_n_video_recommendations.json"
TOP_N = 5  # Change this to however many top matches you want

# === Load Dataset ===
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

video_names = list(data.keys())
transcriptions = list(data.values())

# === Load Embedding Model ===
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# === Create Normalized Embeddings ===
embeddings = embedding_model.encode(transcriptions, convert_to_numpy=True, normalize_embeddings=True)

# === Build FAISS Index for Cosine Similarity ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# === Generate Top-N Recommendations per Video ===
recommendations = []

for i, transcription in enumerate(transcriptions):
    query_embedding = embeddings[i].reshape(1, -1)
    distances, indices = index.search(query_embedding, TOP_N + 1)  # +1 to account for self-match

    video_results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == i:
            continue  # skip self
        video_results.append({
            "matched_video": video_names[idx],
            "score": float(score)
        })
        if len(video_results) == TOP_N:
            break

    recommendations.append({
        "input_video": video_names[i],
        "top_matches": video_results
    })

# === Save to JSON ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(recommendations, f, indent=2)

print(f"✅ Top {TOP_N} video recommendations saved to:\n{output_path}")
