#!/usr/bin/env python3
"""
IRIS Simple Demo
================

A clean, simple demo of IRIS - your intelligent environmental assistant.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'examples'))

from smart_environmental_ai import IRIS

def main():
    """Simple IRIS demo."""
    print("👋 Hi! I'm IRIS")
    print("I'm your intelligent environmental assistant.")
    print()
    
    # Initialize IRIS
    iris = IRIS()
    
    if not iris.agent.connected:
        print("❌ I can't connect to your sensors.")
        print("Make sure your Arduino is connected and try again.")
        return
    
    print("✅ I'm connected and ready to help!")
    print()
    
    # Simple demo flow
    print("Let me show you what I can do:")
    print()
    
    # 1. Analyze environment
    print("1️⃣  First, let me check your environment...")
    analysis = iris.analyze_environment()
    
    if "error" not in analysis:
        print(f"   📊 My thoughts: {analysis.get('my_analysis', 'I need to think about this')}")
        
        actions = analysis.get('actions_i_should_take', [])
        if actions:
            print(f"   🎯 I think I should: {len(actions)} things")
            for action in actions:
                print(f"      • {action.get('action', 'Unknown')}: {action.get('reason', 'This would help')}")
        
        # Execute actions
        executed = iris.take_actions(analysis)
        print(f"   ✅ I did {len(executed)} things to help")
    else:
        print(f"   ❌ I'm having trouble: {analysis.get('error')}")
    
    print()
    
    # 2. Predict future
    print("2️⃣  Now let me predict what might happen...")
    predictions = iris.predict_what_might_happen()
    
    if "error" not in predictions:
        my_predictions = predictions.get('my_predictions', [])
        if my_predictions:
            print(f"   🔮 I think: {my_predictions[0]}")
        
        worries = predictions.get('things_i_worry_about', [])
        if worries:
            print(f"   ⚠️  I'm watching for: {worries[0]}")
        
        confidence = predictions.get('how_confident_i_am', 'Unknown')
        print(f"   🎯 How sure I am: {confidence}")
    else:
        print(f"   ❌ I'm having trouble predicting: {predictions.get('error')}")
    
    print()
    
    # 3. Answer a question
    print("3️⃣  You can ask me anything about your environment!")
    print("   Try: 'Why is the air quality bad?' or 'How can I improve the lighting?'")
    print("   (Press Enter to skip this demo)")
    
    question = input("   What would you like to know? ").strip()
    
    if question:
        response = iris.answer_your_question(question)
        
        if "error" not in response:
            print(f"   🤖 My answer: {response.get('my_answer', 'I need to think about this')}")
            
            suggestions = response.get('things_i_suggest', [])
            if suggestions:
                print(f"   💡 I suggest: {suggestions[0]}")
        else:
            print(f"   ❌ I'm having trouble: {response.get('error')}")
    
    print()
    print("🎉 That's what I can do!")
    print("I'm here to help keep you comfortable and safe.")
    print("Run me anytime with: python3 agents/examples/smart_environmental_ai.py")

if __name__ == "__main__":
    main() 