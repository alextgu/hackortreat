from flask import Flask, request, jsonify
from flask_cors import CORS
from generator import generate_post
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a performative LinkedIn post based on input."""
    try:
        data = request.json
        topic = data.get('topic', '').strip()
        details = data.get('details', '').strip()
        style = data.get('style', 'professional').strip()

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        post = generate_post(topic, details, style)
        return jsonify({"post": post, "style": style}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
