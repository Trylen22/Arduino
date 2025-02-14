import serial
import time
import subprocess
import logging
import sys
import threading
import speech_recognition as sr

class LEDAssistant:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0"):
        """Initialize your friendly LED assistant"""
        self.model_name = model_name
        self.chat_history = []  # Add chat history list
        self.led_states = {     # Track LED states
            'green': False,
            'red': False
        }
        
        # List available microphones first
        print("\nAvailable Microphones:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone {index}: {name}")
        
        # Initialize speech recognizer with specific device
        self.recognizer = sr.Recognizer()
        
        try:
            # Use the HyperX SoloCast microphone
            self.microphone = sr.Microphone(device_index=9)  # HyperX SoloCast
            
            # Test the microphone
            print("\nTesting microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 1000  # Might need adjustment for the HyperX
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.pause_threshold = 0.8
            print("Microphone test successful!")
            
        except Exception as e:
            print(f"\nError initializing microphone: {e}")
            print("Voice control will not be available.")
            self.microphone = None
        
        # Try to connect to Arduino
        try:
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print("\nHi! I'm your LED friend! I can help you control the red and green lights.")
            print("You can type or speak your commands!")
        except Exception as e:
            print("\nOops! I couldn't connect to the Arduino.")
            print(f"Here's what went wrong: {e}")
            self.arduino = None

    def listen(self):
        """Listen for voice command"""
        if not self.microphone:
            print("Sorry, voice control is not available.")
            return None
            
        try:
            with self.microphone as source:
                print("\nListening... (speak now)")
                # Reduced timeout and phrase time limit
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=6)
                print("Processing your command...")
                
                try:
                    # Using a more lenient recognition setting
                    text = self.recognizer.recognize_google(audio)  # Removed language specification for faster processing
                    print(f"You said: {text}")
                    return text
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand that.")
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None
                
        except Exception as e:
            print(f"Error listening: {e}")
            return None

    def _control_green_on(self):
        """Turn green LED on"""
        if self.arduino:
            try:
                self.arduino.write(b'G')
                return True
            except:
                return False

    def _control_green_off(self):
        """Turn green LED off"""
        if self.arduino:
            try:
                self.arduino.write(b'g')
                return True
            except:
                return False

    def _control_red_on(self):
        """Turn red LED on"""
        if self.arduino:
            try:
                self.arduino.write(b'R')
                return True
            except:
                return False

    def _control_red_off(self):
        """Turn red LED off"""
        if self.arduino:
            try:
                self.arduino.write(b'r')
                return True
            except:
                return False

    def _control_both_on(self):
        """Turn both LEDs on"""
        if self.arduino:
            try:
                self.arduino.write(b'B')
                return True
            except:
                return False

    def _control_both_off(self):
        """Turn both LEDs off"""
        if self.arduino:
            try:
                self.arduino.write(b'b')
                return True
            except:
                return False

    def _wait(self, seconds):
        """Wait for specified number of seconds"""
        time.sleep(seconds)
        return True

    def chat(self, user_input):
        """Chat with the assistant"""
        try:
            # Add user input to history
            self.chat_history.append({"role": "user", "content": user_input})
            
            # Create chat history context
            history_text = "\n".join([
                f"{'Assistant' if msg['role'] == 'assistant' else 'User'}: {msg['content']}"
                for msg in self.chat_history[-5:]  # Include last 5 messages
            ])

            system_prompt = f"""You are a friendly LED assistant who can control a red and green LED.
            You have the following commands available:
            - _control_green_on() - Turn green LED on
            - _control_green_off() - Turn green LED off
            - _control_red_on() - Turn red LED on
            - _control_red_off() - Turn red LED off
            - _control_both_on() - Turn both LEDs on
            - _control_both_off() - Turn both LEDs off
            - _wait(seconds) - Wait for specified number of seconds
            
            For sequential tasks, you can use multiple commands. For example:
            - To turn red on, wait 3 seconds, then off: _control_red_on() _wait(3) _control_red_off()
            
            Current LED states:
            - Green LED: {'ON' if self.led_states['green'] else 'OFF'}
            - Red LED: {'ON' if self.led_states['red'] else 'OFF'}
            
            Recent conversation:
            {history_text}
            
            IMPORTANT: You MUST include the appropriate function calls in your response when asked to control lights.
            For sequential tasks, include ALL necessary commands in order.
            Be friendly and helpful! Keep responses brief and clear.
            Only control lights when specifically asked.
            ALWAYS include the function calls in your response when asked to control lights.
            DO NOT USE EMOJIS"""

            # Get response from model
            full_prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            response, _ = process.communicate(input=full_prompt)
            response = response.strip()

            # Update LED states based on commands
            if '_control_green_on()' in response:
                self.led_states['green'] = True
            elif '_control_green_off()' in response:
                self.led_states['green'] = False
            elif '_control_red_on()' in response:
                self.led_states['red'] = True
            elif '_control_red_off()' in response:
                self.led_states['red'] = False
            elif '_control_both_on()' in response:
                self.led_states['green'] = True
                self.led_states['red'] = True
            elif '_control_both_off()' in response:
                self.led_states['green'] = False
                self.led_states['red'] = False

            # Execute commands in sequence
            commands = []
            for command in response.split():
                if '(' in command and ')' in command:
                    commands.append(command)

            for command in commands:
                if '_wait' in command:
                    seconds = float(command.split('(')[1].split(')')[0])
                    success = self._wait(seconds)
                else:
                    success = getattr(self, command.rstrip('()'))()
                if not success:
                    return f"I tried to execute {command} but something went wrong"

            # Add assistant's response to history
            self.chat_history.append({"role": "assistant", "content": response})

            # Clean up the response by removing function calls
            for command in ['_control_green_on()', '_control_green_off()', 
                          '_control_red_on()', '_control_red_off()',
                          '_control_both_on()', '_control_both_off()']:
                response = response.replace(command, "")
            return response.strip()

        except Exception as e:
            return f"Sorry, I had some trouble understanding that ({str(e)})"

    def reset_chat(self):
        """Reset the chat history"""
        self.chat_history = []
        print("Chat history has been reset!")

    def close(self):
        """Close the connection"""
        if self.arduino:
            self.arduino.close()
            print("Goodbye! Thanks for chatting with me! 👋")

if __name__ == "__main__":
    # Example usage
    assistant = LEDAssistant()
    
    print("\nChat with me! (type 'bye' to exit, or 'voice' to use voice command)")
    while True:
        print("\nYou:", end=" ")
        user_input = input()
        
        if user_input.lower() in ['bye', 'goodbye', 'exit']:
            break
        elif user_input.lower() == 'voice':
            voice_input = assistant.listen()
            if voice_input:
                response = assistant.chat(voice_input)
                print("Assistant:", response)
        else:
            response = assistant.chat(user_input)
            print("Assistant:", response)
    
    assistant.close()