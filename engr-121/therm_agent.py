import time
import logging
from typing import Dict, List
from datetime import datetime
from local_model import LocalModel
from Agentic_pipeline import AgentPipeline
import numpy as np

class ThermalAgent:
    def __init__(self):
        self.temperature_history: List[Dict] = []
        self.status_history: List[Dict] = []
        self.alert_thresholds = {
            'critical_high': 30.0,  # Critical high temperature
            'critical_low': 15.0,   # Critical low temperature
            'warning_high': 25.0,   # Warning high temperature
            'warning_low': 20.0     # Warning low temperature
        }
        
        # Initialize AI components
        self.ai = LocalModel()
        self.pipeline = AgentPipeline()
        
        # Add decision thresholds
        self.decision_thresholds = {
            'rapid_change': 2.0,     # °C per minute
            'stability_window': 0.5,  # °C variation for stability
            'response_delay': 5       # seconds between responses
        }
        
        self.last_decision_time = time.time()
        self.last_temperature = None
        self.last_status = None
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('thermal_monitor.log'),
                logging.StreamHandler()
            ]
        )
    
    def analyze_and_decide(self, analog: float, temp_c: float, temp_f: float, status: str) -> Dict:
        """Faster decision making"""
        # Initialize response structure
        response = {
            'reading': {
                'timestamp': datetime.now(),
                'analog': analog,
                'temp_c': temp_c,
                'temp_f': temp_f,
                'status': status
            },
            'analysis': self.analyze_temperature(temp_c),
            'ui_updates': {
                'color': self.get_color_recommendation(temp_c),
                'status_text': status,
                'status_color': 'red' if 'critical' in status else 
                              'yellow' if 'warning' in status else 'green'
            },
            'recommendations': []  # Initialize empty recommendations list
        }
        
        # Store reading in history
        self.temperature_history.append(response['reading'])
        
        # Determine if AI analysis is needed
        need_ai = (
            self.last_temperature is None or
            abs(temp_c - (self.last_temperature or temp_c)) > 1.0 or
            status != (self.last_status or status) or
            time.time() - self.last_decision_time > 10
        )
        
        if need_ai:
            try:
                # Update state
                self.last_decision_time = time.time()
                self.last_temperature = temp_c
                self.last_status = status
                
                # Get AI analysis
                context = f"""
                Current:
                - Temperature: {temp_c:.1f}°C ({temp_f:.1f}°F)
                - Status: {status}
                - Time: {datetime.now().strftime('%H:%M:%S')}
                
                Provide:
                1. Status assessment
                2. Key observation
                3. Recommendation
                """
                
                ai_response = self.ai.respond(context)
                if ai_response:
                    response['ai_insights'] = ai_response
                    # Extract recommendations from AI response
                    recommendations = []
                    for line in ai_response.split('\n'):
                        if 'recommend' in line.lower() or 'should' in line.lower():
                            recommendations.append(line.strip())
                    if recommendations:
                        response['recommendations'] = recommendations
                    else:
                        # Fallback recommendations based on status
                        response['recommendations'] = [
                            f"Monitor temperature trend at {temp_c:.1f}°C",
                            "Check system conditions",
                            "Continue regular monitoring"
                        ]
                
            except Exception as e:
                logging.warning(f"AI analysis failed: {e}")
                # Add fallback recommendations
                response['recommendations'] = [
                    "System monitoring active",
                    "Regular checks recommended",
                    "Maintain normal operations"
                ]
        
        return response
    
    def create_analysis_context(self, reading: Dict, rate_of_change: float) -> str:
        """Create context for AI analysis"""
        recent_temps = [r['temp_c'] for r in self.temperature_history[-5:]]
        stability = np.std(recent_temps) if len(recent_temps) > 1 else 0
        
        return f"""
        Current Reading:
        - Temperature: {reading['temp_c']:.1f}°C ({reading['temp_f']:.1f}°F)
        - Rate of Change: {rate_of_change:.2f}°C/min
        - Stability (σ): {stability:.2f}°C
        - Status: {reading['status']}
        
        Recent History: {recent_temps}
        
        System Limits:
        - Warning: {self.alert_thresholds['warning_low']}°C to {self.alert_thresholds['warning_high']}°C
        - Critical: {self.alert_thresholds['critical_low']}°C to {self.alert_thresholds['critical_high']}°C
        
        Analyze current conditions and provide specific recommendations.
        """
    
    def get_color_recommendation(self, temp_c: float) -> str:
        """Get recommended color for temperature visualization"""
        if temp_c < 0:
            return '#0000FF'  # Deep blue for very cold
        elif temp_c < 20:
            ratio = temp_c / 20
            blue = int(255 * (1 - ratio))
            return f'#00{blue:02x}FF'
        elif temp_c < 25:
            ratio = (temp_c - 20) / 20
            red = int(255 * ratio)
            return f'#{red:02x}00FF'
        else:
            return '#FF0000'  # Red for very hot
    
    def extract_recommendations(self, ai_response: str) -> List[str]:
        """Extract actionable recommendations from AI response"""
        # Simple extraction - could be made more sophisticated
        recommendations = []
        for line in ai_response.split('\n'):
            if any(word in line.lower() for word in ['should', 'recommend', 'consider', 'check', 'monitor']):
                recommendations.append(line.strip())
        return recommendations[:3]  # Return top 3 recommendations
    
    def analyze_temperature(self, temp_c: float) -> Dict:
        """Analyze temperature and determine alert level"""
        if temp_c >= self.alert_thresholds['critical_high']:
            return {
                'alert_level': 'critical_high',
                'message': 'Temperature critically high!',
                'action_needed': True
            }
        elif temp_c <= self.alert_thresholds['critical_low']:
            return {
                'alert_level': 'critical_low',
                'message': 'Temperature critically low!',
                'action_needed': True
            }
        elif temp_c >= self.alert_thresholds['warning_high']:
            return {
                'alert_level': 'warning_high',
                'message': 'Temperature approaching high limit',
                'action_needed': False
            }
        elif temp_c <= self.alert_thresholds['warning_low']:
            return {
                'alert_level': 'warning_low',
                'message': 'Temperature approaching low limit',
                'action_needed': False
            }
        else:
            return {
                'alert_level': 'normal',
                'message': 'Temperature within normal range',
                'action_needed': False
            }
    
    def get_statistics(self) -> Dict:
        """Calculate statistics from temperature history"""
        if not self.temperature_history:
            return {}
        
        temps = [r['temp_c'] for r in self.temperature_history]
        return {
            'current': temps[-1],
            'min': min(temps),
            'max': max(temps),
            'avg': sum(temps) / len(temps),
            'readings_count': len(temps)
        }
    
    def clear_history(self):
        """Clear temperature history"""
        self.temperature_history = []
        self.status_history = []
        logging.info("Temperature history cleared")
    
    def generate_diagnostic_report(self) -> str:
        """Generate a comprehensive diagnostic report after 50 readings"""
        if len(self.temperature_history) < 50:
            return "Insufficient data for diagnostic report (need 50 readings)"
        
        # Get statistics
        stats = self.get_statistics()
        
        # Calculate temperature stability
        temp_std_dev = np.std([r['temp_c'] for r in self.temperature_history])
        
        # Count alerts by type
        alert_counts = {}
        for reading in self.temperature_history:
            alert = self.analyze_temperature(reading['temp_c'])['alert_level']
            alert_counts[alert] = alert_counts.get(alert, 0) + 1
        
        # Create context for AI analysis
        context = f"""
        System Diagnostic Report (50 readings):
        
        Temperature Statistics:
        - Average: {stats['avg']:.1f}°C
        - Range: {stats['min']:.1f}°C to {stats['max']:.1f}°C
        - Stability (std dev): {temp_std_dev:.2f}°C
        
        Alert Distribution:
        {alert_counts}
        
        System Limits:
        - Warning Range: {self.alert_thresholds['warning_low']}°C to {self.alert_thresholds['warning_high']}°C
        - Critical Range: {self.alert_thresholds['critical_low']}°C to {self.alert_thresholds['critical_high']}°C
        
        Full Temperature History:
        {[(r['timestamp'].strftime('%H:%M:%S'), r['temp_c']) for r in self.temperature_history]}
        
        Analyze this data and provide:
        1. Overall system health assessment
        2. Identified patterns or anomalies
        3. Stability analysis
        4. Recommendations for improvement
        5. Maintenance suggestions
        """
        
        # Set diagnostic mode for detailed analysis
        self.ai.set_mode('diagnostic')
        
        # Get AI analysis
        diagnostic_insights = "".join(self.ai.respond(context))
        
        # Log the diagnostic report
        self.pipeline.execute_action(
            'log_event',
            event_type="DIAGNOSTIC",
            details=f"50-reading diagnostic report generated"
        )
        
        return diagnostic_insights