from flask import Flask, render_template, request, jsonify
import json
import nltk
from rapidfuzz import fuzz  # ✅ Use RapidFuzz instead

nltk.download("punkt")
nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Load responses
with open("data/responses.json", "r") as f:
    responses = json.load(f)

stop_words = set(stopwords.words("english"))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalnum() and w not in stop_words]
    return " ".join(tokens)

def chatbot_response(user_input):
    processed_input = preprocess(user_input)

    best_match = None
    highest_score = 0

    for key in responses.keys():
        score = fuzz.ratio(processed_input, key)  # RapidFuzz works same as FuzzyWuzzy
        if score > highest_score:
            highest_score = score
            best_match = key

    if highest_score > 60:
        return responses[best_match]
    else:
        return "Sorry, I didn't understand that. Can you rephrase? 🙏"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")
    bot_reply = chatbot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
