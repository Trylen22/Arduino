"""
LED and Fan Control Agent
========================

This script provides a Python agent that can control an RGB LED and a fan connected to an Arduino board.
The system supports both text and voice commands, using natural language processing to interpret user requests.

Author: [Trylen]
Date: [2025-04-08]
"""

# ===== IMPORTS =====
import serial          # For communicating with Arduino
import time           # For adding delays
import subprocess     # For running external commands (Ollama)
import threading      # For potential multi-threading
import speech_recognition as sr  # For voice recognition
import re             # For parsing function calls

# ===== LED AND FAN ASSISTANT CLASS =====
class LEDFanAssistant:
    """
    Main assistant class that handles communication with Arduino and voice recognition.
    This class provides methods to control the RGB LED and fan, and to listen for voice commands.
    """
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0"):
        """
        Initialize the RGB LED and Fan Assistant with microphone and Arduino connection.
        
        Args:
            port (str): Serial port for Arduino connection (default: '/dev/ttyACM0')
            baud_rate (int): Baud rate for serial communication (default: 9600)
            model_name (str): Name of the Ollama model to use (default: "llama3.1:8b-instruct-q4_0")
        """
        # Store model name for later use
        self.model_name = model_name
        
        # Initialize device states (tracked locally)
        self.device_states = {
            'red': False,
            'green': False,
            'blue': False,
            'fan': False,
            'temperature': 0.0
        }
        
        # ===== MICROPHONE SETUP =====
        # List available microphones for debugging
        #print("\nAvailable Microphones:")
        #for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #    print(f"Microphone {index}: {name}")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        try:
            # Try to use a specific microphone (adjust device_index as needed)
            self.microphone = sr.Microphone(device_index=9)
            #print("\nTesting microphone...")
            
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
            print("\nHi! I'm your RGB LED and Fan assistant! I can help you control the RGB LED and fan.")
            print("You can type or speak your commands!")
            
            # Test Arduino connection with a simple command
            print("\nTesting Arduino connection...")
            self.arduino.write(b'S')
            self.arduino.flush()
            time.sleep(1)
            if self.arduino.in_waiting:
                response = self.arduino.readline().decode('utf-8').strip()
                print(f"Arduino response: {response}")
                print("Arduino connection test successful!")
            else:
                print("WARNING: No response from Arduino. Communication may be one-way.")
        except Exception as e:
            # Handle Arduino connection errors
            print("\nOops! I couldn't connect to the Arduino.")
            print(f"Error: {e}")
            self.arduino = None

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
                    print("Sorry, I couldn't understand that.")
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None

    # ===== DEVICE CONTROL FUNCTIONS =====
    # These functions send commands to the Arduino and update the local state tracking
    
    def _control_red_on(self):
        """
        Turn Red LED on by sending 'R' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'R' command to Arduino")
                self.arduino.write(b'R')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['red'] = True
                return True
            except Exception as e:
                print("Error turning Red LED on:", e)
                return False

    def _control_red_off(self):
        """
        Turn Red LED off by sending 'r' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'r' command to Arduino")
                self.arduino.write(b'r')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['red'] = False
                return True
            except Exception as e:
                print("Error turning Red LED off:", e)
                return False

    def _control_green_on(self):
        """
        Turn Green LED on by sending 'G' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'G' command to Arduino")
                self.arduino.write(b'G')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['green'] = True
                return True
            except Exception as e:
                print("Error turning Green LED on:", e)
                return False

    def _control_green_off(self):
        """
        Turn Green LED off by sending 'g' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'g' command to Arduino")
                self.arduino.write(b'g')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['green'] = False
                return True
            except Exception as e:
                print("Error turning Green LED off:", e)
                return False

    def _control_blue_on(self):
        """
        Turn Blue LED on by sending 'B' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'B' command to Arduino")
                self.arduino.write(b'B')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['blue'] = True
                return True
            except Exception as e:
                print("Error turning Blue LED on:", e)
                return False

    def _control_blue_off(self):
        """
        Turn Blue LED off by sending 'b' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'b' command to Arduino")
                self.arduino.write(b'b')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['blue'] = False
                return True
            except Exception as e:
                print("Error turning Blue LED off:", e)
                return False

    def _control_all_rgb_on(self):
        """
        Turn all RGB LEDs on (White) by sending 'W' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'W' command to Arduino")
                self.arduino.write(b'W')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['red'] = True
                self.device_states['green'] = True
                self.device_states['blue'] = True
                return True
            except Exception as e:
                print("Error turning all RGB LEDs on:", e)
                return False

    def _control_all_rgb_off(self):
        """
        Turn all RGB LEDs off by sending 'w' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'w' command to Arduino")
                self.arduino.write(b'w')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['red'] = False
                self.device_states['green'] = False
                self.device_states['blue'] = False
                return True
            except Exception as e:
                print("Error turning all RGB LEDs off:", e)
                return False

    def _control_fan_on(self):
        """
        Turn fan on by sending 'F' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'F' command to Arduino")
                self.arduino.write(b'F')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['fan'] = True
                return True
            except Exception as e:
                print("Error turning fan on:", e)
                return False

    def _control_fan_off(self):
        """
        Turn fan off by sending 'f' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                print("DEBUG: Sending 'f' command to Arduino")
                self.arduino.write(b'f')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                self.device_states['fan'] = False
                return True
            except Exception as e:
                print("Error turning fan off:", e)
                return False

    def _toggle_red(self):
        """
        Toggle Red LED state (on if off, off if on).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.device_states['red']:
            return self._control_red_off()
        else:
            return self._control_red_on()

    def _toggle_green(self):
        """
        Toggle Green LED state (on if off, off if on).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.device_states['green']:
            return self._control_green_off()
        else:
            return self._control_green_on()

    def _toggle_blue(self):
        """
        Toggle Blue LED state (on if off, off if on).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.device_states['blue']:
            return self._control_blue_off()
        else:
            return self._control_blue_on()

    def _toggle_fan(self):
        """
        Toggle fan state (on if off, off if on).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.device_states['fan']:
            return self._control_fan_off()
        else:
            return self._control_fan_on()

    def _check_status(self):
        """
        Request and display the current status of devices by sending 'S' command to Arduino.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.arduino:
            try:
                # Clear any existing data in the buffer
                while self.arduino.in_waiting:
                    self.arduino.read()
                
                # Send status request command
                print("DEBUG: Sending 'S' command to Arduino")
                self.arduino.write(b'S')
                self.arduino.flush()  # Ensure data is sent
                print("DEBUG: Command sent successfully")
                
                # Wait for response
                time.sleep(0.5)
                
                # Read and print the status report
                print("\nReading status from Arduino...")
                while self.arduino.in_waiting:
                    line = self.arduino.readline().decode('utf-8').strip()
                    if line:
                        print(line)
                        
                        # Update temperature if available
                        if "Temperature:" in line:
                            try:
                                temp_str = line.split("Temperature:")[1].strip().split("°C")[0].strip()
                                self.device_states['temperature'] = float(temp_str)
                            except:
                                pass
                
                return True
            except Exception as e:
                print("Error checking status:", e)
                return False
        else:
            print("Arduino not connected. Cannot check status.")
            return False

    def _wait(self, seconds):
        """
        Wait for the specified number of seconds.
        
        Args:
            seconds (float): Number of seconds to wait
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            time.sleep(seconds)
            return True
        except Exception as e:
            print("Error during wait:", e)
            return False

    def close(self):
        """
        Close the Arduino connection and clean up resources.
        """
        if self.arduino:
            self.arduino.close()
            print("Goodbye! Thanks for using the RGB LED and Fan assistant!")

# ===== AGENT FRAMEWORK COMPONENTS =====
# These functions handle the natural language processing and command execution

def generate_prompt(user_input):
    """
    Generate a prompt that explains available tools and includes the user's input.
    
    Args:
        user_input (str): The user's natural language command
        
    Returns:
        str: A formatted prompt for the language model
    """
    # Define the available tools and their descriptions
    tool_descriptions = """
Available commands:
  - control_red_on(): Turn Red LED on.
  - control_red_off(): Turn Red LED off.
  - control_green_on(): Turn Green LED on.
  - control_green_off(): Turn Green LED off.
  - control_blue_on(): Turn Blue LED on.
  - control_blue_off(): Turn Blue LED off.
  - control_all_rgb_on(): Turn all RGB LEDs on (White).
  - control_all_rgb_off(): Turn all RGB LEDs off.
  - control_fan_on(): Turn fan on.
  - control_fan_off(): Turn fan off.
  - toggle_red(): Toggle Red LED state (on if off, off if on).
  - toggle_green(): Toggle Green LED state (on if off, off if on).
  - toggle_blue(): Toggle Blue LED state (on if off, off if on).
  - toggle_fan(): Toggle fan state (on if off, off if on).
  - check_status(): Request and display the current status of devices.
  - wait(seconds): Wait for a specified number of seconds.
    """
    
    # Format the prompt with the tool descriptions and user input
    prompt = f"""
You are an agent controlling an RGB LED and a fan with the following tools:
{tool_descriptions}

Given the user's request:
{user_input}

Provide a sequence of function calls to perform the task.
Ensure you include the exact function calls with parameters if needed.
    """
    return prompt

def query_local_model(prompt, model_name):
    """
    Query the local Ollama model with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the model
        model_name (str): The name of the Ollama model to use
        
    Returns:
        str: The model's response
    """
    # Run the Ollama model as a subprocess
    process = subprocess.Popen(
        ["ollama", "run", model_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    response, _ = process.communicate(input=prompt)
    return response.strip()

def parse_function_calls(response):
    """
    Parse function calls from the model's response.
    Expected format: functionName(arg1, arg2, ...)
    
    Args:
        response (str): The model's response text
        
    Returns:
        list: List of tuples containing (function_name, args_list)
    """
    # Use regex to find function calls in the response
    pattern = r"(\w+)\((.*?)\)"
    matches = re.findall(pattern, response)
    calls = []
    
    # Process each match to extract function name and arguments
    for func_name, arg_str in matches:
        # Split arguments by comma if present and strip whitespace
        args = [arg.strip() for arg in arg_str.split(',')] if arg_str.strip() else []
        calls.append((func_name, args))
    return calls

# ===== LED AND FAN AGENT CLASS =====
class LEDFanAgent:
    """
    Agent class that uses a language model to interpret user commands and execute the appropriate actions.
    """
    
    def __init__(self, assistant: LEDFanAssistant):
        """
        Initialize the agent with an LEDFanAssistant instance.
        
        Args:
            assistant (LEDFanAssistant): The assistant instance to use for device control
        """
        self.assistant = assistant
        self.model_name = assistant.model_name
        
        # Map tool names to LEDFanAssistant methods
        self.tools = {
            "control_red_on": assistant._control_red_on,
            "control_red_off": assistant._control_red_off,
            "control_green_on": assistant._control_green_on,
            "control_green_off": assistant._control_green_off,
            "control_blue_on": assistant._control_blue_on,
            "control_blue_off": assistant._control_blue_off,
            "control_all_rgb_on": assistant._control_all_rgb_on,
            "control_all_rgb_off": assistant._control_all_rgb_off,
            "control_fan_on": assistant._control_fan_on,
            "control_fan_off": assistant._control_fan_off,
            "toggle_red": assistant._toggle_red,
            "toggle_green": assistant._toggle_green,
            "toggle_blue": assistant._toggle_blue,
            "toggle_fan": assistant._toggle_fan,
            "check_status": assistant._check_status,
            "wait": assistant._wait,
        }
    
    def run(self, user_input):
        """
        Generate a plan using the local model and execute the corresponding tools.
        
        Args:
            user_input (str): The user's natural language command
            
        Returns:
            str: The model's response
        """
        # Generate a prompt for the language model
        prompt = generate_prompt(user_input)
        print("Agent prompt:", prompt)
        
        # Query the language model
        response = query_local_model(prompt, self.model_name)
        print("Model response:", response)
        
        # Parse the function calls from the response
        function_calls = parse_function_calls(response)
        print("Parsed function calls:", function_calls)
        
        # Execute each parsed function call in sequence
        for func_name, args in function_calls:
            if func_name in self.tools:
                try:
                    # Handle special case for wait function with arguments
                    if func_name == "wait" and args:
                        seconds = float(args[0])
                        print(f"Executing: wait({seconds})")
                        self.tools[func_name](seconds)
                    else:
                        # Execute the function without arguments
                        print(f"Executing: {func_name}()")
                        self.tools[func_name]()
                except Exception as e:
                    print(f"Error executing {func_name}: {e}")
            else:
                print(f"Tool '{func_name}' not found!")
        return response

# ===== MAIN PROGRAM =====
if __name__ == "__main__":
    # Create the assistant and agent instances
    assistant = LEDFanAssistant()
    agent = LEDFanAgent(assistant)
    
    # Main interaction loop
    print("\nAgent ready! Type your command (or 'voice' for voice command, 'bye' to exit):")
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Handle special commands
        if user_input.lower() in ['bye', 'exit']:
            break
        elif user_input.lower() == 'voice':
            # Get voice input
            voice_input = assistant.listen()
            if voice_input:
                # Process voice input
                agent.run(voice_input)
        else:
            # Process text input
            agent.run(user_input)
    
    # Clean up resources
    assistant.close() 