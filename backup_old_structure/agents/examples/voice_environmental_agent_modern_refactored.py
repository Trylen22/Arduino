#!/usr/bin/env python3
"""
Refactored Voice-Enabled Environmental Monitoring Agent
=====================================================

Demonstrating better alternatives to elif chains using modern Python patterns.
"""

import time
import sys
import os
from typing import Dict, Any, Callable
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from agents/core and agents/interfaces
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'interfaces'))

from environmental_agent import EnvironmentalAgent
from modern_voice_interface import ModernVoiceInterface
from llm_interface import LLMInterface

class SmartMonitor:
    """Smart monitoring system with change detection and intelligent speech frequency."""
    
    def __init__(self):
        self.last_values = {}
        self.change_thresholds = {
            'temperature': 5,
            'co2': 200,
            'light': 100
        }
        self.speech_cooldown = 60  # seconds - increased from 30
        self.last_speech_time = 0
        self.summary_interval = 300  # 5 minutes - increased from 2 minutes
        self.last_summary_time = 0
        self.emergency_conditions = {
            'temperature': {'min': 50, 'max': 95},
            'co2': {'max': 2000},
            'light': {'min': 50}
        }
        self.action_log = []
        self.start_time = datetime.now()
    
    def has_significant_changes(self, current_values: Dict[str, Any]) -> bool:
        """Check if values have changed significantly."""
        if not self.last_values:
            return True  # First run
        
        for key, threshold in self.change_thresholds.items():
            if key in current_values and key in self.last_values:
                current = float(current_values[key])
                last = float(self.last_values[key])
                if abs(current - last) >= threshold:
                    return True
        return False
    
    def is_emergency(self, current_values: Dict[str, Any]) -> Dict[str, str]:
        """Check for emergency conditions."""
        emergencies = {}
        
        temp = current_values.get('temperature', 0)
        co2 = current_values.get('co2', 0)
        light = current_values.get('light', 0)
        
        if temp > self.emergency_conditions['temperature']['max']:
            emergencies['temperature'] = f"CRITICAL: Temperature {temp}°F - dangerously high!"
        elif temp < self.emergency_conditions['temperature']['min']:
            emergencies['temperature'] = f"CRITICAL: Temperature {temp}°F - dangerously low!"
        
        if co2 > self.emergency_conditions['co2']['max']:
            emergencies['co2'] = "CRITICAL: CO2 levels extremely high - immediate ventilation required!"
        
        if light < self.emergency_conditions['light']['min']:
            emergencies['light'] = "WARNING: Lighting extremely dim - safety concern!"
        
        return emergencies
    
    def should_speak(self, current_values: Dict[str, Any], force: bool = False) -> bool:
        """Determine if speech should occur."""
        if force:
            return True
        
        current_time = time.time()
        
        # Emergency conditions always trigger speech
        if self.is_emergency(current_values):
            return True
        
        # Check speech cooldown
        if current_time - self.last_speech_time < self.speech_cooldown:
            return False
        
        # Significant changes trigger speech
        if self.has_significant_changes(current_values):
            return True
        
        # Periodic summary (every 2 minutes)
        if current_time - self.last_summary_time >= self.summary_interval:
            return True
        
        return False
    
    def update_last_values(self, current_values: Dict[str, Any]):
        """Update last values for change detection."""
        self.last_values = current_values.copy()
    
    def update_speech_time(self):
        """Update last speech time."""
        self.last_speech_time = time.time()
    
    def update_summary_time(self):
        """Update last summary time."""
        self.last_summary_time = time.time()
    
    def log_action(self, action: str, details: str = ""):
        """Log an action for the demo."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.action_log.append(f"[{timestamp}] {action}: {details}")
        # Keep only last 10 actions
        if len(self.action_log) > 10:
            self.action_log.pop(0)
    
    def get_status_display(self, current_values: Dict[str, Any]) -> str:
        """Generate status display for console."""
        temp = current_values.get('temperature', 'N/A')
        co2 = current_values.get('co2', 'N/A')
        light = current_values.get('light', 'N/A')
        led = current_values.get('led', 'OFF')
        
        # Add change indicators
        temp_indicator = self._get_change_indicator('temperature', temp)
        co2_indicator = self._get_change_indicator('co2', co2)
        light_indicator = self._get_change_indicator('light', light)
        
        status = "🟢 Normal"
        if self.is_emergency(current_values):
            status = "🔴 EMERGENCY"
        elif self.has_significant_changes(current_values):
            status = "🟡 Changes Detected"
        
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        display = f"""
🔄 IRIS Intelligent Environmental Monitoring
==========================================
⏰ Last Update: {datetime.now().strftime('%H:%M:%S')} | ⏱️  Uptime: {uptime_str}
🌡️  Temperature: {temp}°F {temp_indicator} | 🌬️  CO2: {co2} {co2_indicator}
💡 Light: {light} {light_indicator} | 🔆 LED: {led}
📊 Status: {status} | 🎯 Actions: {len(self.action_log)} recent
"""
        return display
    
    def _get_change_indicator(self, key: str, current_value: Any) -> str:
        """Get change indicator for a value."""
        if key not in self.last_values or current_value == 'N/A':
            return ""
        
        try:
            current = float(current_value)
            last = float(self.last_values[key])
            if current > last:
                return "↑"
            elif current < last:
                return "↓"
            else:
                return "→"
        except (ValueError, TypeError):
            return ""
    
    def get_recent_actions(self) -> str:
        """Get recent actions for display."""
        if not self.action_log:
            return "No recent actions"
        return "\n".join(self.action_log[-5:])  # Last 5 actions

class RefactoredVoiceEnvironmentalAgent:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0", voice_model="gtts"):
        """Initialize the refactored voice-enabled environmental monitoring agent."""
        # Initialize core components
        self.agent = EnvironmentalAgent(port, baud_rate)
        self.voice = ModernVoiceInterface(voice_model=voice_model)
        self.llm = LLMInterface(model_name)
        
        if not self.agent.connected:
            print("❌ Cannot initialize without Arduino connection")
            return
        
        # Initialize action handlers using dictionary dispatch
        self.action_handlers = {
            "turn_led_on": self._handle_turn_led_on,
            "turn_led_off": self._handle_turn_led_off,
            "status": self._handle_status,
            "analyze": self._handle_analyze,
            "get_temperature": self._handle_get_temperature,
            "get_co2": self._handle_get_co2,
            "get_light": self._handle_get_light,
            "recommend": self._handle_recommend,
            "emergency_check": self._handle_emergency_check
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
        
        # Temperature analysis using dictionary
        self.temp_analysis = {
            lambda t: t < 60: "It's quite cold.",
            lambda t: t > 86: "It's quite warm.",
            lambda t: True: "The temperature is comfortable."
        }
        
        # CO2 analysis using dictionary
        self.co2_analysis = {
            lambda c: c > 1000: "CO2 levels are high, indicating poor ventilation.",
            lambda c: c > 800: "CO2 levels are moderate.",
            lambda c: True: "Air quality appears good."
        }
        
        print("🔧 Refactored Voice-Enabled Environmental Agent Ready!")
        print(f" Using {self.voice.voice_type} voice model for excellent quality!")
        print("I can analyze sensor data and respond with professional voice feedback.")
        self.voice.speak("I'm ready.")
    
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
    
    def _handle_status(self) -> bool:
        """Handle status request."""
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
            
            status_message = f"I'm reading temperature {temp}°F, CO2 {co2}, light {light_info}, LED {led}."
            self.voice.speak(status_message)
            return True
        else:
            self.voice.speak("I can't access the sensors right now.")
            return False
    
    def _handle_analyze(self) -> bool:
        """Handle environmental analysis."""
        status = self.agent.get_status()
        if "error" not in status:
            temp = status.get('temperature', 0)
            co2 = status.get('co2', 0)
            light_raw = status.get('light', 0)
            brightness = status.get('brightness', 'Unknown')
            
            analysis_message = f"My analysis shows temperature {temp}°F. "
            
            # Use dictionary dispatch for temperature analysis
            for condition, message in self.temp_analysis.items():
                if condition(temp):
                    analysis_message += message + " "
                    break
            
            # Use dictionary dispatch for CO2 analysis
            for condition, message in self.co2_analysis.items():
                if condition(co2):
                    analysis_message += message + " "
                    break
            
            # Use match statement for brightness analysis (Python 3.10+)
            analysis_message += self._analyze_brightness(brightness, light_raw)
            
            self.voice.speak(analysis_message)
            return True
        else:
            self.voice.speak("I can't analyze the environment right now.")
            return False
    
    def _handle_get_temperature(self) -> bool:
        """Handle temperature-specific request."""
        status = self.agent.get_status()
        if "error" not in status:
            temp = status.get('temperature', 'N/A')
            temp_message = f"I'm reading temperature {temp}°F."
            
            # Add temperature-specific analysis
            if temp != 'N/A':
                temp_num = float(temp)
                if temp_num < 60:
                    temp_message += " It's cold."
                elif temp_num > 86:
                    temp_message += " It's warm."
                else:
                    temp_message += " Temperature is comfortable."
            
            self.voice.speak(temp_message)
            return True
        else:
            self.voice.speak("I can't get the temperature right now.")
            return False
    
    def _handle_get_co2(self) -> bool:
        """Handle CO2-specific request."""
        status = self.agent.get_status()
        if "error" not in status:
            co2 = status.get('co2', 'N/A')
            co2_message = f"I'm reading CO2 level {co2}."
            
            # Add CO2-specific analysis
            if co2 != 'N/A':
                co2_num = int(co2)
                if co2_num > 1000:
                    co2_message += " Poor ventilation. Open windows or use a fan."
                elif co2_num > 800:
                    co2_message += " Air quality moderate."
                else:
                    co2_message += " Air quality good."
            
            self.voice.speak(co2_message)
            return True
        else:
            self.voice.speak("I can't get the CO2 level right now.")
            return False
    
    def _handle_get_light(self) -> bool:
        """Handle light-specific request."""
        status = self.agent.get_status()
        if "error" not in status:
            light_raw = status.get('light', 'N/A')
            brightness = status.get('brightness', 'Unknown')
            light_percent = status.get('light_percentage', 'N/A')
            
            if brightness != 'Unknown' and light_percent != 'N/A':
                light_message = f"I'm reading light level {light_raw} ({brightness}, {light_percent}% brightness)."
            else:
                light_message = f"I'm reading light level {light_raw}."
            
            # Add light-specific analysis
            if brightness != 'Unknown':
                match brightness:
                    case 'Very Dark' | 'Dark':
                        light_message += " Lighting is dim. Need more light."
                    case 'Very Bright':
                        light_message += " Lighting is very bright."
                    case _:
                        light_message += " Lighting is adequate."
            else:
                if light_raw != 'N/A':
                    light_num = int(light_raw)
                    if light_num < 100:
                        light_message += " Lighting is dim."
                    elif light_num > 800:
                        light_message += " Lighting is bright."
                    else:
                        light_message += " Lighting is adequate."
            
            self.voice.speak(light_message)
            return True
        else:
            self.voice.speak("I can't get the light level right now.")
            return False
    
    def _handle_recommend(self) -> bool:
        """Handle recommendation request."""
        status = self.agent.get_status()
        if "error" not in status:
            temp = status.get('temperature', 0)
            co2 = status.get('co2', 0)
            light_raw = status.get('light', 0)
            brightness = status.get('brightness', 'Unknown')
            led = status.get('led', 'OFF')
            
            recommendations = []
            
            # Temperature recommendations
            if temp < 60:
                recommendations.append("Increase temperature for comfort.")
            elif temp > 86:
                recommendations.append("Decrease temperature for comfort.")
            
            # CO2 recommendations
            if co2 > 1000:
                recommendations.append("Open windows or use a fan for ventilation.")
            elif co2 > 800:
                recommendations.append("Consider opening a window.")
            
            # Lighting recommendations
            if brightness != 'Unknown':
                match brightness:
                    case 'Very Dark' | 'Dark':
                        if led == 'OFF':
                            recommendations.append("I'll turn on the LED for lighting.")
                            self.agent.turn_led_on()
                        else:
                            recommendations.append("The LED is already on for lighting.")
                    case 'Very Bright':
                        if led == 'ON':
                            recommendations.append("I'll turn off the LED - lighting is adequate.")
                            self.agent.turn_led_off()
                        else:
                            recommendations.append("The LED is already off - lighting is adequate.")
            else:
                if light_raw < 100:
                    if led == 'OFF':
                        recommendations.append("I'll turn on the LED for lighting.")
                        self.agent.turn_led_on()
                    else:
                        recommendations.append("The LED is already on for lighting.")
                elif light_raw > 800:
                    if led == 'ON':
                        recommendations.append("I'll turn off the LED - lighting is adequate.")
                        self.agent.turn_led_off()
                    else:
                        recommendations.append("The LED is already off - lighting is adequate.")
            
            if recommendations:
                recommendation_message = "My recommendations: " + " ".join(recommendations)
            else:
                recommendation_message = "Environment is optimal. No recommendations needed."
            
            self.voice.speak(recommendation_message)
            return True
        else:
            self.voice.speak("I can't provide recommendations right now.")
            return False
    
    def _handle_emergency_check(self) -> bool:
        """Handle emergency check request."""
        status = self.agent.get_status()
        if "error" not in status:
            temp = status.get('temperature', 0)
            co2 = status.get('co2', 0)
            light_raw = status.get('light', 0)
            
            emergency_conditions = []
            
            # Check for emergency conditions
            if temp > 95:
                emergency_conditions.append(f"CRITICAL: Temperature {temp}°F - dangerously high!")
            elif temp < 50:
                emergency_conditions.append(f"CRITICAL: Temperature {temp}°F - dangerously low!")
            
            if co2 > 2000:
                emergency_conditions.append("CRITICAL: CO2 levels extremely high - immediate ventilation required!")
            elif co2 > 1500:
                emergency_conditions.append("WARNING: CO2 levels very high - ventilation needed!")
            
            if light_raw < 50:
                emergency_conditions.append("WARNING: Lighting extremely dim - safety concern!")
            
            if emergency_conditions:
                emergency_message = "EMERGENCY CHECK: " + " ".join(emergency_conditions)
                self.voice.speak(emergency_message)
            else:
                self.voice.speak("Emergency check complete. All systems normal.")
            
            return True
        else:
            self.voice.speak("I can't perform emergency check - sensors not responding!")
            return False
    
    def _analyze_brightness(self, brightness: str, light_raw: int) -> str:
        """Analyze brightness using match statement."""
        if brightness != 'Unknown':
            # Using match statement (Python 3.10+)
            match brightness:
                case 'Very Dark' | 'Dark':
                    return f"The lighting is {brightness.lower()}, you might need more light. "
                case 'Very Bright':
                    return f"The lighting is {brightness.lower()}, it might be too bright. "
                case _:
                    return f"The lighting is {brightness.lower()}, which is adequate. "
        else:
            # Fallback to raw value analysis
            if light_raw < 100:
                return "The lighting is quite dim. "
            elif light_raw > 800:
                return "The lighting is very bright. "
            else:
                return "The lighting is adequate. "
    
    def execute_action(self, action: str) -> bool:
        """Execute the specified action using dictionary dispatch."""
        try:
            handler = self.action_handlers.get(action)
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
            explanation = guidance_response.get('explanation', '')
            response_text = guidance_response.get('response', f"I can't perform '{action}' directly.")
            
            print(f" LLM Suggestion: {suggested_action}")
            print(f" Explanation: {explanation}")
            
            self.voice.speak(response_text)
            
            if suggested_action and suggested_action in self.action_handlers:
                return self.action_handlers[suggested_action]()
            else:
                return False
        else:
            self.voice.speak(f"I don't understand '{action}'.")
            return False
    
    def register_action(self, action_name: str, handler_func: Callable[[], bool]):
        """Dynamically register a new action handler."""
        self.action_handlers[action_name] = handler_func
        print(f"🔧 Registered new action: {action_name}")
    
    def get_available_actions(self) -> list:
        """Get list of available actions."""
        return list(self.action_handlers.keys())
    
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
        
        smart_monitor = SmartMonitor()
        smart_monitor.log_action("Demo Mode", "Started intelligent monitoring demo")
        
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
                    smart_monitor.update_last_values(current_values)
                    
                    # Check for emergencies first
                    emergencies = smart_monitor.is_emergency(current_values)
                    if emergencies:
                        for emergency_type, message in emergencies.items():
                            self.voice.speak(message)
                            smart_monitor.log_action("EMERGENCY", f"{emergency_type}: {message}")
                    
                    # Determine if speech is needed
                    should_speak = smart_monitor.should_speak(current_values)
                    
                    if should_speak:
                        smart_monitor.update_speech_time()
                        
                        # Generate appropriate message based on context
                        if emergencies:
                            # Emergency already handled above
                            pass
                        elif smart_monitor.has_significant_changes(current_values):
                            # Change detected
                            change_message = self._get_change_alert(current_values, smart_monitor)
                            self.voice.speak(change_message)
                            smart_monitor.log_action("Change Alert", change_message)
                        else:
                            # Periodic summary
                            summary_message = self._get_periodic_summary(current_values)
                            self.voice.speak(summary_message)
                            smart_monitor.update_summary_time()
                            smart_monitor.log_action("Periodic Summary", summary_message)
                    
                    # Always show console display
                    print("\n" + "="*60)
                    print(smart_monitor.get_status_display(current_values))
                    print("\n📋 Recent Actions:")
                    print(smart_monitor.get_recent_actions())
                    print("="*60)
                    
                    # Perform automatic LED control (silent)
                    led_action = self._get_led_action(brightness, light_raw, led)
                    if led_action:
                        smart_monitor.log_action("Auto LED Control", led_action['message'])
                    
                else:
                    self.voice.speak("Sensors unavailable.")
                    smart_monitor.log_action("Error", "Arduino sensors not responding")
                    
                time.sleep(1) # Check every second
                
        except KeyboardInterrupt:
            print("\n🛑 Intelligent monitoring demo stopped by user")
            self.voice.speak("I've stopped the demo.")
            smart_monitor.log_action("System Stop", "Intelligent monitoring demo stopped by user")
    
    def _handle_exit(self):
        """Handle exit."""
        return 'exit'
    
    def run_voice_monitoring(self):
        """Run continuous voice monitoring with user interaction using dictionary dispatch."""
        print("🎤 Starting refactored voice-enabled environmental monitoring...")
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
- turn_led_on: Turn LED ON
- turn_led_off: Turn LED OFF
- status: Get current sensor readings
- analyze: Comprehensive environmental analysis
- get_temperature: Get temperature-specific information
- get_co2: Get CO2-specific information
- get_light: Get light-specific information
- recommend: Provide recommendations based on conditions
- emergency_check: Check for critical conditions

Note: If the user requests an action not in this list, I will intelligently suggest the most appropriate available action.

User request: "{user_input}"

Please respond with a JSON object containing:
1. "action": The action to perform (choose from available actions above, or suggest a new one)
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
        
        # Generate LLM prompt with full environmental context
        prompt = self.generate_environmental_prompt(user_input)
        
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
        print(f"🔄 Starting continuous refactored voice monitoring (every {interval} seconds)")
        self.voice.speak(f"I'll monitor every {interval} seconds.")
        print("Press Ctrl+C to stop")
        
        smart_monitor = SmartMonitor()
        smart_monitor.log_action("Continuous Monitoring", f"Started with {interval}s interval")
        
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
                    smart_monitor.update_last_values(current_values)
                    
                    # Check for emergencies
                    emergencies = smart_monitor.is_emergency(current_values)
                    if emergencies:
                        for emergency_type, message in emergencies.items():
                            self.voice.speak(message)
                            smart_monitor.log_action("EMERGENCY", f"{emergency_type}: {message}")
                    
                    # Use smart speech frequency
                    should_speak = smart_monitor.should_speak(current_values, force=False)
                    
                    if should_speak:
                        smart_monitor.update_speech_time()
                        
                        # Generate warnings based on conditions
                        warnings = []
                        if temp < 60:
                            warnings.append(f"Temperature {temp}°F - cold.")
                        elif temp > 86:
                            warnings.append(f"Temperature {temp}°F - warm.")
                        
                        if co2 > 1000:
                            warnings.append("CO2 levels high - poor ventilation.")
                        
                        # Use match statement for brightness warnings
                        brightness_warning = self._get_brightness_warning(brightness, light_raw)
                        if brightness_warning:
                            warnings.append(brightness_warning)
                        
                        # Speak all warnings
                        for warning in warnings:
                            self.voice.speak(warning)
                            smart_monitor.log_action("Warning", warning)
                    else:
                        smart_monitor.update_summary_time()
                        smart_monitor.log_action("Silent Check", "Conditions stable")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Continuous monitoring stopped by user")
            self.voice.speak("I've stopped monitoring.")
            smart_monitor.log_action("System Stop", "Continuous monitoring stopped by user")
    
    def _get_brightness_warning(self, brightness: str, light_raw: int) -> str:
        """Get brightness warning using match statement."""
        if brightness != 'Unknown':
            match brightness:
                case 'Very Dark' | 'Dark':
                    return f"Lighting {brightness.lower()} - need more light."
                case 'Very Bright':
                    return f"Lighting {brightness.lower()} - too bright."
                case _:
                    return ""
        else:
            if light_raw < 100:
                return "Lighting dim."
            return ""
    
    def run_intelligent_decision_system(self):
        """Run the intelligent decision system for continuous monitoring and recommendations."""
        print("\n🧠 Intelligent Decision System (Press Ctrl+C to exit)")
        print("--------------------------------------------------")
        smart_monitor = SmartMonitor()
        
        # Initial startup announcement
        self.voice.speak("I'm starting intelligent monitoring. I'll alert you to important changes.")
        smart_monitor.log_action("System Start", "Intelligent monitoring initialized")
        
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
                    smart_monitor.update_last_values(current_values)
                    
                    # Check for emergencies first
                    emergencies = smart_monitor.is_emergency(current_values)
                    if emergencies:
                        for emergency_type, message in emergencies.items():
                            self.voice.speak(message)
                            smart_monitor.log_action("EMERGENCY", f"{emergency_type}: {message}")
                    
                    # Determine if speech is needed
                    should_speak = smart_monitor.should_speak(current_values)
                    
                    if should_speak:
                        smart_monitor.update_speech_time()
                        
                        # Generate appropriate message based on context
                        if emergencies:
                            # Emergency already handled above
                            pass
                        elif smart_monitor.has_significant_changes(current_values):
                            # Change detected
                            change_message = self._get_change_alert(current_values, smart_monitor)
                            self.voice.speak(change_message)
                            smart_monitor.log_action("Change Alert", change_message)
                        else:
                            # Periodic summary
                            summary_message = self._get_periodic_summary(current_values)
                            self.voice.speak(summary_message)
                            smart_monitor.update_summary_time()
                            smart_monitor.log_action("Periodic Summary", summary_message)
                    
                    # Always show console display
                    print("\n" + "="*60)
                    print(smart_monitor.get_status_display(current_values))
                    print("\n📋 Recent Actions:")
                    print(smart_monitor.get_recent_actions())
                    print("="*60)
                    
                    # Perform automatic LED control (silent)
                    led_action = self._get_led_action(brightness, light_raw, led)
                    if led_action:
                        smart_monitor.log_action("Auto LED Control", led_action['message'])
                    
                else:
                    self.voice.speak("I can't access the sensors right now.")
                    smart_monitor.log_action("Error", "Arduino sensors not responding")
                    
                time.sleep(1) # Check every second
                
            except KeyboardInterrupt:
                print("\n🛑 Intelligent decision system stopped by user")
                self.voice.speak("I've stopped the intelligent system.")
                break
    
    def _get_change_alert(self, current_values: Dict[str, Any], smart_monitor: SmartMonitor) -> str:
        """Generate alert message for significant changes."""
        changes = []
        
        for key, threshold in smart_monitor.change_thresholds.items():
            if key in current_values and key in smart_monitor.last_values:
                current = float(current_values[key])
                last = float(smart_monitor.last_values[key])
                if abs(current - last) >= threshold:
                    if key == 'temperature':
                        changes.append(f"Temperature {last}°F to {current}°F")
                    elif key == 'co2':
                        changes.append(f"CO2 {last} to {current}")
                    elif key == 'light':
                        changes.append(f"Light {last} to {current}")
        
        if changes:
            return f"Changes detected: {'; '.join(changes)}."
        else:
            return "Environmental changes detected."
    
    def _get_periodic_summary(self, current_values: Dict[str, Any]) -> str:
        """Generate periodic summary message."""
        temp = current_values.get('temperature', 0)
        co2 = current_values.get('co2', 0)
        light = current_values.get('light', 0)
        
        summary_parts = []
        
        # Temperature summary
        if temp < 60:
            summary_parts.append("temperature cool")
        elif temp > 86:
            summary_parts.append("temperature warm")
        else:
            summary_parts.append("temperature comfortable")
        
        # CO2 summary
        if co2 > 1000:
            summary_parts.append("air quality poor")
        elif co2 > 800:
            summary_parts.append("air quality moderate")
        else:
            summary_parts.append("air quality good")
        
        # Light summary
        if light < 100:
            summary_parts.append("lighting dim")
        elif light > 800:
            summary_parts.append("lighting bright")
        else:
            summary_parts.append("lighting adequate")
        
        return f"Status: {', '.join(summary_parts)}."
    
    def _get_led_action(self, brightness: str, light_raw: int, led: str) -> Dict[str, str]:
        """Get LED action based on lighting conditions."""
        if brightness != 'Unknown':
            match brightness:
                case 'Very Dark' | 'Dark':
                    if led == 'OFF':
                        self.agent.turn_led_on()
                        return {
                            'message': 'LED turned ON automatically for poor lighting',
                            'explanation': "I turned on the LED for lighting."
                        }
                case 'Very Bright':
                    if led == 'ON':
                        self.agent.turn_led_off()
                        return {
                            'message': 'LED turned OFF automatically - lighting is adequate',
                            'explanation': "I turned off the LED - lighting is adequate."
                        }
                case _:
                    if led == 'ON':
                        self.agent.turn_led_off()
                        return {
                            'message': 'LED turned OFF automatically - lighting is adequate',
                            'explanation': "I turned off the LED - lighting is adequate."
                        }
        else:
            # Fallback to raw value analysis
            if light_raw < 100 and led == 'OFF':
                self.agent.turn_led_on()
                return {
                    'message': 'LED turned ON automatically for poor lighting',
                    'explanation': "I turned on the LED for lighting."
                }
            elif light_raw > 800 and led == 'ON':
                self.agent.turn_led_off()
                return {
                    'message': 'LED turned OFF automatically - lighting is adequate',
                    'explanation': "I turned off the LED - lighting is adequate."
                }
            elif light_raw >= 100 and light_raw <= 800 and led == 'ON':
                self.agent.turn_led_off()
                return {
                    'message': 'LED turned OFF automatically - lighting is adequate',
                    'explanation': "I turned off the LED - lighting is adequate."
                }
        
        return None
    
    def close(self):
        """Close the agent and clean up resources."""
        if self.agent:
            self.agent.close()
        if self.voice:
            self.voice.close()
        print("🔌 Refactored voice environmental agent closed.")

def main():
    """Main function to run the refactored voice-enabled environmental agent."""
    print("🎤 Starting Refactored Voice-Enabled Environmental Monitoring Agent...")
    
    # Create the refactored voice agent
    agent = RefactoredVoiceEnvironmentalAgent()
    
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