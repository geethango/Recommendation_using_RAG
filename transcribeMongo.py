import os
import subprocess
import whisper
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get credentials from environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_url = os.getenv("MONGO_CLUSTER")

# MongoDB URI
uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)
db = client["mydatabase"]
collection = db["mycollection"]

# Initialize Whisper model
model = whisper.load_model("base")

# Folder paths
video_folder = r"D:\audio_rec\data\videos"
output_folder = "transcriptions"
os.makedirs(output_folder, exist_ok=True)

# Dictionary to store all transcriptions
transcriptions = {}

# Loop through videos and process
for video_file in os.listdir(video_folder):
    video_file_path = os.path.join(video_folder, video_file)
    print("Processing video:", video_file_path)
    
    if video_file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
        # Extract audio
        audio_path = os.path.join(output_folder, f"{video_file}.wav")
        command = f"ffmpeg -i \"{video_file_path}\" -vn -acodec pcm_s16le -ar 44100 -ac 2 \"{audio_path}\""
        subprocess.run(command, shell=True)

        # Transcribe audio
        result = model.transcribe(audio_path)
        transcription_text = result["text"]
        transcriptions[video_file] = transcription_text

        # Insert into MongoDB
        document = {
            "file_name": video_file,
            "transcription": transcription_text
        }
        collection.insert_one(document)
        print(f"Inserted transcription for {video_file} into MongoDB.")

# Save all transcriptions to a JSON file
json_file_path = os.path.join(output_folder, "all_transcriptions.json")
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transcriptions, json_file, indent=4)

print("✅ All videos processed, transcriptions saved to JSON and uploaded to MongoDB.")
