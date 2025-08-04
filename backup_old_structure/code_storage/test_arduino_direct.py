#!/usr/bin/env python3
"""
Direct Arduino Communication Test
================================

This script tests direct communication with the Arduino to verify the protocol.
"""

import serial
import time

def test_arduino_communication():
    """Test Arduino communication with different command formats."""
    
    try:
        # Connect to Arduino
        print("Connecting to Arduino...")
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # Allow Arduino to reset
        
        # Clear any startup messages
        while arduino.in_waiting:
            arduino.read()
        
        print("Arduino connected! Testing different command formats...")
        
        # Test 1: Single character without newline (current Python agent method)
        print("\n=== Test 1: Single character without newline ===")
        print("Sending: '2' (without newline)")
        arduino.write(b'2')
        arduino.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while arduino.in_waiting:
            response += arduino.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Test 2: Single character with newline
        print("\n=== Test 2: Single character with newline ===")
        print("Sending: '2\\n' (with newline)")
        arduino.write(b'2\n')
        arduino.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while arduino.in_waiting:
            response += arduino.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Test 3: Turn off green LED
        print("\n=== Test 3: Turn off green LED ===")
        print("Sending: 'b\\n'")
        arduino.write(b'b\n')
        arduino.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while arduino.in_waiting:
            response += arduino.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Test 4: Status request
        print("\n=== Test 4: Status request ===")
        print("Sending: 'S\\n'")
        arduino.write(b'S\n')
        arduino.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while arduino.in_waiting:
            response += arduino.read().decode('utf-8')
        print(f"Response: {response}")
        
        arduino.close()
        print("\nTest completed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_arduino_communication() 