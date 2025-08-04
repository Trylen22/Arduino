# LED and Fan Control System

This project provides a Python agent that can control an LED and a fan connected to an Arduino board. The system supports both text and voice commands.

## Components

- **led_fan_agent.py**: Python agent that processes user commands and communicates with the Arduino
- **led_fan_control.ino**: Arduino sketch that controls the LED and fan based on serial commands

## Hardware Requirements

- Arduino board (Uno, Nano, or similar)
- LED (connected to pin 8)
- Fan (connected to pin 13)
- USB cable to connect Arduino to computer
- Microphone (optional, for voice commands)

## Software Requirements

- Python 3.6+
- Required Python packages:
  - pyserial
  - speech_recognition
  - subprocess
  - threading
  - re

## Installation

1. Install the required Python packages:
   ```
   pip install pyserial speech_recognition
   ```

2. Upload the `led_fan_control.ino` sketch to your Arduino board using the Arduino IDE.

3. Connect your Arduino to your computer via USB.

## Usage

1. Run the Python agent:
   ```
   python led_fan_agent.py
   ```

2. The agent will attempt to connect to the Arduino and initialize the microphone (if available).

3. You can control the LED and fan using text commands or voice commands:
   - Type your command and press Enter
   - Type "voice" to use voice commands
   - Type "bye" or "exit" to quit the program

## Available Commands

The agent understands natural language commands. Here are some examples:

- "Turn on the LED"
- "Turn off the fan"
- "Turn both on"
- "Turn both off"
- "Toggle the LED"
- "Toggle the fan"
- "What's the status of the devices?"
- "Check the status"

## Communication Protocol

The Python agent communicates with the Arduino using the following commands:

- `L` - Turn LED ON
- `l` - Turn LED OFF
- `F` - Turn Fan ON
- `f` - Turn Fan OFF
- `B` - Turn both ON
- `b` - Turn both OFF
- `S` - Request status report

## Troubleshooting

- If the agent cannot connect to the Arduino, check:
  - The Arduino is properly connected to your computer
  - The correct port is specified in the `LEDFanAssistant` initialization
  - The baud rate matches between the Python agent and Arduino sketch (9600)

- If voice commands are not working:
  - Check that your microphone is properly connected
  - Adjust the `device_index` in the `LEDFanAssistant` initialization to match your microphone

- If commands are not being recognized:
  - Check the serial monitor in the Arduino IDE to see if commands are being received
  - Ensure the Arduino sketch is properly uploaded and running

## Extending the System

You can extend this system by:

1. Adding more devices to control
2. Implementing more complex control patterns
3. Adding temperature sensing and automatic control
4. Creating a web interface for remote control
5. Adding more status information (e.g., temperature readings)

## License

This project is open source and available for personal and educational use. 