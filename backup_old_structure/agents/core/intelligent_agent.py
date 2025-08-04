#!/usr/bin/env python3
"""
Intelligent Environmental Monitoring Agent
========================================

LLM-powered agent that analyzes sensor data and makes intelligent decisions
for environmental monitoring and control.

Author: [Your Name]
Date: [2025-01-27]
"""

import serial
import time
import json
import subprocess
from typing import Dict, Any, Optional, List
from environmental_agent import EnvironmentalAgent

class IntelligentEnvironmentalAgent:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, model_name="llama3.1:8b-instruct-q4_0"):
        """Initialize the intelligent environmental monitoring agent."""
        self.model_name = model_name
        self.agent = EnvironmentalAgent(port, baud_rate)
        self.decision_history = []
        
        if not self.agent.connected:
            print("❌ Cannot initialize without Arduino connection")
            return
        
        print("🤖 Intelligent Environmental Agent Ready!")
        print("I can analyze sensor data and make automated decisions.")
    
    def get_environmental_status(self) -> Dict[str, Any]:
        """Get current environmental status with analysis."""
        status = self.agent.get_status()
        
        if "error" in status:
            return status
        
        # Add environmental analysis
        analysis = self._analyze_environment(status)
        status["analysis"] = analysis
        
        return status
    
    def _analyze_environment(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze environmental conditions and provide recommendations."""
        analysis = {
            "overall_health": "unknown",
            "temperature_status": "unknown",
            "air_quality_status": "unknown",
            "lighting_status": "unknown",
            "recommendations": [],
            "alerts": []
        }
        
        # Temperature analysis (using Fahrenheit)
        temp = status.get("temperature", 0)
        if temp < 60:  # Below 60°F
            analysis["temperature_status"] = "cold"
            analysis["alerts"].append("Temperature is too cold")
        elif temp > 86:  # Above 86°F
            analysis["temperature_status"] = "hot"
            analysis["alerts"].append("Temperature is too hot")
        else:
            analysis["temperature_status"] = "comfortable"
        
        # CO2 analysis (note: still warming up)
        co2 = status.get("co2", 0)
        if co2 > 1000:
            analysis["air_quality_status"] = "poor"
            analysis["alerts"].append("CO2 levels are high - poor ventilation")
        elif co2 > 800:
            analysis["air_quality_status"] = "moderate"
            analysis["recommendations"].append("Consider improving ventilation")
        else:
            analysis["air_quality_status"] = "good"
        
        # Light analysis
        light = status.get("light", 0)
        if light < 100:
            analysis["lighting_status"] = "dark"
            analysis["recommendations"].append("Consider turning on lights")
        elif light > 800:
            analysis["lighting_status"] = "bright"
        else:
            analysis["lighting_status"] = "adequate"
        
        # Overall health assessment
        if len(analysis["alerts"]) == 0:
            analysis["overall_health"] = "good"
        elif len(analysis["alerts"]) <= 2:
            analysis["overall_health"] = "moderate"
        else:
            analysis["overall_health"] = "poor"
        
        return analysis
    
    def make_intelligent_decision(self, user_query: str = "") -> Dict[str, Any]:
        """Make an intelligent decision based on current environmental data."""
        status = self.get_environmental_status()
        
        if "error" in status:
            return {"error": "Cannot make decision without sensor data"}
        
        # Create prompt for LLM
        prompt = self._create_decision_prompt(status, user_query)
        
        # Get LLM response
        decision = self._query_llm(prompt)
        
        # Execute any actions
        actions_taken = self._execute_actions(decision, status)
        
        return {
            "status": status,
            "decision": decision,
            "actions_taken": actions_taken,
            "timestamp": time.time()
        }
    
    def _create_decision_prompt(self, status: Dict[str, Any], user_query: str) -> str:
        """Create a prompt for the LLM decision making."""
        prompt = f"""
You are an intelligent environmental monitoring system. Analyze the current environmental data and provide recommendations.

Current Environmental Data:
- Temperature: {status.get('temperature', 'N/A')}°F
- CO2 Level: {status.get('co2', 'N/A')} (raw value, sensor warming up)
- Light Level: {status.get('light', 'N/A')} (raw value)
- LED Status: {status.get('led', 'N/A')}

Environmental Analysis:
{json.dumps(status.get('analysis', {}), indent=2)}

Available Actions:
- Turn LED ON (L1)
- Turn LED OFF (L0)
- Monitor sensors
- Provide recommendations

User Query: {user_query if user_query else "Analyze the environment and suggest any actions needed."}

Please provide:
1. Analysis of current conditions
2. Recommended actions (if any)
3. Specific commands to execute (L1, L0, or none)
4. Explanation of your reasoning

Respond in JSON format:
{{
    "analysis": "brief analysis of conditions",
    "recommendations": ["list of recommendations"],
    "actions": ["L1", "L0", or empty list],
    "reasoning": "explanation of decisions"
}}
"""
        return prompt
    
    def _query_llm(self, prompt: str) -> Dict[str, Any]:
        """Query the local LLM for decision making."""
        try:
            # Use Ollama for local LLM (like in two_led_agent.py)
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            response, _ = process.communicate(input=prompt)
            response = response.strip()
            
            # Try to parse JSON response
            try:
                # Extract JSON from response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response[start:end]
                    return json.loads(json_str)
                else:
                    # If no JSON found, try to parse the response as text
                    return {
                        "analysis": response[:200] + "..." if len(response) > 200 else response,
                        "recommendations": ["Consider the environmental conditions"],
                        "actions": [],
                        "reasoning": "LLM provided text response"
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, return the text response
                return {
                    "analysis": response[:200] + "..." if len(response) > 200 else response,
                    "recommendations": ["Consider the environmental conditions"],
                    "actions": [],
                    "reasoning": "LLM provided text response"
                }
            
        except Exception as e:
            print(f"LLM query failed: {e}")
            return self._fallback_decision_logic(prompt)
    
    def _fallback_decision_logic(self, prompt: str) -> Dict[str, Any]:
        """Fallback decision logic when LLM is unavailable."""
        # Simple rule-based decision making
        return {
            "analysis": "Using fallback decision logic",
            "recommendations": ["Consider using local LLM for more intelligent decisions"],
            "actions": [],
            "reasoning": "No LLM available, using basic monitoring"
        }
    
    def _execute_actions(self, decision: Dict[str, Any], status: Dict[str, Any]) -> List[str]:
        """Execute actions based on LLM decision."""
        actions_taken = []
        
        if "actions" in decision:
            for action in decision["actions"]:
                if action == "L1":
                    if self.agent.turn_led_on():
                        actions_taken.append("LED turned ON")
                
                elif action == "L0":
                    if self.agent.turn_led_off():
                        actions_taken.append("LED turned OFF")
        
        return actions_taken
    
    def run_continuous_monitoring(self, interval: int = 60):
        """Run continuous environmental monitoring."""
        print(f"🔄 Starting continuous monitoring (every {interval} seconds)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print("\n" + "="*50)
                print(f"📊 Environmental Check - {time.strftime('%H:%M:%S')}")
                
                decision = self.make_intelligent_decision()
                
                if "error" not in decision:
                    print(f"🌡️  Temperature: {decision['status']['temperature']}°F")
                    print(f"💨 CO2: {decision['status']['co2']}")
                    print(f"💡 Light: {decision['status']['light']}")
                    print(f"🔴 LED: {decision['status']['led']}")
                    
                    if "analysis" in decision["status"]:
                        analysis = decision["status"]["analysis"]
                        print(f"🏥 Overall Health: {analysis['overall_health']}")
                        
                        if analysis["alerts"]:
                            print("⚠️  Alerts:")
                            for alert in analysis["alerts"]:
                                print(f"   - {alert}")
                        
                        if analysis["recommendations"]:
                            print("💡 Recommendations:")
                            for rec in analysis["recommendations"]:
                                print(f"   - {rec}")
                    
                    if decision["actions_taken"]:
                        print("⚡ Actions Taken:")
                        for action in decision["actions_taken"]:
                            print(f"   - {action}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
    
    def close(self):
        """Close the agent."""
        if self.agent:
            self.agent.close()

def main():
    """Test the intelligent environmental agent."""
    agent = IntelligentEnvironmentalAgent()
    
    if not agent.agent.connected:
        print("Cannot test without Arduino connection.")
        return
    
    print("\n=== Testing Intelligent Environmental Agent ===")
    
    # Test intelligent decision making
    print("\n1. Making intelligent decision...")
    decision = agent.make_intelligent_decision("Should I turn on the LED?")
    print(f"Decision: {json.dumps(decision, indent=2)}")
    
    # Test continuous monitoring
    print("\n2. Starting continuous monitoring (30 seconds)...")
    agent.run_continuous_monitoring(30)
    
    agent.close()

if __name__ == "__main__":
    main() 