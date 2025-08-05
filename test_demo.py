#!/usr/bin/env python3
"""
Test script for the new IRIS demo
================================

Quick test to verify the demo works correctly.
"""

import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(__file__))

def test_demo_import():
    """Test that the demo can be imported."""
    try:
        from demo_student_companion import IRISDemo
        print("Demo import successful")
        return True
    except Exception as e:
        print(f"Demo import failed: {e}")
        return False

def test_simulator():
    """Test the demo simulator."""
    try:
        from demo_student_companion import DemoSimulator
        
        simulator = DemoSimulator()
        status = simulator.get_simulated_status()
        
        print("Simulator test successful")
        print(f"   Temperature: {status['temperature']}°F")
        print(f"   CO2: {status['co2']}")
        print(f"   Light: {status['light']} ({status['brightness']})")
        
        return True
    except Exception as e:
        print(f"Simulator test failed: {e}")
        return False

def test_alert_detection():
    """Test alert detection logic."""
    try:
        from demo_student_companion import IRISDemo
        
        demo = IRISDemo()
        
        # Test normal conditions
        normal_status = {
            'temperature': 72,
            'co2': 450,
            'brightness': 'Moderate'
        }
        alerts = demo.check_for_alerts(normal_status)
        print(f"Normal conditions: {len(alerts)} alerts (expected: 0)")
        
        # Test high temperature
        hot_status = {
            'temperature': 82,
            'co2': 450,
            'brightness': 'Moderate'
        }
        alerts = demo.check_for_alerts(hot_status)
        print(f"High temperature: {len(alerts)} alerts (expected: 1)")
        
        # Test high CO2
        stuffy_status = {
            'temperature': 72,
            'co2': 1200,
            'brightness': 'Moderate'
        }
        alerts = demo.check_for_alerts(stuffy_status)
        print(f"High CO2: {len(alerts)} alerts (expected: 1)")
        
        return True
    except Exception as e:
        print(f"Alert detection test failed: {e}")
        return False

def test_chat_simulation():
    """Test chat simulation."""
    try:
        from demo_student_companion import IRISDemo
        
        demo = IRISDemo()
        
        # Test stress response
        response = demo._simulate_chat_response("I'm feeling stressed")
        print(f"Stress response: {response[:50]}...")
        
        # Test motivation response
        response = demo._simulate_chat_response("I need motivation")
        print(f"Motivation response: {response[:50]}...")
        
        return True
    except Exception as e:
        print(f"Chat simulation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing IRIS Demo Components")
    print("=" * 40)
    
    tests = [
        ("Demo Import", test_demo_import),
        ("Simulator", test_simulator),
        ("Alert Detection", test_alert_detection),
        ("Chat Simulation", test_chat_simulation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
            print(f"{test_name} passed")
        else:
            print(f"{test_name} failed")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Demo is ready to run.")
        print("\nTo run the demo:")
        print("python demo_student_companion.py")
    else:
        print("Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main() 