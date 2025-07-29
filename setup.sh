#!/bin/bash

echo "🚀 Setting up Environmental Monitoring System..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "tts_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv tts_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source tts_env/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🎤 To run the system:"
echo "   source tts_env/bin/activate"
echo "   python agents/examples/voice_environmental_agent_modern.py"
echo ""
echo "📚 For documentation, see README.md"
