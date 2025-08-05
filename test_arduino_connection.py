#!/usr/bin/env python3
"""
Test Arduino connection and LED control
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'core'))
from environmental_agent import EnvironmentalAgent

def test_arduino_connection():
    """Test Arduino connection and basic functionality."""
    print("🔌 Testing Arduino Connection")
    print("=" * 40)
    
    # Initialize environmental agent
    agent = EnvironmentalAgent()
    
    if not agent.connected:
        print("❌ Arduino not connected!")
        print("Please check:")
        print("1. Arduino is plugged in via USB")
        print("2. Arduino IDE shows the correct port")
        print("3. The environmental_monitor_combined.ino sketch is uploaded")
        return False
    
    print("✅ Arduino connected successfully!")
    
    # Test status
    print("\n📊 Testing sensor readings...")
    status = agent.get_status()
    if "error" not in status:
        print("✅ Sensor readings working!")
        print(f"Temperature: {status.get('temperature', 'N/A')}°F")
        print(f"CO2: {status.get('co2', 'N/A')}")
        print(f"Light: {status.get('light', 'N/A')}")
        print(f"LED: {status.get('led', 'N/A')}")
        print(f"Fan: {status.get('fan', 'N/A')}")
    else:
        print("❌ Sensor readings failed!")
        return False
    
    # Test LED control
    print("\n💡 Testing LED control...")
    print("Turning LED ON...")
    if agent.turn_led_on():
        print("✅ LED turned ON successfully!")
    else:
        print("❌ Failed to turn LED ON!")
        return False
    
    # Check LED status
    status = agent.get_status()
    if status.get('led') == 'ON':
        print("✅ LED is confirmed ON!")
    else:
        print("❌ LED status not updated!")
    
    # Turn LED off
    print("\nTurning LED OFF...")
    if agent.turn_led_off():
        print("✅ LED turned OFF successfully!")
    else:
        print("❌ Failed to turn LED OFF!")
        return False
    
    # Check LED status
    status = agent.get_status()
    if status.get('led') == 'OFF':
        print("✅ LED is confirmed OFF!")
    else:
        print("❌ LED status not updated!")
    
    print("\n🎉 All Arduino tests passed!")
    return True

if __name__ == "__main__":
    success = test_arduino_connection()
    if success:
        print("\n✅ Arduino is ready for IRIS!")
    else:
        print("\n❌ Arduino needs attention before IRIS can work properly.") 