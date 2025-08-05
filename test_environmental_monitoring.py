#!/usr/bin/env python3
"""
Real-time Environmental Monitoring Test
=====================================

Test script to monitor environmental changes and autonomous interventions
in real-time.

Author: [Your Name]
Date: [2025-01-27]
"""

import time
import sys
import os

# Add the agents directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'examples'))

from environmental_agent import EnvironmentalAgent
from agent_memory import AgentMemory
from autonomous_agent import AutonomousAgent

def monitor_environment():
    """Monitor environment in real-time and test autonomous interventions."""
    print("🌡️  Real-time Environmental Monitoring Test")
    print("=" * 60)
    print("This will monitor temperature, CO2, and light levels")
    print("and test autonomous interventions when conditions change.")
    print("=" * 60)
    
    # Initialize components
    agent = EnvironmentalAgent()
    memory = AgentMemory()
    autonomous_agent = AutonomousAgent(memory)
    
    if not agent.connected:
        print("❌ Arduino not connected. Please connect your Arduino.")
        return
    
    print("✅ Connected to Arduino!")
    print("🔍 Starting real-time monitoring...")
    print("💡 TIP: Try heating up the temperature sensor to test autonomous interventions!")
    print("=" * 60)
    
    try:
        while True:
            # Get current environment
            status = agent.get_status()
            
            if "error" in status:
                print("❌ Error reading sensors")
                time.sleep(2)
                continue
            
            # Display current readings
            print(f"\n📊 Current Readings:")
            print(f"  Temperature: {status.get('temperature', 'N/A')}°F")
            print(f"  CO2: {status.get('co2', 'N/A')}")
            print(f"  Light: {status.get('light', 'N/A')} ({status.get('brightness', 'N/A')})")
            print(f"  LED: {status.get('led', 'N/A')}")
            print(f"  Fan: {status.get('fan', 'N/A')}")
            
            # Test autonomous decision making
            context = {
                "study_time_minutes": 30,  # Simulate active study session
                "stress_level": 3,
                "environment": status
            }
            
            # Analyze context
            analysis = autonomous_agent.analyze_context(context)
            
            print(f"\n🔍 Analysis:")
            print(f"  Study Health: {analysis['study_health']}")
            print(f"  Environmental Health: {analysis['environmental_health']}")
            print(f"  Emotional Health: {analysis['emotional_health']}")
            
            # Check for autonomous interventions
            decision = autonomous_agent.make_autonomous_decision(context)
            if decision:
                print(f"\n🚨 AUTONOMOUS INTERVENTION DETECTED!")
                print(f"  Type: {decision['type']}")
                print(f"  Message: {decision['message']}")
                print(f"  Actions: {decision['actions']}")
                print(f"  Priority: {decision['priority']}")
            else:
                print(f"\n✅ No intervention needed")
            
            print("=" * 60)
            time.sleep(3)  # Update every 3 seconds
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Main function."""
    print("Environmental Monitoring Test")
    print("=" * 40)
    print("1. Start real-time monitoring")
    print("2. Exit")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            monitor_environment()
        else:
            print("Goodbye!")
    
    except KeyboardInterrupt:
        print("\n\nTest ended. Thanks!")

if __name__ == "__main__":
    main() 