#!/bin/bash
# FlowForge Quick Start Script

echo "🚀 FlowForge - Agentic Sales System"
echo "=================================="
echo ""

# Backend Setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -q fastapi uvicorn langchain langchain-groq pydantic pydantic-settings

echo "✅ Backend ready"
echo ""

# Frontend Setup
echo "📦 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install -q
fi

echo "✅ Frontend ready"
echo ""

# Start servers
echo "🎬 Starting servers..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Backend
cd ../backend
echo "📡 Starting backend on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Frontend
cd ../frontend
echo "🎨 Starting frontend on http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✨ FlowForge is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Dashboard: http://localhost:5173"
echo "🔧 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for any process to exit
wait $BACKEND_PID
wait $FRONTEND_PID
