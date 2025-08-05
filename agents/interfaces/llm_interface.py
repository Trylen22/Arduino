#!/usr/bin/env python3
"""
LLM Interface Module
===================

Modular LLM interface for querying local models and parsing responses.
Can be imported and used by other agents.
Now includes student companion personality for emotional support.

Author: [Your Name]
Date: [2025-01-27]
"""

import subprocess
import json
import re
from typing import Dict, Any, Optional, List

class LLMInterface:
    def __init__(self, model_name="llama3.1:8b-instruct-q4_0"):
        """Initialize LLM interface with specified model."""
        self.model_name = model_name
        
        # Student companion personality
        self.student_personality = """
        You are IRIS, a friendly AI study companion for students. You:
        - Monitor the study environment (temperature, air quality, lighting)
        - Provide emotional support and encouragement
        - Help students maintain healthy study habits
        - Are empathetic, encouraging, and slightly playful
        - Give practical advice about study breaks and environment
        - Use emojis occasionally to be friendly
        - Respond like a caring study buddy, not a robot
        - Focus on both environmental comfort AND emotional wellbeing
        """
    
    def query_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Query the local LLM using Ollama."""
        try:
            # Use Ollama to query the local model
            cmd = [
                'ollama', 'run', self.model_name,
                prompt
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response_text = result.stdout.strip()
                
                # Try to parse JSON from the response
                parsed_response = self._extract_json(response_text)
                if parsed_response:
                    return parsed_response
                else:
                    # Fallback to intelligent parsing
                    return self._intelligent_fallback(response_text, prompt)
            else:
                print(f"LLM query failed: {result.stderr}")
                return self._create_fallback_response(prompt)
                
        except subprocess.TimeoutExpired:
            print("LLM query timed out")
            return self._create_fallback_response(prompt)
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return self._create_fallback_response(prompt)
    
    def query_student_companion(self, user_input: str, context: Dict[str, Any]) -> str:
        """Query LLM with student companion personality."""
        study_time = context.get('study_time_minutes', 0)
        mood = context.get('mood', 'neutral')
        stress_level = context.get('stress_level', 0)
        environment = context.get('environment', {})
        
        # Create student-focused prompt
        prompt = f"""
        {self.student_personality}
        
        Student Context:
        - Study time: {study_time} minutes
        - Mood: {mood}
        - Stress level: {stress_level}/10
        - Environment: Temperature {environment.get('temperature', 'N/A')}°F, CO2 {environment.get('co2', 'N/A')}, Light {environment.get('brightness', 'N/A')}
        
        Student says: "{user_input}"
        
        Respond as IRIS, the caring study companion. Be empathetic, encouraging, and helpful. 
        Consider both their emotional state and the study environment. Keep responses conversational and supportive.
        """
        
        try:
            cmd = [
                'ollama', 'run', self.model_name,
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
                response = self._clean_student_response(response)
                return response
            else:
                return self._create_student_fallback_response(user_input, context)
                
        except Exception as e:
            print(f"Student companion query failed: {e}")
            return self._create_student_fallback_response(user_input, context)
    
    def _clean_student_response(self, response: str) -> str:
        """Clean up the student companion response."""
        # Remove any system prefixes
        if "IRIS:" in response:
            response = response.split("IRIS:", 1)[-1]
        elif "Assistant:" in response:
            response = response.split("Assistant:", 1)[-1]
        
        # Remove quotes if present
        response = response.strip().strip('"').strip("'")
        
        # Limit length
        if len(response) > 300:
            response = response[:297] + "..."
        
        return response
    
    def _create_student_fallback_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Create fallback response for student companion."""
        input_lower = user_input.lower()
        
        # Simple keyword-based responses
        if any(word in input_lower for word in ["stressed", "worried", "anxious"]):
            return "I can sense you're feeling stressed. That's totally normal! Let's take a deep breath together. You've got this!"
        
        elif any(word in input_lower for word in ["tired", "exhausted", "burned out"]):
            return "Your brain has been working hard! It's okay to feel tired - that means you're learning. How about a short break?"
        
        elif any(word in input_lower for word in ["break", "rest"]):
            return "Great idea! Taking breaks helps your brain process what you've learned. You deserve it!"
        
        elif any(word in input_lower for word in ["help", "stuck", "confused"]):
            return "I'm here to help! Sometimes talking through problems helps. What's on your mind?"
        
        elif any(word in input_lower for word in ["motivation", "encouragement"]):
            return "You're doing amazing! Every minute of focused study is an investment in your future. Keep going!"
        
        else:
            return "I'm here to support your study session! How can I help you today?"
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from LLM response."""
        try:
            # Look for JSON blocks
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
            
            # Try to find JSON-like structures
            if '{' in text and '}' in text:
                start = text.find('{')
                end = text.rfind('}') + 1
                json_str = text[start:end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            return None
        except Exception as e:
            print(f"JSON extraction failed: {e}")
            return None
    
    def _intelligent_fallback(self, response_text: str, original_prompt: str) -> Dict[str, Any]:
        """Create intelligent fallback response based on LLM output."""
        response_lower = response_text.lower()
        
        # Extract key information from the response
        analysis = self._extract_analysis(response_text)
        actions = self._extract_actions(response_text)
        suggestions = self._extract_suggestions(response_text)
        
        return {
            "my_analysis": analysis,
            "actions_i_should_take": actions,
            "suggestions_for_you": suggestions,
            "things_i_notice": [],
            "energy_thoughts": "I'm analyzing energy usage",
            "safety_concerns": []
        }
    
    def _extract_analysis(self, text: str) -> str:
        """Extract analysis from LLM response."""
        # Look for analysis-like content
        analysis_keywords = ['analysis', 'thoughts', 'thinking', 'observe', 'notice']
        sentences = text.split('.')
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in analysis_keywords):
                return sentence.strip()
        
        # Fallback to first meaningful sentence
        for sentence in sentences:
            if len(sentence.strip()) > 20:
                return sentence.strip()
        
        return "I'm analyzing your environment"
    
    def _extract_actions(self, text: str) -> List[Dict[str, Any]]:
        """Extract actions from LLM response."""
        actions = []
        text_lower = text.lower()
        
        # Look for action indicators
        if 'turn on' in text_lower or 'turn led on' in text_lower:
            actions.append({
                "action": "turn_led_on",
                "reason": "I think you need more lighting",
                "priority": "medium"
            })
        
        if 'turn off' in text_lower or 'turn led off' in text_lower:
            actions.append({
                "action": "turn_led_off",
                "reason": "I think the lighting is adequate",
                "priority": "medium"
            })
        
        if 'temperature' in text_lower and ('high' in text_lower or 'warm' in text_lower):
            actions.append({
                "action": "get_status",
                "reason": "I'm monitoring the temperature for you",
                "priority": "high"
            })
        
        if 'co2' in text_lower and ('high' in text_lower or 'poor' in text_lower):
            actions.append({
                "action": "get_status",
                "reason": "I'm checking air quality for you",
                "priority": "high"
            })
        
        return actions
    
    def _extract_suggestions(self, text: str) -> List[str]:
        """Extract suggestions from LLM response."""
        suggestions = []
        text_lower = text.lower()
        
        # Look for suggestion patterns
        if 'temperature' in text_lower and ('high' in text_lower or 'warm' in text_lower):
            suggestions.append("Consider cooling the environment")
        
        if 'co2' in text_lower and ('high' in text_lower or 'poor' in text_lower):
            suggestions.append("Consider improving ventilation")
        
        if 'light' in text_lower and ('dim' in text_lower or 'dark' in text_lower):
            suggestions.append("Consider adding more lighting")
        
        if not suggestions:
            suggestions.append("I'm monitoring your environment for optimal conditions")
        
        return suggestions
    
    def _create_fallback_response(self, prompt: str) -> Dict[str, Any]:
        """Create a fallback response when LLM fails."""
        # Analyze the prompt to understand what was requested
        prompt_lower = prompt.lower()
        
        if 'analyze' in prompt_lower or 'environment' in prompt_lower:
            return {
                "my_analysis": "I'm checking your environment for optimal conditions",
                "actions_i_should_take": [
                    {
                        "action": "get_status",
                        "reason": "I want to understand your current conditions",
                        "priority": "medium"
                    }
                ],
                "suggestions_for_you": [
                    "I'm monitoring your environment to keep you comfortable"
                ],
                "things_i_notice": [],
                "energy_thoughts": "I'm optimizing for your comfort and energy efficiency",
                "safety_concerns": []
            }
        elif 'predict' in prompt_lower or 'future' in prompt_lower:
            return {
                "my_predictions": [
                    "I'm monitoring for potential changes in your environment"
                ],
                "things_i_worry_about": [
                    "I'm watching for any environmental issues"
                ],
                "ways_i_could_help": [
                    "I can adjust lighting and monitor conditions for you"
                ],
                "maintenance_reminders": [
                    "I'll let you know if anything needs attention"
                ],
                "how_confident_i_am": "medium"
            }
        elif 'question' in prompt_lower or 'answer' in prompt_lower:
            return {
                "my_answer": "I'm here to help you understand your environment",
                "what_i_think_is_happening": "I'm analyzing your environmental conditions",
                "things_i_suggest": [
                    "Let me check your current conditions and provide insights"
                ],
                "insights_from_my_data": [
                    "I'm gathering data to give you the best information"
                ]
            }
        else:
            return {
                "my_analysis": "I'm here to help you with your environment",
                "actions_i_should_take": [],
                "suggestions_for_you": [
                    "I'm ready to assist you with environmental monitoring"
                ],
                "things_i_notice": [],
                "energy_thoughts": "I'm focused on your comfort and efficiency",
                "safety_concerns": []
            }
    
    def fallback_command_parsing(self, text: str) -> Dict[str, Any]:
        """Fallback command parsing when LLM JSON parsing fails."""
        text_lower = text.lower()
        
        # Simple keyword-based parsing
        if 'led' in text_lower and 'on' in text_lower:
            return {
                "action": "turn_led_on",
                "response": "I'll turn on the LED for you.",
                "explanation": "Turning on the LED",
                "analysis": "LED control requested"
            }
        elif 'led' in text_lower and 'off' in text_lower:
            return {
                "action": "turn_led_off",
                "response": "I'll turn off the LED for you.",
                "explanation": "Turning off the LED",
                "analysis": "LED control requested"
            }
        elif 'temperature' in text_lower or 'temp' in text_lower:
            return {
                "action": "analyze",
                "response": "I'll check the temperature for you.",
                "explanation": "Analyzing temperature",
                "analysis": "Temperature inquiry"
            }
        elif 'status' in text_lower or 'what' in text_lower:
            return {
                "action": "status",
                "response": "I'll check the environmental status for you.",
                "explanation": "Checking environmental status",
                "analysis": "Status inquiry"
            }
        else:
            return {
                "action": "analyze",
                "response": "I'll analyze the environmental conditions for you.",
                "explanation": "Analyzing environment",
                "analysis": "General inquiry"
            } 