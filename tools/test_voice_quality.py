#!/usr/bin/env python3
"""
Test Voice Quality
=================

Test different voices to find one that speaks naturally.
"""

import pyttsx3
import time

def test_voice_natural_speech():
    """Test voices for natural speech without letter-by-letter spelling."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n🎤 Testing {len(voices)} voices for natural speech:")
    print("=" * 60)
    
    test_phrases = [
        "Hello, this is a test.",
        "The temperature is seventy-two degrees.",
        "LED status: ON",
        "Environmental monitoring system ready."
    ]
    
    for i, voice in enumerate(voices):
        print(f"\n🎤 Testing Voice {i+1}: {voice.name}")
        print(f"   ID: {voice.id}")
        
        # Configure voice for natural speech
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 150)      # Normal speed
        engine.setProperty('volume', 0.8)    # Good volume
        
        # Test each phrase
        for j, phrase in enumerate(test_phrases, 1):
            print(f"   {j}. Speaking: '{phrase}'")
            engine.say(phrase)
            engine.runAndWait()
            time.sleep(0.5)  # Brief pause between phrases
        
        # Ask user if this voice is good
        print(f"\n   Does Voice {i+1} sound natural? (y/n/s to skip): ", end="")
        response = input().lower().strip()
        
        if response == 'y':
            print(f"✅ Voice {i+1} selected as best!")
            print(f"   Name: {voice.name}")
            print(f"   ID: {voice.id}")
            return voice
        elif response == 's':
            print("   Skipping to next voice...")
            continue
        else:
            print("   Moving to next voice...")
    
    print("\n❌ No voice found that sounds natural.")
    return None

def quick_voice_test():
    """Quick test of the first few voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n🎤 Quick test of first 3 voices:")
    print("=" * 40)
    
    for i in range(min(3, len(voices))):
        voice = voices[i]
        print(f"\n🎤 Voice {i+1}: {voice.name}")
        
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        
        test_phrase = "Hello, this is a natural speech test."
        print(f"   Speaking: '{test_phrase}'")
        engine.say(test_phrase)
        engine.runAndWait()
        
        print(f"   Good voice? (y/n): ", end="")
        if input().lower().strip() == 'y':
            print(f"✅ Selected: {voice.name} ({voice.id})")
            return voice
    
    return None

def main():
    """Main function."""
    print("🎤 Voice Quality Tester")
    print("=" * 30)
    
    print("\nOptions:")
    print("1. Quick test (first 3 voices)")
    print("2. Full test (all voices)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        best_voice = quick_voice_test()
    elif choice == '2':
        best_voice = test_voice_natural_speech()
    elif choice == '3':
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")
        return
    
    if best_voice:
        print(f"\n🎯 Best voice found: {best_voice.name}")
        print(f"   ID: {best_voice.id}")
        print(f"\n📝 Update your voice interface to use this voice ID!")

if __name__ == "__main__":
    main() 