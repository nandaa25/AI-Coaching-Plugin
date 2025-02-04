import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai

# Load environment variables
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# API Route: Generate Coaching Plan
@app.route('/generate_coaching_plan', methods=['POST'])
def generate_coaching_plan():
    print("✅ Received request at /generate_coaching_plan")  # Debugging log

    # Ensure request contains JSON
    if not request.is_json:
        print("❌ Error: Request is not JSON")
        return jsonify({"error": "Request must be in JSON format"}), 415
    
    data = request.get_json()
    print("📩 Request Data:", data)  # Debugging log

    goal = data.get("goal")
    time_per_day = data.get("time_per_day")
    challenge_level = data.get("challenge_level")

    # Ensure all required fields are provided
    if not goal or not time_per_day or not challenge_level:
        print("❌ Error: Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    prompt = f"""
    You are an AI personal coach. A user wants to achieve the goal '{goal}'.
    They will commit {time_per_day} minutes per day at '{challenge_level}' challenge level.
    Generate a structured coaching plan for 7 days with:
    - Daily lessons
    - Action steps
    - Progress challenges
    """

    try:
        print("⏳ Sending request to OpenAI...")
        response = openai.chat.completions.create(  # Corrected API call for OpenAI v1.0.0+
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI coach."},
                {"role": "user", "content": prompt}
            ]
        )
        coaching_plan = response.choices[0].message.content
        print("✅ OpenAI Response Received!")

        return jsonify({"coaching_plan": coaching_plan})

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
