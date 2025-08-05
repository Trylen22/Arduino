#!/usr/bin/env python3
"""
IRIS Student Companion AI - Presentation Demo
============================================

Simple demo script for showcasing the student companion features.
Perfect for presentations and demonstrations.

Author: [Your Name]
Date: [2025-01-27]
"""

import sys
import os
import time

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'examples'))
from student_companion_ai import IRISStudentCompanionAI


def run_presentation_demo():
    """Run a presentation-friendly demo of the student companion."""
    print("IRIS Student Companion AI - Presentation Demo")
    print("=" * 60)
    print("This demo showcases how IRIS helps students study better")
    print("by combining environmental monitoring with emotional support.")
    print("=" * 60)
    
    # Initialize the system
    iris = IRISStudentCompanionAI()
    
    if not iris.agent.connected:
        print("❌ Arduino not connected. Please connect your Arduino and try again.")
        return
    
    print("\n✅ System ready! Starting demo...")
    time.sleep(1)
    
    # Demo sequence
    demos = [
        {
            "title": "1. Starting a Study Session",
            "description": "IRIS welcomes the student and starts tracking study time",
            "action": lambda: iris._handle_start_session()
        },
        {
            "title": "2. Environmental Monitoring",
            "description": "IRIS checks the study environment for optimal conditions",
            "action": lambda: iris._handle_analyze()
        },
        {
            "title": "3. Emotional Support",
            "description": "IRIS provides emotional support and encouragement",
            "action": lambda: iris._handle_emotional_support()
        },
        {
            "title": "4. Study Advice",
            "description": "IRIS gives personalized study advice based on session length",
            "action": lambda: iris._handle_study_advice()
        },
        {
            "title": "5. Environmental Control",
            "description": "IRIS can control the environment (LED, fan) for better studying",
            "action": lambda: iris._handle_turn_led_on()
        },
        {
            "title": "6. Study Statistics",
            "description": "IRIS tracks study progress and provides insights",
            "action": lambda: iris._handle_get_stats()
        },
        {
            "title": "7. Ending Study Session",
            "description": "IRIS summarizes the study session and celebrates progress",
            "action": lambda: iris._handle_end_session()
        }
    ]
    
    # Run each demo
    for i, demo in enumerate(demos, 1):
        print(f"\n📋 {demo['title']}")
        print(f"   {demo['description']}")
        print("   " + "=" * 50)
        
        # Run the demo action
        demo['action']()
        
        # Pause between demos
        if i < len(demos):
            print("\n⏳ Pausing for 3 seconds...")
            time.sleep(3)
    
    print("\nDemo complete!")
    print("=" * 60)
    print("IRIS Student Companion AI combines:")
    print("• Environmental monitoring (temperature, air quality, lighting)")
    print("• Emotional support and encouragement")
    print("• Study habit coaching and break reminders")
    print("• Proactive interventions for optimal studying")
    print("=" * 60)
    
    # Clean up
    iris.close()


def run_interactive_demo():
    """Run an interactive demo where the user can talk to IRIS."""
    print("IRIS Student Companion AI - Interactive Demo")
    print("=" * 60)
    print("Talk to IRIS naturally! Try these examples:")
    print("• 'I'm stressed about my exam tomorrow'")
    print("• 'I've been studying for 2 hours, should I take a break?'")
    print("• 'The room feels stuffy, can you help?'")
    print("• 'I need some motivation'")
    print("• 'start session' - Begin studying")
    print("• 'end session' - Finish studying")
    print("• 'quit' - Exit demo")
    print("\nYou can type or speak to IRIS!")
    print("=" * 60)
    
    iris = IRISStudentCompanionAI()
    
    if not iris.agent.connected:
        print("❌ Arduino not connected. Please connect your Arduino and try again.")
        return
    
    iris.run_interactive_mode()


def main():
    """Main demo function."""
    print("IRIS Student Companion AI - Demo")
    print("=" * 40)
    
    print("\nChoose demo type:")
    print("1. Presentation demo (automated)")
    print("2. Interactive demo (talk to IRIS)")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "2":
            run_interactive_demo()
        else:
            run_presentation_demo()
    
    except KeyboardInterrupt:
        print("\n\nDemo ended. Thanks for trying IRIS!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")


if __name__ == "__main__":
    main() 