#!/usr/bin/env python3
"""
Interactive Environmental Monitoring Agent
========================================

Interactive interface for testing and using the intelligent environmental agent.
Allows user interaction and real-time monitoring.

Author: [Your Name]
Date: [2025-01-27]
"""

import time
import json
from intelligent_environmental_agent import IntelligentEnvironmentalAgent

def print_banner():
    """Print the application banner."""
    print("="*60)
    print("🌍 INTELLIGENT ENVIRONMENTAL MONITORING SYSTEM")
    print("="*60)
    print("🤖 LLM-Powered Environmental Analysis & Control")
    print("📊 Real-time sensor monitoring and intelligent decisions")
    print("="*60)

def print_menu():
    """Print the main menu."""
    print("\n📋 Available Commands:")
    print("  1. 📊 Get current status")
    print("  2. 🤔 Make intelligent decision")
    print("  3. 🔄 Start continuous monitoring")
    print("  4. 💡 Turn LED ON")
    print("  5. 🔴 Turn LED OFF")
    print("  6. 🌡️  Get temperature only")
    print("  7. 💨 Get CO2 only")
    print("  8. 💡 Get light level only")
    print("  9. ❓ Ask LLM a question")
    print("  0. 🚪 Exit")
    print("-" * 40)

def print_status(status):
    """Print formatted status information."""
    print("\n📊 ENVIRONMENTAL STATUS:")
    print("-" * 30)
    print(f"🌡️  Temperature: {status.get('temperature', 'N/A')}°F")
    print(f"💨 CO2 Level: {status.get('co2', 'N/A')}")
    print(f"💡 Light Level: {status.get('light', 'N/A')}")
    print(f"🔴 LED Status: {status.get('led', 'N/A')}")
    
    if "analysis" in status:
        analysis = status["analysis"]
        print(f"\n🏥 Overall Health: {analysis['overall_health']}")
        print(f"🌡️  Temperature Status: {analysis['temperature_status']}")
        print(f"💨 Air Quality: {analysis['air_quality_status']}")
        print(f"💡 Lighting: {analysis['lighting_status']}")
        
        if analysis["alerts"]:
            print("\n⚠️  ALERTS:")
            for alert in analysis["alerts"]:
                print(f"   • {alert}")
        
        if analysis["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for rec in analysis["recommendations"]:
                print(f"   • {rec}")

def interactive_loop():
    """Main interactive loop."""
    print_banner()
    
    # Initialize agent
    print("🔌 Connecting to Arduino...")
    agent = IntelligentEnvironmentalAgent()
    
    if not agent.agent.connected:
        print("❌ Failed to connect to Arduino!")
        print("Please check your Arduino connection and try again.")
        return
    
    print("✅ Connected successfully!")
    
    while True:
        print_menu()
        
        try:
            choice = input("🎯 Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
                
            elif choice == "1":
                print("\n🔄 Getting current status...")
                status = agent.get_environmental_status()
                print_status(status)
                
            elif choice == "2":
                print("\n🤔 Making intelligent decision...")
                decision = agent.make_intelligent_decision()
                print_status(decision["status"])
                print(f"\n🤖 LLM Decision: {decision['decision']}")
                if decision["actions_taken"]:
                    print("⚡ Actions taken:")
                    for action in decision["actions_taken"]:
                        print(f"   • {action}")
                        
            elif choice == "3":
                interval = input("⏱️  Enter monitoring interval in seconds (default 60): ").strip()
                try:
                    interval = int(interval) if interval else 60
                    print(f"\n🔄 Starting continuous monitoring (every {interval} seconds)...")
                    print("Press Ctrl+C to stop monitoring")
                    agent.run_continuous_monitoring(interval)
                except ValueError:
                    print("❌ Invalid interval. Using default 60 seconds.")
                    agent.run_continuous_monitoring(60)
                    
            elif choice == "4":
                print("\n💡 Turning LED ON...")
                if agent.agent.turn_led_on():
                    print("✅ LED turned ON")
                else:
                    print("❌ Failed to turn LED ON")
                    
            elif choice == "5":
                print("\n🔴 Turning LED OFF...")
                if agent.agent.turn_led_off():
                    print("✅ LED turned OFF")
                else:
                    print("❌ Failed to turn LED OFF")
                    
            elif choice == "6":
                temp = agent.agent.get_temperature()
                if temp is not None:
                    print(f"\n🌡️  Temperature: {temp}°C")
                else:
                    print("❌ Failed to get temperature")
                    
            elif choice == "7":
                co2 = agent.agent.get_co2()
                if co2 is not None:
                    print(f"\n💨 CO2 Level: {co2}")
                else:
                    print("❌ Failed to get CO2 reading")
                    
            elif choice == "8":
                light = agent.agent.get_light()
                if light is not None:
                    print(f"\n💡 Light Level: {light}")
                else:
                    print("❌ Failed to get light reading")
                    
            elif choice == "9":
                question = input("\n❓ Ask the LLM a question: ").strip()
                if question:
                    print(f"\n🤔 Asking: '{question}'")
                    decision = agent.make_intelligent_decision(question)
                    print_status(decision["status"])
                    print(f"\n🤖 LLM Response: {decision['decision']}")
                else:
                    print("❌ No question provided")
                    
            else:
                print("❌ Invalid choice. Please enter 0-9.")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\n⏸️  Press Enter to continue...")
    
    agent.close()

def main():
    """Main function."""
    try:
        interactive_loop()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main() 