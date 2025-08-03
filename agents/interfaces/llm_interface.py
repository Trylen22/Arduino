#!/usr/bin/env python3
"""
LLM Interface Module
===================

Modular LLM interface for querying local models and parsing responses.
Can be imported and used by other agents.

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