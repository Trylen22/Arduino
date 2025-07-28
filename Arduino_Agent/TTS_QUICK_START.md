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
