#!/bin/bash

echo "🎓 Education ROI Engine - Starting..."
echo ""

# Check if requirements are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "🚀 Launching application..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
