# Red & Green LED Control Project

This project provides a natural language interface to control a red LED and a green LED connected to an Arduino. The system uses a Python agent with voice and text input capabilities to interpret user commands and control the LEDs through serial communication.

## Project Structure

```
Arduino_Agent/
├── two_led_agent.py              # Python agent for controlling red & green LEDs
├── red_green_led_arduino.ino     # Arduino code for red & green LED control
└── README_two_led_project.md     # This file
```

## Hardware Requirements

### Arduino Setup
- Arduino Uno (or compatible board)
- 1x Red LED
- 1x Green LED
- 2x 220Ω resistors
- Breadboard and jumper wires

### Computer Setup
- Python 3.7+
- Required Python packages (see Installation section)
- Ollama installed with a language model (e.g., llama3.1:8b-instruct-q4_0)
- Microphone for voice commands

## Wiring Diagram

```
Arduino Pin 13 ──── 220Ω Resistor ──── Red LED ──── GND
Arduino Pin 12 ──── 220Ω Resistor ──── Green LED ──── GND
```

### Detailed Wiring Instructions

1. **Red LED (Pin 13)**:
   - Connect Arduino pin 13 to one end of a 220Ω resistor
   - Connect the other end of the resistor to the anode (longer leg) of the red LED
   - Connect the cathode (shorter leg) of the red LED to GND

2. **Green LED (Pin 12)**:
   - Connect Arduino pin 12 to one end of a 220Ω resistor
   - Connect the other end of the resistor to the anode (longer leg) of the green LED
   - Connect the cathode (shorter leg) of the green LED to GND

3. **USB Connection**:
   - Connect Arduino to your computer via USB cable

## Installation

### 1. Install Python Dependencies

```bash
pip install pyserial speechrecognition pyaudio
```

### 2. Install Ollama

Follow the instructions at [ollama.ai](https://ollama.ai) to install Ollama on your system.

### 3. Download a Language Model

```bash
ollama pull llama3.1:8b-instruct-q4_0
```

## Setup Instructions

### Step 1: Upload Arduino Code

1. Open the Arduino IDE
2. Load the `red_green_led_arduino.ino` file
3. Select your Arduino board and port
4. Upload the code to your Arduino

### Step 2: Test Arduino Connection

1. Open the Arduino Serial Monitor (Tools → Serial Monitor)
2. Set baud rate to 9600
3. You should see the startup message with available commands
4. Test a command by typing `1` and pressing Enter
5. Red LED should turn on

### Step 3: Configure Python Agent

1. Open `two_led_agent.py`
2. Update the port name if needed (default: `/dev/ttyACM0` on Linux)
3. Adjust microphone device index if needed (line 47)

### Step 4: Run the Agent

```bash
python two_led_agent.py
```

## Usage Examples

### Text Commands

The agent understands natural language commands:

```
You: Turn on the red LED
You: Switch off the green light
You: Toggle the red LED
You: Turn on both LEDs for 3 seconds then turn them off
You: What's the current status?
You: Make the LEDs blink alternately
You: Turn on the green LED and wait 2 seconds
You: Create a traffic light pattern - red on, wait 3 seconds, red off green on, wait 3 seconds, green off
```

### Voice Commands

Type `voice` to activate voice recognition, then speak your command.

### Direct Arduino Commands

You can also send direct commands to the Arduino:
- `1` - Turn Red LED ON
- `a` - Turn Red LED OFF
- `2` - Turn Green LED ON
- `b` - Turn Green LED OFF
- `3` - Turn both LEDs ON
- `c` - Turn both LEDs OFF
- `S` - Status report
- `t1` - Toggle Red LED
- `t2` - Toggle Green LED

## Troubleshooting

### Arduino Connection Issues

1. **Port not found**: Check if Arduino is connected and identify the correct port
   ```bash
   ls /dev/tty*
   ```

2. **Permission denied**: Add your user to the dialout group
   ```bash
   sudo usermod -a -G dialout $USER
   ```
   Then log out and log back in.

### Microphone Issues

1. **No microphone detected**: Check available microphones
   ```python
   import speech_recognition as sr
   print(sr.Microphone.list_microphone_names())
   ```

2. **Adjust device index**: Update the device_index in the code (line 47)

### Ollama Issues

1. **Model not found**: Download the model
   ```bash
   ollama pull llama3.1:8b-instruct-q4_0
   ```

2. **Ollama not running**: Start the Ollama service
   ```bash
   ollama serve
   ```

## Customization

### Adding More LEDs

1. Update the Arduino code to add more LED pins
2. Add corresponding control functions
3. Update the Python agent's device states and control methods
4. Modify the command protocol

### Changing LED Pins

Update the `RED_LED_PIN` and `GREEN_LED_PIN` constants in the Arduino code.

### Using Different Language Models

Change the `model_name` parameter when initializing the `RedGreenLEDAssistant`:

```python
assistant = RedGreenLEDAssistant(model_name="your-model-name")
```

## Advanced Features

### Creating LED Patterns

You can create custom patterns by combining commands with wait functions:

```
You: Create a traffic light pattern - turn on red LED, wait 3 seconds, turn off red and turn on green, wait 3 seconds, turn off green
```

### Traffic Light Simulation

The red and green LEDs are perfect for creating traffic light simulations:

```
You: Simulate a traffic light - red on for 5 seconds, then green on for 5 seconds, repeat
```

### Voice Control Integration

The system supports voice commands through Google's speech recognition service. Make sure you have an internet connection for voice features.

## Project Extensions

1. **Add a yellow LED**: Create a full traffic light system
2. **Add sensors**: Integrate motion sensors or light sensors
3. **Web interface**: Create a web-based control panel
4. **Mobile app**: Develop a mobile app for remote control
5. **Home automation**: Integrate with smart home systems
6. **Bluetooth control**: Add Bluetooth module for wireless control

## Creative Applications

1. **Traffic Light Simulator**: Use for educational purposes
2. **Status Indicators**: Red for error, green for success
3. **Game Controllers**: Use LEDs as visual feedback
4. **Art Installations**: Create light patterns and displays
5. **Safety Systems**: Emergency lighting or warning systems

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

---

**Happy coding!** 🚀 