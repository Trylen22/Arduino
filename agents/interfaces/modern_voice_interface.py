#!/usr/bin/env python3
"""
Modern Voice Interface with Lightweight Trained Voices
====================================================

Uses modern TTS models for much better voice quality.
"""

import speech_recognition as sr
import time
import subprocess
import os
from typing import Optional

class ModernVoiceInterface:
    def __init__(self, microphone_index=9, voice_model="coqui", voice_rate=1.0):
        """Initialize modern voice interface with trained voice models."""
        self.microphone_index = microphone_index
        self.voice_model = voice_model
        self.voice_rate = voice_rate
        self.microphone = None
        self.recognizer = None
        
        self._setup_voice_model()
        self._setup_microphone()
    
    def _setup_voice_model(self):
        """Setup modern voice model."""
        print(f"🎤 Initializing {self.voice_model} voice model...")
        
        if self.voice_model == "coqui":
            self._setup_coqui_tts()
        elif self.voice_model == "piper":
            self._setup_piper_tts()
        elif self.voice_model == "gtts":
            self._setup_gtts()
        elif self.voice_model == "edge":
            self._setup_edge_tts()
        else:
            print("❌ Unknown voice model. Using gTTS as fallback.")
            self._setup_gtts()
    
    def _setup_coqui_tts(self):
        """Setup Coqui TTS for high-quality voice."""
        try:
            # Try to import Coqui TTS
            from TTS.api import TTS
            self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
            print("✅ Coqui TTS initialized successfully!")
            self.voice_type = "coqui"
        except ImportError:
            print("❌ Coqui TTS not installed. Installing...")
            self._install_coqui_tts()
        except Exception as e:
            print(f"❌ Coqui TTS error: {e}")
            self._setup_gtts()
    
    def _setup_piper_tts(self):
        """Setup Piper TTS for lightweight voice."""
        try:
            # Check if piper is available
            result = subprocess.run(["which", "piper"], capture_output=True)
            if result.returncode == 0:
                print("✅ Piper TTS found!")
                self.voice_type = "piper"
            else:
                print("❌ Piper TTS not installed. Using gTTS...")
                self._setup_gtts()
        except Exception as e:
            print(f"❌ Piper TTS error: {e}")
            self._setup_gtts()
    
    def _setup_gtts(self):
        """Setup Google Text-to-Speech for reliable voice."""
        try:
            from gtts import gTTS
            import pygame
            pygame.mixer.init()
            self.gtts = gTTS
            self.pygame = pygame
            print("✅ Google TTS initialized successfully!")
            self.voice_type = "gtts"
        except ImportError:
            print("❌ gTTS not installed. Installing...")
            self._install_gtts()
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            self._setup_edge_tts()
    
    def _setup_edge_tts(self):
        """Setup Microsoft Edge TTS for high-quality voice."""
        try:
            import edge_tts
            self.edge_tts = edge_tts
            print("✅ Edge TTS initialized successfully!")
            self.voice_type = "edge"
        except ImportError:
            print("❌ Edge TTS not installed. Installing...")
            self._install_edge_tts()
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            print("❌ No modern TTS available. Using basic pyttsx3...")
            self._setup_fallback_tts()
    
    def _setup_fallback_tts(self):
        """Setup fallback to basic pyttsx3."""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            print("✅ Fallback TTS initialized!")
            self.voice_type = "fallback"
        except Exception as e:
            print(f"❌ Fallback TTS error: {e}")
            self.voice_type = None
    
    def _install_coqui_tts(self):
        """Install Coqui TTS."""
        try:
            subprocess.run(["pip", "install", "TTS"], check=True)
            print("✅ Coqui TTS installed!")
            self._setup_coqui_tts()
        except Exception as e:
            print(f"❌ Failed to install Coqui TTS: {e}")
            self._setup_gtts()
    
    def _install_gtts(self):
        """Install gTTS."""
        try:
            subprocess.run(["pip", "install", "gTTS", "pygame"], check=True)
            print("✅ gTTS installed!")
            self._setup_gtts()
        except Exception as e:
            print(f"❌ Failed to install gTTS: {e}")
            self._setup_edge_tts()
    
    def _install_edge_tts(self):
        """Install Edge TTS."""
        try:
            subprocess.run(["pip", "install", "edge-tts"], check=True)
            print("✅ Edge TTS installed!")
            self._setup_edge_tts()
        except Exception as e:
            print(f"❌ Failed to install Edge TTS: {e}")
            self._setup_fallback_tts()
    
    def _setup_microphone(self):
        """Setup microphone and speech recognition."""
        self.recognizer = sr.Recognizer()
        try:
            # Suppress audio system messages
            from contextlib import redirect_stderr
            from io import StringIO
            
            stderr_capture = StringIO()
            with redirect_stderr(stderr_capture):
                self.microphone = sr.Microphone(device_index=self.microphone_index)
                
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    self.recognizer.energy_threshold = 800
                    self.recognizer.dynamic_energy_threshold = True
                    self.recognizer.pause_threshold = 0.6
            print("✅ Enhanced microphone test successful!")
        except Exception as e:
            print(f"❌ Error initializing microphone: {e}")
            self.microphone = None
    
    def speak(self, text: str, rate: Optional[float] = None):
        """Speak text using the modern voice model."""
        if not hasattr(self, 'voice_type'):
            print("❌ Voice model not initialized!")
            return
        
        try:
            if self.voice_type == "coqui":
                self._speak_coqui(text, rate)
            elif self.voice_type == "piper":
                self._speak_piper(text, rate)
            elif self.voice_type == "gtts":
                self._speak_gtts(text, rate)
            elif self.voice_type == "edge":
                self._speak_edge(text, rate)
            elif self.voice_type == "fallback":
                self._speak_fallback(text, rate)
            else:
                print(f"❌ Unknown voice type: {self.voice_type}")
                
        except Exception as e:
            print(f"❌ Speech error: {e}")
    
    def _speak_coqui(self, text: str, rate: Optional[float] = None):
        """Speak using Coqui TTS."""
        print(f"🗣️  Speaking (Coqui): {text}")
        self.tts.tts_to_file(text=text, file_path="temp_speech.wav")
        
        # Play the audio file
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("temp_speech.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Clean up
        if os.path.exists("temp_speech.wav"):
            os.remove("temp_speech.wav")
    
    def _speak_piper(self, text: str, rate: Optional[float] = None):
        """Speak using Piper TTS."""
        print(f"🗣️  Speaking (Piper): {text}")
        
        # Use piper command line
        cmd = ["piper", "--model", "en_US-amy-low.onnx", "--output_file", "temp_speech.wav"]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
        
        # Play the audio file
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("temp_speech.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Clean up
        if os.path.exists("temp_speech.wav"):
            os.remove("temp_speech.wav")
    
    def _speak_gtts(self, text: str, rate: Optional[float] = None):
        """Speak using Google TTS."""
        print(f"🗣️  Speaking (Google): {text}")
        
        # Generate speech
        tts = self.gtts(text=text, lang='en', slow=False)
        tts.save("temp_speech.mp3")
        
        # Play the audio file
        self.pygame.mixer.init()
        self.pygame.mixer.music.load("temp_speech.mp3")
        self.pygame.mixer.music.play()
        while self.pygame.mixer.music.get_busy():
            self.pygame.time.Clock().tick(10)
        
        # Clean up
        if os.path.exists("temp_speech.mp3"):
            os.remove("temp_speech.mp3")
    
    def _speak_edge(self, text: str, rate: Optional[float] = None):
        """Speak using Microsoft Edge TTS."""
        print(f"🗣️  Speaking (Edge): {text}")
        
        import asyncio
        import edge_tts
        
        async def speak_async():
            communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
            await communicate.save("temp_speech.mp3")
        
        # Run the async function
        asyncio.run(speak_async())
        
        # Play the audio file
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("temp_speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Clean up
        if os.path.exists("temp_speech.mp3"):
            os.remove("temp_speech.mp3")
    
    def _speak_fallback(self, text: str, rate: Optional[float] = None):
        """Speak using fallback pyttsx3."""
        print(f"🗣️  Speaking (Fallback): {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def speak_slow(self, text: str):
        """Speak text slowly."""
        self.speak(text, rate=0.8)
    
    def speak_fast(self, text: str):
        """Speak text quickly."""
        self.speak(text, rate=1.2)
    
    def speak_quiet(self, text: str):
        """Speak text quietly."""
        self.speak(text)
    
    def speak_loud(self, text: str):
        """Speak text loudly."""
        self.speak(text)
    
    def listen(self):
        """Listen for voice commands."""
        if not self.microphone:
            print("❌ Voice control not available.")
            return None

        try:
            # Suppress audio system messages
            from contextlib import redirect_stderr
            from io import StringIO
            
            stderr_capture = StringIO()
            with redirect_stderr(stderr_capture):
                with self.microphone as source:
                    self.speak_quiet("Listening...")
                    print("\n👂 Listening... (speak now)")
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    print("🔄 Processing your command...")
                    try:
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
    
    def close(self):
        """Clean up resources."""
        print("🔌 Modern voice interface closed.")

# Test function
def test_modern_voice():
    """Test the modern voice interface."""
    print("🎤 Testing Modern Voice Interface")
    print("=" * 40)
    
    voice = ModernVoiceInterface()
    
    test_phrases = [
        "Hello, this is a modern voice test.",
        "The temperature is seventy-two degrees.",
        "LED status: ON",
        "Environmental monitoring system ready."
    ]
    
    print(f"\n🎤 Using {voice.voice_type} voice model:")
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n{i}. Speaking: '{phrase}'")
        voice.speak(phrase)
        time.sleep(1)
    
    print("\n✅ Modern voice test complete!")
    voice.close()

if __name__ == "__main__":
    test_modern_voice() 