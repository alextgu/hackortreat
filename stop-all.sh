#!/bin/bash

# Stop all servers

echo "🛑 Stopping all servers..."

# Kill processes on specific ports
for port in 3000 5001 8080; do
    if lsof -ti:$port > /dev/null 2>&1; then
        echo "  Stopping process on port $port"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
    fi
done

# Also kill by process name
pkill -f "node backend/video/server.cjs" 2>/dev/null || true
pkill -f "python.*backend/app.py" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

echo "✅ All servers stopped"

