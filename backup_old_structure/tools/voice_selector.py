#!/usr/bin/env python3
"""
Voice Selector for TTS Enhanced Agent
=====================================

This utility helps you select and test different voices for better clarity.
"""

import pyttsx3
import speech_recognition as sr

def list_voices():
    """List all available voices with their properties."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n🎤 Found {len(voices)} available voices:")
    print("=" * 60)
    
    # Group voices by language
    english_voices = []
    other_voices = []
    
    for i, voice in enumerate(voices):
        if 'en' in voice.id.lower():
            english_voices.append((i, voice))
        else:
            other_voices.append((i, voice))
    
    print("\n🇺🇸 ENGLISH VOICES (Recommended):")
    print("-" * 40)
    for i, voice in english_voices:
        print(f"{i+1:3d}. {voice.name} ({voice.id})")
    
    print(f"\n🌍 OTHER VOICES ({len(other_voices)} total):")
    print("-" * 40)
    for i, voice in other_voices[:10]:  # Show first 10
        print(f"{i+1:3d}. {voice.name} ({voice.id})")
    
    if len(other_voices) > 10:
        print(f"... and {len(other_voices) - 10} more voices")
    
    return voices

def test_voice(voice_index=None, voice_id=None):
    """Test a specific voice with sample text."""
    engine = pyttsx3.init()
    
    # Configure for clarity
    engine.setProperty('rate', 120)     # Slower speed
    engine.setProperty('volume', 0.9)   # Higher volume
    engine.setProperty('pitch', 1.1)    # Slightly higher pitch
    
    if voice_id:
        engine.setProperty('voice', voice_id)
    elif voice_index is not None:
        voices = engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            engine.setProperty('voice', voices[voice_index].id)
            print(f"Testing voice: {voices[voice_index].name}")
        else:
            print("Invalid voice index!")
            return
    
    # Test phrases
    test_phrases = [
        "Hello! I'm your LED assistant.",
        "The red LED is now on.",
        "Both LEDs are currently off.",
        "Please speak your command clearly.",
        "I'm sorry, I didn't understand that."
    ]
    
    print("\n🎤 Testing voice with sample phrases:")
    print("=" * 50)
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n{i}. Speaking: '{phrase}'")
        engine.say(phrase)
        engine.runAndWait()
        
        # Wait for user input to continue
        input("Press Enter to continue to next phrase...")

def find_best_english_voice():
    """Find and recommend the best English voice."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Priority order for English voices
    priority_voices = [
        'gmw/en-us',      # English (America)
        'gmw/en-gb',      # English (Great Britain)
        'gmw/en-029',     # English (Caribbean)
        'gmw/en-gb-x-rp', # English (Received Pronunciation)
        'gmw/en-us-nyc'   # English (America, New York City)
    ]
    
    print("\n🔍 Finding best English voice...")
    
    for priority_id in priority_voices:
        for voice in voices:
            if priority_id in voice.id:
                print(f"✅ Found recommended voice: {voice.name} ({voice.id})")
                return voice
    
    # Fallback to any English voice
    for voice in voices:
        if 'en' in voice.id.lower():
            print(f"✅ Found English voice: {voice.name} ({voice.id})")
            return voice
    
    # Last resort
    if voices:
        print(f"⚠️  Using default voice: {voices[0].name} ({voices[0].id})")
        return voices[0]
    
    return None

def main():
    """Main function for voice selection."""
    print("🎤 Voice Selector for TTS Enhanced Agent")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. List all voices")
        print("2. Test specific voice")
        print("3. Find best English voice")
        print("4. Test best English voice")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            list_voices()
            
        elif choice == '2':
            try:
                voice_num = int(input("Enter voice number to test: "))
                test_voice(voice_index=voice_num-1)
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == '3':
            best_voice = find_best_english_voice()
            if best_voice:
                print(f"\n🎯 Recommended voice: {best_voice.name}")
                print(f"   ID: {best_voice.id}")
                
        elif choice == '4':
            best_voice = find_best_english_voice()
            if best_voice:
                test_voice(voice_id=best_voice.id)
            else:
                print("No suitable English voice found!")
                
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 