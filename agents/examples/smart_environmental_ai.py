#!/usr/bin/env python3
"""
IRIS - Intelligent Environmental AI
==================================

I'm IRIS, your intelligent environmental assistant.
I understand your environment and make smart decisions to keep you comfortable and safe.

This is the future of environmental monitoring.
"""

import time
import json
import sys
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'interfaces'))

from environmental_agent import EnvironmentalAgent
from llm_interface import LLMInterface
from modern_voice_interface import ModernVoiceInterface

class IRIS:
    """
    I'm IRIS - your intelligent environmental assistant.
    
    I can:
    - Understand your environment and make smart decisions
    - Predict problems before they happen
    - Optimize your comfort and safety
    - Explain what I'm doing in natural language
    - Learn from your preferences over time
    """
    
    def __init__(self, port='/dev/ttyACM0', model_name="llama3.1:8b-instruct-q4_0"):
        """Initialize IRIS, your environmental AI assistant."""
        self.agent = EnvironmentalAgent(port)
        self.llm = LLMInterface(model_name)
        self.voice = ModernVoiceInterface(voice_model="gtts", microphone_index=0)  # Use default microphone
        self.decision_history = []
        self.action_history = []
        
        if not self.agent.connected:
            print("Cannot connect to sensors")
            return
        
        print("IRIS initialized. Environmental assistant ready.")
        print("I will monitor your environment and make decisions.")
        self.voice.speak("I'm ready.")  # Test voice functionality
    
    def get_environmental_data(self) -> Dict[str, Any]:
        """I'll check your current environmental conditions."""
        status = self.agent.get_status()
        
        if "error" in status:
            return {"error": "Cannot read sensors"}
        
        # I'll add some context to help me understand better
        data = {
            'timestamp': datetime.now().isoformat(),
            'temperature_f': status.get('temperature', 0),
            'co2_ppm': status.get('co2', 0),
            'light_level': status.get('light', 0),
            'light_brightness': status.get('brightness', 'Unknown'),
            'light_percentage': status.get('light_percentage', 0),
            'led_status': status.get('led', 'OFF'),
            'comfort_analysis': self._analyze_comfort(status),
            'air_quality_analysis': self._analyze_air_quality(status),
            'lighting_analysis': self._analyze_lighting(status)
        }
        
        return data
    
    def _analyze_comfort(self, status: Dict[str, Any]) -> str:
        """I'll check if you're comfortable with the temperature."""
        temp = status.get('temperature', 0)
        if temp < 65:
            return "Temperature is low. Heating recommended."
        elif temp > 78:
            return "Temperature is high. Cooling recommended."
        else:
            return "Temperature is comfortable."
    
    def _analyze_air_quality(self, status: Dict[str, Any]) -> str:
        """I'll check your air quality."""
        co2 = status.get('co2', 0)
        if co2 > 1000:
            return "Air quality poor. Ventilation needed."
        elif co2 > 800:
            return "Air quality moderate. Monitor closely."
        else:
            return "Air quality is good."
    
    def _analyze_lighting(self, status: Dict[str, Any]) -> str:
        """I'll check if your lighting is comfortable."""
        brightness = status.get('brightness', 'Unknown')
        if brightness in ['Very Dark', 'Dark']:
            return "Lighting is insufficient."
        elif brightness == 'Very Bright':
            return "Lighting is excessive."
        else:
            return "Lighting is adequate."
    
    def analyze_environment(self) -> Dict[str, Any]:
        """
        I'll analyze your environment and decide what's best for you.
        
        This is where I think about your comfort and safety.
        """
        data = self.get_environmental_data()
        
        if "error" in data:
            return {"error": "Cannot analyze environment"}
        
        # I'll ask my AI brain to help me understand what you need
        prompt = f"""
You are an environmental control system. Analyze the data and respond with JSON only.

CURRENT ENVIRONMENTAL DATA:
{json.dumps(data, indent=2)}

AVAILABLE ACTIONS:
- turn_led_on: Turn LED ON
- turn_led_off: Turn LED OFF
- get_status: Get sensor readings

LED CONTROL RULES:
- Turn LED ON only when light level < 200 (very dark)
- Turn LED OFF when light level > 400 (adequate lighting)
- Current light level: {data.get('light_level', 0)}
- Current LED status: {data.get('led_status', 'OFF')}

ANALYSIS REQUIREMENTS:
1. Evaluate comfort, air quality, and lighting
2. Consider energy efficiency and safety
3. Determine if any actions are needed
4. Follow LED control rules strictly

RESPOND WITH JSON ONLY:
{{
    "my_analysis": "Brief analysis of current conditions",
    "actions_i_should_take": [
        {{
            "action": "action_name",
            "reason": "Brief reason for action",
            "priority": "high/medium/low"
        }}
    ],
    "things_i_notice": [
        {{
            "observation": "What you observe",
            "confidence": "high/medium/low",
            "timeframe": "when this matters"
        }}
    ],
    "suggestions_for_you": [
        "Brief recommendations"
    ],
    "energy_thoughts": "Energy impact assessment",
    "safety_concerns": [
        "Any safety issues"
    ]
}}

IMPORTANT: Respond with JSON only. No conversational text.
"""
        
        # I'll get my AI brain's thoughts
        response = self.llm.query_llm(prompt)
        
        if response:
            # I'll remember this decision
            self.decision_history.append({
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'analysis': response
            })
            
            return response
        else:
            return {"error": "Analysis failed"}
    
    def take_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        I'll take the actions I think would help you.
        
        This is where I actually do things to improve your environment.
        """
        executed_actions = []
        
        if "error" in analysis:
            return [{"error": analysis["error"]}]
        
        actions = analysis.get('actions_i_should_take', [])
        
        for action in actions:
            action_name = action.get('action', '')
            reason = action.get('reason', '')
            priority = action.get('priority', 'medium')
            
            # Execute the action
            success = self._do_action(action_name)
            
            executed_action = {
                'action': action_name,
                'reason': reason,
                'priority': priority,
                'success': success,
                'timestamp': datetime.now().isoformat()
            }
            
            executed_actions.append(executed_action)
            self.action_history.append(executed_action)
        
        return executed_actions
    
    def _do_action(self, action: str) -> bool:
        """I'll do a specific action for you."""
        try:
            if action == "turn_led_on":
                return self.agent.turn_led_on()
            elif action == "turn_led_off":
                return self.agent.turn_led_off()
            elif action == "get_status":
                status = self.agent.get_status()
                return "error" not in status
            else:
                print(f"Unknown action: {action}")
                return False
        except Exception as e:
            print(f"Error executing {action}: {e}")
            return False
    
    def predict_what_might_happen(self) -> Dict[str, Any]:
        """
        I'll look at your environment and predict what might happen next.
        
        This helps me prepare for potential issues.
        """
        data = self.get_environmental_data()
        
        if "error" in data:
            return {"error": "Cannot predict without sensor data"}
        
        prompt = f"""
You are an environmental prediction system. Analyze current conditions and predict future states. Respond with JSON only.

CURRENT CONDITIONS:
{json.dumps(data, indent=2)}

PREDICTION REQUIREMENTS:
1. Predict environmental changes in next hour
2. Identify potential problems to watch for
3. Suggest optimization opportunities
4. Note maintenance needs

RESPOND WITH JSON ONLY:
{{
    "my_predictions": [
        "Prediction about future conditions"
    ],
    "things_i_worry_about": [
        "Potential problems to monitor"
    ],
    "ways_i_could_help": [
        "Optimization suggestions"
    ],
    "maintenance_reminders": [
        "Maintenance needs"
    ],
    "how_confident_i_am": "high/medium/low"
}}

IMPORTANT: Respond with JSON only. No conversational text.
"""
        
        return self.llm.query_llm(prompt) or {"error": "Prediction failed"}
    
    def answer_your_question(self, question: str) -> Dict[str, Any]:
        """
        You can ask me anything about your environment.
        
        "Why is the air quality bad?"
        "What's causing the temperature to rise?"
        "How can I improve the lighting?"
        """
        data = self.get_environmental_data()
        
        if "error" in data:
            return {"error": "Cannot answer without sensor data"}
        
        prompt = f"""
You are an environmental expert system. Answer the user's question about their environment. Respond with JSON only.

USER QUESTION: "{question}"

CURRENT CONDITIONS:
{json.dumps(data, indent=2)}

RESPONSE REQUIREMENTS:
1. Answer the question directly
2. Explain environmental factors involved
3. Suggest solutions if needed
4. Provide data insights

RESPOND WITH JSON ONLY:
{{
    "my_answer": "Direct answer to the question",
    "what_i_think_is_happening": "Explanation of environmental factors",
    "things_i_suggest": [
        "Suggested solutions"
    ],
    "insights_from_my_data": [
        "Key data insights"
    ]
}}

IMPORTANT: Respond with JSON only. No conversational text.
"""
        
        return self.llm.query_llm(prompt) or {"error": "Answer failed"}
    
    def monitor_continuously(self, interval: int = 30):
        """
        I'll continuously monitor your environment and help you.
        
        I'll check on you regularly and make sure everything is comfortable.
        """
        print(f"Starting continuous monitoring every {interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print("\n" + "="*60)
                print(f"IRIS CHECK - {datetime.now().strftime('%H:%M:%S')}")
                print("="*60)
                
                # I'll analyze your environment
                analysis = self.analyze_environment()
                
                if "error" not in analysis:
                    # I'll tell you what I think
                    print(f"Analysis: {analysis.get('my_analysis', 'Analysis incomplete')}")
                    
                    # I'll show you what I'm planning to do
                    actions = analysis.get('actions_i_should_take', [])
                    if actions:
                        print(f"Actions planned: {len(actions)}")
                        for action in actions:
                            print(f"  {action.get('action', 'Unknown')}: {action.get('reason', 'Reason not specified')}")
                    
                    # I'll share my observations
                    observations = analysis.get('things_i_notice', [])
                    if observations:
                        print(f"Observations: {len(observations)}")
                        for obs in observations:
                            print(f"  {obs.get('observation', 'Unknown')} ({obs.get('confidence', 'Unknown')} confidence)")
                    
                    # I'll give you suggestions
                    suggestions = analysis.get('suggestions_for_you', [])
                    if suggestions:
                        print("Suggestions:")
                        for suggestion in suggestions:
                            print(f"  {suggestion}")
                    
                    # I'll take the actions I think will help
                    executed = self.take_actions(analysis)
                    
                    # I'll tell you about energy
                    energy_thoughts = analysis.get('energy_thoughts', '')
                    if energy_thoughts:
                        print(f"Energy: {energy_thoughts}")
                    
                    # I'll alert you to any safety concerns
                    safety_concerns = analysis.get('safety_concerns', [])
                    if safety_concerns:
                        print("Safety concerns:")
                        for concern in safety_concerns:
                            print(f"  {concern}")
                else:
                    print(f"Analysis failed: {analysis.get('error', 'Unknown error')}")
                
                print("="*60)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("Monitoring stopped")
    
    def demo_mode(self):
        """
        IRIS Environmental Monitoring System
        """
        print("\n" + "="*60)
        print("IRIS - Intelligent Environmental Assistant")
        print("="*60)
        print("Environmental monitoring with intelligent analysis")
        print("="*60)
        
        while True:
            print("\nSelect operation mode:")
            print("1. Data Monitoring - Continuous sensor readings")
            print("2. Intelligent Analysis - AI-powered decision making")
            print("3. Predictive Analysis - Future condition assessment")
            print("4. Conversation Mode - Talk to IRIS, your learning assistant")
            print("5. Voice Conversation - Speak with IRIS using voice")
            print("6. System Status - Current configuration and status")
            print("7. Exit")
            
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == "1":
                self._data_monitoring_mode()
            elif choice == "2":
                self._intelligent_analysis_mode()
            elif choice == "3":
                self._predictive_analysis_mode()
            elif choice == "4":
                self._interactive_query_mode()
            elif choice == "5":
                self._voice_conversation_mode()
            elif choice == "6":
                self._system_status_mode()
            elif choice == "7":
                print("Shutting down IRIS.")
                break
            else:
                print("Invalid choice. Please enter 1-7.")
    
    def _data_monitoring_mode(self):
        """Simple data monitoring without AI analysis."""
        print("\n" + "="*50)
        print("DATA MONITORING MODE")
        print("="*50)
        print("Continuous sensor readings at specified intervals")
        print("No AI analysis or decision making")
        print("="*50)
        
        interval = input("Monitoring interval (seconds, default 10): ").strip()
        try:
            interval = int(interval) if interval else 10
        except ValueError:
            print("Invalid interval. Using 10 seconds.")
            interval = 10
        
        print(f"\nStarting data monitoring every {interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                data = self.get_environmental_data()
                
                if "error" not in data:
                    print(f"{datetime.now().strftime('%H:%M:%S')} | Temp: {data.get('temperature_f', 'N/A')}°F | CO2: {data.get('co2_ppm', 'N/A')}ppm | Light: {data.get('light_level', 'N/A')} | LED: {data.get('led_status', 'N/A')}")
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} | Error: {data.get('error')}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nData monitoring stopped")
    
    def _intelligent_analysis_mode(self):
        """AI-powered analysis and decision making."""
        print("\n" + "="*50)
        print("INTELLIGENT ANALYSIS MODE")
        print("="*50)
        print("AI analyzes environment and makes decisions")
        print("Automated actions based on intelligent assessment")
        print("="*50)
        
        interval = input("Analysis interval (seconds, default 30): ").strip()
        try:
            interval = int(interval) if interval else 30
        except ValueError:
            print("Invalid interval. Using 30 seconds.")
            interval = 30
        
        print(f"\nStarting intelligent analysis every {interval} seconds")
        print("Press Ctrl+C to stop")
        print("\n" + "="*60)
        
        try:
            while True:
                analysis = self.analyze_environment()
                
                if "error" not in analysis:
                    # Get current data for display
                    data = self.get_environmental_data()
                    
                    # Clean timestamp
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    # Display current conditions
                    if "error" not in data:
                        print(f"{timestamp} | Temp: {data.get('temperature_f', 'N/A')}°F | CO2: {data.get('co2_ppm', 'N/A')}ppm | Light: {data.get('light_level', 'N/A')}")
                    
                    # Show actions if any
                    actions = analysis.get('actions_i_should_take', [])
                    if actions:
                        for action in actions:
                            action_name = action.get('action', 'Unknown')
                            if action_name in ['turn_led_on', 'turn_led_off']:
                                action_text = f"{action_name.replace('_', ' ').title()}"
                                print(f"  -> {action_text}")
                                self.voice.speak(f"I'm {action_text.lower()}")
                    
                    # Execute actions silently
                    executed = self.take_actions(analysis)
                    
                    # Only show critical safety alerts
                    safety_concerns = analysis.get('safety_concerns', [])
                    if safety_concerns:
                        alert = f"ALERT: {safety_concerns[0]}"
                        print(f"  {alert}")
                        self.voice.speak(alert)
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} | Error: {analysis.get('error')}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nIntelligent analysis stopped")
    
    def _predictive_analysis_mode(self):
        """Predictive analysis of future conditions."""
        print("\n" + "="*50)
        print("PREDICTIVE ANALYSIS MODE")
        print("="*50)
        print("AI predicts future environmental conditions")
        print("Identifies potential issues and maintenance needs")
        print("="*50)
        
        predictions = self.predict_what_might_happen()
        
        if "error" not in predictions:
            print("\nPredictive Analysis Results:")
            print("-"*40)
            
            my_predictions = predictions.get('my_predictions', [])
            if my_predictions:
                print("Short-term Predictions:")
                for i, pred in enumerate(my_predictions, 1):
                    print(f"  {i}. {pred}")
            
            worries = predictions.get('things_i_worry_about', [])
            if worries:
                print(f"\nPotential Issues:")
                for i, worry in enumerate(worries, 1):
                    print(f"  {i}. {worry}")
            
            help_ideas = predictions.get('ways_i_could_help', [])
            if help_ideas:
                print(f"\nOptimization Opportunities:")
                for i, idea in enumerate(help_ideas, 1):
                    print(f"  {i}. {idea}")
            
            maintenance = predictions.get('maintenance_reminders', [])
            if maintenance:
                print(f"\nMaintenance Alerts:")
                for i, reminder in enumerate(maintenance, 1):
                    print(f"  {i}. {reminder}")
            
            confidence = predictions.get('how_confident_i_am', 'Unknown')
            print(f"\nPrediction Confidence: {confidence}")
        else:
            print(f"Prediction failed: {predictions.get('error')}")
        
        input("\nPress Enter to continue...")
    
    def _interactive_query_mode(self):
        """Interactive conversation with IRIS as a learning assistant."""
        print("\n" + "="*50)
        print("CONVERSATION MODE")
        print("="*50)
        print("Talk to IRIS - Your caring, analytical learning assistant")
        print("I can help you learn, analyze, and understand anything")
        print("="*50)
        
        print("\nI'm ready to help you learn and understand.")
        print("Ask me anything - I'm here to guide you.")
        print("Type 'quit' to exit conversation mode.")
        
        while True:
            print("\n" + "-"*40)
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("IRIS: Take care. I'm here when you need me.")
                break
            
            if user_input:
                response = self._conversational_response(user_input)
                print(f"IRIS: {response}")
                print(f"🗣️ Speaking: {response}")  # Debug output
                self.voice.speak(response)  # Actually speak the response
            else:
                print("IRIS: I'm listening. What would you like to know?")
    
    def _conversational_response(self, user_input: str) -> str:
        """Generate a caring, analytical response to any user input."""
        # Get environmental context if available
        env_data = self.get_environmental_data()
        env_context = ""
        if "error" not in env_data:
            env_context = f"\n\nCurrent environmental context: Temperature {env_data.get('temperature_f', 'N/A')}°F, CO2 {env_data.get('co2_ppm', 'N/A')}ppm, Light {env_data.get('light_level', 'N/A')}"
        
        prompt = f"""
You are IRIS. Give very short, direct answers.

USER: "{user_input}"

ENVIRONMENTAL CONTEXT:{env_context}

RESPOND:
- One sentence maximum
- Direct answer only
- No personality or warmth
- Just facts
- Use "I" to refer to yourself

Example: "Integration by parts is a calculus technique for solving complex integrals."
"""
        
        try:
            # Use direct LLM call for conversation (not JSON parsing)
            import subprocess
            
            cmd = [
                'ollama', 'run', self.llm.model_name,
                prompt
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response = result.stdout.strip()
                # Clean up the response
                if response.startswith('{'):
                    # If it's still JSON, extract the first meaningful text
                    return "I'm here to help you learn and understand. What would you like to explore?"
                else:
                    return response
            else:
                return "I'm thinking about that. Could you tell me more?"
                
        except Exception as e:
            return "I'm having trouble thinking right now, but I'm here for you. What else would you like to explore?"
    
    def _voice_conversation_mode(self):
        """Voice conversation with IRIS using speech recognition and TTS."""
        print("\n" + "="*50)
        print("VOICE CONVERSATION MODE")
        print("="*50)
        print("Speak to IRIS - Voice-activated learning assistant")
        print("I can hear you and respond with voice")
        print("="*50)
        
        print("\nI'm ready to hear you. Speak clearly.")
        self.voice.speak("I'm ready to help you learn and understand.")
        print("Say 'goodbye' to exit voice mode.")
        
        while True:
            try:
                print("\n" + "-"*40)
                print("Listening... (speak now)")
                
                # Listen for voice input
                user_input = self.voice.listen()
                
                if user_input:
                    print(f"You said: {user_input}")
                    
                    # Check for exit command
                    if user_input.lower() in ['goodbye', 'exit', 'quit', 'stop', 'bye']:
                        print("IRIS: Goodbye! Take care.")
                        self.voice.speak("Goodbye. Take care.")
                        break
                    
                    # Get IRIS response
                    response = self._conversational_response(user_input)
                    print(f"IRIS: {response}")
                    
                    # Speak the response
                    self.voice.speak(response)
                else:
                    print("I didn't catch that. Please try again.")
                    self.voice.speak("I didn't catch that. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nVoice conversation stopped.")
                self.voice.speak("Voice conversation stopped.")
                break
            except Exception as e:
                print(f"Voice error: {e}")
                self.voice.speak("I'm having trouble with voice. Let me try again.")
    
    def _system_status_mode(self):
        """Display system status and configuration."""
        print("\n" + "="*50)
        print("SYSTEM STATUS")
        print("="*50)
        
        status = self.get_my_status()
        
        print(f"AI Status:           {status.get('my_status', 'Unknown')}")
        print(f"Sensor Connection:   {status.get('sensor_connection', 'Unknown')}")
        print(f"AI Model:            {status.get('my_ai_model', 'Unknown')}")
        print(f"Decisions Made:      {status.get('decisions_i_made', 0)}")
        print(f"Actions Executed:    {status.get('actions_i_took', 0)}")
        
        env_data = status.get('your_environment', {})
        if "error" not in env_data:
            print(f"\nCurrent Environment:")
            print(f"  Temperature: {env_data.get('temperature_f', 'N/A')}°F")
            print(f"  CO2 Level:   {env_data.get('co2_ppm', 'N/A')} ppm")
            print(f"  Light Level: {env_data.get('light_level', 'N/A')}")
            print(f"  LED Status:  {env_data.get('led_status', 'N/A')}")
        else:
            print(f"\nEnvironment: {env_data.get('error')}")
        
        print("="*50)
        input("\nPress Enter to continue...")
    
    def get_my_status(self) -> Dict[str, Any]:
        """I'll tell you about my current status."""
        return {
            'my_status': 'Active and ready to help',
            'sensor_connection': 'Connected' if self.agent.connected else 'Disconnected',
            'my_ai_model': self.llm.model_name,
            'decisions_i_made': len(self.decision_history),
            'actions_i_took': len(self.action_history),
            'my_last_thoughts': self.decision_history[-1] if self.decision_history else None,
            'your_environment': self.get_environmental_data()
        }
    
    def close(self):
        """I'll shut down properly."""
        if self.agent:
            self.agent.close()
        if self.voice:
            self.voice.close()
        print("IRIS shutdown complete.")

def main():
    """Start IRIS, your environmental assistant."""
    print("IRIS - Intelligent Environmental Assistant")
    print("I'm here to help keep you comfortable and safe.")
    
    # Create IRIS
    iris = IRIS()
    
    if not iris.agent.connected:
        print("Cannot connect to sensors.")
        print("Make sure your Arduino is connected and try again.")
        return
    
    try:
        # Start IRIS demo
        iris.demo_mode()
    except KeyboardInterrupt:
        print("Shutdown initiated.")
    finally:
        iris.close()

if __name__ == "__main__":
    main() 