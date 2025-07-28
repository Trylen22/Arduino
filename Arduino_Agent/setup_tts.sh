#!/bin/bash

# Setup Script for Enhanced LED Assistant with TTS
# ================================================

echo "🎤 Setting up Enhanced LED Assistant with Text-to-Speech..."
echo "=========================================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This script is designed for Linux. Some features may not work on other systems."
fi

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    espeak-ng \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv tts_env
source tts_env/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements_tts.txt

# Test TTS installation
echo "🧪 Testing TTS installation..."
python3 -c "
import pyttsx3
try:
    engine = pyttsx3.init()
    print('✅ TTS engine initialized successfully!')
    voices = engine.getProperty('voices')
    print(f'🎤 Found {len(voices)} voice(s)')
    for i, voice in enumerate(voices):
        print(f'   {i+1}. {voice.name} ({voice.id})')
except Exception as e:
    print(f'❌ TTS initialization failed: {e}')
"

# Test speech recognition
echo "🎤 Testing speech recognition..."
python3 -c "
import speech_recognition as sr
try:
    r = sr.Recognizer()
    m = sr.Microphone()
    print('✅ Speech recognition initialized successfully!')
    print(f'🎤 Available microphones: {sr.Microphone.list_microphone_names()}')
except Exception as e:
    print(f'❌ Speech recognition failed: {e}')
"

# Create a simple test script
echo "📝 Creating test script..."
cat > test_tts.py << 'EOF'
#!/usr/bin/env python3
"""
Simple TTS Test Script
======================
Tests the text-to-speech functionality.
"""

import pyttsx3
import speech_recognition as sr
import time

def test_tts():
    """Test text-to-speech functionality."""
    try:
        # Initialize TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        
        # Test speech
        print("🎤 Testing text-to-speech...")
        engine.say("Hello! This is a test of the text to speech system.")
        engine.runAndWait()
        print("✅ TTS test completed!")
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")

def test_speech_recognition():
    """Test speech recognition functionality."""
    try:
        # Initialize speech recognition
        r = sr.Recognizer()
        m = sr.Microphone()
        
        print("🎤 Testing speech recognition...")
        print("Please speak something when prompted...")
        
        with m as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening... (speak now)")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing...")
            
            try:
                text = r.recognize_google(audio)
                print(f"✅ You said: {text}")
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")

if __name__ == "__main__":
    print("🧪 Running TTS and Speech Recognition Tests...")
    print("=" * 50)
    
    test_tts()
    print()
    
    choice = input("Test speech recognition? (y/n): ").lower()
    if choice == 'y':
        test_speech_recognition()
    
    print("\n✅ Tests completed!")
EOF

chmod +x test_tts.py

# Create activation script
echo "📝 Creating activation script..."
cat > activate_tts.sh << 'EOF'
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
EOF

chmod +x activate_tts.sh

# Create a quick start guide
echo "📖 Creating quick start guide..."
cat > TTS_QUICK_START.md << 'EOF'
# Quick Start Guide - Enhanced LED Assistant with TTS

## 🚀 Getting Started

1. **Activate the environment:**
   ```bash
   source activate_tts.sh
   ```

2. **Test the setup:**
   ```bash
   python3 test_tts.py
   ```

3. **Run the basic TTS agent:**
   ```bash
   python3 tts_enhanced_agent.py
   ```

4. **Run the LLM-enhanced agent:**
   ```bash
   python3 llm_tts_agent.py
   ```

## 🎤 Voice Commands You Can Try

### Basic Commands:
- "Turn on the red LED"
- "Turn off the green LED"
- "Toggle the red LED"
- "What's the status?"
- "Wait for 5 seconds"

### Advanced Commands (LLM version):
- "Switch on the red light"
- "Turn off both LEDs"
- "Check the current status"
- "Wait for 3 seconds"

## 🔧 Troubleshooting

### TTS Issues:
- Make sure speakers are connected and working
- Check volume levels
- Try different voices: `python3 -c "import pyttsx3; engine = pyttsx3.init(); print(engine.getProperty('voices'))"`

### Speech Recognition Issues:
- Check microphone permissions
- Test microphone: `python3 test_tts.py`
- Adjust microphone index in the code if needed

### Arduino Issues:
- Check USB connection
- Verify port name (usually `/dev/ttyACM0` or `/dev/ttyUSB0`)
- Upload the Arduino code first

## 📁 File Structure

```
Arduino_Agent/
├── tts_enhanced_agent.py    # Basic TTS agent
├── llm_tts_agent.py         # LLM-enhanced TTS agent
├── test_tts.py              # TTS test script
├── requirements_tts.txt      # Python dependencies
├── activate_tts.sh          # Environment activation
└── TTS_QUICK_START.md      # This guide
```

## 🎯 Next Steps

1. **Customize voices:** Edit the TTS settings in the agent files
2. **Add more commands:** Extend the LLM prompt for new capabilities
3. **Integrate with other sensors:** Add temperature, motion, etc.
4. **Create voice profiles:** Different voices for different users

## 🆘 Need Help?

- Check the console output for error messages
- Test individual components with `test_tts.py`
- Verify Arduino connection with basic serial communication
- Check microphone and speaker connections

Happy coding! 🎤✨
EOF

echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "📋 Next steps:"
echo "1. Activate the environment: source activate_tts.sh"
echo "2. Test the setup: python3 test_tts.py"
echo "3. Run the agent: python3 tts_enhanced_agent.py"
echo ""
echo "📖 See TTS_QUICK_START.md for detailed instructions"
echo ""
echo "🎤 Your LED assistant is now ready for voice interaction!" 