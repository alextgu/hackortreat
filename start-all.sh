#!/bin/bash

# Start all servers for the HackOrTreat LinkedIn Post Generator

cd "$(dirname "$0")"

echo "🚀 Starting All Servers..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    lsof -ti:$1 > /dev/null 2>&1
    return $?
}

# Kill processes on ports if needed
echo "🧹 Cleaning up existing processes..."
for port in 3000 5001 8080; do
    if check_port $port; then
        echo "  Killing process on port $port"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
done

echo ""
echo "${GREEN}✓ Ports cleared${NC}"
echo ""

# Start Video Server (Node.js - Port 3000)
echo "📹 Starting Video Server (Port 3000)..."
node backend/video/server.cjs > logs/video-server.log 2>&1 &
VIDEO_PID=$!
sleep 2

if check_port 3000; then
    echo "${GREEN}✓ Video Server running on http://localhost:3000${NC}"
    # Get local IP
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "unknown")
    if [ "$LOCAL_IP" != "unknown" ]; then
        echo "  ${YELLOW}📱 Phone access: http://${LOCAL_IP}:3000${NC}"
    fi
else
    echo "❌ Video Server failed to start"
fi

echo ""

# Start Flask API (Python - Port 5001)
echo "🐍 Starting Flask API (Port 5001)..."
python3 backend/app.py > logs/flask-api.log 2>&1 &
FLASK_PID=$!
sleep 2

if check_port 5001; then
    echo "${GREEN}✓ Flask API running on http://localhost:5001${NC}"
else
    echo "❌ Flask API failed to start"
fi

echo ""

# Start Frontend (Vite - Port 8080)
echo "⚛️  Starting Frontend (Port 8080)..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 3

if check_port 8080; then
    echo "${GREEN}✓ Frontend running on http://localhost:8080${NC}"
else
    echo "❌ Frontend failed to start"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "${GREEN}🎉 All servers started!${NC}"
echo ""
echo "📍 Access Points:"
echo "   • Frontend:  http://localhost:8080"
echo "   • Backend:   http://localhost:5001"
echo "   • Video:     http://localhost:3000"
echo ""
echo "📝 Logs are in the logs/ directory"
echo ""
echo "To stop all servers:"
echo "  ./stop-all.sh"
echo ""
echo "Press Ctrl+C to stop this script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Keep script running
wait

