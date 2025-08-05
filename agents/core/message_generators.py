#!/usr/bin/env python3
"""
Message Generators - Centralized Message Creation
===============================================

Provides centralized message generation for environmental monitoring system.
Handles status messages, alerts, warnings, and user responses.
Now includes student companion features for emotional support and study assistance.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta


class MessageGenerators:
    """Centralized message generation for environmental monitoring and student support."""
    
    # Student companion personality traits
    STUDENT_PERSONALITY = {
        "encouraging": True,
        "empathetic": True,
        "playful": True,
        "supportive": True,
        "practical": True
    }
    
    @staticmethod
    def get_status_message(status: Dict[str, Any]) -> str:
        """Generate status message from sensor data."""
        if "error" in status:
            return "I can't access the sensors right now."
        
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
        
        return f"I'm reading temperature {temp}°F, CO2 {co2}, light {light_info}, LED {led}."
    
    @staticmethod
    def get_student_support_message(student_context: Dict[str, Any]) -> str:
        """Generate student-focused support messages based on context."""
        mood = student_context.get('mood', 'neutral')
        study_time = student_context.get('study_time_minutes', 0)
        stress_level = student_context.get('stress_level', 0)
        environment = student_context.get('environment', {})
        
        messages = []
        
        # Emotional support based on mood
        if mood == "stressed":
            messages.append("I can sense you're feeling stressed. That's totally normal, especially during exams. Let's take a moment together.")
        elif mood == "frustrated":
            messages.append("Frustration is part of the learning process. You're growing your brain right now!")
        elif mood == "tired":
            messages.append("Your brain has been working hard. It's okay to feel tired - that means you're learning!")
        
        # Study time awareness
        if study_time > 120:  # 2 hours
            messages.append(f"Wow! You've been studying for {study_time} minutes. That's some serious dedication!")
        elif study_time > 60:  # 1 hour
            messages.append(f"You've been focused for {study_time} minutes. Great work!")
        
        # Environmental support
        temp = environment.get('temperature', 0)
        co2 = environment.get('co2', 0)
        light = environment.get('brightness', 'Unknown')
        
        if temp > 80:
            messages.append("The room is getting warm. Want me to turn on the fan to help you stay comfortable?")
        elif temp < 65:
            messages.append("It's a bit chilly in here. A comfortable temperature helps with focus!")
        
        if co2 > 1000:
            messages.append("The air is getting stuffy. Fresh air helps your brain work better!")
        
        if light == "dim":
            messages.append("The lighting is a bit dim. Good lighting reduces eye strain and helps you focus!")
        
        return " ".join(messages) if messages else "I'm here to support your study session!"
    
    @staticmethod
    def get_study_break_message(study_time: int, stress_level: int) -> str:
        """Generate study break recommendations."""
        if study_time > 180:  # 3 hours
            return "You've been studying for over 3 hours! Your brain needs a proper break. How about a 15-minute walk or some stretching?"
        elif study_time > 90:  # 1.5 hours
            return f"You've been focused for {study_time} minutes. Time for a 5-minute break? Stand up, stretch, maybe grab some water!"
        elif study_time > 45:  # 45 minutes
            return "You're in the zone! But remember, short breaks help you stay sharp. Want to take a quick stretch break?"
        
        return "You're just getting started! Remember to take breaks when you need them."
    
    @staticmethod
    def get_stress_management_message(stress_level: int, context: str = "") -> str:
        """Generate stress management support."""
        if stress_level > 8:
            return "I can tell you're really stressed. Let's take a deep breath together. Inhale for 4, hold for 4, exhale for 4. You've got this!"
        elif stress_level > 6:
            return "Stress is your body's way of preparing for a challenge. You're stronger than you think! Want to talk about what's on your mind?"
        elif stress_level > 4:
            return "A little stress is normal and can actually help you perform better. You're doing great!"
        
        return "You seem to be in a good headspace. Keep up the positive energy!"
    
    @staticmethod
    def get_motivation_message(achievement: str = "", study_time: int = 0) -> str:
        """Generate motivational messages."""
        if achievement:
            return f"{achievement}! You're making amazing progress!"
        elif study_time > 60:
            return f"You've been studying for {study_time} minutes. That's dedication! Your future self will thank you for this effort."
        else:
            return "Every minute of focused study is an investment in your future. You're building something amazing!"
    
    @staticmethod
    def get_environmental_comfort_message(environment: Dict[str, Any]) -> str:
        """Generate messages about environmental comfort for studying."""
        temp = environment.get('temperature', 0)
        co2 = environment.get('co2', 0)
        light = environment.get('brightness', 'Unknown')
        
        comfort_messages = []
        
        if 68 <= temp <= 72:
            comfort_messages.append("Perfect study temperature! Your brain loves this comfortable environment.")
        elif temp > 75:
            comfort_messages.append("It's getting warm in here. Comfortable temperature helps you focus better.")
        elif temp < 65:
            comfort_messages.append("A bit chilly! Warm up and your concentration will improve.")
        
        if co2 < 800:
            comfort_messages.append("Great air quality! Fresh air keeps your mind sharp.")
        elif co2 < 1000:
            comfort_messages.append("The air is getting a bit stuffy. Fresh air helps with concentration!")
        
        if light == "bright" or light == "moderate":
            comfort_messages.append("Good lighting! It's easier on your eyes and helps you stay alert.")
        elif light == "dim":
            comfort_messages.append("The lighting is a bit dim. Better lighting can help reduce eye strain.")
        
        return " ".join(comfort_messages) if comfort_messages else "Your study environment looks good!"
    
    @staticmethod
    def get_conversation_starter() -> str:
        """Generate conversation starters for the student companion."""
        starters = [
            "How's your study session going? I'm here if you need anything!",
            "What are you working on today? I'd love to hear about it!",
            "How are you feeling about your studies? I'm here to support you!",
            "Need a study buddy? I'm ready to help you stay focused and motivated!",
            "What's on your mind? Sometimes talking helps with problem-solving!"
        ]
        import random
        return random.choice(starters)
    
    @staticmethod
    def get_analysis_message(status: Dict[str, Any]) -> str:
        """Generate environmental analysis message."""
        if "error" in status:
            return "I can't analyze the environment right now."
        
        temp = status.get('temperature', 0)
        co2 = status.get('co2', 0)
        light_raw = status.get('light', 0)
        brightness = status.get('brightness', 'Unknown')
        
        analysis_parts = [f"My analysis shows temperature {temp}°F."]
        
        # Temperature analysis
        if temp < 60:
            analysis_parts.append("It's quite cold.")
        elif temp > 80:  # Changed from 86 to 80
            analysis_parts.append("It's quite warm.")
        else:
            analysis_parts.append("The temperature is comfortable.")
        
        # CO2 analysis
        if co2 > 1000:
            analysis_parts.append("CO2 levels are high, indicating poor ventilation.")
        elif co2 > 800:
            analysis_parts.append("CO2 levels are moderate.")
        else:
            analysis_parts.append("Air quality appears good.")
        
        # Brightness analysis
        brightness_analysis = MessageGenerators._analyze_brightness(brightness, light_raw)
        analysis_parts.append(brightness_analysis)
        
        return " ".join(analysis_parts)
    
    @staticmethod
    def get_temperature_message(status: Dict[str, Any]) -> str:
        """Generate temperature-specific message."""
        if "error" in status:
            return "I can't get the temperature right now."
        
        temp = status.get('temperature', 'N/A')
        message = f"I'm reading temperature {temp}°F."
        
        if temp != 'N/A':
            temp_num = float(temp)
            if temp_num < 60:
                message += " It's cold."
            elif temp_num > 80:
                message += " It's warm."
            else:
                message += " Temperature is comfortable."
        
        return message
    
    @staticmethod
    def get_co2_message(status: Dict[str, Any]) -> str:
        """Generate CO2-specific message."""
        if "error" in status:
            return "I can't get the CO2 level right now."
        
        co2 = status.get('co2', 'N/A')
        message = f"I'm reading CO2 level {co2}."
        
        if co2 != 'N/A':
            co2_num = int(co2)
            if co2_num > 1000:
                message += " Poor ventilation. Open windows or use a fan."
            elif co2_num > 800:
                message += " Air quality moderate."
            else:
                message += " Air quality good."
        
        return message
    
    @staticmethod
    def get_light_message(status: Dict[str, Any]) -> str:
        """Generate light-specific message."""
        if "error" in status:
            return "I can't get the light level right now."
        
        light_raw = status.get('light', 'N/A')
        brightness = status.get('brightness', 'Unknown')
        light_percent = status.get('light_percentage', 'N/A')
        
        if brightness != 'Unknown' and light_percent != 'N/A':
            light_message = f"I'm reading light level {light_raw} ({brightness}, {light_percent}% brightness)."
        else:
            light_message = f"I'm reading light level {light_raw}."
        
        # Add light-specific analysis
        brightness_analysis = MessageGenerators._analyze_brightness(brightness, light_raw)
        light_message += " " + brightness_analysis
        
        return light_message
    
    @staticmethod
    def get_recommendation_message(status: Dict[str, Any]) -> str:
        """Generate recommendation message."""
        if "error" in status:
            return "I can't provide recommendations right now."
        
        temp = status.get('temperature', 0)
        co2 = status.get('co2', 0)
        light_raw = status.get('light', 0)
        brightness = status.get('brightness', 'Unknown')
        led = status.get('led', 'OFF')
        
        recommendations = []
        
        # Temperature recommendations
        if temp < 60:
            recommendations.append("Increase temperature for comfort.")
        elif temp > 80:
            recommendations.append("Decrease temperature for comfort.")
        
        # CO2 recommendations
        if co2 > 1000:
            recommendations.append("Open windows or use a fan for ventilation.")
        elif co2 > 800:
            recommendations.append("Consider opening a window.")
        
        # Lighting recommendations
        led_recommendation = MessageGenerators._get_led_recommendation(brightness, light_raw, led)
        if led_recommendation:
            recommendations.append(led_recommendation)
        
        if recommendations:
            return "My recommendations: " + " ".join(recommendations)
        else:
            return "Environment is optimal. No recommendations needed."
    
    @staticmethod
    def get_emergency_message(status: Dict[str, Any]) -> str:
        """Generate emergency check message."""
        if "error" in status:
            return "I can't perform emergency check - sensors not responding!"
        
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
            return "EMERGENCY CHECK: " + " ".join(emergency_conditions)
        else:
            return "Emergency check complete. All systems normal."
    
    @staticmethod
    def get_change_alert(current_values: Dict[str, Any], last_values: Dict[str, Any], thresholds: Dict[str, int]) -> str:
        """Generate alert message for significant changes."""
        changes = []
        
        for key, threshold in thresholds.items():
            if key in current_values and key in last_values:
                current = float(current_values[key])
                last = float(last_values[key])
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
        elif temp > 80:
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
        """Get brightness warning message."""
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
    def _analyze_brightness(brightness: str, light_raw: int) -> str:
        """Analyze brightness using match statement."""
        if brightness != 'Unknown':
            match brightness:
                case 'Very Dark' | 'Dark':
                    return f"The lighting is {brightness.lower()}, you might need more light."
                case 'Very Bright':
                    return f"The lighting is {brightness.lower()}, it might be too bright."
                case _:
                    return f"The lighting is {brightness.lower()}, which is adequate."
        else:
            # Fallback to raw value analysis
            if light_raw < 100:
                return "The lighting is quite dim."
            elif light_raw > 800:
                return "The lighting is very bright."
            else:
                return "The lighting is adequate."
    
    @staticmethod
    def _get_led_recommendation(brightness: str, light_raw: int, led: str) -> str:
        """Get LED recommendation based on lighting conditions."""
        if brightness != 'Unknown':
            match brightness:
                case 'Very Dark' | 'Dark':
                    if led == 'OFF':
                        return "I'll turn on the LED for lighting."
                    else:
                        return "The LED is already on for lighting."
                case 'Very Bright':
                    if led == 'ON':
                        return "I'll turn off the LED - lighting is adequate."
                    else:
                        return "The LED is already off - lighting is adequate."
                case _:
                    if led == 'ON':
                        return "I'll turn off the LED - lighting is adequate."
                    else:
                        return "The LED is already off - lighting is adequate."
        else:
            # Fallback to raw value analysis
            if light_raw < 100:
                if led == 'OFF':
                    return "I'll turn on the LED for lighting."
                else:
                    return "The LED is already on for lighting."
            elif light_raw > 800:
                if led == 'ON':
                    return "I'll turn off the LED - lighting is adequate."
                else:
                    return "The LED is already off - lighting is adequate."
            else:
                if led == 'ON':
                    return "I'll turn off the LED - lighting is adequate."
                else:
                    return "The LED is already off - lighting is adequate."
        
        return "" 