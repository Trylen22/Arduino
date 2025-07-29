#!/usr/bin/env python3
"""
Environmental Monitoring Agent
=============================

Python agent that communicates with the Arduino environmental monitoring system.
Provides a simple interface for LLM control of sensors and actuators.

Author: [Your Name]
Date: [2025-01-27]
"""

import serial
import time
import json
from typing import Dict, Any, Optional

class EnvironmentalAgent:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600):
        """Initialize the environmental monitoring agent."""
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = None
        self.connected = False
        
        # Try to connect to Arduino
        try:
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Allow Arduino to reset
            self.connected = True
            print(f"✅ Connected to Arduino on {port}")
            print("Environmental monitoring system ready!")
        except Exception as e:
            print(f"❌ Failed to connect to Arduino: {e}")
            self.connected = False
    
    def send_command(self, command: str) -> Optional[str]:
        """Send a command to Arduino and return response."""
        if not self.connected or not self.arduino:
            return None
        
        try:
            # Send command with newline
            self.arduino.write(f"{command}\n".encode())
            time.sleep(0.1)  # Small delay for processing
            
            # Read response
            response = ""
            while self.arduino.in_waiting:
                line = self.arduino.readline().decode().strip()
                if line:
                    response += line + "\n"
            
            return response.strip() if response else None
        except Exception as e:
            print(f"Error sending command: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get complete status of all sensors and actuators."""
        response = self.send_command("S")
        if not response:
            return {"error": "No response from Arduino"}
        
        # Parse status report
        status = {}
        lines = response.split('\n')
        
        for line in lines:
            if "LED:" in line:
                status["led"] = "ON" if "ON" in line else "OFF"
            elif "Temperature:" in line:
                temp_str = line.split("Temperature: ")[1].replace("°F", "")
                status["temperature"] = float(temp_str)
            elif "CO2:" in line:
                co2_str = line.split("CO2: ")[1]
                status["co2"] = int(co2_str)
            elif "Light:" in line:
                light_str = line.split("Light: ")[1]
                status["light"] = int(light_str)
        
        return status
    
    def get_temperature(self) -> Optional[float]:
        """Get temperature reading only."""
        response = self.send_command("T")
        if response and "TEMP:" in response:
            temp_str = response.split("TEMP:")[1].strip()
            return float(temp_str)
        return None
    
    def get_co2(self) -> Optional[int]:
        """Get CO2 reading only."""
        response = self.send_command("C")
        if response and "CO2:" in response:
            co2_str = response.split("CO2:")[1].strip()
            return int(co2_str)
        return None
    
    def get_light(self) -> Optional[int]:
        """Get light level reading only."""
        response = self.send_command("P")
        if response and "LIGHT:" in response:
            light_str = response.split("LIGHT:")[1].strip()
            return int(light_str)
        return None
    
    def get_all_readings(self) -> Dict[str, Any]:
        """Get all sensor readings in one call."""
        response = self.send_command("A")
        if response and "ALL:" in response:
            data_str = response.split("ALL:")[1].strip()
            temp, co2, light = data_str.split(",")
            return {
                "temperature": float(temp),
                "co2": int(co2),
                "light": int(light)
            }
        return {"error": "Failed to get readings"}
    
    def turn_led_on(self) -> bool:
        """Turn LED on."""
        response = self.send_command("L1")
        return response and "LED: ON" in response
    
    def turn_led_off(self) -> bool:
        """Turn LED off."""
        response = self.send_command("L0")
        return response and "LED: OFF" in response
    
    def close(self):
        """Close the serial connection."""
        if self.arduino:
            self.arduino.close()
            print("Connection closed.")

# Example usage and testing
def main():
    """Test the environmental agent."""
    agent = EnvironmentalAgent()
    
    if not agent.connected:
        print("Cannot test without Arduino connection.")
        return
    
    print("\n=== Testing Environmental Agent ===")
    
    # Test LED control
    print("\n1. Testing LED control...")
    agent.turn_led_on()
    time.sleep(2)
    agent.turn_led_off()
    
    # Test sensor readings
    print("\n2. Testing sensor readings...")
    status = agent.get_status()
    print(f"Status: {json.dumps(status, indent=2)}")
    
    # Test individual readings
    print("\n3. Testing individual readings...")
    temp = agent.get_temperature()
    co2 = agent.get_co2()
    light = agent.get_light()
    
    print(f"Temperature: {temp}°C")
    print(f"CO2: {co2}")
    print(f"Light: {light}")
    
    # Test all readings
    print("\n4. Testing all readings...")
    all_readings = agent.get_all_readings()
    print(f"All readings: {json.dumps(all_readings, indent=2)}")
    
    agent.close()

if __name__ == "__main__":
    main() 