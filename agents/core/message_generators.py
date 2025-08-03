#!/usr/bin/env python3
"""
Message Generators Module
========================

Handles generation of various messages and prompts for the voice agent.
"""

from typing import Dict, Any
from .smart_monitor import SmartMonitor

class MessageGenerators:
    """Generates various messages for the voice agent."""
    
    @staticmethod
    def get_change_alert(current_values: Dict[str, Any], smart_monitor: SmartMonitor) -> str:
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
    
    @staticmethod
    def get_periodic_summary(current_values: Dict[str, Any]) -> str:
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
    
    @staticmethod
    def get_brightness_warning(brightness: str, light_raw: int) -> str:
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
    
    @staticmethod
    def generate_environmental_prompt(user_input: str, agent) -> str:
        """Generate a prompt for the LLM based on environmental data and user input."""
        # Get current environmental status
        status = agent.get_status()
        
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