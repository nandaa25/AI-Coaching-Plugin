import os
from flask import Flask, request, jsonify
import openai

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please set OPENAI_API_KEY in environment variables.")

openai.api_key = OPENAI_API_KEY

# Initialize Flask app
app = Flask(__name__)

# Home Route (GET Request)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Coaching API is running!"})

# Coaching Plan Route (POST Request)
@app.route("/generate_coaching_plan", methods=["POST"])
def generate_coaching_plan():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    goal = data.get("goal")
    time_per_day = data.get("time_per_day")
    challenge_level = data.get("challenge_level")

    if not goal or not time_per_day or not challenge_level:
        return jsonify({"error": "Missing required fields"}), 400

    prompt = f"You are an AI personal coach. A user wants to achieve the goal '{goal}' and will commit {time_per_day} minutes per day at '{challenge_level}' challenge level. Generate a 7-day structured coaching plan."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI coach."},
                {"role": "user", "content": prompt}
            ]
        )
        coaching_plan = response.choices[0].message.content
        return jsonify({"coaching_plan": coaching_plan})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
