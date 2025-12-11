#!/bin/bash

# Kill background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

echo "🚀 Starting KubeZap in Development Mode..."

# Clean up any previous Docker-created build artifacts (with root permissions)
echo "🧹 Cleaning build artifacts..."
if [ -d "frontend/.next" ]; then
    echo "   Removing .next directory (might ask for sudo password)..."
    sudo rm -rf frontend/.next frontend/.swc 2>/dev/null || {
        echo "   ⚠️  Could not remove with sudo, trying regular removal..."
        rm -rf frontend/.next frontend/.swc 2>/dev/null || echo "   ⚠️  Some files might have permission issues"
    }
fi

# Start Backend
echo "🐍 Starting FastAPI Backend on port 8000..."
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready (optional but nice)
sleep 2

# Start Frontend
echo "⚛️  Starting Next.js Frontend on port 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ KubeZap is running!"
echo "   Backend: http://localhost:8000/docs"
echo "   Frontend: http://localhost:3000"
echo "   Press Ctrl+C to stop both servers."

wait
