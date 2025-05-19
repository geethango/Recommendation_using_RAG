import os
import subprocess
import whisper
import json

# Initialize Whisper model
model = whisper.load_model("base")  # Use other models like "small", "medium" as needed

# Path to the folder containing videos
video_folder = r"D:\audio_rec\data\videos"
output_folder = "transcriptions"

# Create output folder for transcriptions if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize a dictionary to store transcriptions
transcriptions = {}

# Loop through each video file in the video folder
for video_file in os.listdir(video_folder):
    video_file_path = os.path.join(video_folder, video_file)
    print("Processing video:", video_file_path)
    
    # Check if it's a video file (you can add more extensions)
    if video_file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):

        # Step 1: Extract audio using FFmpeg
        audio_path = os.path.join(output_folder, f"{video_file}.wav")
        command = f"ffmpeg -i \"{video_file_path}\" -vn -acodec pcm_s16le -ar 44100 -ac 2 \"{audio_path}\""
        subprocess.run(command, shell=True)

        # Step 2: Transcribe audio using Whisper
        result = model.transcribe(audio_path)

        # Step 3: Store the transcription in the dictionary
        transcriptions[video_file] = result["text"]
        print(f"Processed: {video_file}")

# Step 4: Save all transcriptions to a single JSON file
json_file_path = os.path.join(output_folder, "all_transcriptions.json")
with open(json_file_path, "w") as json_file:
    json.dump(transcriptions, json_file, indent=4)

print("All videos processed and transcriptions saved to JSON!")
