#!/usr/bin/env python3
"""
Modular Voice-Enabled Environmental Monitoring Agent
==================================================

A clean, modular implementation using separate modules for better organization.
"""

import time
import sys
import os
from typing import Dict, Any, Callable

# Add the parent directory to the path so we can import from agents/core and agents/interfaces
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'interfaces'))

from environmental_agent import EnvironmentalAgent
from modern_voice_interface import ModernVoiceInterface
from llm_interface import LLMInterface
from smart_monitor import SmartMonitor
from action_handlers import ActionHandlers
from message_generators import MessageGenerators

class VoiceEnvironmentalAgent:
    """Modular voice-enabled environmental monitoring agent."""
    
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0", voice_model="gtts"):
        """Initialize the modular voice-enabled environmental monitoring agent."""
        # Initialize core components
        self.agent = EnvironmentalAgent(port, baud_rate)
        self.voice = ModernVoiceInterface(voice_model=voice_model)
        self.llm = LLMInterface(model_name)
        
        if not self.agent.connected:
            print("❌ Cannot initialize without Arduino connection")
            return
        
        # Initialize modules
        self.smart_monitor = SmartMonitor()
        self.action_handlers = ActionHandlers(self.agent, self.voice)
        self.message_generators = MessageGenerators()
        
        # Initialize action handlers using dictionary dispatch
        self.action_handlers_map = {
            "turn_led_on": self.action_handlers.turn_led_on,
            "turn_led_off": self.action_handlers.turn_led_off,
            "status": self.action_handlers.get_status,
            "analyze": self.action_handlers.analyze_environment,
            "get_temperature": self.action_handlers.get_temperature,
            "get_co2": self.action_handlers.get_co2,
            "get_light": self.action_handlers.get_light,
            "recommend": self.action_handlers.get_recommendations,
            "emergency_check": self.action_handlers.emergency_check
        }
        
        # Initialize menu handlers
        self.menu_handlers = {
            '1': self._handle_voice_input,
            '2': self._handle_text_input,
            '3': self._handle_continuous_monitoring,
            '4': self._handle_intelligent_system,
            '5': self._handle_demo_mode,
            '6': self._handle_exit
        }
        
        print("🔧 Modular Voice-Enabled Environmental Agent Ready!")
        print(f" Using {self.voice.voice_type} voice model for excellent quality!")
        print("I can analyze sensor data and respond with professional voice feedback.")
        self.voice.speak("I'm ready.")
    
    def execute_action(self, action: str) -> bool:
        """Execute the specified action using dictionary dispatch."""
        try:
            handler = self.action_handlers_map.get(action)
            if handler:
                return handler()
            else:
                # Try to handle unknown actions dynamically
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
{list(self.action_handlers_map.keys())}

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
            explanation = guidance_response.get('explanation', '')
            response_text = guidance_response.get('response', f"I can't perform '{action}' directly.")
            
            print(f" LLM Suggestion: {suggested_action}")
            print(f" Explanation: {explanation}")
            
            self.voice.speak(response_text)
            
            if suggested_action and suggested_action in self.action_handlers_map:
                return self.action_handlers_map[suggested_action]()
            else:
                return False
        else:
            self.voice.speak(f"I don't understand '{action}'.")
            return False
    
    def register_action(self, action_name: str, handler_func: Callable[[], bool]):
        """Dynamically register a new action handler."""
        self.action_handlers_map[action_name] = handler_func
        print(f"🔧 Registered new action: {action_name}")
    
    def get_available_actions(self) -> list:
        """Get list of available actions."""
        return list(self.action_handlers_map.keys())
    
    def _handle_voice_input(self):
        """Handle voice input."""
        user_input = self.voice.listen()
        if user_input:
            self.process_voice_command(user_input)
    
    def _handle_text_input(self):
        """Handle text input."""
        user_input = input("\nEnter your command: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            return 'exit'
        if user_input:
            self.process_voice_command(user_input)
        return None
    
    def _handle_continuous_monitoring(self):
        """Handle continuous monitoring."""
        interval = input("⏱️  Enter monitoring interval in seconds (default 30): ").strip()
        try:
            interval = int(interval) if interval else 30
            self.run_continuous_voice_monitoring(interval)
        except ValueError:
            print("❌ Invalid interval. Using default 30 seconds.")
            self.run_continuous_voice_monitoring(30)
    
    def _handle_intelligent_system(self):
        """Handle intelligent decision system."""
        self.run_intelligent_decision_system()
    
    def _handle_demo_mode(self):
        """Handle demo mode."""
        print("\n🎮 Demo Mode: Intelligent Monitoring Features")
        print("=============================================")
        print("This mode showcases the advanced features of the intelligent monitoring system.")
        print("The system will automatically alert you to significant changes and provide periodic summaries.")
        print("You can press Ctrl+C to exit this demo.")
        
        self.smart_monitor.log_action("Demo Mode", "Started intelligent monitoring demo")
        
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
                    
                    # Update smart monitor
                    current_values = {
                        'temperature': temp,
                        'co2': co2,
                        'light': light_raw,
                        'led': led
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
                        
                        # Generate appropriate message based on context
                        if emergencies:
                            # Emergency already handled above
                            pass
                        elif self.smart_monitor.has_significant_changes(current_values):
                            # Change detected
                            change_message = self.message_generators.get_change_alert(current_values, self.smart_monitor)
                            self.voice.speak(change_message)
                            self.smart_monitor.log_action("Change Alert", change_message)
                        else:
                            # Periodic summary
                            summary_message = self.message_generators.get_periodic_summary(current_values)
                            self.voice.speak(summary_message)
                            self.smart_monitor.update_summary_time()
                            self.smart_monitor.log_action("Periodic Summary", summary_message)
                    
                    # Always show console display
                    print("\n" + "="*60)
                    print(self.smart_monitor.get_status_display(current_values))
                    print("\n📋 Recent Actions:")
                    print(self.smart_monitor.get_recent_actions())
                    print("="*60)
                    
                    # Perform automatic LED control (silent)
                    led_action = self.action_handlers.get_led_action(brightness, light_raw, led)
                    if led_action:
                        self.smart_monitor.log_action("Auto LED Control", led_action['message'])
                    
                else:
                    self.voice.speak("I can't access the sensors right now.")
                    self.smart_monitor.log_action("Error", "Arduino sensors not responding")
                    
                time.sleep(1) # Check every second
                
        except KeyboardInterrupt:
            print("\n🛑 Intelligent monitoring demo stopped by user")
            self.voice.speak("I've stopped the demo.")
            self.smart_monitor.log_action("System Stop", "Intelligent monitoring demo stopped by user")
    
    def _handle_exit(self):
        """Handle exit."""
        return 'exit'
    
    def run_voice_monitoring(self):
        """Run continuous voice monitoring with user interaction using dictionary dispatch."""
        print("🎤 Starting modular voice-enabled environmental monitoring...")
        self.voice.speak("I'm ready. Ask me about the environment or control the LED.")
        
        try:
            while True:
                print("\n" + "="*60)
                print("🎤 IRIS VOICE-ENABLED ENVIRONMENTAL MONITORING")
                print("="*60)
                print("Try these voice commands:")
                print("- 'What's the temperature?'")
                print("- 'Turn on the LED'")
                print("- 'Turn off the LED'")
                print("- 'What's the environmental status?'")
                print("- 'Analyze the environment'")
                print("- 'How's the air quality?'")
                print("="*60)
                
                # Get user input method using dictionary dispatch
                choice = input("\nChoose input method:\n1. Voice command\n2. Text command\n3. Continuous monitoring\n4. Intelligent decision system (analyze & recommend)\n5. Demo mode (advanced features)\n6. Exit\nEnter choice (1-6): ").strip()
                
                handler = self.menu_handlers.get(choice)
                if handler:
                    result = handler()
                    if result == 'exit':
                        break
                else:
                    print("❌ Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n🛑 Voice monitoring stopped by user")
        finally:
            self.voice.speak("I'm stopping. Goodbye!")
    
    def process_voice_command(self, user_input: str):
        """Process a voice command using LLM intelligence and modern TTS feedback."""
        print(f"\n Processing: {user_input}")
        
        # Generate LLM prompt with full environmental context
        prompt = self.message_generators.generate_environmental_prompt(user_input, self.agent)
        
        # Query the LLM
        llm_response = self.llm.query_llm(prompt)
        
        if llm_response:
            # Extract action and response from LLM decision
            action = llm_response.get('action', 'analyze')
            response_text = llm_response.get('response', 'Processing your request.')
            explanation = llm_response.get('explanation', '')
            analysis = llm_response.get('analysis', '')
            
            print(f" LLM Action: {action}")
            print(f" Explanation: {explanation}")
            if analysis:
                print(f" Analysis: {analysis}")
            
            # Speak the response with modern voice
            self.voice.speak(response_text)
            
            # Execute the action using dictionary dispatch
            success = self.execute_action(action)
            
            if not success:
                self.voice.speak("I encountered an error executing that command.")
        else:
            self.voice.speak("I couldn't process your request. Please try again.")
    
    def run_continuous_voice_monitoring(self, interval=30):
        """Run continuous monitoring with modern voice announcements."""
        print(f"🔄 Starting continuous modular voice monitoring (every {interval} seconds)")
        self.voice.speak(f"I'll monitor every {interval} seconds.")
        print("Press Ctrl+C to stop")
        
        self.smart_monitor.log_action("Continuous Monitoring", f"Started with {interval}s interval")
        
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
                    led = status.get('led', 'OFF')
                    
                    current_values = {
                        'temperature': temp,
                        'co2': co2,
                        'light': light_raw,
                        'led': led
                    }
                    
                    print(f"  Temperature: {temp}°F")
                    print(f" CO2: {co2}")
                    print(f" Light: {light_raw}")
                    print(f" LED: {led}")
                    
                    # Update smart monitor
                    self.smart_monitor.update_last_values(current_values)
                    
                    # Check for emergencies
                    emergencies = self.smart_monitor.is_emergency(current_values)
                    if emergencies:
                        for emergency_type, message in emergencies.items():
                            self.voice.speak(message)
                            self.smart_monitor.log_action("EMERGENCY", f"{emergency_type}: {message}")
                    
                    # Use smart speech frequency
                    should_speak = self.smart_monitor.should_speak(current_values, force=False)
                    
                    if should_speak:
                        self.smart_monitor.update_speech_time()
                        
                        # Generate warnings based on conditions
                        warnings = []
                        if temp < 60:
                            warnings.append(f"Temperature {temp}°F - cold.")
                        elif temp > 86:
                            warnings.append(f"Temperature {temp}°F - warm.")
                        
                        if co2 > 1000:
                            warnings.append("CO2 levels high - poor ventilation.")
                        
                        # Use match statement for brightness warnings
                        brightness_warning = self.message_generators.get_brightness_warning(brightness, light_raw)
                        if brightness_warning:
                            warnings.append(brightness_warning)
                        
                        # Speak all warnings
                        for warning in warnings:
                            self.voice.speak(warning)
                            self.smart_monitor.log_action("Warning", warning)
                    else:
                        self.smart_monitor.update_summary_time()
                        self.smart_monitor.log_action("Silent Check", "Conditions stable")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Continuous monitoring stopped by user")
            self.voice.speak("I've stopped monitoring.")
            self.smart_monitor.log_action("System Stop", "Continuous monitoring stopped by user")
    
    def run_intelligent_decision_system(self):
        """Run the intelligent decision system for continuous monitoring and recommendations."""
        print("\n🧠 Intelligent Decision System (Press Ctrl+C to exit)")
        print("--------------------------------------------------")
        
        # Initial startup announcement
        self.voice.speak("I'm starting intelligent monitoring. I'll alert you to important changes.")
        self.smart_monitor.log_action("System Start", "Intelligent monitoring initialized")
        
        while True:
            try:
                # Get environmental status
                status = self.agent.get_status()
                
                if "error" not in status:
                    temp = status.get('temperature', 0)
                    co2 = status.get('co2', 0)
                    light_raw = status.get('light', 0)
                    brightness = status.get('brightness', 'Unknown')
                    led = status.get('led', 'OFF')
                    
                    # Update smart monitor
                    current_values = {
                        'temperature': temp,
                        'co2': co2,
                        'light': light_raw,
                        'led': led
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
                        
                        # Generate appropriate message based on context
                        if emergencies:
                            # Emergency already handled above
                            pass
                        elif self.smart_monitor.has_significant_changes(current_values):
                            # Change detected
                            change_message = self.message_generators.get_change_alert(current_values, self.smart_monitor)
                            self.voice.speak(change_message)
                            self.smart_monitor.log_action("Change Alert", change_message)
                        else:
                            # Periodic summary
                            summary_message = self.message_generators.get_periodic_summary(current_values)
                            self.voice.speak(summary_message)
                            self.smart_monitor.update_summary_time()
                            self.smart_monitor.log_action("Periodic Summary", summary_message)
                    
                    # Always show console display
                    print("\n" + "="*60)
                    print(self.smart_monitor.get_status_display(current_values))
                    print("\n📋 Recent Actions:")
                    print(self.smart_monitor.get_recent_actions())
                    print("="*60)
                    
                    # Perform automatic LED control (silent)
                    led_action = self.action_handlers.get_led_action(brightness, light_raw, led)
                    if led_action:
                        self.smart_monitor.log_action("Auto LED Control", led_action['message'])
                    
                else:
                    self.voice.speak("I can't access the sensors right now.")
                    self.smart_monitor.log_action("Error", "Arduino sensors not responding")
                    
                time.sleep(1) # Check every second
                
            except KeyboardInterrupt:
                print("\n🛑 Intelligent decision system stopped by user")
                self.voice.speak("I've stopped the intelligent system.")
                break
    
    def close(self):
        """Close the agent and clean up resources."""
        if self.agent:
            self.agent.close()
        if self.voice:
            self.voice.close()
        print("🔌 Modular voice environmental agent closed.")

def main():
    """Main function to run the modular voice-enabled environmental agent."""
    print("🎤 Starting Modular Voice-Enabled Environmental Monitoring Agent...")
    
    # Create the modular voice agent
    agent = VoiceEnvironmentalAgent()
    
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