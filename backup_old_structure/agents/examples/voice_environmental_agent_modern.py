#!/usr/bin/env python3
"""
Voice-Enabled Environmental Monitoring Agent (Modern)
==================================================

Modern version using lightweight trained voice models for excellent quality.
"""

import time
import sys
import os

# Add the parent directory to the path so we can import from agents/core and agents/interfaces
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'interfaces'))

from typing import Dict, Any
from environmental_agent import EnvironmentalAgent
from modern_voice_interface import ModernVoiceInterface
from llm_interface import LLMInterface

class ModernVoiceEnvironmentalAgent:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0", voice_model="gtts"):
        """Initialize the modern voice-enabled environmental monitoring agent."""
        # Initialize core components
        self.agent = EnvironmentalAgent(port, baud_rate)
        self.voice = ModernVoiceInterface(voice_model=voice_model)
        self.llm = LLMInterface(model_name)
        
        if not self.agent.connected:
            print("❌ Cannot initialize without Arduino connection")
            return
        
        print(" Modern Voice-Enabled Environmental Agent Ready!")
        print(f" Using {self.voice.voice_type} voice model for excellent quality!")
        print("I can analyze sensor data and respond with professional voice feedback.")
        self.voice.speak("Modern voice-enabled environmental monitoring system ready!")
    
    def generate_environmental_prompt(self, user_input: str) -> str:
        """Generate a prompt for the LLM based on environmental data and user input."""
        # Get current environmental status
        status = self.agent.get_status()
        
        if "error" in status:
            return f"""You are an environmental monitoring assistant. The sensors are not responding.

User request: "{user_input}"

Please respond with a JSON object containing:
1. "response": A helpful response to the user
2. "explanation": Brief explanation of the issue

Example response:
{{
    "response": "I'm sorry, but I cannot access the environmental sensors right now. Please check the Arduino connection.",
    "explanation": "Sensors not responding"
}}"""

        # Create environmental context
        temp = status.get('temperature', 'N/A')
        co2 = status.get('co2', 'N/A')
        light_raw = status.get('light', 'N/A')
        brightness = status.get('brightness', 'Unknown')
        light_percent = status.get('light_percentage', 'N/A')
        led = status.get('led', 'N/A')
        
        # Format light information
        if brightness != 'Unknown' and light_percent != 'N/A':
            light_info = f"{light_raw} ({brightness}, {light_percent}% brightness)"
        else:
            light_info = f"{light_raw} (raw value)"
        
        environmental_context = f"""
Current Environmental Data:
- Temperature: {temp}°F
- CO2 Level: {co2} (raw value)
- Light Level: {light_info}
- LED Status: {led}

Available Actions:
- Turn LED ON (L1)
- Turn LED OFF (L0)
- Get sensor readings
- Analyze environmental conditions
- Provide recommendations

User request: "{user_input}"

Please respond with a JSON object containing:
1. "action": The action to perform (e.g., "turn_led_on", "turn_led_off", "analyze", "status")
2. "response": A natural language response to speak to the user
3. "explanation": Brief explanation of what you're doing
4. "analysis": Optional environmental analysis

Example response:
{{
    "action": "analyze",
    "response": "The current temperature is {temp} degrees Fahrenheit. The environment appears comfortable.",
    "explanation": "Analyzing environmental conditions",
    "analysis": "Temperature is in comfortable range"
}}

Respond only with the JSON object:"""

        return environmental_context
    
    def process_voice_command(self, user_input: str):
        """Process a voice command using LLM intelligence and modern TTS feedback."""
        print(f"\n Processing: {user_input}")
        
        # Generate LLM prompt
        prompt = self.generate_environmental_prompt(user_input)
        
        # Query the LLM
        llm_response = self.llm.query_llm(prompt)
        
        if llm_response:
            # Extract action and response
            action = llm_response.get('action', 'analyze')
            response_text = llm_response.get('response', 'Processing your request.')
            explanation = llm_response.get('explanation', '')
            analysis = llm_response.get('analysis', '')
            
            print(f" LLM Action: {action}")
            print(f" Explanation: {explanation}")
            
            # Speak the response with modern voice
            self.voice.speak(response_text)
            
            # Execute the action
            success = self.execute_action(action)
            
            if not success:
                self.voice.speak("Sorry, there was an error executing that command.")
        else:
            self.voice.speak("Sorry, I couldn't process your request. Please try again.")
    
    def execute_action(self, action: str) -> bool:
        """Execute the specified action."""
        try:
            if action == "turn_led_on":
                success = self.agent.turn_led_on()
                if success:
                    self.voice.speak("LED turned on successfully.")
                return success
                
            elif action == "turn_led_off":
                success = self.agent.turn_led_off()
                if success:
                    self.voice.speak("LED turned off successfully.")
                return success
                
            elif action == "status":
                status = self.agent.get_status()
                if "error" not in status:
                    temp = status.get('temperature', 'N/A')
                    co2 = status.get('co2', 'N/A')
                    light_raw = status.get('light', 'N/A')
                    brightness = status.get('brightness', 'Unknown')
                    light_percent = status.get('light_percentage', 'N/A')
                    led = status.get('led', 'N/A')
                    
                    # Format light information
                    if brightness != 'Unknown' and light_percent != 'N/A':
                        light_info = f"{light_raw} ({brightness}, {light_percent}% brightness)"
                    else:
                        light_info = f"{light_raw}"
                    
                    status_message = f"Current status: Temperature is {temp} degrees Fahrenheit, CO2 level is {co2}, light level is {light_info}, and the LED is {led}."
                    self.voice.speak(status_message)
                    return True
                else:
                    self.voice.speak("Sorry, I cannot get the status right now.")
                    return False
                    
            elif action == "analyze":
                # Get environmental analysis
                status = self.agent.get_status()
                if "error" not in status:
                    temp = status.get('temperature', 0)
                    co2 = status.get('co2', 0)
                    light_raw = status.get('light', 0)
                    brightness = status.get('brightness', 'Unknown')
                    light_percent = status.get('light_percentage', 0)
                    
                    analysis_message = f"Environmental analysis: Temperature is {temp} degrees Fahrenheit. "
                    
                    if temp < 60:
                        analysis_message += "It's quite cold. "
                    elif temp > 86:
                        analysis_message += "It's quite warm. "
                    else:
                        analysis_message += "The temperature is comfortable. "
                    
                    if co2 > 1000:
                        analysis_message += "CO2 levels are high, indicating poor ventilation. "
                    elif co2 > 800:
                        analysis_message += "CO2 levels are moderate. "
                    else:
                        analysis_message += "Air quality appears good. "
                    
                    # Use brightness description for better analysis
                    if brightness != 'Unknown':
                        if brightness in ['Very Dark', 'Dark']:
                            analysis_message += f"The lighting is {brightness.lower()}, you might need more light. "
                        elif brightness in ['Very Bright']:
                            analysis_message += f"The lighting is {brightness.lower()}, it might be too bright. "
                        else:
                            analysis_message += f"The lighting is {brightness.lower()}, which is adequate. "
                    else:
                        # Fallback to raw value analysis
                        if light_raw < 100:
                            analysis_message += "The lighting is quite dim. "
                        elif light_raw > 800:
                            analysis_message += "The lighting is very bright. "
                        else:
                            analysis_message += "The lighting is adequate. "
                    
                    self.voice.speak(analysis_message)
                    return True
                else:
                    self.voice.speak("Sorry, I cannot analyze the environment right now.")
                    return False
                    
            else:
                print(f"❌ Unknown action: {action}")
                return False
                
        except Exception as e:
            print(f"❌ Error executing action {action}: {e}")
            return False
    
    def run_voice_monitoring(self):
        """Run continuous voice monitoring with user interaction."""
        print("🎤 Starting modern voice-enabled environmental monitoring...")
        self.voice.speak("Modern voice monitoring started. You can ask me about the environment or control the LED.")
        
        try:
            while True:
                print("\n" + "="*60)
                print("🎤 MODERN VOICE-ENABLED ENVIRONMENTAL MONITORING")
                print("="*60)
                print("Try these voice commands:")
                print("- 'What's the temperature?'")
                print("- 'Turn on the LED'")
                print("- 'Turn off the LED'")
                print("- 'What's the environmental status?'")
                print("- 'Analyze the environment'")
                print("- 'How's the air quality?'")
                print("="*60)
                
                # Get user input method
                choice = input("\nChoose input method:\n1. Voice command\n2. Text command\n3. Continuous monitoring\n4. Intelligent decision system (analyze & recommend)\n5. Exit\nEnter choice (1-5): ").strip()
                
                if choice == '1':
                    # Voice input
                    user_input = self.voice.listen()
                    if user_input:
                        self.process_voice_command(user_input)
                        
                elif choice == '2':
                    # Text input
                    user_input = input("\nEnter your command: ").strip()
                    if user_input.lower() in ['quit', 'exit']:
                        break
                    if user_input:
                        self.process_voice_command(user_input)
                        
                elif choice == '3':
                    # Continuous monitoring
                    interval = input("⏱️  Enter monitoring interval in seconds (default 30): ").strip()
                    try:
                        interval = int(interval) if interval else 30
                        self.run_continuous_voice_monitoring(interval)
                    except ValueError:
                        print("❌ Invalid interval. Using default 30 seconds.")
                        self.run_continuous_voice_monitoring(30)
                        
                elif choice == '4':
                    # Intelligent decision system
                    self.run_intelligent_decision_system()
                    
                elif choice == '5':
                    break
                    
                else:
                    print("❌ Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n🛑 Voice monitoring stopped by user")
        finally:
            self.voice.speak("Voice monitoring stopped. Goodbye!")
    
    def run_continuous_voice_monitoring(self, interval=30):
        """Run continuous monitoring with modern voice announcements."""
        print(f"🔄 Starting continuous modern voice monitoring (every {interval} seconds)")
        self.voice.speak(f"Starting continuous monitoring every {interval} seconds.")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print("\n" + "="*50)
                print(f" Environmental Check - {time.strftime('%H:%M:%S')}")
                
                # Get environmental status
                status = self.agent.get_status()
                
                if "error" not in status:
                    temp = status.get('temperature', 0)
                    co2 = status.get('co2', 0)
                    light_raw = status.get('light', 0)
                    brightness = status.get('brightness', 'Unknown')
                    light_percent = status.get('light_percentage', 0)
                    led = status.get('led', 'OFF')
                    
                    print(f"  Temperature: {temp}°F")
                    print(f" CO2: {co2}")
                    print(f" Light: {light_raw}")
                    print(f" LED: {led}")
                    
                    # Voice announcement for significant changes
                    if temp < 60:
                        self.voice.speak(f"Warning: Temperature is {temp} degrees, which is quite cold.")
                    elif temp > 86:
                        self.voice.speak(f"Warning: Temperature is {temp} degrees, which is quite warm.")
                    
                    if co2 > 1000:
                        self.voice.speak("Warning: CO2 levels are high, indicating poor ventilation.")
                    
                    # Use brightness description for voice announcements
                    if brightness != 'Unknown':
                        if brightness in ['Very Dark', 'Dark']:
                            self.voice.speak(f"Notice: Lighting is {brightness.lower()}, you might need more light.")
                        elif brightness in ['Very Bright']:
                            self.voice.speak(f"Notice: Lighting is {brightness.lower()}, it might be too bright.")
                    else:
                        if light_raw < 100:
                            self.voice.speak("Notice: Lighting is quite dim.")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Continuous monitoring stopped by user")
            self.voice.speak("Continuous monitoring stopped.")
    
    def run_intelligent_decision_system(self):
        """Run the intelligent decision system for continuous monitoring and recommendations."""
        print("\n🧠 Intelligent Decision System (Press Ctrl+C to exit)")
        print("--------------------------------------------------")
        while True:
            try:
                print("\n" + "="*50)
                print(f" Environmental Check - {time.strftime('%H:%M:%S')}")
                
                # Get environmental status
                status = self.agent.get_status()
                
                if "error" not in status:
                    temp = status.get('temperature', 0)
                    co2 = status.get('co2', 0)
                    light_raw = status.get('light', 0)
                    brightness = status.get('brightness', 'Unknown')
                    light_percent = status.get('light_percentage', 0)
                    led = status.get('led', 'OFF')
                    
                    print(f"  Temperature: {temp}°F")
                    print(f" CO2: {co2}")
                    print(f" Light: {light_raw}")
                    print(f" LED: {led}")
                    
                    # Voice announcement for significant changes
                    if temp < 60:
                        self.voice.speak(f"Warning: Temperature is {temp} degrees, which is quite cold.")
                    elif temp > 86:
                        self.voice.speak(f"Warning: Temperature is {temp} degrees, which is quite warm.")
                    
                    if co2 > 1000:
                        self.voice.speak("Warning: CO2 levels are high, indicating poor ventilation.")
                    
                    # Use brightness description for voice announcements
                    if brightness != 'Unknown':
                        if brightness in ['Very Dark', 'Dark']:
                            self.voice.speak(f"Notice: Lighting is {brightness.lower()}, you might need more light.")
                        elif brightness in ['Very Bright']:
                            self.voice.speak(f"Notice: Lighting is {brightness.lower()}, it might be too bright.")
                    else:
                        if light_raw < 100:
                            self.voice.speak("Notice: Lighting is quite dim.")
                    
                    # Analyze and provide recommendations
                    analysis_message = ""
                    actions_taken = []
                    
                    if temp < 60:
                        analysis_message += "It's quite cold. You might want to increase the temperature. "
                    elif temp > 86:
                        analysis_message += "It's quite warm. You might want to decrease the temperature. "
                    else:
                        analysis_message += "The temperature is comfortable. "
                    
                    if co2 > 1000:
                        analysis_message += "CO2 levels are high, indicating poor ventilation. You might need to open windows or use a fan. "
                    elif co2 > 800:
                        analysis_message += "CO2 levels are moderate. Air quality is good. "
                    else:
                        analysis_message += "Air quality appears good. "
                    
                    # Automatic LED control based on lighting conditions
                    if brightness != 'Unknown':
                        if brightness in ['Very Dark', 'Dark']:
                            analysis_message += f"The lighting is {brightness.lower()}, you might need more light. "
                            # Auto-turn on LED for poor lighting
                            if led == 'OFF':
                                self.agent.turn_led_on()
                                actions_taken.append("LED turned ON automatically for poor lighting")
                                analysis_message += "I've turned on the LED to help with the lighting. "
                        elif brightness in ['Very Bright']:
                            analysis_message += f"The lighting is {brightness.lower()}, it might be too bright. "
                            # Auto-turn off LED if too bright
                            if led == 'ON':
                                self.agent.turn_led_off()
                                actions_taken.append("LED turned OFF automatically - lighting is adequate")
                                analysis_message += "I've turned off the LED since the lighting is already bright. "
                        else:
                            analysis_message += f"The lighting is {brightness.lower()}, which is adequate. "
                            # Turn off LED if lighting is adequate
                            if led == 'ON':
                                self.agent.turn_led_off()
                                actions_taken.append("LED turned OFF automatically - lighting is adequate")
                                analysis_message += "I've turned off the LED since the lighting is adequate. "
                    else:
                        # Fallback to raw value analysis
                        if light_raw < 100:
                            analysis_message += "The lighting is quite dim. "
                            if led == 'OFF':
                                self.agent.turn_led_on()
                                actions_taken.append("LED turned ON automatically for poor lighting")
                                analysis_message += "I've turned on the LED to help with the lighting. "
                        elif light_raw > 800:
                            analysis_message += "The lighting is very bright. "
                            if led == 'ON':
                                self.agent.turn_led_off()
                                actions_taken.append("LED turned OFF automatically - lighting is adequate")
                                analysis_message += "I've turned off the LED since the lighting is already bright. "
                        else:
                            analysis_message += "The lighting is adequate. "
                            if led == 'ON':
                                self.agent.turn_led_off()
                                actions_taken.append("LED turned OFF automatically - lighting is adequate")
                                analysis_message += "I've turned off the LED since the lighting is adequate. "
                    
                    # Show actions taken in console
                    if actions_taken:
                        print(f"🤖 Actions taken: {', '.join(actions_taken)}")
                    
                    self.voice.speak(analysis_message)
                    
                else:
                    self.voice.speak("Error getting status from Arduino.")
                    
                time.sleep(1) # Check every second
                
            except KeyboardInterrupt:
                print("\n🛑 Intelligent decision system stopped by user")
                self.voice.speak("Intelligent decision system stopped.")
                break
    
    def close(self):
        """Close the agent and clean up resources."""
        if self.agent:
            self.agent.close()
        if self.voice:
            self.voice.close()
        print("🔌 Modern voice environmental agent closed.")

def main():
    """Main function to run the modern voice-enabled environmental agent."""
    print("🎤 Starting Modern Voice-Enabled Environmental Monitoring Agent...")
    
    # Create the modern voice agent
    agent = ModernVoiceEnvironmentalAgent()
    
    if not agent.agent.connected:
        print("❌ Cannot run without Arduino connection.")
        return
    
    try:
        agent.run_voice_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        agent.close()

if __name__ == "__main__":
    main() 