#!/usr/bin/env python3
"""
Fan Integration Test
===================

Simple test script to verify fan control integration.
"""

import sys
import os
import time

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'core'))
from environmental_agent import EnvironmentalAgent

def test_fan_integration():
    """Test fan control functionality."""
    print("🧪 Testing Fan Integration")
    print("=" * 40)
    
    # Initialize the environmental agent
    agent = EnvironmentalAgent()
    
    if not agent.connected:
        print("❌ Cannot test without Arduino connection.")
        return False
    
    print("✅ Connected to Arduino")
    
    # Test 1: Get initial status
    print("\n1. Getting initial status...")
    status = agent.get_status()
    print(f"   Initial status: {status}")
    
    # Test 2: Turn fan on
    print("\n2. Testing fan ON...")
    success = agent.turn_fan_on()
    print(f"   Fan ON result: {success}")
    
    if success:
        time.sleep(2)  # Let the fan run for a moment
        
        # Test 3: Check status with fan on
        print("\n3. Checking status with fan ON...")
        status = agent.get_status()
        print(f"   Status with fan ON: {status}")
        
        # Test 4: Turn fan off
        print("\n4. Testing fan OFF...")
        success = agent.turn_fan_off()
        print(f"   Fan OFF result: {success}")
        
        if success:
            time.sleep(1)
            
            # Test 5: Check final status
            print("\n5. Checking final status...")
            status = agent.get_status()
            print(f"   Final status: {status}")
            
            # Test 6: Test all readings
            print("\n6. Testing all readings...")
            all_readings = agent.get_all_readings()
            print(f"   All readings: {all_readings}")
            
            print("\n✅ Fan integration test completed successfully!")
            return True
        else:
            print("❌ Failed to turn fan OFF")
            return False
    else:
        print("❌ Failed to turn fan ON")
        return False

def main():
    """Main test function."""
    print("🎯 Fan Integration Test")
    print("======================")
    
    try:
        success = test_fan_integration()
        if success:
            print("\n🎉 All tests passed! Fan integration is working.")
        else:
            print("\n💥 Some tests failed. Check your connections.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
    finally:
        print("\n🔌 Closing connection...")

if __name__ == "__main__":
    main() 