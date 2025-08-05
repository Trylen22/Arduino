#!/usr/bin/env python3
"""
Simple microphone test for IRIS project
"""

import speech_recognition as sr
import time

def test_microphone():
    """Test microphone functionality."""
    print("🎤 Testing Microphone Setup")
    print("=" * 40)
    
    # List available microphones
    print("Available microphones:")
    mic_list = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mic_list):
        print(f"  {i}: {mic}")
    
    print(f"\nYour HyperX SoloCast is at index: 9")
    
    # Test with your USB microphone
    try:
        # Use your HyperX SoloCast (index 9)
        mic = sr.Microphone(device_index=9)
        recognizer = sr.Recognizer()
        
        print(f"\n🎤 Testing microphone: {mic_list[9]}")
        print("Speak something when prompted...")
        
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening... (speak now)")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                
                text = recognizer.recognize_google(audio)
                print(f"✅ Success! You said: '{text}'")
                return True
                
            except sr.WaitTimeoutError:
                print("❌ No speech detected within timeout")
                return False
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return False
            except sr.RequestError as e:
                print(f"❌ Could not request results; {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing microphone: {e}")
        return False

def test_default_microphone():
    """Test default microphone as fallback."""
    print("\n🎤 Testing Default Microphone")
    print("=" * 40)
    
    try:
        mic = sr.Microphone()  # Use default
        recognizer = sr.Recognizer()
        
        print("Testing default microphone...")
        print("Speak something when prompted...")
        
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening... (speak now)")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                
                text = recognizer.recognize_google(audio)
                print(f"✅ Success! You said: '{text}'")
                return True
                
            except sr.WaitTimeoutError:
                print("❌ No speech detected within timeout")
                return False
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return False
            except sr.RequestError as e:
                print(f"❌ Could not request results; {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing default microphone: {e}")
        return False

if __name__ == "__main__":
    print("IRIS Microphone Test")
    print("=" * 50)
    
    # Test your USB microphone first
    success = test_microphone()
    
    if not success:
        print("\n🔄 Trying default microphone as fallback...")
        test_default_microphone()
    
    print("\n" + "=" * 50)
    print("Test complete!") 