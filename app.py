from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma:2b"
 # Change if using another model

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    payload = {
        "model": MODEL_NAME,
        "prompt": user_message,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get("response", "").strip()
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"reply": "Error: Unable to connect to Ollama."})
    except Exception as e:
        return jsonify({"reply": f"Server Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
