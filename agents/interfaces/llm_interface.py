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
from typing import Dict, Any, Optional

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
                print(f"🤖 LLM Response: {response_text}")
                
                # Try to parse JSON from the response
                try:
                    # Extract JSON from the response
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start != -1 and json_end != 0:
                        json_str = response_text[json_start:json_end]
                        return json.loads(json_str)
                    else:
                        raise ValueError("No JSON found in response")
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON: {e}")
                    # Fallback to simple command parsing
                    return self.fallback_command_parsing(response_text)
            else:
                print(f"❌ LLM query failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ LLM query timed out")
            return None
        except Exception as e:
            print(f"❌ Error querying LLM: {e}")
            return None
    
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