import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """
You are StackMate AI, a helpful Full Stack Web Development assistant.
Answer questions about HTML, CSS, JavaScript, React, Node.js, Python Flask,
Django, databases, SQL, MongoDB, REST APIs, Git/GitHub, authentication,
deployment, debugging, and web development best practices.
Give beginner-friendly explanations and practical code examples when useful.
If the user provides code, identify the problem and explain how to fix it.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please enter a question."}), 400

    if not client:
        return jsonify({
            "reply": "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."
        }), 500

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=SYSTEM_PROMPT + "\n\nUser question:\n" + message
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Sorry, something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
