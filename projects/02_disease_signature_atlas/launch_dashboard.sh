#!/bin/bash
# Launch Disease Signature Atlas Dashboard

echo "🧬 Launching Disease Signature Atlas Dashboard..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Activate environment
source ../../venv-scanpy/bin/activate

# Launch Streamlit
echo "✅ Environment activated"
echo "🚀 Starting Streamlit server..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app/app.py
