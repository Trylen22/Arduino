#!/usr/bin/env python3
"""
Arduino Communication Test Script
================================

This script tests direct communication with the Arduino by sending simple commands
and displaying the responses. It bypasses the natural language processing to help
isolate communication issues.

Usage:
    python3 test_arduino_communication.py
"""

import serial
import time
import sys

def main():
    """Main function to test Arduino communication."""
    # Default serial port and baud rate
    port = '/dev/ttyACM0'
    baud_rate = 9600
    
    # Check if a different port was specified
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    print(f"Testing Arduino communication on port {port} at {baud_rate} baud...")
    
    try:
        # Connect to Arduino
        arduino = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Allow time for Arduino to reset
        
        print("Connected to Arduino successfully!")
        print("\nAvailable commands:")
        print("  R - Turn Red LED ON")
        print("  r - Turn Red LED OFF")
        print("  G - Turn Green LED ON")
        print("  g - Turn Green LED OFF")
        print("  B - Turn Blue LED ON")
        print("  b - Turn Blue LED OFF")
        print("  W - Turn all RGB LEDs ON (White)")
        print("  w - Turn all RGB LEDs OFF")
        print("  F - Turn Fan ON")
        print("  f - Turn Fan OFF")
        print("  S - Send status report")
        print("  q - Quit")
        
        # Main command loop
        while True:
            # Get command from user
            command = input("\nEnter command: ").strip().upper()
            
            # Check if user wants to quit
            if command == 'Q':
                break
            
            # Send command to Arduino
            if command:
                print(f"Sending command: {command}")
                arduino.write(command.encode())
                arduino.flush()  # Ensure data is sent
                
                # Wait for response
                time.sleep(0.5)
                
                # Read and print response
                print("Arduino response:")
                while arduino.in_waiting:
                    line = arduino.readline().decode('utf-8').strip()
                    if line:
                        print(f"  {line}")
        
        # Close connection
        arduino.close()
        print("Connection closed.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Arduino is connected and the correct port is specified.")
        print("Try running: python3 test_arduino_communication.py /dev/ttyUSB0")
        print("or: python3 test_arduino_communication.py /dev/ttyACM1")

if __name__ == "__main__":
    main() 