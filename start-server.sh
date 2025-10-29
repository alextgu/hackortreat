#!/bin/bash

# Start Flask Backend Server

cd "$(dirname "$0")"

echo "🚀 Starting Flask Backend Server..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Create one with: GEMINI_API_KEY=your_key"
    echo ""
fi

# Start the server
python backend/app.py

