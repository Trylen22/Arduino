#!/usr/bin/env python3
"""
IRIS Demo - Your Intelligent Environmental Assistant
==================================================

I'm IRIS, and I'm here to help you understand your environment.
Simple, helpful, and focused on what matters to you.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'examples'))

from smart_environmental_ai import IRIS

def demo_iris():
    """Show you what IRIS can do for you."""
    print("👋 Hi! I'm IRIS, your environmental assistant.")
    print("="*60)
    print("I'm here to help you understand and control your environment.")
    print()
    print("🎯 What I can do for you:")
    print("   • Understand your environment and make smart decisions")
    print("   • Predict problems before they happen")
    print("   • Optimize your comfort and safety")
    print("   • Answer your questions naturally")
    print("   • Learn from your preferences over time")
    print()
    print("🚀 The future I'm building:")
    print("   • Homes that think and optimize themselves")
    print("   • Buildings that predict and prevent issues")
    print("   • Environments that adapt to your needs")
    print("   • A world where AI and environment work together")
    print("="*60)
    
    # Initialize IRIS
    print("\n🧠 Let me connect to your sensors...")
    iris = IRIS()
    
    if not iris.agent.connected:
        print("❌ I can't connect to your sensors right now.")
        print("This demo shows what I can do - connect your sensors to see me in action!")
        print("\n💡 To see the full demo:")
        print("   1. Connect your Arduino with sensors")
        print("   2. Run: python3 agents/examples/smart_environmental_ai.py")
        print("   3. I'll show you what I can do!")
        return
    
    print("✅ Great! I'm connected and ready to help.")
    print("\n🎬 Let me show you what I can do...")
    
    # Start IRIS demo
    iris.demo_mode()

if __name__ == "__main__":
    demo_iris() 