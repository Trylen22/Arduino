# Arduino LED Control Agent

A Python-based intelligent agent that controls red and green LEDs on an Arduino board using natural language commands, voice recognition, and text-to-speech capabilities.

## 🌟 Features

- **Dual LED Control**: Control both red and green LEDs independently or together
- **Voice Recognition**: Speak commands to control the LEDs using your microphone
- **Text-to-Speech**: The agent responds with voice feedback
- **Natural Language Processing**: Use conversational commands like "turn on the red light" or "make both lights blink"
- **Local AI Integration**: Uses Ollama for local language model processing
- **Real-time Communication**: Direct serial communication with Arduino

## 🚀 Quick Start

### Prerequisites

- Arduino board (Uno, Nano, or similar)
- Red and green LEDs with resistors
- Python 3.8+
- Microphone for voice commands
- Speakers for text-to-speech output

### Hardware Setup

1. **Connect the LEDs to your Arduino:**
   ```
   Red LED:   Pin 13 -> LED -> 220Ω resistor -> GND
   Green LED: Pin 12 -> LED -> 220Ω resistor -> GND
   ```

2. **Upload the Arduino sketch:**
   - Open `Arduino_Agent/two_led_arduino/two_led_arduino.ino` in Arduino IDE
   - Upload to your Arduino board

### Software Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Trylen22/Arduino.git
   cd Arduino
   ```

2. **Install Python dependencies:**
   ```bash
   cd Arduino_Agent
   python -m venv tts_env
   source tts_env/bin/activate  # On Windows: tts_env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Ollama (for local AI processing):**
   ```bash
   # On Linux/macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull the language model
   ollama pull llama3.1:8b-instruct-q4_0
   ```

## 🎮 Usage

### Running the Agent

```bash
cd Arduino_Agent
python two_led_agent.py
```

### Available Commands

#### Text Commands
- `"turn on the red light"`
- `"turn off the green LED"`
- `"turn both lights on"`
- `"turn both lights off"`
- `"toggle the red light"`
- `"check status"`
- `"wait 3 seconds"`

#### Voice Commands
- Type `voice` to activate voice recognition
- Speak your commands naturally
- The agent will process and execute your voice commands

### Example Interactions

```
You: turn on the red light
Agent: [Turns on red LED]

You: voice
Agent: Listening... (speak now)
You: [speak] "turn on the green light"
Agent: [Turns on green LED]

You: make both lights blink
Agent: [Turns both LEDs on and off in sequence]
```

## 🔧 Configuration

### Arduino Connection
- **Default Port**: `/dev/ttyACM0` (Linux) or `COM3` (Windows)
- **Baud Rate**: 9600
- **Custom Port**: Modify the port parameter in `RedGreenLEDAssistant()`

### Voice Recognition
- **Microphone**: Automatically detects available microphones
- **Sensitivity**: Adjustable energy threshold for better recognition
- **Timeout**: 6-second listening window for voice commands

### AI Model
- **Default Model**: `llama3.1:8b-instruct-q4_0`
- **Custom Model**: Change the `model_name` parameter in the assistant initialization

## 📁 Project Structure

```
Arduino_Agent/
├── two_led_agent.py          # Main agent application
├── voice_selector.py          # Voice input handling
├── two_led_arduino/
│   └── two_led_arduino.ino   # Arduino sketch
├── tts_env/                  # Python virtual environment
└── requirements.txt           # Python dependencies
```

## 🛠️ Troubleshooting

### Common Issues

1. **Arduino not detected:**
   - Check USB connection
   - Verify correct port in code
   - Ensure Arduino drivers are installed

2. **Voice recognition not working:**
   - Check microphone permissions
   - Test microphone in system settings
   - Adjust energy threshold in code

3. **Ollama model not found:**
   - Run `ollama pull llama3.1:8b-instruct-q4_0`
   - Check Ollama installation

4. **LEDs not responding:**
   - Verify wiring connections
   - Check Arduino sketch upload
   - Test with Arduino IDE serial monitor

### Debug Mode

Enable debug output by checking the console for detailed command execution logs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🙏 Acknowledgments

- Built with Python, Arduino, and Ollama
- Uses speech recognition and text-to-speech libraries
- Inspired by the need for intuitive IoT control interfaces

---

**Happy LED controlling!** 💡✨ 