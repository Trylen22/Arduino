#!/usr/bin/env python3
"""
Set Preferred Voice
==================

Quick script to set your preferred voice number as the default.
"""

import pyttsx3

def set_preferred_voice():
    """Set the preferred voice based on user input."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n🎤 Found {len(voices)} available voices:")
    print("=" * 60)
    
    # Show all voices
    for i, voice in enumerate(voices):
        print(f"{i+1:3d}. {voice.name} ({voice.id})")
    
    print("\n" + "=" * 60)
    print("Which voice number did you find to be the best?")
    print("(You said option 4 was the best)")
    
    try:
        # Default to option 4, but allow override
        choice = input("Enter voice number (default 4): ").strip()
        if not choice:
            choice = "4"
        
        voice_index = int(choice) - 1
        if 0 <= voice_index < len(voices):
            selected_voice = voices[voice_index]
            print(f"\n✅ Selected: {selected_voice.name}")
            print(f"   ID: {selected_voice.id}")
            
            # Test the voice
            print("\n🎤 Testing the selected voice...")
            engine.setProperty('voice', selected_voice.id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            test_phrase = "This is your preferred voice for the environmental monitoring system."
            engine.say(test_phrase)
            engine.runAndWait()
            
            print("\n✅ Voice set successfully!")
            print(f"📝 The voice interface will now automatically use voice #{voice_index + 1}")
            print(f"   Voice: {selected_voice.name}")
            print(f"   ID: {selected_voice.id}")
            
            return selected_voice, voice_index + 1
        else:
            print("❌ Invalid voice number!")
            return None, None
            
    except ValueError:
        print("❌ Please enter a valid number!")
        return None, None

if __name__ == "__main__":
    set_preferred_voice() 