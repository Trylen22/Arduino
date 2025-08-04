#!/usr/bin/env python3
"""
Simple Arduino LED Test Script
==============================

This script tests the Arduino LED control functionality.
"""

import serial
import time

def test_arduino_connection():
    """Test Arduino connection and LED control."""
    
    try:
        # Connect to Arduino
        print("Connecting to Arduino...")
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        
        # Wait for Arduino to reset
        print("Waiting for Arduino to reset...")
        time.sleep(3)
        
        # Clear any startup messages
        while ser.in_waiting:
            ser.read()
        
        print("Arduino ready! Testing LED control...")
        
        # Test Green LED ON
        print("\n1. Testing Green LED ON...")
        ser.write(b'2\n')
        ser.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while ser.in_waiting:
            response += ser.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Wait 2 seconds
        print("Green LED should be ON for 2 seconds...")
        time.sleep(2)
        
        # Test Green LED OFF
        print("\n2. Testing Green LED OFF...")
        ser.write(b'b\n')
        ser.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while ser.in_waiting:
            response += ser.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Test Red LED ON
        print("\n3. Testing Red LED ON...")
        ser.write(b'1\n')
        ser.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while ser.in_waiting:
            response += ser.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Wait 2 seconds
        print("Red LED should be ON for 2 seconds...")
        time.sleep(2)
        
        # Test Red LED OFF
        print("\n4. Testing Red LED OFF...")
        ser.write(b'a\n')
        ser.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while ser.in_waiting:
            response += ser.read().decode('utf-8')
        print(f"Response: {response}")
        
        # Test Status
        print("\n5. Testing Status Report...")
        ser.write(b'S\n')
        ser.flush()
        time.sleep(1)
        
        # Read response
        response = ""
        while ser.in_waiting:
            response += ser.read().decode('utf-8')
        print(f"Status: {response}")
        
        ser.close()
        print("\nTest completed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_arduino_connection() 