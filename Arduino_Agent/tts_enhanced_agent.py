"""
Enhanced Two LED Control Agent with Text-to-Speech
=================================================

This enhanced version adds text-to-speech capabilities to provide voice feedback
when controlling the LEDs. The agent can now speak responses and confirmations.

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

# ===== ENHANCED RED & GREEN LED ASSISTANT CLASS =====
class EnhancedRedGreenLEDAssistant:
    """
    Enhanced assistant class with text-to-speech capabilities.
    Provides voice feedback for all LED control operations.
    """
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0"):
        """
        Initialize the Enhanced Red & Green LED Assistant with TTS capabilities.
        
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
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            print(f"Found {len(voices)} available voices")
            
            # Try to find a good English voice
            good_voice = None
            for voice in voices:
                if 'en-us' in voice.id.lower() or 'en-gb' in voice.id.lower():
                    good_voice = voice
                    break
            
            # Configure TTS settings for better clarity
            self.tts_engine.setProperty('rate', 120)     # Slower speed for clarity
            self.tts_engine.setProperty('volume', 0.9)   # Higher volume
            self.tts_engine.setProperty('pitch', 1.1)    # Slightly higher pitch for clarity
            
            # Set the best available voice
            if good_voice:
                self.tts_engine.setProperty('voice', good_voice.id)
                print(f"Using voice: {good_voice.name}")
            elif voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                print(f"Using voice: {voices[0].name}")
            
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
            self.speak("Hi! I'm your Red and Green LED assistant! I can help you control the LEDs.")
            print("\nHi! I'm your Red & Green LED assistant! I can help you control the red and green LEDs.")
            print("You can type or speak your commands!")
            
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

    # ===== ENHANCED DEVICE CONTROL FUNCTIONS =====
    # These functions now include voice feedback
    
    def _control_red_led_on(self):
        """
        Turn Red LED on with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending '1' command to Arduino (Red LED ON)")
                self.arduino.write(b'1\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = True
                self.speak("Red LED is now on")
                return True
            except Exception as e:
                print("Error turning Red LED on:", e)
                self.speak("Sorry, there was an error turning on the red LED")
                return False

    def _control_red_led_off(self):
        """
        Turn Red LED off with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'a' command to Arduino (Red LED OFF)")
                self.arduino.write(b'a\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = False
                self.speak("Red LED is now off")
                return True
            except Exception as e:
                print("Error turning Red LED off:", e)
                self.speak("Sorry, there was an error turning off the red LED")
                return False

    def _control_green_led_on(self):
        """
        Turn Green LED on with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending '2' command to Arduino (Green LED ON)")
                self.arduino.write(b'2\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['green_led'] = True
                self.speak("Green LED is now on")
                return True
            except Exception as e:
                print("Error turning Green LED on:", e)
                self.speak("Sorry, there was an error turning on the green LED")
                return False

    def _control_green_led_off(self):
        """
        Turn Green LED off with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'b' command to Arduino (Green LED OFF)")
                self.arduino.write(b'b\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['green_led'] = False
                self.speak("Green LED is now off")
                return True
            except Exception as e:
                print("Error turning Green LED off:", e)
                self.speak("Sorry, there was an error turning off the green LED")
                return False

    def _control_both_leds_on(self):
        """
        Turn both LEDs on with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending '3' command to Arduino (Both LEDs ON)")
                self.arduino.write(b'3\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = True
                self.device_states['green_led'] = True
                self.speak("Both LEDs are now on")
                return True
            except Exception as e:
                print("Error turning both LEDs on:", e)
                self.speak("Sorry, there was an error turning on both LEDs")
                return False

    def _control_both_leds_off(self):
        """
        Turn both LEDs off with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'c' command to Arduino (Both LEDs OFF)")
                self.arduino.write(b'c\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = False
                self.device_states['green_led'] = False
                self.speak("Both LEDs are now off")
                return True
            except Exception as e:
                print("Error turning both LEDs off:", e)
                self.speak("Sorry, there was an error turning off both LEDs")
                return False

    def _toggle_red_led(self):
        """
        Toggle Red LED state with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 't1' command to Arduino (Toggle Red LED)")
                self.arduino.write(b't1\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['red_led'] = not self.device_states['red_led']
                status = "on" if self.device_states['red_led'] else "off"
                self.speak(f"Red LED is now {status}")
                return True
            except Exception as e:
                print("Error toggling Red LED:", e)
                self.speak("Sorry, there was an error toggling the red LED")
                return False

    def _toggle_green_led(self):
        """
        Toggle Green LED state with voice confirmation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 't2' command to Arduino (Toggle Green LED)")
                self.arduino.write(b't2\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                print("DEBUG: Command sent successfully")
                self.device_states['green_led'] = not self.device_states['green_led']
                status = "on" if self.device_states['green_led'] else "off"
                self.speak(f"Green LED is now {status}")
                return True
            except Exception as e:
                print("Error toggling Green LED:", e)
                self.speak("Sorry, there was an error toggling the green LED")
                return False

    def _check_status(self):
        """
        Check and report LED status with voice feedback.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'S' command to Arduino (Status)")
                self.arduino.write(b'S\n')  # Add newline
                self.arduino.flush()  # Ensure data is sent
                time.sleep(0.2)  # Wait for Arduino to process
                
                # Read Arduino response
                if self.arduino.in_waiting:
                    response = self.arduino.readline().decode('utf-8').strip()
                    print(f"Arduino status: {response}")
                
                # Create voice status report
                red_status = "on" if self.device_states['red_led'] else "off"
                green_status = "on" if self.device_states['green_led'] else "off"
                status_message = f"Red LED is {red_status}, Green LED is {green_status}"
                self.speak(status_message)
                print(f"Status: {status_message}")
                return True
            except Exception as e:
                print("Error checking status:", e)
                self.speak("Sorry, there was an error checking the LED status")
                return False

    def _wait(self, seconds):
        """
        Wait for specified seconds with voice confirmation.
        
        Args:
            seconds (float): Number of seconds to wait
        """
        try:
            self.speak(f"Waiting for {seconds} seconds")
            print(f"Waiting for {seconds} seconds...")
            time.sleep(seconds)
            self.speak("Wait complete")
            print("Wait complete!")
        except Exception as e:
            print(f"Error during wait: {e}")

    def _delay(self, seconds):
        """
        Alias for _wait function.
        
        Args:
            seconds (float): Number of seconds to wait
        """
        self._wait(seconds)

    def close(self):
        """
        Clean up resources and close connections.
        """
        if self.arduino:
            self.arduino.close()
        if self.tts_engine:
            self.tts_engine.stop()
        print("Assistant closed.")

# ===== MAIN INTERFACE =====
def main():
    """
    Main function to run the enhanced LED assistant with TTS.
    """
    print("Starting Enhanced Red & Green LED Assistant with TTS...")
    
    # Create the enhanced assistant
    assistant = EnhancedRedGreenLEDAssistant()
    
    try:
        while True:
            print("\n" + "="*50)
            print("Enhanced LED Assistant - Voice & Text Interface")
            print("="*50)
            print("Commands you can try:")
            print("- 'Turn on the red LED'")
            print("- 'Turn off the green LED'")
            print("- 'Toggle both LEDs'")
            print("- 'What's the status?'")
            print("- 'Wait 3 seconds'")
            print("- Type 'quit' to exit")
            print("="*50)
            
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
                # Process the command (you can integrate with your existing LLM logic here)
                print(f"\nProcessing: {user_input}")
                assistant.speak(f"Processing your request: {user_input}")
                
                # Simple command processing (you can enhance this with your LLM)
                user_input_lower = user_input.lower()
                
                if 'red' in user_input_lower and 'on' in user_input_lower:
                    assistant._control_red_led_on()
                elif 'red' in user_input_lower and 'off' in user_input_lower:
                    assistant._control_red_led_off()
                elif 'green' in user_input_lower and 'on' in user_input_lower:
                    assistant._control_green_led_on()
                elif 'green' in user_input_lower and 'off' in user_input_lower:
                    assistant._control_green_led_off()
                elif 'both' in user_input_lower and 'on' in user_input_lower:
                    assistant._control_both_leds_on()
                elif 'both' in user_input_lower and 'off' in user_input_lower:
                    assistant._control_both_leds_off()
                elif 'toggle' in user_input_lower and 'red' in user_input_lower:
                    assistant._toggle_red_led()
                elif 'toggle' in user_input_lower and 'green' in user_input_lower:
                    assistant._toggle_green_led()
                elif 'status' in user_input_lower or 'what' in user_input_lower:
                    assistant._check_status()
                elif 'wait' in user_input_lower:
                    # Extract number from command
                    import re
                    numbers = re.findall(r'\d+', user_input)
                    if numbers:
                        seconds = int(numbers[0])
                        assistant._wait(seconds)
                    else:
                        assistant.speak("Please specify how many seconds to wait")
                else:
                    assistant.speak("I'm not sure how to handle that command. Please try again.")
                    print("Unknown command. Please try again.")
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        assistant.speak("Goodbye!")
        assistant.close()

if __name__ == "__main__":
    main() 