# Recommendating using RAG

An end-to-end AI-powered system that recommends and retrieves educational video content using **RAG (Retrieval-Augmented Generation)**, **Whisper** for transcription, **Flask** for the API layer, and **MongoDB Atlas** for transcript and metadata storage.

## 🧠 Tech Stack

- **Whisper** – Automatic speech recognition for transcribing video audio
- **MongoDB Atlas** – Cloud database to store transcripts and metadata
- **RAG (LangChain + LLM)** – For contextual Q&A and source-aware answers
- **Flask** – RESTful API backend
- **Python** – Core language for orchestration
- **FFmpeg** – Extract audio from videos

---

## 📌 Features

- 🎞️ Extracts audio from video files and transcribes them using Whisper
- 💾 Stores video metadata and transcripts in MongoDB Atlas
- 🤖 Retrieves relevant videos using LLM-based RAG pipeline
- 🔗 Maps video IDs from sources to actual filenames using metadata
- 🧠 Recommends videos based on semantic understanding of user queries
- 🌐 Flask API to serve recommendations and Q&A responses

---

## 🚀 Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/recommendating-using-RAG.git
cd recommendating-using-RAG
```

### 2. Run Locally

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Run the Flask app:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### 3. GitHub Deployment

A GitHub Actions workflow is included to automatically deploy the Flask app on pushes to the main branch.

- The workflow installs dependencies and runs the Flask app.
- You can customize the workflow in `.github/workflows/deploy.yml`.

