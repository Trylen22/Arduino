import serial
import time
import subprocess
import threading
import speech_recognition as sr
import re

class LEDAssistant:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0"):
        """Initialize the LED Assistant with microphone and Arduino connection."""
        self.model_name = model_name
        self.led_states = {
            'green': False,
            'red': False
        }
        
        # List available microphones
        print("\nAvailable Microphones:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone {index}: {name}")
        
        # Initialize speech recognizer and choose the HyperX SoloCast microphone (adjust device_index if needed)
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone(device_index=9)  # Change device_index as needed
            print("\nTesting microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 1000  # Adjust as necessary
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.pause_threshold = 0.8
            print("Microphone test successful!")
        except Exception as e:
            print(f"\nError initializing microphone: {e}")
            print("Voice control will not be available.")
            self.microphone = None

        # Connect to Arduino
        try:
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Allow time for Arduino to reset
            print("\nHi! I'm your LED assistant! I can help you control the red and green lights.")
            print("You can type or speak your commands!")
        except Exception as e:
            print("\nOops! I couldn't connect to the Arduino.")
            print(f"Error: {e}")
            self.arduino = None

    def listen(self):
        """Listen for a voice command."""
        if not self.microphone:
            print("Voice control not available.")
            return None

        try:
            with self.microphone as source:
                print("\nListening... (speak now)")
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=6)
                print("Processing your command...")
                try:
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

    # LED control functions (tools)
    def _control_green_on(self):
        """Turn green LED on."""
        if self.arduino:
            try:
                self.arduino.write(b'G')
                self.led_states['green'] = True
                return True
            except Exception as e:
                print("Error turning green LED on:", e)
                return False

    def _control_green_off(self):
        """Turn green LED off."""
        if self.arduino:
            try:
                self.arduino.write(b'g')
                self.led_states['green'] = False
                return True
            except Exception as e:
                print("Error turning green LED off:", e)
                return False

    def _control_red_on(self):
        """Turn red LED on."""
        if self.arduino:
            try:
                self.arduino.write(b'R')
                self.led_states['red'] = True
                return True
            except Exception as e:
                print("Error turning red LED on:", e)
                return False

    def _control_red_off(self):
        """Turn red LED off."""
        if self.arduino:
            try:
                self.arduino.write(b'r')
                self.led_states['red'] = False
                return True
            except Exception as e:
                print("Error turning red LED off:", e)
                return False

    def _control_both_on(self):
        """Turn both LEDs on."""
        if self.arduino:
            try:
                self.arduino.write(b'B')
                self.led_states['green'] = True
                self.led_states['red'] = True
                return True
            except Exception as e:
                print("Error turning both LEDs on:", e)
                return False

    def _control_both_off(self):
        """Turn both LEDs off."""
        if self.arduino:
            try:
                self.arduino.write(b'b')
                self.led_states['green'] = False
                self.led_states['red'] = False
                return True
            except Exception as e:
                print("Error turning both LEDs off:", e)
                return False

    def _wait(self, seconds):
        """Wait for the specified number of seconds."""
        try:
            time.sleep(seconds)
            return True
        except Exception as e:
            print("Error during wait:", e)
            return False

    def close(self):
        """Close the Arduino connection."""
        if self.arduino:
            self.arduino.close()
            print("Goodbye! Thanks for using the LED assistant!")

# --- Agent Framework Components ---

def generate_prompt(user_input):
    """Generate a prompt that explains available tools and includes the user's input."""
    tool_descriptions = """
Available commands:
  - control_green_on(): Turn green LED on.
  - control_green_off(): Turn green LED off.
  - control_red_on(): Turn red LED on.
  - control_red_off(): Turn red LED off.
  - control_both_on(): Turn both LEDs on.
  - control_both_off(): Turn both LEDs off.
  - wait(seconds): Wait for a specified number of seconds.
    """
    prompt = f"""
You are an agent controlling LEDs with the following tools:
{tool_descriptions}

Given the user's request:
{user_input}

Provide a sequence of function calls to perform the task.
Ensure you include the exact function calls with parameters if needed.
    """
    return prompt

def query_local_model(prompt, model_name):
    """Query the local Ollama model with the given prompt."""
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
    """
    pattern = r"(\w+)\((.*?)\)"
    matches = re.findall(pattern, response)
    calls = []
    for func_name, arg_str in matches:
        # Split arguments by comma if present and strip whitespace.
        args = [arg.strip() for arg in arg_str.split(',')] if arg_str.strip() else []
        calls.append((func_name, args))
    return calls

class LEDAgent:
    def __init__(self, assistant: LEDAssistant):
        self.assistant = assistant
        self.model_name = assistant.model_name
        # Map tool names to LEDAssistant methods
        self.tools = {
            "control_green_on": assistant._control_green_on,
            "control_green_off": assistant._control_green_off,
            "control_red_on": assistant._control_red_on,
            "control_red_off": assistant._control_red_off,
            "control_both_on": assistant._control_both_on,
            "control_both_off": assistant._control_both_off,
            "wait": assistant._wait,
        }
    
    def run(self, user_input):
        """Generate a plan using the local model and execute the corresponding tools."""
        prompt = generate_prompt(user_input)
        print("Agent prompt:", prompt)
        
        response = query_local_model(prompt, self.model_name)
        print("Model response:", response)
        
        function_calls = parse_function_calls(response)
        print("Parsed function calls:", function_calls)
        
        # Execute each parsed function call in sequence
        for func_name, args in function_calls:
            if func_name in self.tools:
                try:
                    if func_name == "wait" and args:
                        seconds = float(args[0])
                        print(f"Executing: wait({seconds})")
                        self.tools[func_name](seconds)
                    else:
                        print(f"Executing: {func_name}()")
                        self.tools[func_name]()
                except Exception as e:
                    print(f"Error executing {func_name}: {e}")
            else:
                print(f"Tool '{func_name}' not found!")
        return response

# --- Main Loop ---

if __name__ == "__main__":
    assistant = LEDAssistant()
    agent = LEDAgent(assistant)
    
    print("\nAgent ready! Type your command (or 'voice' for voice command, 'bye' to exit):")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['bye', 'exit']:
            break
        elif user_input.lower() == 'voice':
            voice_input = assistant.listen()
            if voice_input:
                agent.run(voice_input)
        else:
            agent.run(user_input)
    
    assistant.close()
