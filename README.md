# Environmental Monitoring System
================================

A sophisticated environmental monitoring system with Arduino sensors, LLM intelligence, and modern voice interface.

## 🎯 Project Overview

This system combines:
- **Arduino sensors** (CO2, Temperature, Light, LED control)
- **LLM intelligence** (Ollama integration for smart decisions)
- **Modern voice interface** (Google TTS for natural speech)
- **Environmental analysis** (Real-time monitoring and alerts)

## 📁 Project Structure

```
Arduino_Agent/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── setup.sh                          # Quick setup script
│
├── arduino/                          # Arduino code
│   ├── environmental_monitor_combined.ino  # Main Arduino sketch
│   ├── simple_tests/                 # Individual sensor tests
│   └── legacy/                       # Old/experimental code
│
├── agents/                           # Python agents
│   ├── core/                         # Core agent classes
│   │   ├── environmental_agent.py    # Base environmental agent
│   │   ├── intelligent_agent.py      # LLM-powered agent
│   │   └── voice_agent.py           # Voice-enabled agent
│   │
│   │   ├── interfaces/               # Interface modules
│   │   ├── voice_interface.py       # Voice/TTS interface
│   │   ├── llm_interface.py         # LLM query interface
│   │   └── modern_voice_interface.py # Modern TTS interface
│   │
│   │   └── examples/                 # Example implementations
│   │   ├── voice_environmental_agent_modern.py  # Main modern agent
│   │   └── interactive_environmental_agent.py   # Interactive agent
│
├── tools/                            # Utility tools
│   ├── voice_selector.py            # Voice testing tool
│   ├── test_voice_quality.py        # Voice quality tester
│   └── set_preferred_voice.py       # Voice configuration
│
├── docs/                             # Documentation
│   ├── CIRCUIT_TESTING_GUIDE.md     # Hardware setup guide
│   ├── system_improvements.md        # Future improvements
│   └── TTS_QUICK_START.md          # Voice setup guide
│
└── config/                           # Configuration files
    └── settings.json                 # System settings
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Activate virtual environment
source tts_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Upload Arduino Code
```bash
# Upload the main sketch to your Arduino
# File: arduino/environmental_monitor_combined.ino
```

### 3. Run the System
```bash
# Run the modern voice-enabled agent
python agents/examples/voice_environmental_agent_modern.py
```

## 🎤 Voice Commands

Try these voice commands:
- "What's the temperature?"
- "Turn on the LED"
- "Turn off the LED"
- "What's the environmental status?"
- "Analyze the environment"
- "How's the air quality?"

## 🔧 System Features

### **Sensors**
- **CO2 Sensor (MQ-135)** - Air quality monitoring
- **Thermistor** - Temperature measurement (calibrated)
- **Photoresistor** - Light level detection
- **LED** - Visual indicator and control

### **Intelligence**
- **LLM Integration** - Ollama with llama3.1:8b-instruct-q4_0
- **Smart Analysis** - Environmental condition assessment
- **Voice Interface** - Google TTS for natural speech
- **Command Processing** - Natural language understanding

### **Voice Quality**
- **Modern TTS** - Google Text-to-Speech
- **Natural Speech** - No letter-by-letter spelling
- **Professional Quality** - Clear, human-like voice
- **Emotional Responses** - Context-aware voice feedback

## 📊 Environmental Analysis

The system provides:
- **Temperature analysis** - Comfort level assessment
- **CO2 monitoring** - Air quality evaluation
- **Light level analysis** - Lighting condition assessment
- **Smart recommendations** - LLM-powered suggestions

## 🛠️ Development

### **Adding New Sensors**
1. Create Arduino test sketch in `arduino/simple_tests/`
2. Add sensor reading to `environmental_monitor_combined.ino`
3. Update `environmental_agent.py` to handle new sensor
4. Test with voice commands

### **Voice Improvements**
- Use `tools/voice_selector.py` to test different voices
- Modify `agents/interfaces/modern_voice_interface.py` for voice settings
- Test with `tools/test_voice_quality.py`

### **LLM Enhancements**
- Update prompts in agent files
- Modify `agents/interfaces/llm_interface.py` for different models
- Test with `agents/examples/interactive_environmental_agent.py`

## 🔄 System Architecture

```
Arduino Sensors → Environmental Agent → LLM Interface → Voice Interface
     ↓                    ↓                    ↓              ↓
  Raw Data → Processed Data → Intelligent Analysis → Voice Response
```

## 📈 Future Improvements

See `docs/system_improvements.md` for detailed improvement roadmap:
- **Hardware expansion** (humidity, air quality sensors)
- **AI enhancements** (predictive analytics, anomaly detection)
- **User interface** (web dashboard, mobile app)
- **Automation** (smart controls, scheduling)
- **Data analytics** (logging, visualization)

## 🐛 Troubleshooting

### **Voice Issues**
```bash
# Test voice quality
python tools/test_voice_quality.py

# Select preferred voice
python tools/set_preferred_voice.py
```

### **Arduino Connection**
```bash
# Check connection
python agents/examples/interactive_environmental_agent.py
```

### **LLM Issues**
```bash
# Test LLM connection
python agents/examples/intelligent_environmental_agent.py
```

## 📝 License

This project is open source. Feel free to modify and improve!

## 🤝 Contributing

1. Test your changes thoroughly
2. Update documentation
3. Follow the existing code structure
4. Add voice commands for new features

---

**Happy environmental monitoring! 🌍✨** 