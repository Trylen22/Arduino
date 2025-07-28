"""
LLM-Enhanced LED Assistant with Text-to-Speech
==============================================

This advanced version combines your existing LLM capabilities with text-to-speech
for intelligent voice interactions. The LLM can now respond with voice feedback
and handle complex natural language commands.

Author: [Your Name]
Date: [2025-01-27]
"""

# ===== IMPORTS =====
import serial          # For communicating with Arduino
import time           # For adding delays
import subprocess     # For running external commands (Ollama)
import threading      # For potential multi-threading
import speech_recognition as sr  # For voice recognition
import pyttsx3        # For text-to-speech
import re             # For parsing function calls
import json           # For structured responses

# ===== LLM-ENHANCED LED ASSISTANT CLASS =====
class LLMEnhancedLEDAssistant:
    """
    Advanced assistant class that combines LLM intelligence with TTS capabilities.
    Provides intelligent voice interactions and natural language processing.
    """
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0"):
        """
        Initialize the LLM-Enhanced LED Assistant.
        
        Args:
            port (str): Serial port for Arduino connection
            baud_rate (int): Baud rate for serial communication
            model_name (str): Name of the Ollama model to use
        """
        # Store model name for later use
        self.model_name = model_name
        
        # Initialize device states (tracked locally)
        self.device_states = {
            'red_led': False,
            'green_led': False
        }
        
        # ===== TEXT-TO-SPEECH SETUP =====
        try:
            self.tts_engine = pyttsx3.init()
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)    # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            # Get available voices and set a nice one
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            print("Text-to-speech initialized successfully!")
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            self.tts_engine = None
        
        # ===== MICROPHONE SETUP =====
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        try:
            # Try to use a specific microphone (adjust device_index as needed)
            self.microphone = sr.Microphone(device_index=9)
            
            # Configure the recognizer
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 1000  # Adjust sensitivity
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.pause_threshold = 0.8
            print("Microphone test successful!")
        except Exception as e:
            # Handle microphone initialization errors
            print(f"\nError initializing microphone: {e}")
            print("Voice control will not be available.")
            self.microphone = None

        # ===== ARDUINO CONNECTION =====
        try:
            # Attempt to connect to Arduino
            print(f"\nAttempting to connect to Arduino on port {port} at {baud_rate} baud...")
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Allow time for Arduino to reset
            self.speak("Hi! I'm your intelligent LED assistant! I can help you control the LEDs with natural language.")
            print("\nHi! I'm your intelligent LED assistant! I can help you control the LEDs with natural language.")
            print("You can speak or type your commands!")
            
            # Test Arduino connection with a simple command
            print("\nTesting Arduino connection...")
            self.arduino.write(b'S\n')  # Add newline
            self.arduino.flush()
            time.sleep(1)
            if self.arduino.in_waiting:
                response = self.arduino.readline().decode('utf-8').strip()
                print(f"Arduino response: {response}")
                print("Arduino connection test successful!")
                self.speak("Arduino connected successfully!")
            else:
                print("WARNING: No response from Arduino. Communication may be one-way.")
                self.speak("Warning: Arduino communication may be limited.")
        except Exception as e:
            # Handle Arduino connection errors
            print("\nOops! I couldn't connect to the Arduino.")
            print(f"Error: {e}")
            self.speak("Sorry, I couldn't connect to the Arduino.")
            self.arduino = None

    # ===== TEXT-TO-SPEECH FUNCTION =====
    def speak(self, text):
        """
        Convert text to speech and play it.
        
        Args:
            text (str): The text to speak
        """
        if self.tts_engine:
            try:
                print(f"Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
        else:
            print(f"TTS not available: {text}")

    # ===== VOICE RECOGNITION =====
    def listen(self):
        """
        Listen for a voice command using the microphone.
        
        Returns:
            str: The recognized text command, or None if recognition failed
        """
        if not self.microphone:
            print("Voice control not available.")
            return None

        try:
            with self.microphone as source:
                self.speak("Listening...")
                print("\nListening... (speak now)")
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=6)
                print("Processing your command...")
                try:
                    # Use Google's speech recognition service
                    text = self.recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text
                except sr.UnknownValueError:
                    self.speak("Sorry, I couldn't understand that.")
                    print("Sorry, I couldn't understand that.")
                    return None
                except sr.RequestError as e:
                    self.speak("Could not process your request.")
                    print(f"Could not request results; {e}")
                    return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None

    # ===== LLM INTEGRATION =====
    def generate_llm_prompt(self, user_input):
        """
        Generate a prompt for the LLM based on user input and current state.
        
        Args:
            user_input (str): The user's input (voice or text)
            
        Returns:
            str: Formatted prompt for the LLM
        """
        current_state = f"Red LED: {'ON' if self.device_states['red_led'] else 'OFF'}, Green LED: {'ON' if self.device_states['green_led'] else 'OFF'}"
        
        prompt = f"""You are an intelligent LED control assistant. You can control a red LED and a green LED connected to an Arduino.

Current LED states: {current_state}

Available actions:
- Turn red LED on/off
- Turn green LED on/off  
- Turn both LEDs on/off
- Toggle red LED
- Toggle green LED
- Check status
- Wait for specified time

User request: "{user_input}"

Please respond with a JSON object containing:
1. "action": The action to perform (e.g., "turn_red_on", "toggle_green", "status", "wait")
2. "parameters": Any parameters needed (e.g., {"seconds": 5} for wait)
3. "response": A natural language response to speak to the user
4. "explanation": Brief explanation of what you're doing

Example response:
{{
    "action": "turn_red_on",
    "parameters": {{}},
    "response": "I'll turn on the red LED for you.",
    "explanation": "Turning on the red LED"
}}

Respond only with the JSON object:"""

        return prompt

    def query_llm(self, prompt):
        """
        Query the local LLM using Ollama.
        
        Args:
            prompt (str): The prompt to send to the LLM
            
        Returns:
            dict: Parsed JSON response from the LLM
        """
        try:
            # Use Ollama to query the local model
            cmd = [
                'ollama', 'run', self.model_name,
                prompt
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response_text = result.stdout.strip()
                print(f"LLM Response: {response_text}")
                
                # Try to parse JSON from the response
                try:
                    # Extract JSON from the response (handle cases where LLM adds extra text)
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start != -1 and json_end != 0:
                        json_str = response_text[json_start:json_end]
                        return json.loads(json_str)
                    else:
                        raise ValueError("No JSON found in response")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON: {e}")
                    # Fallback to simple command parsing
                    return self.fallback_command_parsing(response_text)
            else:
                print(f"LLM query failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("LLM query timed out")
            return None
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return None

    def fallback_command_parsing(self, text):
        """
        Fallback command parsing when LLM JSON parsing fails.
        
        Args:
            text (str): The LLM response text
            
        Returns:
            dict: Parsed command structure
        """
        text_lower = text.lower()
        
        # Simple keyword-based parsing
        if 'red' in text_lower and 'on' in text_lower:
            return {
                "action": "turn_red_on",
                "parameters": {},
                "response": "I'll turn on the red LED.",
                "explanation": "Turning on the red LED"
            }
        elif 'red' in text_lower and 'off' in text_lower:
            return {
                "action": "turn_red_off", 
                "parameters": {},
                "response": "I'll turn off the red LED.",
                "explanation": "Turning off the red LED"
            }
        elif 'green' in text_lower and 'on' in text_lower:
            return {
                "action": "turn_green_on",
                "parameters": {},
                "response": "I'll turn on the green LED.",
                "explanation": "Turning on the green LED"
            }
        elif 'green' in text_lower and 'off' in text_lower:
            return {
                "action": "turn_green_off",
                "parameters": {},
                "response": "I'll turn off the green LED.",
                "explanation": "Turning off the green LED"
            }
        elif 'both' in text_lower and 'on' in text_lower:
            return {
                "action": "turn_both_on",
                "parameters": {},
                "response": "I'll turn on both LEDs.",
                "explanation": "Turning on both LEDs"
            }
        elif 'both' in text_lower and 'off' in text_lower:
            return {
                "action": "turn_both_off",
                "parameters": {},
                "response": "I'll turn off both LEDs.",
                "explanation": "Turning off both LEDs"
            }
        elif 'status' in text_lower or 'what' in text_lower:
            return {
                "action": "status",
                "parameters": {},
                "response": "I'll check the current LED status.",
                "explanation": "Checking LED status"
            }
        else:
            return {
                "action": "unknown",
                "parameters": {},
                "response": "I'm not sure how to handle that request. Please try again.",
                "explanation": "Unknown command"
            }

    # ===== DEVICE CONTROL FUNCTIONS =====
    def _control_red_led_on(self):
        """Turn Red LED on with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b'1\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['red_led'] = True
                return True
            except Exception as e:
                print("Error turning Red LED on:", e)
                return False

    def _control_red_led_off(self):
        """Turn Red LED off with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b'a\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['red_led'] = False
                return True
            except Exception as e:
                print("Error turning Red LED off:", e)
                return False

    def _control_green_led_on(self):
        """Turn Green LED on with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b'2\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['green_led'] = True
                return True
            except Exception as e:
                print("Error turning Green LED on:", e)
                return False

    def _control_green_led_off(self):
        """Turn Green LED off with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b'b\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['green_led'] = False
                return True
            except Exception as e:
                print("Error turning Green LED off:", e)
                return False

    def _control_both_leds_on(self):
        """Turn both LEDs on with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b'3\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['red_led'] = True
                self.device_states['green_led'] = True
                return True
            except Exception as e:
                print("Error turning both LEDs on:", e)
                return False

    def _control_both_leds_off(self):
        """Turn both LEDs off with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b'c\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['red_led'] = False
                self.device_states['green_led'] = False
                return True
            except Exception as e:
                print("Error turning both LEDs off:", e)
                return False

    def _toggle_red_led(self):
        """Toggle Red LED state with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b't1\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['red_led'] = not self.device_states['red_led']
                return True
            except Exception as e:
                print("Error toggling Red LED:", e)
                return False

    def _toggle_green_led(self):
        """Toggle Green LED state with voice confirmation."""
        if self.arduino:
            try:
                self.arduino.write(b't2\n')
                self.arduino.flush()
                time.sleep(0.2)
                self.device_states['green_led'] = not self.device_states['green_led']
                return True
            except Exception as e:
                print("Error toggling Green LED:", e)
                return False

    def _check_status(self):
        """Check and report LED status with voice feedback."""
        if self.arduino:
            try:
                self.arduino.write(b'S\n')
                self.arduino.flush()
                time.sleep(0.2)
                
                if self.arduino.in_waiting:
                    response = self.arduino.readline().decode('utf-8').strip()
                    print(f"Arduino status: {response}")
                
                red_status = "on" if self.device_states['red_led'] else "off"
                green_status = "on" if self.device_states['green_led'] else "off"
                status_message = f"Red LED is {red_status}, Green LED is {green_status}"
                self.speak(status_message)
                print(f"Status: {status_message}")
                return True
            except Exception as e:
                print("Error checking status:", e)
                return False

    def _wait(self, seconds):
        """Wait for specified seconds with voice confirmation."""
        try:
            self.speak(f"Waiting for {seconds} seconds")
            print(f"Waiting for {seconds} seconds...")
            time.sleep(seconds)
            self.speak("Wait complete")
            print("Wait complete!")
        except Exception as e:
            print(f"Error during wait: {e}")

    # ===== MAIN PROCESSING FUNCTION =====
    def process_command(self, user_input):
        """
        Process a user command using LLM intelligence and TTS feedback.
        
        Args:
            user_input (str): The user's input (voice or text)
        """
        print(f"\nProcessing: {user_input}")
        
        # Generate LLM prompt
        prompt = self.generate_llm_prompt(user_input)
        
        # Query the LLM
        llm_response = self.query_llm(prompt)
        
        if llm_response:
            # Extract action and parameters
            action = llm_response.get('action', 'unknown')
            parameters = llm_response.get('parameters', {})
            response_text = llm_response.get('response', 'Processing your request.')
            explanation = llm_response.get('explanation', '')
            
            print(f"LLM Action: {action}")
            print(f"Explanation: {explanation}")
            
            # Speak the response
            self.speak(response_text)
            
            # Execute the action
            success = self.execute_action(action, parameters)
            
            if not success:
                self.speak("Sorry, there was an error executing that command.")
        else:
            self.speak("Sorry, I couldn't process your request. Please try again.")

    def execute_action(self, action, parameters):
        """
        Execute the specified action with given parameters.
        
        Args:
            action (str): The action to perform
            parameters (dict): Parameters for the action
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if action == "turn_red_on":
                return self._control_red_led_on()
            elif action == "turn_red_off":
                return self._control_red_led_off()
            elif action == "turn_green_on":
                return self._control_green_led_on()
            elif action == "turn_green_off":
                return self._control_green_led_off()
            elif action == "turn_both_on":
                return self._control_both_leds_on()
            elif action == "turn_both_off":
                return self._control_both_leds_off()
            elif action == "toggle_red":
                return self._toggle_red_led()
            elif action == "toggle_green":
                return self._toggle_green_led()
            elif action == "status":
                return self._check_status()
            elif action == "wait":
                seconds = parameters.get('seconds', 1)
                self._wait(seconds)
                return True
            else:
                print(f"Unknown action: {action}")
                return False
        except Exception as e:
            print(f"Error executing action {action}: {e}")
            return False

    def close(self):
        """Clean up resources and close connections."""
        if self.arduino:
            self.arduino.close()
        if self.tts_engine:
            self.tts_engine.stop()
        print("Assistant closed.")

# ===== MAIN INTERFACE =====
def main():
    """Main function to run the LLM-enhanced LED assistant."""
    print("Starting LLM-Enhanced LED Assistant with TTS...")
    
    # Create the enhanced assistant
    assistant = LLMEnhancedLEDAssistant()
    
    try:
        while True:
            print("\n" + "="*60)
            print("LLM-Enhanced LED Assistant - Intelligent Voice Interface")
            print("="*60)
            print("Try these natural language commands:")
            print("- 'Turn on the red light'")
            print("- 'Switch off the green LED'")
            print("- 'Toggle the red LED'")
            print("- 'What's the current status?'")
            print("- 'Wait for 5 seconds'")
            print("- 'Turn on both lights'")
            print("- Type 'quit' to exit")
            print("="*60)
            
            # Get user input (voice or text)
            choice = input("\nChoose input method:\n1. Voice command\n2. Text command\nEnter choice (1 or 2): ").strip()
            
            if choice == '1':
                # Voice input
                user_input = assistant.listen()
                if user_input is None:
                    continue
            elif choice == '2':
                # Text input
                user_input = input("\nEnter your command: ").strip()
                if user_input.lower() == 'quit':
                    break
            else:
                print("Invalid choice. Please try again.")
                continue
            
            if user_input:
                # Process the command using LLM intelligence
                assistant.process_command(user_input)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        assistant.speak("Goodbye!")
        assistant.close()

if __name__ == "__main__":
    main() 