#!/usr/bin/env python3
"""
Voice Interface Module
=====================

Modular voice interface for speech recognition and text-to-speech.
Can be imported and used by other agents.

Author: [Your Name]
Date: [2025-01-27]
"""

import speech_recognition as sr
import pyttsx3
import time

class VoiceInterface:
    def __init__(self, microphone_index=9, voice_rate=150, voice_volume=0.9):
        """Initialize voice interface with microphone and TTS."""
        self.microphone_index = microphone_index
        self.voice_rate = voice_rate
        self.voice_volume = voice_volume
        self.microphone = None
        self.tts_engine = None
        self.recognizer = None
        
        self._setup_tts()
        self._setup_microphone()
    
    def _setup_tts(self):
        """Setup text-to-speech engine with enhanced settings."""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Enhanced TTS settings for better quality
            self.tts_engine.setProperty('rate', self.voice_rate)      # Speed of speech (lower = slower)
            self.tts_engine.setProperty('volume', self.voice_volume)   # Volume level (0.0 to 1.0)
            
            # Get available voices and select the best one
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find the specific voice the user identified as best (option 4)
                best_voice = None
                
                # First, try to find voice option 4 (or the user's preferred voice)
                if len(voices) >= 4:
                    best_voice = voices[3]  # Option 4 (index 3)
                    print(f"✅ Using user's preferred voice: {best_voice.name}")
                    print(f"   Voice ID: {best_voice.id}")
                else:
                    # Fallback to voice selection logic
                    for voice in voices:
                        voice_id = voice.id.lower()
                        voice_name = voice.name.lower()
                        
                        # Look for high-quality voices that the user likely found best
                        if any(keyword in voice_id or keyword in voice_name for keyword in [
                            'gmw/en-us', 'gmw/en-gb', 'gmw/en-029', 'gmw/en-gb-x-rp', 'gmw/en-us-nyc',
                            'samantha', 'victoria', 'alex', 'karen', 'daniel', 'tom',
                            'female', 'english', 'us', 'gb', 'american', 'british'
                        ]):
                            best_voice = voice
                            break
                    
                    # If no preferred voice found, use the first one
                    if not best_voice and voices:
                        best_voice = voices[0]
                
                if best_voice:
                    self.tts_engine.setProperty('voice', best_voice.id)
                    print(f"✅ Using voice: {best_voice.name}")
                    print(f"   Voice ID: {best_voice.id}")
            
            # Additional settings to prevent letter-by-letter spelling
            try:
                # Set word boundary settings to ensure natural speech
                self.tts_engine.setProperty('word_boundary', True)
            except:
                pass  # Some engines don't support this property
            
            print("✅ Enhanced text-to-speech initialized successfully!")
            print(f"📊 Voice settings: Rate={self.voice_rate}, Volume={self.voice_volume}")
            
        except Exception as e:
            print(f"❌ Error initializing TTS: {e}")
            self.tts_engine = None
    
    def _setup_microphone(self):
        """Setup microphone and speech recognition."""
        self.recognizer = sr.Recognizer()
        try:
            # Try to use a specific microphone
            self.microphone = sr.Microphone(device_index=self.microphone_index)
            
            # Enhanced recognizer settings for better accuracy
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)  # Longer calibration
                self.recognizer.energy_threshold = 800  # Lower threshold for better sensitivity
                self.recognizer.dynamic_energy_threshold = True  # Adaptive threshold
                self.recognizer.pause_threshold = 0.6  # Shorter pause for faster response
                self.recognizer.phrase_threshold = 0.3  # Shorter phrase threshold
                self.recognizer.non_speaking_duration = 0.5  # Shorter non-speaking duration
            print("✅ Enhanced microphone test successful!")
        except Exception as e:
            print(f"❌ Error initializing microphone: {e}")
            print("Voice control will not be available.")
            self.microphone = None
    
    def speak(self, text, rate=None, volume=None):
        """Convert text to speech and play it with optional rate/volume override."""
        if self.tts_engine:
            try:
                # Temporarily override settings if provided
                original_rate = self.tts_engine.getProperty('rate')
                original_volume = self.tts_engine.getProperty('volume')
                
                if rate is not None:
                    self.tts_engine.setProperty('rate', rate)
                if volume is not None:
                    self.tts_engine.setProperty('volume', volume)
                
                print(f"🗣️  Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
                # Restore original settings
                self.tts_engine.setProperty('rate', original_rate)
                self.tts_engine.setProperty('volume', original_volume)
                
            except Exception as e:
                print(f"❌ TTS Error: {e}")
        else:
            print(f"📝 TTS not available: {text}")
    
    def speak_slow(self, text):
        """Speak text at a slower rate for important messages."""
        self.speak(text, rate=120)
    
    def speak_fast(self, text):
        """Speak text at a faster rate for quick responses."""
        self.speak(text, rate=180)
    
    def speak_quiet(self, text):
        """Speak text at a lower volume."""
        self.speak(text, volume=0.6)
    
    def speak_loud(self, text):
        """Speak text at a higher volume for alerts."""
        self.speak(text, volume=1.0)
    
    def listen(self):
        """Listen for a voice command using the microphone."""
        if not self.microphone:
            print("❌ Voice control not available.")
            return None

        try:
            with self.microphone as source:
                self.speak_quiet("Listening...")
                print("\n👂 Listening... (speak now)")
                # Listen for audio input with enhanced settings
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
                print("🔄 Processing your command...")
                try:
                    # Use Google's speech recognition service
                    text = self.recognizer.recognize_google(audio)
                    print(f"🎤 You said: {text}")
                    return text
                except sr.UnknownValueError:
                    self.speak("Sorry, I couldn't understand that. Please try again.")
                    print("❌ Sorry, I couldn't understand that.")
                    return None
                except sr.RequestError as e:
                    self.speak("Could not process your request. Please check your internet connection.")
                    print(f"❌ Could not request results; {e}")
                    return None
        except Exception as e:
            print(f"❌ Error listening: {e}")
            return None
    
    def get_available_voices(self):
        """Get list of available voices for debugging."""
        if self.tts_engine:
            voices = self.tts_engine.getProperty('voices')
            print("🎤 Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name} ({voice.id})")
            return voices
        return []
    
    def change_voice(self, voice_index):
        """Change to a different voice by index."""
        if self.tts_engine:
            voices = self.tts_engine.getProperty('voices')
            if 0 <= voice_index < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_index].id)
                print(f"✅ Changed to voice: {voices[voice_index].name}")
                return True
            else:
                print(f"❌ Invalid voice index: {voice_index}")
                return False
        return False
    
    def adjust_rate(self, new_rate):
        """Adjust the speech rate."""
        if self.tts_engine:
            self.tts_engine.setProperty('rate', new_rate)
            self.voice_rate = new_rate
            print(f"✅ Speech rate adjusted to: {new_rate}")
            return True
        return False
    
    def adjust_volume(self, new_volume):
        """Adjust the speech volume (0.0 to 1.0)."""
        if self.tts_engine:
            if 0.0 <= new_volume <= 1.0:
                self.tts_engine.setProperty('volume', new_volume)
                self.voice_volume = new_volume
                print(f"✅ Speech volume adjusted to: {new_volume}")
                return True
            else:
                print("❌ Volume must be between 0.0 and 1.0")
                return False
        return False
    
    def close(self):
        """Clean up voice interface resources."""
        if self.tts_engine:
            self.tts_engine.stop()
        print("🔌 Voice interface closed.") 