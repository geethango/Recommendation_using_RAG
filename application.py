from flask import Flask, render_template, request
import json
import os


application = Flask(__name__)







# Load recommendations
with open('recommendations/top_n_video_recommendations.json', 'r', encoding='utf-8') as f:
    recommendations = json.load(f)

# Map video name to its recommendations
recommendation_dict = {entry["input_video"]: entry["top_matches"] for entry in recommendations}

# List of available videos
VIDEO_DIR = "static/videos"
videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".mov", ".avi"))]

@application.route('/')
def index():
    return render_template("index.html", videos=videos)

@application.route('/video/<video_name>')
def play_video(video_name):
    recs = recommendation_dict.get(video_name, [])
    return render_template("video.html", video_name=video_name, recommendations=recs)

if __name__ == '__main__':
    application.run(debug=True)
