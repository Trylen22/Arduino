#!/bin/bash

# Environmental Monitoring System - Repository Reorganization Script
# This script reorganizes the repository into a clean, structured layout

echo "🧹 Reorganizing Environmental Monitoring System Repository..."
echo "========================================================"

# Create new directory structure
echo "📁 Creating directory structure..."

mkdir -p arduino/simple_tests
mkdir -p arduino/legacy
mkdir -p agents/core
mkdir -p agents/interfaces
mkdir -p agents/examples
mkdir -p tools
mkdir -p docs
mkdir -p config

echo "✅ Directory structure created"

# Move Arduino files
echo "🔧 Organizing Arduino files..."

# Move main Arduino sketch
mv arduino_code/environmental_monitor_combined.ino arduino/

# Move simple test files
mv arduino_code/simple_test_*.ino arduino/simple_tests/

# Move legacy Arduino files
mv arduino_code/test_*.ino arduino/legacy/
mv arduino_code/*.ino arduino/legacy/ 2>/dev/null || true

echo "✅ Arduino files organized"

# Move agent files
echo "🤖 Organizing agent files..."

# Move core agents
mv environmental_agent.py agents/core/
mv intelligent_environmental_agent.py agents/core/intelligent_agent.py
mv voice_environmental_agent_modern.py agents/examples/
mv interactive_environmental_agent.py agents/examples/

# Move interface files
mv voice_interface.py agents/interfaces/
mv modern_voice_interface.py agents/interfaces/
mv llm_interface.py agents/interfaces/

# Move legacy agent files
mv voice_environmental_agent.py agents/legacy/ 2>/dev/null || true
mv voice_environmental_agent_modular.py agents/legacy/ 2>/dev/null || true
mv voice_interface_fixed.py agents/legacy/ 2>/dev/null || true
mv agent.py agents/legacy/ 2>/dev/null || true
mv two_led_agent.py agents/legacy/ 2>/dev/null || true
mv llm_tts_agent.py agents/legacy/ 2>/dev/null || true
mv tts_enhanced_agent.py agents/legacy/ 2>/dev/null || true

echo "✅ Agent files organized"

# Move tool files
echo "🛠️ Organizing tool files..."

mv voice_selector.py tools/
mv test_voice_quality.py tools/
mv set_preferred_voice.py tools/
mv set_best_voice.py tools/

echo "✅ Tool files organized"

# Move documentation files
echo "📚 Organizing documentation files..."

mv CIRCUIT_TESTING_GUIDE.md docs/
mv system_improvements.md docs/
mv TTS_QUICK_START.md docs/

echo "✅ Documentation files organized"

# Clean up old directories
echo "🧹 Cleaning up old directories..."

rm -rf arduino_code/code_storage 2>/dev/null || true
rm -rf arduino_code/two_led 2>/dev/null || true
rm -rf arduino_code/led_fan_control 2>/dev/null || true
rm -rf arduino_code/sketch_feb12a 2>/dev/null || true
rm -rf two_led_arduino 2>/dev/null || true

echo "✅ Old directories cleaned up"

# Create configuration file
echo "⚙️ Creating configuration file..."

cat > config/settings.json << 'EOF'
{
    "arduino": {
        "port": "/dev/ttyACM0",
        "baud_rate": 9600
    },
    "llm": {
        "model": "llama3.1:8b-instruct-q4_0",
        "timeout": 30
    },
    "voice": {
        "model": "gtts",
        "rate": 150,
        "volume": 0.9,
        "microphone_index": 9
    },
    "sensors": {
        "co2_pin": "A0",
        "thermistor_pin": "A5",
        "photoresistor_pin": "A2",
        "led_pin": 3,
        "fan_pin": 8
    },
    "calibration": {
        "thermistor_coefficient": 0.0916,
        "thermistor_offset": -22.8683
    }
}
EOF

echo "✅ Configuration file created"

# Update requirements.txt
echo "📦 Updating requirements file..."

cat > requirements.txt << 'EOF'
# Core dependencies
pyserial>=3.5
SpeechRecognition>=3.8.1
pyttsx3>=2.90

# Modern TTS
gTTS>=2.3.1
pygame>=2.1.2
edge-tts>=6.1.9

# LLM integration
subprocess.run

# Optional: Coqui TTS (uncomment if needed)
# TTS>=0.13.0

# Optional: Piper TTS (install system-wide)
# sudo apt install piper-tts
EOF

echo "✅ Requirements file updated"

# Create setup script
echo "🚀 Creating setup script..."

cat > setup.sh << 'EOF'
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
EOF

chmod +x setup.sh

echo "✅ Setup script created"

# Create .gitignore
echo "📝 Creating .gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
tts_env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
temp_speech.wav
temp_speech.mp3
*.log
.env

# Arduino
*.hex
*.elf
*.bin
EOF 