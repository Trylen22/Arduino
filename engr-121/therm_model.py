import logging
from typing import List, Dict
from datetime import datetime

class ThermalModel:
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )
        
        # Temperature analysis prompts
        self.analysis_prompts = {
            'normal': [
                "Temperature is stable and within normal range.",
                "System is operating as expected.",
                "All parameters are nominal.",
                "Temperature control is effective."
            ],
            'warning_high': [
                "Temperature is approaching upper limit.",
                "Monitor system for further increases.",
                "Consider preventive cooling measures.",
                "Check for potential heat sources."
            ],
            'warning_low': [
                "Temperature is approaching lower limit.",
                "Monitor system for further decreases.",
                "Check heating system efficiency.",
                "Verify temperature sensor placement."
            ],
            'critical_high': [
                "ALERT: Temperature critically high!",
                "Immediate cooling required!",
                "Check for system malfunction.",
                "Emergency temperature reduction needed."
            ],
            'critical_low': [
                "ALERT: Temperature critically low!",
                "Immediate heating required!",
                "Check for system malfunction.",
                "Emergency temperature increase needed."
            ],
            'voltage_high': [
                "Arduino voltage above normal range.",
                "Check power supply stability.",
                "Monitor for potential overvoltage."
            ],
            'voltage_low': [
                "Arduino voltage below normal range.",
                "Check USB connection or power supply.",
                "Verify power source stability."
            ]
        }
        
        # System state tracking
        self.system_state = {
            'current_status': 'normal',
            'trend': 'stable',
            'last_readings': [],
            'alert_count': 0
        }
        
        # Analysis thresholds
        self.trend_threshold = 0.5  # °C change for trend detection
        self.max_readings = 10      # Number of readings to keep for trend analysis
        
        # Arduino system specifications
        self.arduino_specs = {
            'voltage': 5.0,          # Arduino operating voltage
            'analog_max': 1023,      # Maximum analog reading (10-bit)
            'analog_min': 0,         # Minimum analog reading
            'sample_rate': 5,        # Sampling rate in seconds
            'voltage_tolerance': 0.2  # Acceptable voltage variation (±0.2V)
        }
        
        # System boundaries
        self.system_limits = {
            'analog_ucl': 519,    # Upper Control Limit in analog
            'analog_lcl': 495,    # Lower Control Limit in analog
            'temp_ucl': 23.5,     # Upper Control Limit in Celsius
            'temp_lcl': 21.5,     # Lower Control Limit in Celsius
            'voltage_min': 4.8,   # Minimum acceptable voltage
            'voltage_max': 5.2    # Maximum acceptable voltage
        }
    
    def analyze_trend(self, readings: List[Dict]) -> str:
        """Analyze temperature trend from recent readings"""
        if len(readings) < 2:
            return 'stable'
        
        # Extract temperature values from the readings
        temps = [reading['temp_c'] for reading in readings]
        
        # Calculate average change and rate
        changes = [temps[i] - temps[i-1] for i in range(1, len(temps))]
        avg_change = sum(changes) / len(changes)
        rate_of_change = avg_change / (self.arduino_specs['sample_rate'] / 60)  # °C per minute
        
        if abs(avg_change) < self.trend_threshold:
            return 'stable'
        elif avg_change > 0:
            return f'rising ({rate_of_change:.1f}°C/min)'
        else:
            return f'falling ({abs(rate_of_change):.1f}°C/min)'
    
    def check_voltage_from_analog(self, analog_value: float) -> Dict:
        """Estimate system voltage from analog reading"""
        # For thermistor readings, we need to adjust the voltage calculation
        # The analog reading is inversely proportional to temperature
        # and we know we're operating on Arduino's 5V system
        reference_voltage = 5.0
        estimated_voltage = reference_voltage * (analog_value / self.arduino_specs['analog_max'])
        
        # Add some tolerance for normal operation
        status = {
            'voltage': reference_voltage,  # Report reference voltage instead of calculated
            'status': 'normal',
            'message': 'Voltage within normal range'
        }
        
        # Only report voltage issues if significantly out of range
        if estimated_voltage < (reference_voltage * 0.9):  # Below 90% of reference
            status.update({
                'status': 'voltage_low',
                'message': 'Warning: Check power supply or connections'
            })
        elif estimated_voltage > (reference_voltage * 1.1):  # Above 110% of reference
            status.update({
                'status': 'voltage_high',
                'message': 'Warning: Voltage above normal range'
            })
            
        return status
    
    def get_system_advice(self, temp_c: float, status: str, trend: str) -> Dict:
        """Generate system advice based on current conditions"""
        advice = {
            'message': '',
            'action_items': [],
            'priority': 'normal'
        }
        
        # Store the current temperature as a reading in the state (only once)
        self.system_state['last_readings'].append({'temp_c': temp_c})
        if len(self.system_state['last_readings']) > self.max_readings:
            self.system_state['last_readings'].pop(0)
        
        # Update system state
        self.system_state['current_status'] = status
        self.system_state['trend'] = trend
        
        # Generate appropriate message
        if status in self.analysis_prompts:
            advice['message'] = self.analysis_prompts[status][
                self.system_state['alert_count'] % len(self.analysis_prompts[status])
            ]
        
        # Add action items based on conditions
        if 'critical' in status:
            advice['priority'] = 'high'
            advice['action_items'] = [
                "Verify sensor readings",
                "Check system controls",
                "Document incident",
                "Alert system administrator"
            ]
            self.system_state['alert_count'] += 1
        elif 'warning' in status:
            advice['priority'] = 'medium'
            advice['action_items'] = [
                "Monitor system closely",
                "Prepare for intervention",
                "Review recent changes"
            ]
        
        # Add trend-specific advice
        if trend == 'rising' and ('high' in status):
            advice['action_items'].append("Investigate heat sources")
        elif trend == 'falling' and ('low' in status):
            advice['action_items'].append("Check insulation")
        
        # Add Arduino-specific checks
        if status in ['voltage_high', 'voltage_low']:
            advice['action_items'].extend([
                "Check Arduino power supply",
                "Verify USB connection",
                "Monitor system voltage"
            ])
            advice['priority'] = 'high'
        
        return advice
    
    def generate_report(self, temp_data: Dict) -> str:
        """Generate a detailed system report"""
        trend = self.analyze_trend(self.system_state['last_readings'])
        advice = self.get_system_advice(
            temp_data['temp_c'],
            temp_data['status'],
            trend
        )
        
        # Get voltage status
        voltage_status = self.check_voltage_from_analog(temp_data['analog'])
        
        # Generate concise report
        report = f"""
THERMAL SYSTEM STATUS ({datetime.now().strftime('%H:%M:%S')})
Temperature: {temp_data['temp_c']:.1f}°C ({temp_data['temp_f']:.1f}°F)
Status: {temp_data['status'].upper()}
Trend: {trend}"""

        # Always add recommendations for non-normal conditions
        if 'warning' in temp_data['status'] or 'critical' in temp_data['status']:
            report += f"\n\nRECOMMENDATIONS:"
            report += f"\n• {advice['message']}"
            if advice['action_items']:
                for item in advice['action_items'][:2]:  # Show top 2 action items
                    report += f"\n• {item}"
            report += f"\nPriority: {advice['priority'].upper()}"

        # Only add voltage info if there's an issue
        if voltage_status['status'] != 'normal':
            report += f"\n\nVOLTAGE ALERT: {voltage_status['message']}"

        # Add AI insights if available
        if 'ai_insights' in advice:
            report += f"\n\nAI ANALYSIS:"
            report += f"\n{advice['ai_insights']}"

        return report + "\n"
    
    def reset_state(self):
        """Reset system state tracking"""
        self.system_state = {
            'current_status': 'normal',
            'trend': 'stable',
            'last_readings': [],
            'alert_count': 0
        }
        logging.info("System state reset") 
    
    def validate_reading(self, analog_value: float, temp_c: float) -> bool:
        """Validate that readings are within expected ranges"""
        # Check analog value range
        if not (0 <= analog_value <= self.arduino_specs['analog_max']):
            logging.warning(f"Analog value {analog_value} outside valid range (0-{self.arduino_specs['analog_max']})")
            return False
        
        # Check temperature range (reasonable limits for room temperature monitoring)
        if not (0 <= temp_c <= 50):
            logging.warning(f"Temperature {temp_c}°C outside reasonable range (0-50°C)")
            return False
        
        # Check for sudden large changes (more than 5°C between readings)
        if self.system_state['last_readings']:
            last_temp = self.system_state['last_readings'][-1]['temp_c']
            if abs(temp_c - last_temp) > 5:
                logging.warning(f"Suspicious temperature change: {last_temp}°C to {temp_c}°C")
                return False
            
        return True
    
    def analyze_batch(self, readings: List[Dict]) -> str:
        """Analyze a batch of temperature readings and provide a summary"""
        if len(readings) < 2:
            return "Need more readings for analysis"
        
        # Extract temperatures and times
        temps = [r['temp_c'] for r in readings]
        times = [(r['timestamp'] - readings[0]['timestamp']).total_seconds() for r in readings]
        
        # Calculate statistics
        avg_temp = sum(temps) / len(temps)
        min_temp = min(temps)
        max_temp = max(temps)
        temp_range = max_temp - min_temp
        
        # Calculate rates
        rates = []
        for i in range(1, len(temps)):
            time_diff = (times[i] - times[i-1]) / 60  # Convert to minutes
            if time_diff > 0:
                rate = (temps[i] - temps[i-1]) / time_diff
                rates.append(rate)
        
        avg_rate = sum(rates) / len(rates) if rates else 0
        max_rate = max(abs(min(rates)), abs(max(rates))) if rates else 0
        
        # Determine overall trend
        if abs(avg_rate) < 0.1:
            trend = "stable"
        elif avg_rate > 0:
            trend = f"rising ({avg_rate:+.1f}°C/min)"
        else:
            trend = f"falling ({avg_rate:.1f}°C/min)"
        
        # Generate summary
        summary = f"""
THERMAL ANALYSIS REPORT
Time Period: {readings[0]['timestamp'].strftime('%H:%M:%S')} - {readings[-1]['timestamp'].strftime('%H:%M:%S')}
Readings: {len(readings)}

Current Status:
• Temperature: {temps[-1]:.1f}°C
• Trend: {trend}
• Rate: {rates[-1]:+.2f}°C/min (current)

Statistics:
• Average: {avg_temp:.1f}°C
• Range: {min_temp:.1f}°C to {max_temp:.1f}°C
• Variation: {temp_range:.1f}°C
• Max Rate: {max_rate:.1f}°C/min

System Health:"""
        
        # Add health assessment
        health_issues = []
        if temp_range > 5:
            health_issues.append("HIGH VARIABILITY - Temperature fluctuating significantly")
        if max_rate > 2:
            health_issues.append("RAPID CHANGES - Temperature changing too quickly")
        if min_temp < self.system_limits['temp_lcl']:
            health_issues.append("LOW TEMP - Below minimum threshold")
        if max_temp > self.system_limits['temp_ucl']:
            health_issues.append("HIGH TEMP - Above maximum threshold")
        
        if not health_issues:
            summary += "\n• System operating within normal parameters"
        else:
            for issue in health_issues:
                summary += f"\n• WARNING: {issue}"
        
        # Add action items
        summary += "\n\nRecommended Actions:"
        if not health_issues:
            summary += "\n• Continue normal monitoring"
        else:
            if "HIGH VARIABILITY" in str(health_issues):
                summary += "\n• Investigate source of temperature fluctuations"
            if "RAPID CHANGES" in str(health_issues):
                summary += "\n• Check environmental factors and system controls"
            if "LOW TEMP" in str(health_issues):
                summary += "\n• Verify heating system operation"
            if "HIGH TEMP" in str(health_issues):
                summary += "\n• Check cooling system and heat sources"
            summary += "\n• Document conditions and maintain close observation"
        
        return summary