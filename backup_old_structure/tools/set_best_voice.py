#!/usr/bin/env python3
"""
Set Best Voice for Voice Interface
==================================

Quick script to set your preferred voice as the default.
"""

import pyttsx3

def set_best_voice():
    """Set the best voice based on user input."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n🎤 Found {len(voices)} available voices:")
    print("=" * 60)
    
    # Show all voices
    for i, voice in enumerate(voices):
        print(f"{i+1:3d}. {voice.name} ({voice.id})")
    
    print("\n" + "=" * 60)
    print("Which voice did you find to be the best?")
    print("Enter the number of your preferred voice:")
    
    try:
        choice = int(input("Voice number: ")) - 1
        if 0 <= choice < len(voices):
            selected_voice = voices[choice]
            print(f"\n✅ Selected: {selected_voice.name}")
            print(f"   ID: {selected_voice.id}")
            
            # Test the voice
            print("\n🎤 Testing the selected voice...")
            engine.setProperty('voice', selected_voice.id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            test_phrase = "This is your selected voice for the environmental monitoring system."
            engine.say(test_phrase)
            engine.runAndWait()
            
            print("\n✅ Voice set successfully!")
            print(f"📝 To use this voice in your voice interface, update the voice selection logic")
            print(f"   to prioritize: '{selected_voice.id}'")
            
            return selected_voice
        else:
            print("❌ Invalid voice number!")
            return None
            
    except ValueError:
        print("❌ Please enter a valid number!")
        return None

if __name__ == "__main__":
    set_best_voice() 