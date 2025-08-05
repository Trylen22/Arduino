# IRIS Student Companion AI
==========================

An AI study companion that combines environmental monitoring with emotional support to help students study better and feel supported.

## 🎯 Project Overview

IRIS is an intelligent study companion that:

- **Monitors your study environment** (temperature, air quality, lighting)
- **Provides emotional support** and encouragement during study sessions
- **Tracks study habits** and suggests optimal break times
- **Controls the environment** (LED lighting, fan) for better studying
- **Offers personalized advice** based on your study patterns and mood

## 🎓 Student-Focused Features

### **Emotional Support**
- Detects stress and provides calming responses
- Offers encouragement and motivation
- Helps with study-related anxiety
- Celebrates achievements and progress

### **Study Assistance**
- Tracks study session duration
- Recommends optimal break times
- Provides study advice and tips
- Monitors environmental comfort

### **Environmental Intelligence**
- Monitors temperature, CO2, and lighting
- Automatically adjusts environment for optimal studying
- Provides environmental recommendations
- Ensures comfortable study conditions

## 🚀 Quick Start for Presentation

### 1. Setup Environment
```bash
# Navigate to the project directory
cd Arduino_Agent

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

### 3. Run the Demo
```bash
# Run the presentation demo
python demo_student_companion.py

# Or run the main student companion
python agents/examples/student_companion_ai.py
```

## 🎤 Presentation Demo Commands

### **Automated Demo**
```bash
python demo_student_companion.py
# Choose option 1 for automated presentation demo
```

### **Interactive Demo**
```bash
python demo_student_companion.py
# Choose option 2 for interactive demo
```

### **Natural Conversation Examples**
- "I'm stressed about my exam tomorrow"
- "I've been studying for 2 hours, should I take a break?"
- "The room feels stuffy, can you help?"
- "I need some motivation"
- "start session" - Begin studying
- "end session" - Finish studying

## 📁 Project Structure

```
Arduino_Agent/
├── README.md                           # This file
├── demo_student_companion.py           # Presentation demo script
├── requirements.txt                    # Python dependencies
├── agents/
│   ├── core/
│   │   ├── environmental_agent.py     # Arduino communication
│   │   ├── smart_monitor.py           # Environmental monitoring
│   │   ├── message_generators.py      # Student-focused messages
│   │   └── student_companion.py       # Student companion logic
│   ├── interfaces/
│   │   ├── llm_interface.py           # AI personality and responses
│   │   └── modern_voice_interface.py  # Voice interaction
│   └── examples/
│       └── student_companion_ai.py    # Main student companion system
├── arduino/
│   └── environmental_monitor_combined.ino
└── tools/
    └── voice_selector.py
```

## 🎯 Key Features for Students

### **Environmental Monitoring**
- **Temperature monitoring** - Ensures comfortable study conditions
- **CO2 monitoring** - Maintains good air quality for focus
- **Light monitoring** - Optimizes lighting for eye comfort
- **Automatic control** - LED and fan control for comfort

### **Emotional Intelligence**
- **Mood detection** - Recognizes stress, frustration, excitement
- **Personalized responses** - Tailored support based on emotional state
- **Stress management** - Breathing exercises and calming techniques
- **Motivation** - Encouragement and celebration of progress

### **Study Habit Coaching**
- **Session tracking** - Monitors study time and breaks
- **Break reminders** - Suggests optimal break times
- **Progress celebration** - Acknowledges achievements
- **Study advice** - Personalized tips and strategies

## 🎤 Voice Commands

### **Study Session Commands**
- "start session" - Begin a study session
- "end session" - End current study session
- "take break" - Take a study break
- "stats" - Get study statistics

### **Support Commands**
- "support" - Get emotional support
- "advice" - Get study advice
- "environment" - Get environmental help
- "analyze" - Full environmental and student analysis

### **Environmental Commands**
- "status" - Check environmental status
- "turn on LED" - Improve lighting
- "turn on fan" - Improve air circulation

## 🔧 System Features

### **Hardware Integration**
- **Arduino sensors** (CO2, Temperature, Light, LED control, Fan control)
- **Real-time monitoring** - Continuous environmental assessment
- **Automatic control** - Smart environment adjustments

### **AI Intelligence**
- **LLM integration** - Ollama with student-focused personality
- **Emotional analysis** - Mood and stress level detection
- **Contextual responses** - Environment + emotional state awareness
- **Proactive interventions** - Automatic suggestions for better studying

### **Voice Interface**
- **Natural conversation** - Talk to IRIS like a study buddy
- **High-quality TTS** - Google TTS for natural speech
- **Emotional voice** - Supportive and encouraging tone

## 🎓 Student Use Cases

### **Study Session Management**
1. **Start session** - IRIS welcomes you and begins tracking
2. **Environmental check** - IRIS monitors your study environment
3. **Proactive support** - IRIS suggests improvements and breaks
4. **Emotional support** - IRIS provides encouragement and stress relief
5. **End session** - IRIS celebrates your progress and summarizes

### **Stress Management**
- **Stress detection** - IRIS recognizes when you're stressed
- **Calming responses** - Breathing exercises and encouragement
- **Environmental adjustments** - Comfort improvements for stress relief
- **Break suggestions** - Optimal timing for stress reduction

### **Study Optimization**
- **Environment monitoring** - Ensures optimal study conditions
- **Break timing** - Suggests breaks based on study duration
- **Motivation** - Provides encouragement and celebrates progress
- **Personalized advice** - Study tips based on your patterns

## 🚀 Future Enhancements

### **Advanced Features**
- **Study goal tracking** - Set and monitor academic goals
- **Progress analytics** - Detailed study session insights
- **Social features** - Study group coordination
- **Integration** - Calendar and task management

### **Hardware Expansion**
- **Humidity sensor** - Complete environmental monitoring
- **Noise monitoring** - Sound level assessment
- **Motion detection** - Study session validation
- **Smart lighting** - Advanced lighting control

## 🤝 Contributing

This project is designed to help students study better. Contributions that improve:
- Student experience
- Emotional support capabilities
- Environmental monitoring
- Study habit coaching

Are all welcome!

---

**Happy studying with IRIS! 🎓✨**
