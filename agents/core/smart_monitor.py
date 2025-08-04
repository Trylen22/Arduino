#!/usr/bin/env python3
"""
SmartMonitor - Intelligent Environmental Monitoring System
=======================================================

Provides intelligent monitoring capabilities with change detection,
emergency alerts, and smart speech frequency management.
"""

import time
from typing import Dict, Any
from datetime import datetime


class SmartMonitor:
    """Smart monitoring system with change detection and intelligent speech frequency."""
    
    def __init__(self):
        self.last_values = {}
        self.change_thresholds = {
            'temperature': 5,
            'co2': 200,
            'light': 100
        }
        self.speech_cooldown = 60  # seconds
        self.last_speech_time = 0
        self.summary_interval = 300  # 5 minutes
        self.last_summary_time = 0
        self.emergency_conditions = {
            'temperature': {'min': 50, 'max': 80},  # Changed from 95 to 80
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
        
        # Periodic summary
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
        """Log an action for tracking."""
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