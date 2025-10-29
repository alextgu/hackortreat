from flask import Flask, request, jsonify
from flask_cors import CORS
from generator import generate_post
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from project root
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

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
    port = int(os.getenv('FLASK_PORT', 5001))
    print(f'\n🚀 Content Generator API running on http://localhost:{port}')
    print('📊 Endpoints available:')
    print(f'   GET  http://localhost:{port}/health')
    print(f'   POST http://localhost:{port}/generate')
    print('\n')
    app.run(debug=True, port=port, host='0.0.0.0')

