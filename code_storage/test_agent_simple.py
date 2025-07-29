#!/usr/bin/env python3
"""
Simple Test for Two LED Agent
==============================

This script tests the Arduino communication without speech recognition.
"""

import serial
import time
import subprocess
import re

# ===== SIMPLIFIED ASSISTANT CLASS =====
class SimpleLEDAssistant:
    """Simplified assistant without speech recognition."""
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600):
        """Initialize the assistant with Arduino connection."""
        
        # Initialize device states (tracked locally)
        self.device_states = {
            'red_led': False,
            'green_led': False
        }
        
        # ===== ARDUINO CONNECTION =====
        try:
            # Attempt to connect to Arduino
            print(f"\nAttempting to connect to Arduino on port {port} at {baud_rate} baud...")
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Allow time for Arduino to reset
            print("\nHi! I'm your Red & Green LED assistant!")
            
            # Test Arduino connection with a simple command
            print("\nTesting Arduino connection...")
            self.arduino.write(b'S\n')  # Add newline
            self.arduino.flush()
            time.sleep(1)
            if self.arduino.in_waiting:
                response = self.arduino.readline().decode('utf-8').strip()
                print(f"Arduino response: {response}")
                print("Arduino connection test successful!")
            else:
                print("WARNING: No response from Arduino. Communication may be one-way.")
        except Exception as e:
            # Handle Arduino connection errors
            print("\nOops! I couldn't connect to the Arduino.")
            print(f"Error: {e}")
            self.arduino = None

    def _control_red_led_on(self):
        """Turn Red LED on."""
        if self.arduino:
            try:
                print("DEBUG: Sending '1' command to Arduino (Red LED ON)")
                self.arduino.write(b'1\n')
                self.arduino.flush()
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = True
                return True
            except Exception as e:
                print("Error turning Red LED on:", e)
                return False

    def _control_green_led_on(self):
        """Turn Green LED on."""
        if self.arduino:
            try:
                print("DEBUG: Sending '2' command to Arduino (Green LED ON)")
                self.arduino.write(b'2\n')
                self.arduino.flush()
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['green_led'] = True
                return True
            except Exception as e:
                print("Error turning Green LED on:", e)
                return False

    def _control_both_leds_on(self):
        """Turn both LEDs on."""
        if self.arduino:
            try:
                print("DEBUG: Sending '3' command to Arduino (Both LEDs ON)")
                self.arduino.write(b'3\n')
                self.arduino.flush()
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = True
                self.device_states['green_led'] = True
                return True
            except Exception as e:
                print("Error turning both LEDs on:", e)
                return False

    def _control_both_leds_off(self):
        """Turn both LEDs off."""
        if self.arduino:
            try:
                print("DEBUG: Sending 'c' command to Arduino (Both LEDs OFF)")
                self.arduino.write(b'c\n')
                self.arduino.flush()
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = False
                self.device_states['green_led'] = False
                return True
            except Exception as e:
                print("Error turning both LEDs off:", e)
                return False

    def close(self):
        """Close the Arduino connection."""
        if self.arduino:
            self.arduino.close()
            print("Goodbye!")

# ===== SIMPLIFIED AGENT =====
class SimpleLEDAgent:
    """Simplified agent for testing."""
    
    def __init__(self, assistant: SimpleLEDAssistant):
        """Initialize the agent."""
        self.assistant = assistant
        
        # Map tool names to assistant methods
        self.tools = {
            "control_red_led_on": assistant._control_red_led_on,
            "control_green_led_on": assistant._control_green_led_on,
            "control_both_leds_on": assistant._control_both_leds_on,
            "control_both_leds_off": assistant._control_both_leds_off,
        }
    
    def run(self, user_input):
        """Execute a simple command."""
        print(f"\nProcessing: {user_input}")
        
        if "both" in user_input.lower() and "on" in user_input.lower():
            print("Executing: control_both_leds_on()")
            self.tools["control_both_leds_on"]()
        elif "both" in user_input.lower() and "off" in user_input.lower():
            print("Executing: control_both_leds_off()")
            self.tools["control_both_leds_off"]()
        elif "red" in user_input.lower() and "on" in user_input.lower():
            print("Executing: control_red_led_on()")
            self.tools["control_red_led_on"]()
        elif "green" in user_input.lower() and "on" in user_input.lower():
            print("Executing: control_green_led_on()")
            self.tools["control_green_led_on"]()
        else:
            print("Command not recognized. Try: 'turn both LEDs on' or 'turn both LEDs off'")

# ===== MAIN PROGRAM =====
if __name__ == "__main__":
    # Create the assistant and agent instances
    assistant = SimpleLEDAssistant()
    agent = SimpleLEDAgent(assistant)
    
    # Main interaction loop
    print("\nAgent ready! Type your command (or 'bye' to exit):")
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Handle special commands
        if user_input.lower() in ['bye', 'exit']:
            break
        else:
            # Process text input
            agent.run(user_input)
    
    # Clean up resources
    assistant.close() 