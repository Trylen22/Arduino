#!/bin/bash

# Environmental Monitoring System - Cleanup Script
# This script removes old and duplicate files after reorganization

echo "🧹 Cleaning up Environmental Monitoring System Repository..."
echo "========================================================"

# Remove old files that are no longer needed
echo "🗑️ Removing old files..."

# Remove old agent files (now in legacy)
rm -f voice_environmental_agent.py
rm -f voice_environmental_agent_modular.py
rm -f voice_interface_fixed.py
rm -f agent.py
rm -f two_led_agent.py
rm -f llm_tts_agent.py
rm -f tts_enhanced_agent.py

# Remove old tool files (now in tools/)
rm -f voice_selector.py
rm -f test_voice_quality.py
rm -f set_preferred_voice.py
rm -f set_best_voice.py

# Remove old documentation files (now in docs/)
rm -f CIRCUIT_TESTING_GUIDE.md
rm -f system_improvements.md
rm -f TTS_QUICK_START.md

# Remove old Arduino files (now in arduino/)
rm -f arduino_code/simple_test_*.ino
rm -f arduino_code/test_*.ino
rm -f arduino_code/*.ino

# Remove old directories
rm -rf arduino_code/code_storage
rm -rf arduino_code/two_led
rm -rf arduino_code/led_fan_control
rm -rf arduino_code/sketch_feb12a
rm -rf two_led_arduino

# Remove old setup files
rm -f activate_tts.sh
rm -f setup_tts.sh
rm -f requirements_tts.txt

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Old files removed"

# Remove empty directories
echo "📁 Removing empty directories..."
find . -type d -empty -delete 2>/dev/null || true

echo "✅ Empty directories removed"

# Create a summary of the new structure
echo ""
echo "📋 New Repository Structure:"
echo "============================"
echo ""
echo "Arduino_Agent/"
echo "├── README.md                           # Project documentation"
echo "├── requirements.txt                    # Python dependencies"
echo "├── setup.sh                          # Quick setup script"
echo "├── reorganize.sh                     # This reorganization script"
echo "├── cleanup.sh                        # This cleanup script"
echo "│"
echo "├── arduino/                          # Arduino code"
echo "│   ├── environmental_monitor_combined.ino  # Main sketch"
echo "│   ├── simple_tests/                 # Individual sensor tests"
echo "│   └── legacy/                       # Old/experimental code"
echo "│"
echo "├── agents/                           # Python agents"
echo "│   ├── core/                         # Core agent classes"
echo "│   ├── interfaces/                   # Interface modules"
echo "│   └── examples/                     # Example implementations"
echo "│"
echo "├── tools/                            # Utility tools"
echo "├── docs/                             # Documentation"
echo "└── config/                           # Configuration files"
echo ""

echo "🎉 Repository cleanup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Run: chmod +x reorganize.sh"
echo "   2. Run: ./reorganize.sh"
echo "   3. Run: ./cleanup.sh"
echo "   4. Test the system: python agents/examples/voice_environmental_agent_modern.py"
echo ""
echo "📚 See README.md for full documentation" 