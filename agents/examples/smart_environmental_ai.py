#!/usr/bin/env python3
"""
IRIS Smart Environmental AI - Main System
========================================

Clean, focused main system for intelligent environmental monitoring.
Uses extracted components for maintainable, modular code.
"""

import time
import sys
import os
from typing import Dict, Any, Callable

# Handle imports for both direct execution and package import
try:
    # Try relative imports first (when run as package)
    from ..core import EnvironmentalAgent, SmartMonitor, MessageGenerators
    from ..interfaces import ModernVoiceInterface, LLMInterface
except ImportError:
    # Fallback to absolute imports (when run directly)
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'interfaces'))
    from environmental_agent import EnvironmentalAgent
    from smart_monitor import SmartMonitor
    from message_generators import MessageGenerators
    from modern_voice_interface import ModernVoiceInterface
    from llm_interface import LLMInterface


class IRISEnvironmentalAI:
    """Main IRIS Environmental AI system with clean architecture."""
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, 
                 model_name="llama3.1:8b-instruct-q4_0", voice_model="gtts"):
        """Initialize the IRIS Environmental AI system."""
        # Initialize core components
        self.agent = EnvironmentalAgent(port, baud_rate)
        self.voice = ModernVoiceInterface(voice_model=voice_model)
        self.llm = LLMInterface(model_name)
        self.smart_monitor = SmartMonitor()
        self.messages = MessageGenerators()
        
        if not self.agent.connected:
            print("❌ Cannot initialize without Arduino connection")
            return
        
        # Initialize action handlers using dictionary dispatch
        self.action_handlers = {
            "turn_led_on": self._handle_turn_led_on,
            "turn_led_off": self._handle_turn_led_off,
            "turn_fan_on": self._handle_turn_fan_on,
            "turn_fan_off": self._handle_turn_fan_off,
            "status": self._handle_status,
            "analyze": self._handle_analyze,
            "get_temperature": self._handle_get_temperature,
            "get_co2": self._handle_get_co2,
            "get_light": self._handle_get_light,
            "recommend": self._handle_recommend,
            "emergency_check": self._handle_emergency_check
        }
        
        print("🔧 IRIS Environmental AI Ready!")
        print(f" Using {self.voice.voice_type} voice model for excellent quality!")
        self.voice.speak("IRIS Environmental AI is ready.")
    
    def _handle_turn_led_on(self) -> bool:
        """Handle turning LED on."""
        success = self.agent.turn_led_on()
        if success:
            self.voice.speak("I've turned the LED on.")
        return success
    
    def _handle_turn_led_off(self) -> bool:
        """Handle turning LED off."""
        success = self.agent.turn_led_off()
        if success:
            self.voice.speak("I've turned the LED off.")
        return success
    
    def _handle_turn_fan_on(self) -> bool:
        """Handle turning fan on."""
        success = self.agent.turn_fan_on()
        if success:
            self.voice.speak("I've turned the fan on.")
        return success
    
    def _handle_turn_fan_off(self) -> bool:
        """Handle turning fan off."""
        success = self.agent.turn_fan_off()
        if success:
            self.voice.speak("I've turned the fan off.")
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
        message = self.messages.get_analysis_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def _handle_get_temperature(self) -> bool:
        """Handle temperature-specific request."""
        status = self.agent.get_status()
        message = self.messages.get_temperature_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def _handle_get_co2(self) -> bool:
        """Handle CO2-specific request."""
        status = self.agent.get_status()
        message = self.messages.get_co2_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def _handle_get_light(self) -> bool:
        """Handle light-specific request."""
        status = self.agent.get_status()
        message = self.messages.get_light_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def _handle_recommend(self) -> bool:
        """Handle recommendation request."""
        status = self.agent.get_status()
        message = self.messages.get_recommendation_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def _handle_emergency_check(self) -> bool:
        """Handle emergency check request."""
        status = self.agent.get_status()
        message = self.messages.get_emergency_message(status)
        self.voice.speak(message)
        return "error" not in status
    
    def execute_action(self, action: str) -> bool:
        """Execute the specified action using dictionary dispatch."""
        try:
            handler = self.action_handlers.get(action)
            if handler:
                return handler()
            else:
                return self._handle_unknown_action(action)
        except Exception as e:
            print(f"❌ Error executing action {action}: {e}")
            return False
    
    def _handle_unknown_action(self, action: str) -> bool:
        """Handle unknown actions by asking the LLM for guidance."""
        print(f"🤖 Unknown action '{action}' - asking LLM for guidance...")
        
        guidance_prompt = f"""
You are an environmental monitoring assistant. The user requested action: "{action}"

Available actions are:
{list(self.action_handlers.keys())}

Please suggest the most appropriate action from the available list, or explain why this action cannot be performed.

Respond with JSON:
{{
    "suggested_action": "action_name",
    "explanation": "Why this action was chosen",
    "response": "Message to speak to user"
}}
"""
        
        guidance_response = self.llm.query_llm(guidance_prompt)
        if guidance_response:
            suggested_action = guidance_response.get('suggested_action')
            response_text = guidance_response.get('response', f"I can't perform '{action}' directly.")
            
            print(f" LLM Suggestion: {suggested_action}")
            self.voice.speak(response_text)
            
            if suggested_action and suggested_action in self.action_handlers:
                return self.action_handlers[suggested_action]()
            else:
                return False
        else:
            self.voice.speak(f"I don't understand '{action}'.")
            return False
    
    def process_voice_command(self, user_input: str):
        """Process a voice command using LLM intelligence."""
        print(f"\n Processing: {user_input}")
        
        # Generate LLM prompt with environmental context
        prompt = self._generate_environmental_prompt(user_input)
        
        # Query the LLM
        llm_response = self.llm.query_llm(prompt)
        
        if llm_response:
            action = llm_response.get('action', 'analyze')
            response_text = llm_response.get('response', 'Processing your request.')
            
            print(f" LLM Action: {action}")
            self.voice.speak(response_text)
            
            success = self.execute_action(action)
            if not success:
                self.voice.speak("I encountered an error executing that command.")
        else:
            self.voice.speak("I couldn't process your request. Please try again.")
    
    def _generate_environmental_prompt(self, user_input: str) -> str:
        """Generate a prompt for the LLM based on environmental data and user input."""
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
        fan = status.get('fan', 'N/A')
        
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
- Fan Status: {fan}

Available Actions:
- turn_led_on: Turn LED ON
- turn_led_off: Turn LED OFF
- turn_fan_on: Turn Fan ON
- turn_fan_off: Turn Fan OFF
- status: Get current sensor readings
- analyze: Comprehensive environmental analysis
- get_temperature: Get temperature-specific information
- get_co2: Get CO2-specific information
- get_light: Get light-specific information
- recommend: Provide recommendations based on conditions
- emergency_check: Check for critical conditions

User request: "{user_input}"

Please respond with a JSON object containing:
1. "action": The action to perform (choose from available actions above)
2. "response": A natural language response to speak to the user
3. "explanation": Brief explanation of what you're doing

Example response:
{{
    "action": "analyze",
    "response": "The current temperature is {temp} degrees Fahrenheit. The environment appears comfortable.",
    "explanation": "Analyzing environmental conditions"
}}

Respond only with the JSON object:"""

        return environmental_context
    
    def run_intelligent_monitoring(self):
        """Run intelligent monitoring with smart alerts."""
        print("\n🧠 IRIS Intelligent Monitoring (Press Ctrl+C to exit)")
        print("==================================================")
        
        self.voice.speak("Starting intelligent monitoring. I'll alert you to important changes.")
        self.smart_monitor.log_action("System Start", "Intelligent monitoring initialized")
        
        try:
            while True:
                # Get environmental status
                status = self.agent.get_status()
                
                if "error" not in status:
                    temp = status.get('temperature', 0)
                    co2 = status.get('co2', 0)
                    light_raw = status.get('light', 0)
                    brightness = status.get('brightness', 'Unknown')
                    led = status.get('led', 'OFF')
                    fan = status.get('fan', 'OFF') # Get fan status
                    
                    # Update smart monitor
                    current_values = {
                        'temperature': temp,
                        'co2': co2,
                        'light': light_raw,
                        'led': led,
                        'fan': fan  # Add fan status
                    }
                    self.smart_monitor.update_last_values(current_values)
                    
                    # Check for emergencies first
                    emergencies = self.smart_monitor.is_emergency(current_values)
                    if emergencies:
                        for emergency_type, message in emergencies.items():
                            self.voice.speak(message)
                            self.smart_monitor.log_action("EMERGENCY", f"{emergency_type}: {message}")
                    
                    # Determine if speech is needed
                    should_speak = self.smart_monitor.should_speak(current_values)
                    
                    if should_speak:
                        self.smart_monitor.update_speech_time()
                        
                        if emergencies:
                            # Emergency already handled above
                            pass
                        elif self.smart_monitor.has_significant_changes(current_values):
                            # Change detected
                            change_message = self.messages.get_change_alert(
                                current_values, 
                                self.smart_monitor.last_values, 
                                self.smart_monitor.change_thresholds
                            )
                            self.voice.speak(change_message)
                            self.smart_monitor.log_action("Change Alert", change_message)
                        else:
                            # Periodic summary
                            summary_message = self.messages.get_periodic_summary(current_values)
                            self.voice.speak(summary_message)
                            self.smart_monitor.update_summary_time()
                            self.smart_monitor.log_action("Periodic Summary", summary_message)
                    
                    # Show console display
                    print("\n" + "="*60)
                    print(self.smart_monitor.get_status_display(current_values))
                    print("\n📋 Recent Actions:")
                    print(self.smart_monitor.get_recent_actions())
                    print("="*60)
                    
                    # Automatic LED control based on lighting conditions
                    self._perform_automatic_led_control(brightness, light_raw, led)
                    
                    # Automatic fan control based on temperature
                    self._perform_automatic_fan_control(temp, fan)
                    
                else:
                    self.voice.speak("I can't access the sensors right now.")
                    self.smart_monitor.log_action("Error", "Arduino sensors not responding")
                    
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\n🛑 Intelligent monitoring stopped by user")
            self.voice.speak("I've stopped the intelligent system.")
    
    def _perform_automatic_led_control(self, brightness: str, light_raw: int, led: str):
        """Perform automatic LED control based on lighting conditions."""
        if brightness != 'Unknown':
            match brightness:
                case 'Very Dark' | 'Dark':
                    if led == 'OFF':
                        self.agent.turn_led_on()
                        self.voice.speak("I've turned on the LED to improve lighting.")
                        self.smart_monitor.log_action("Auto LED Control", "LED turned ON for poor lighting")
                case 'Very Bright':
                    if led == 'ON':
                        self.agent.turn_led_off()
                        self.voice.speak("I've turned off the LED - lighting is adequate.")
                        self.smart_monitor.log_action("Auto LED Control", "LED turned OFF - lighting adequate")
                case _:
                    if led == 'ON':
                        self.agent.turn_led_off()
                        self.smart_monitor.log_action("Auto LED Control", "LED turned OFF - lighting adequate")
        else:
            # Fallback to raw value analysis
            if light_raw < 200:  # Very low light
                if led == 'OFF':
                    self.agent.turn_led_on()
                    self.voice.speak("I've turned on the LED to improve lighting.")
                    self.smart_monitor.log_action("Auto LED Control", "LED turned ON for poor lighting")
            elif light_raw > 800:  # Very bright
                if led == 'ON':
                    self.agent.turn_led_off()
                    self.voice.speak("I've turned off the LED - lighting is adequate.")
                    self.smart_monitor.log_action("Auto LED Control", "LED turned OFF - lighting adequate")
            elif light_raw >= 200 and light_raw <= 800 and led == 'ON':
                self.agent.turn_led_off()
                self.smart_monitor.log_action("Auto LED Control", "LED turned OFF - lighting adequate")
    
    def _perform_automatic_fan_control(self, temp: float, fan: str):
        """Perform automatic fan control based on temperature."""
        if temp > 80:  # High temperature - turn fan on
            if fan == 'OFF':
                self.agent.turn_fan_on()
                self.voice.speak("I've turned on the fan to cool down the environment.")
                self.smart_monitor.log_action("Auto Fan Control", "Fan turned ON for high temperature")
        elif temp < 75:  # Cool temperature - turn fan off
            if fan == 'ON':
                self.agent.turn_fan_off()
                self.voice.speak("I've turned off the fan - temperature is comfortable.")
                self.smart_monitor.log_action("Auto Fan Control", "Fan turned OFF - temperature comfortable")
    
    def run_interactive_mode(self):
        """Run interactive mode with voice and text commands."""
        print("🎤 IRIS Interactive Mode")
        print("=======================")
        self.voice.speak("I'm ready. Ask me about the environment or control the LED.")
        
        try:
            while True:
                print("\n" + "="*60)
                print("🎤 IRIS VOICE-ENABLED ENVIRONMENTAL MONITORING")
                print("="*60)
                print("Try these commands:")
                print("- 'What's the temperature?'")
                print("- 'Turn on the LED'")
                print("- 'Turn on the fan'")
                print("- 'Turn off the fan'")
                print("- 'Analyze the environment'")
                print("- 'How's the air quality?'")
                print("="*60)
                
                choice = input("\nChoose input method:\n1. Voice command\n2. Text command\n3. Intelligent monitoring\n4. Exit\nEnter choice (1-4): ").strip()
                
                if choice == '1':
                    user_input = self.voice.listen()
                    if user_input:
                        self.process_voice_command(user_input)
                elif choice == '2':
                    user_input = input("\nEnter your command: ").strip()
                    if user_input.lower() in ['quit', 'exit']:
                        break
                    if user_input:
                        self.process_voice_command(user_input)
                elif choice == '3':
                    self.run_intelligent_monitoring()
                elif choice == '4':
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                
                # Automatic LED control in interactive mode
                status = self.agent.get_status()
                if "error" not in status:
                    temp = status.get('temperature', 0)
                    co2 = status.get('co2', 0)
                    light_raw = status.get('light', 0)
                    brightness = status.get('brightness', 'Unknown')
                    led = status.get('led', 'OFF')
                    fan = status.get('fan', 'OFF') # Get fan status
                    
                    # Perform automatic LED control
                    self._perform_automatic_led_control(brightness, light_raw, led)
                    
                    # Perform automatic fan control
                    self._perform_automatic_fan_control(temp, fan)
        
        except KeyboardInterrupt:
            print("\n🛑 Interactive mode stopped by user")
        finally:
            self.voice.speak("Goodbye!")
    
    def close(self):
        """Close the system and clean up resources."""
        if self.agent:
            self.agent.close()
        if self.voice:
            self.voice.close()
        print("🔌 IRIS Environmental AI closed.")


def main():
    """Main function to run the IRIS Environmental AI system."""
    print("🎯 Starting IRIS Environmental AI...")
    
    # Create the IRIS system
    iris = IRISEnvironmentalAI()
    
    if not iris.agent.connected:
        print("❌ Cannot run without Arduino connection.")
        return
    
    try:
        iris.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        iris.close()


if __name__ == "__main__":
    main() 