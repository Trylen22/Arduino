#!/bin/bash
# Activation script for TTS environment

echo "🎤 Activating TTS environment..."
source tts_env/bin/activate
echo "✅ TTS environment activated!"
echo ""
echo "Available scripts:"
echo "  python3 test_tts.py          - Test TTS functionality"
echo "  python3 tts_enhanced_agent.py - Basic TTS agent"
echo "  python3 llm_tts_agent.py     - LLM-enhanced TTS agent"
echo ""
echo "To deactivate, run: deactivate"
