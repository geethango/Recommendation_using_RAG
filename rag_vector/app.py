from flask import Flask, request, jsonify, render_template
from rag_chain import RAGSystem
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Initialize RAG system
rag_system = RAGSystem()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST","GET"])
def chat():
    data = request.get_json()
    print("data:",data)
    query = data.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' in request"}), 400
    try:
        result = rag_system.answer(query)
        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
