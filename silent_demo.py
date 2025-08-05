#!/usr/bin/env python3
"""
Silent IRIS Demo - No Verbose Output
====================================

Runs the IRIS demo with ALL verbose output completely suppressed.
"""

import os
import sys
import time
import random
from datetime import datetime

# COMPLETE SUPPRESSION - Must be at the very top
import warnings
warnings.filterwarnings("ignore")

# Suppress all audio system messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['ALSA_DEBUG'] = '0'
os.environ['ALSA_VERBOSE'] = '0'
os.environ['PULSE_VERBOSE'] = '0'
os.environ['JACK_VERBOSE'] = '0'
os.environ['SPEECH_RECOGNITION_VERBOSE'] = '0'

# Redirect ALL output to suppress everything
import io
original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'examples'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'interfaces'))

class SilentDemoSimulator:
    """Silent simulator for demo."""
    
    def __init__(self):
        self.base_conditions = {
            'temperature': 72,
            'co2': 450,
            'light': 600,
            'led': 'OFF',
            'fan': 'OFF'
        }
    
    def get_simulated_status(self):
        """Return realistic simulated sensor data."""
        temp = self.base_conditions['temperature'] + random.uniform(-1, 1)
        co2 = self.base_conditions['co2'] + random.uniform(-20, 20)
        light = self.base_conditions['light'] + random.uniform(-50, 50)
        
        return {
            'temperature': round(temp, 1),
            'co2': int(co2),
            'light': int(light),
            'brightness': self._get_brightness_description(light),
            'led': self.base_conditions['led'],
            'fan': self.base_conditions['fan']
        }
    
    def _get_brightness_description(self, light_value):
        """Convert light value to brightness description."""
        if light_value < 200:
            return "Very Dark"
        elif light_value < 400:
            return "Dark"
        elif light_value < 600:
            return "Dim"
        elif light_value < 800:
            return "Moderate"
        else:
            return "Bright"
    
    def trigger_alert(self, alert_type):
        """Trigger a specific alert condition."""
        if alert_type == "high_temp":
            self.base_conditions['temperature'] = 82
        elif alert_type == "high_co2":
            self.base_conditions['co2'] = 1200
        elif alert_type == "low_light":
            self.base_conditions['light'] = 150
        elif alert_type == "normal":
            self.base_conditions = {
                'temperature': 72,
                'co2': 450,
                'light': 600,
                'led': 'OFF',
                'fan': 'OFF'
            }
    
    def take_action(self, action):
        """Simulate taking an action."""
        if action == "turn_on_fan":
            self.base_conditions['fan'] = 'ON'
            self.base_conditions['temperature'] = 75
        elif action == "turn_on_led":
            self.base_conditions['led'] = 'ON'
            self.base_conditions['light'] = 800
        elif action == "turn_off_fan":
            self.base_conditions['fan'] = 'OFF'
        elif action == "turn_off_led":
            self.base_conditions['led'] = 'OFF'
            self.base_conditions['light'] = 600

class SilentIRISDemo:
    """Completely silent IRIS demo."""
    
    def __init__(self):
        self.simulator = SilentDemoSimulator()
        self.monitoring_active = False
        self.alert_history = []
        self.use_real_system = False  # Always use simulation for silent demo
    
    def get_current_status(self):
        """Get current environmental status."""
        return self.simulator.get_simulated_status()
    
    def take_action(self, action):
        """Take an environmental action."""
        self.simulator.take_action(action)
        return True
    
    def speak(self, message):
        """Silent speak - just print."""
        print(f"IRIS: {message}")
    
    def chat(self, user_input):
        """Process user chat input."""
        return self._simulate_chat_response(user_input)
    
    def _simulate_chat_response(self, user_input):
        """Simulate chat responses for demo."""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["stressed", "worried", "anxious"]):
            return "I can sense you're feeling stressed. That's totally normal! Let's take a deep breath together. You've got this!"
        elif any(word in input_lower for word in ["tired", "exhausted"]):
            return "Your brain has been working hard! It's okay to feel tired - that means you're learning. How about a short break?"
        elif any(word in input_lower for word in ["break", "rest"]):
            return "Great idea! Taking breaks helps your brain process what you've learned. You deserve it!"
        elif any(word in input_lower for word in ["help", "stuck"]):
            return "I'm here to help! Sometimes talking through problems helps. What's on your mind?"
        elif any(word in input_lower for word in ["motivation", "encouragement"]):
            return "You're doing amazing! Every minute of focused study is an investment in your future. Keep going!"
        else:
            return "I'm here to support your study session! How can I help you today?"
    
    def check_for_alerts(self, status):
        """Check for alert conditions and take action."""
        alerts = []
        
        # Temperature alerts
        if status.get('temperature', 0) > 80:
            alerts.append({
                'type': 'high_temperature',
                'message': f"Temperature is {status['temperature']}°F - it's getting warm!",
                'action': 'turn_on_fan',
                'priority': 'high'
            })
        
        # CO2 alerts
        if status.get('co2', 0) > 1000:
            alerts.append({
                'type': 'high_co2',
                'message': f"CO2 level is {status['co2']} - air quality is poor!",
                'action': 'turn_on_fan',
                'priority': 'high'
            })
        
        # Lighting alerts
        if status.get('brightness', 'Unknown') in ['Very Dark', 'Dark']:
            alerts.append({
                'type': 'low_light',
                'message': f"Lighting is {status['brightness'].lower()} - need better lighting!",
                'action': 'turn_on_led',
                'priority': 'medium'
            })
        
        return alerts
    
    def run_continuous_monitoring(self, duration_minutes=5):
        """Run continuous monitoring demo."""
        print("\nStarting Continuous Monitoring Demo")
        print("=" * 50)
        print("IRIS will monitor your environment and take action when needed.")
        print("Press Ctrl+C to stop monitoring.")
        print("=" * 50)
        
        self.monitoring_active = True
        start_time = time.time()
        
        try:
            while self.monitoring_active:
                # Get current status
                status = self.get_current_status()
                
                # Check for alerts
                alerts = self.check_for_alerts(status)
                
                # Display current status
                print(f"\nCurrent Status ({datetime.now().strftime('%H:%M:%S')}):")
                print(f"   Temperature: {status.get('temperature', 'N/A')}°F")
                print(f"   CO2: {status.get('co2', 'N/A')}")
                print(f"   Light: {status.get('light', 'N/A')} ({status.get('brightness', 'N/A')})")
                print(f"   LED: {status.get('led', 'N/A')}")
                print(f"   Fan: {status.get('fan', 'N/A')}")
                
                # Handle alerts
                for alert in alerts:
                    print(f"\nALERT: {alert['message']}")
                    self.speak(alert['message'])
                    
                    # Take action
                    if self.take_action(alert['action']):
                        action_message = f"Taking action: {alert['action'].replace('_', ' ')}"
                        print(f"   {action_message}")
                        self.speak(f"I'm {action_message} to help you.")
                    
                    # Record alert
                    self.alert_history.append({
                        'timestamp': datetime.now(),
                        'alert': alert,
                        'action_taken': alert['action']
                    })
                
                # Wait before next check
                time.sleep(10)  # Check every 10 seconds
                
                # Check if demo time is up
                if time.time() - start_time > duration_minutes * 60:
                    print(f"\nDemo completed after {duration_minutes} minutes")
                    break
                    
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        
        self.monitoring_active = False
        self._show_demo_summary()
    
    def run_interactive_chat(self):
        """Run interactive chat demo."""
        print("\nInteractive Chat Demo")
        print("=" * 40)
        print("Talk to IRIS naturally! Try these examples:")
        print("• 'I'm stressed about my exam tomorrow'")
        print("• 'I've been studying for 2 hours, should I take a break?'")
        print("• 'The room feels stuffy, can you help?'")
        print("• 'I need some motivation'")
        print("• 'quit' - Exit chat")
        print("=" * 40)
        
        self.speak("Hello! I'm IRIS, your AI study companion. How can I help you today?")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'quit':
                    self.speak("Goodbye! Great job studying today!")
                    break
                
                if user_input:
                    # Get response
                    response = self.chat(user_input)
                    print(f"IRIS: {response}")
                    
                    # Also speak the response
                    self.speak(response)
                    
            except KeyboardInterrupt:
                print("\n\nChat ended. Thanks for talking with IRIS!")
                break
    
    def run_alert_demo(self):
        """Demo specific alert scenarios."""
        print("\nAlert Scenario Demo")
        print("=" * 40)
        print("This demo will trigger different alert conditions")
        print("to show how IRIS responds to problems.")
        print("=" * 40)
        
        scenarios = [
            ("High Temperature", "high_temp", "Temperature rises to 82°F"),
            ("High CO2", "high_co2", "CO2 levels rise to 1200"),
            ("Low Light", "low_light", "Lighting becomes very dark"),
            ("Return to Normal", "normal", "Conditions return to normal")
        ]
        
        for scenario_name, alert_type, description in scenarios:
            print(f"\nScenario: {scenario_name}")
            print(f"   {description}")
            input("   Press Enter to trigger this scenario...")
            
            # Trigger the scenario
            self.simulator.trigger_alert(alert_type)
            
            # Get status and check for alerts
            status = self.get_current_status()
            alerts = self.check_for_alerts(status)
            
            # Display status
            print(f"\nCurrent Status:")
            print(f"   Temperature: {status.get('temperature', 'N/A')}°F")
            print(f"   CO2: {status.get('co2', 'N/A')}")
            print(f"   Light: {status.get('light', 'N/A')} ({status.get('brightness', 'N/A')})")
            
            # Handle alerts
            for alert in alerts:
                print(f"\nALERT: {alert['message']}")
                self.speak(alert['message'])
                
                # Take action
                if self.take_action(alert['action']):
                    action_message = f"Taking action: {alert['action'].replace('_', ' ')}"
                    print(f"   {action_message}")
                    self.speak(f"I'm {action_message} to help you.")
            
            time.sleep(3)
        
        print("\nAlert scenario demo completed!")
    
    def _show_demo_summary(self):
        """Show summary of demo activities."""
        print("\nDemo Summary")
        print("=" * 30)
        
        if self.alert_history:
            print(f"Alerts triggered: {len(self.alert_history)}")
            for alert in self.alert_history:
                print(f"   • {alert['timestamp'].strftime('%H:%M:%S')}: {alert['alert']['message']}")
        else:
            print("No alerts triggered - conditions remained optimal")
        
        print("\nKey Features Demonstrated:")
        print("   • Continuous environmental monitoring")
        print("   • Proactive alert detection")
        print("   • Autonomous action taking")
        print("   • Natural conversation interface")
    
    def run_main_demo(self):
        """Run the main demo with all features."""
        print("IRIS Student Companion AI - Silent Demo")
        print("=" * 60)
        print("This demo showcases the real value of IRIS:")
        print("1. Continuous environmental monitoring")
        print("2. Proactive alerts when conditions are bad")
        print("3. Autonomous actions to solve problems")
        print("4. Natural conversation interface")
        print("=" * 60)
        
        while True:
            print("\nChoose demo mode:")
            print("1. Continuous Monitoring (5 minutes)")
            print("2. Interactive Chat")
            print("3. Alert Scenarios")
            print("4. Quick Demo (all features)")
            print("5. Exit")
            
            try:
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == "1":
                    self.run_continuous_monitoring()
                elif choice == "2":
                    self.run_interactive_chat()
                elif choice == "3":
                    self.run_alert_demo()
                elif choice == "4":
                    self.run_quick_demo()
                elif choice == "5":
                    print("Thanks for trying IRIS!")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nDemo ended. Thanks for trying IRIS!")
                break
    
    def run_quick_demo(self):
        """Run a quick demo of all features."""
        print("\nQuick Demo - All Features")
        print("=" * 40)
        
        # Start monitoring
        print("Starting monitoring...")
        status = self.get_current_status()
        print(f"Current conditions: {status['temperature']}°F, CO2: {status['co2']}, Light: {status['brightness']}")
        
        # Simulate an alert
        print("\nSimulating high temperature alert...")
        self.simulator.trigger_alert("high_temp")
        status = self.get_current_status()
        alerts = self.check_for_alerts(status)
        
        for alert in alerts:
            print(f"ALERT: {alert['message']}")
            self.speak(alert['message'])
            
            if self.take_action(alert['action']):
                print(f"Action taken: {alert['action']}")
                self.speak("I'm turning on the fan to help you stay comfortable.")
        
        # Show chat capability
        print("\nChat demonstration...")
        response = self.chat("I'm feeling a bit stressed")
        print(f"IRIS: {response}")
        
        print("\nQuick demo completed!")
        print("IRIS successfully demonstrated monitoring, alerts, actions, and chat!")

def main():
    """Main demo function."""
    try:
        # Restore stdout for demo output
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        demo = SilentIRISDemo()
        demo.run_main_demo()
    finally:
        # Restore original output
        sys.stdout = original_stdout
        sys.stderr = original_stderr

if __name__ == "__main__":
    main() 