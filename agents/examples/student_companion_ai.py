#!/usr/bin/env python3
"""
IRIS Student Companion AI - Main System
======================================

AI study companion that combines environmental monitoring with emotional support
and study assistance to create optimal learning conditions.

Author: [Your Name]
Date: [2025-01-27]
"""

import time
import sys
import os
from typing import Dict, Any, Callable
import speech_recognition as sr

# Add the parent directories to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'interfaces'))

from environmental_agent import EnvironmentalAgent
from smart_monitor import SmartMonitor
from message_generators import MessageGenerators
from student_companion import StudentCompanion
from modern_voice_interface import ModernVoiceInterface
from llm_interface import LLMInterface


class IRISStudentCompanionAI:
    """Main IRIS Student Companion AI system with emotional intelligence."""
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, 
                 model_name="llama3.1:8b-instruct-q4_0", voice_model="gtts"):
        """Initialize the IRIS Student Companion AI system."""
        # Initialize core components
        self.agent = EnvironmentalAgent(port, baud_rate)
        self.voice = ModernVoiceInterface(voice_model=voice_model)
        self.llm = LLMInterface(model_name)
        self.smart_monitor = SmartMonitor()
        self.messages = MessageGenerators()
        self.student_companion = StudentCompanion()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        if not self.agent.connected:
            print("❌ Cannot initialize without Arduino connection")
            return
        
        # Initialize action handlers
        self.action_handlers = {
            "start_session": self._handle_start_session,
            "end_session": self._handle_end_session,
            "take_break": self._handle_take_break,
            "get_stats": self._handle_get_stats,
            "environmental_help": self._handle_environmental_help,
            "emotional_support": self._handle_emotional_support,
            "study_advice": self._handle_study_advice,
            "turn_led_on": self._handle_turn_led_on,
            "turn_led_off": self._handle_turn_led_off,
            "turn_fan_on": self._handle_turn_fan_on,
            "turn_fan_off": self._handle_turn_fan_off,
            "status": self._handle_status,
            "analyze": self._handle_analyze
        }
        
        print("IRIS Student Companion AI Ready!")
        print(f" Using {self.voice.voice_type} voice model for natural conversation!")
        self.voice.speak("Hello! I'm IRIS, your AI study companion. I'm here to help you study better and feel supported.")
    
    def get_voice_input(self) -> str:
        """Get voice input from the user."""
        try:
            with self.microphone as source:
                print("Listening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower().strip()
            
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
        except Exception as e:
            print(f"Error with voice input: {e}")
            return ""
    
    def get_user_input(self) -> str:
        """Get input from user (text or voice)."""
        print("\nInput options:")
        print("1. Type your message")
        print("2. Speak your message (voice)")
        
        try:
            choice = input("Choose input method (1 or 2): ").strip()
            
            if choice == "2":
                return self.get_voice_input()
            else:
                return input("You: ").strip().lower()
                
        except KeyboardInterrupt:
            return "quit"
        except Exception as e:
            print(f"Input error: {e}")
            return input("You: ").strip().lower()
    
    def _handle_start_session(self) -> bool:
        """Handle starting a study session."""
        message = self.student_companion.start_study_session()
        self.voice.speak(message)
        return True
    
    def _handle_end_session(self) -> bool:
        """Handle ending a study session."""
        message = self.student_companion.end_study_session()
        self.voice.speak(message)
        return True
    
    def _handle_take_break(self) -> bool:
        """Handle taking a study break."""
        message = self.student_companion.take_break()
        self.voice.speak(message)
        return True
    
    def _handle_get_stats(self) -> bool:
        """Handle getting study statistics."""
        stats = self.student_companion.get_study_stats()
        if stats["session_active"]:
            message = f"You've been studying for {stats['study_time_minutes']} minutes, taken {stats['breaks_taken']} breaks, and your current mood is {stats['current_mood']}."
        else:
            message = "No active study session. Say 'start session' to begin studying!"
        self.voice.speak(message)
        return True
    
    def _handle_environmental_help(self) -> bool:
        """Handle environmental assistance requests."""
        status = self.agent.get_status()
        if "error" not in status:
            recommendations = self.student_companion.get_environmental_recommendations(status)
            if recommendations:
                message = " ".join(recommendations)
            else:
                message = "Your study environment looks great! Perfect conditions for learning."
        else:
            message = "I can't check the environment right now, but I'm here to help!"
        self.voice.speak(message)
        return True
    
    def _handle_emotional_support(self) -> bool:
        """Handle emotional support requests."""
        # Get current environment
        status = self.agent.get_status()
        environment = status if "error" not in status else {}
        
        # Generate supportive message
        context = {
            "study_time_minutes": self.student_companion.study_time_minutes,
            "mood": self.student_companion.student_mood,
            "stress_level": self.student_companion.stress_level,
            "environment": environment
        }
        
        message = self.messages.get_student_support_message(context)
        self.voice.speak(message)
        return True
    
    def _handle_study_advice(self) -> bool:
        """Handle study advice requests."""
        study_time = self.student_companion.study_time_minutes
        stress_level = self.student_companion.stress_level
        
        if study_time > 90:
            message = "You've been studying for a while. How about a 5-minute break? Your brain will thank you!"
        elif stress_level > 6:
            message = "I can sense you're feeling stressed. Let's take a moment to breathe. You're doing great!"
        else:
            message = "You're in a great study rhythm! Keep up the good work and remember to take breaks when you need them."
        
        self.voice.speak(message)
        return True
    
    def _handle_turn_led_on(self) -> bool:
        """Handle turning LED on."""
        success = self.agent.turn_led_on()
        if success:
            self.voice.speak("I've turned on the LED to help with better lighting for your studies.")
        return success
    
    def _handle_turn_led_off(self) -> bool:
        """Handle turning LED off."""
        success = self.agent.turn_led_off()
        if success:
            self.voice.speak("I've turned off the LED.")
        return success
    
    def _handle_turn_fan_on(self) -> bool:
        """Handle turning fan on."""
        success = self.agent.turn_fan_on()
        if success:
            self.voice.speak("I've turned on the fan to help keep you comfortable while studying.")
        return success
    
    def _handle_turn_fan_off(self) -> bool:
        """Handle turning fan off."""
        success = self.agent.turn_fan_off()
        if success:
            self.voice.speak("I've turned off the fan.")
        return success
    
    def _handle_status(self) -> bool:
        """Handle status request."""
        status = self.agent.get_status()
        message = self.messages.get_status_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def _handle_analyze(self) -> bool:
        """Handle environmental analysis."""
        status = self.agent.get_status()
        if "error" not in status:
            # Combine environmental and student analysis
            env_message = self.messages.get_analysis_message(status)
            student_context = {
                "study_time_minutes": self.student_companion.study_time_minutes,
                "mood": self.student_companion.student_mood,
                "stress_level": self.student_companion.stress_level,
                "environment": status
            }
            student_message = self.messages.get_student_support_message(student_context)
            
            full_message = f"{env_message} {student_message}"
        else:
            full_message = "I can't analyze the environment right now, but I'm here to support your study session!"
        
        self.voice.speak(full_message)
        return True
    
    def process_student_input(self, user_input: str):
        """Process student input with emotional intelligence."""
        # Update study time
        self.student_companion.update_study_time()
        
        # Analyze student input
        analysis = self.student_companion.analyze_student_input(user_input)
        
        # Get current environment
        status = self.agent.get_status()
        environment = status if "error" not in status else {}
        
        # Generate response using LLM with student personality
        try:
            context = {
                "study_time_minutes": self.student_companion.study_time_minutes,
                "mood": analysis.get("mood", "neutral"),
                "stress_level": analysis.get("stress_level", 0),
                "environment": environment
            }
            
            response = self.llm.query_student_companion(user_input, context)
        except Exception as e:
            print(f"LLM query failed: {e}")
            # Fallback to rule-based response
            response = self.student_companion.generate_student_response(analysis, environment)
        
        # Speak the response
        self.voice.speak(response)
        
        # Check for proactive interventions
        if self.student_companion.should_intervene():
            intervention = self.student_companion.get_intervention_message(environment)
            if intervention:
                time.sleep(2)  # Brief pause
                self.voice.speak(intervention)
    
    def run_interactive_mode(self):
        """Run the student companion in interactive mode."""
        print("\nIRIS Student Companion AI - Interactive Mode")
        print("=" * 50)
        print("Commands:")
        print("  'start session' - Begin a study session")
        print("  'end session' - End current study session")
        print("  'take break' - Take a study break")
        print("  'stats' - Get study statistics")
        print("  'environment' - Get environmental help")
        print("  'support' - Get emotional support")
        print("  'advice' - Get study advice")
        print("  'status' - Check environmental status")
        print("  'analyze' - Full environmental and student analysis")
        print("  'quit' - Exit the program")
        print("\nOr just talk to me naturally! I'm here to help you study better.")
        print("You can type or speak to IRIS!")
        print("=" * 50)
        
        # Start with a greeting
        self.voice.speak("I'm ready to be your study companion! What would you like to do?")
        
        while True:
            try:
                user_input = self.get_user_input()
                
                if user_input == "quit":
                    self.voice.speak("Goodbye! Great job studying today!")
                    break
                
                # Handle specific commands
                if user_input == 'start session':
                    self._handle_start_session()
                elif user_input == 'end session':
                    self._handle_end_session()
                elif user_input == 'take break':
                    self._handle_take_break()
                elif user_input == 'stats':
                    self._handle_get_stats()
                elif user_input == 'environment':
                    self._handle_environmental_help()
                elif user_input == 'support':
                    self._handle_emotional_support()
                elif user_input == 'advice':
                    self._handle_study_advice()
                elif user_input == 'status':
                    self._handle_status()
                elif user_input == 'analyze':
                    self._handle_analyze()
                else:
                    # Process as natural conversation
                    self.process_student_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! Keep up the great studying!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.voice.speak("I'm having a moment. Let's try again!")
    
    def run_demo_mode(self):
        """Run a demonstration of student companion features."""
        print("\nIRIS Student Companion AI - Demo Mode")
        print("=" * 50)
        
        # Demo 1: Start session
        print("Demo 1: Starting a study session")
        self.voice.speak("Let's start your study session!")
        self._handle_start_session()
        time.sleep(2)
        
        # Demo 2: Environmental monitoring
        print("Demo 2: Environmental monitoring")
        self.voice.speak("Let me check your study environment.")
        self._handle_analyze()
        time.sleep(2)
        
        # Demo 3: Emotional support
        print("Demo 3: Emotional support")
        self.voice.speak("I'm here to support you emotionally and academically.")
        self._handle_emotional_support()
        time.sleep(2)
        
        # Demo 4: Study advice
        print("Demo 4: Study advice")
        self.voice.speak("Let me give you some study advice.")
        self._handle_study_advice()
        time.sleep(2)
        
        # Demo 5: End session
        print("Demo 5: Ending study session")
        self.voice.speak("Great job studying! Let's wrap up your session.")
        self._handle_end_session()
        
        print("\nDemo complete! IRIS is ready to be your study companion!")
    
    def close(self):
        """Clean up resources."""
        if hasattr(self, 'agent'):
            self.agent.close()


def main():
    """Main function to run the student companion AI."""
    print("IRIS Student Companion AI")
    print("=" * 40)
    
    # Initialize the system
    iris = IRISStudentCompanionAI()
    
    if not iris.agent.connected:
        print("❌ Please connect your Arduino and try again.")
        return
    
    # Choose mode
    print("\nChoose mode:")
    print("1. Interactive mode (talk to IRIS)")
    print("2. Demo mode (see features)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            iris.run_demo_mode()
        else:
            iris.run_interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        iris.close()


if __name__ == "__main__":
    main() 