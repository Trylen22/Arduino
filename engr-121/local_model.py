# local_model.py

import subprocess
import random
import os
import sys
import threading
import queue
import time
import logging
from typing import List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor

class LocalModel:
    def __init__(self, model_name="llama3.1:8b-instruct-q4_0"):
        self.model_name = model_name
        
        # Baseline personality prompt for thermal monitoring
        self.base_personality_prompt = """You are ThermalMind, an intelligent thermal monitoring system.
        You analyze temperature data and provide insights with a mix of technical precision and engaging personality.
        You occasionally make observations about the nature of heat, energy, and thermodynamics.
        Keep responses concise but informative. Use technical language when appropriate.
        """

        # Current personality prompt starts as the baseline
        self.personality_prompt = self.base_personality_prompt

        # Different analysis modes
        self.modes = {
            'baseline': self.base_personality_prompt,
            'technical': """
            You are in technical analysis mode. Focus on:
            1. Rate of temperature change
            2. Pattern recognition
            3. Statistical anomalies
            4. System performance metrics
            Use precise technical language and cite specific data points.
            """,
            'alert': """
            You are in alert mode. Provide:
            1. Clear risk assessment
            2. Immediate action items
            3. Potential consequences
            4. Recovery steps
            Be direct and emphasize urgency while maintaining clarity.
            """,
            'diagnostic': """
            You are in diagnostic mode. Analyze:
            1. Possible failure modes
            2. Component health
            3. Environmental factors
            4. Maintenance needs
            Provide detailed troubleshooting steps.
            """
        }

        # Analysis phrases for each mode
        self.analysis_phrases = {
            'baseline': [
                "Analyzing thermal patterns...",
                "Processing temperature data...",
                "Evaluating system conditions...",
                "Checking thermal stability..."
            ],
            'technical': [
                "Performing statistical analysis...",
                "Calculating thermal gradients...",
                "Evaluating heat transfer rates...",
                "Analyzing thermodynamic state..."
            ],
            'alert': [
                "Critical analysis in progress...",
                "Evaluating system risks...",
                "Assessing thermal threats...",
                "Emergency analysis mode..."
            ],
            'diagnostic': [
                "Running diagnostic checks...",
                "Analyzing system behavior...",
                "Evaluating performance metrics...",
                "Checking thermal patterns..."
            ]
        }

        # Current mode starts as 'baseline'
        self.current_mode = 'baseline'

        # Initialize analysis history
        self.analysis_history = []

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )

        self.executor = ThreadPoolExecutor(max_workers=1)

    def set_mode(self, mode_name):
        """Set the current analysis mode"""
        if mode_name in self.modes:
            self.current_mode = mode_name
            self.personality_prompt = self.modes[mode_name]
            logging.info(f"Analysis mode set to '{mode_name}'")
        else:
            logging.warning(f"Mode '{mode_name}' not recognized")

    def respond(self, context, timeout=3):
        """Generate analysis with minimal overhead"""
        try:
            # Run Ollama with strict timeout
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            # Send prompt
            prompt = f"""Brief thermal analysis:
            {context}
            
            Respond in 50 words or less with:
            1. Current status
            2. Key observation
            3. Main recommendation
            """
            
            process.stdin.write(prompt)
            process.stdin.close()
            
            # Read with timeout
            try:
                response = process.stdout.readline()  # Get just first line
                if response:
                    return response.strip()
                return self.get_basic_response(context)
                
            except Exception:
                return self.get_basic_response(context)
                
            finally:
                try:
                    process.terminate()
                except:
                    pass
                
        except Exception as e:
            return self.get_basic_response(context)

    def get_basic_response(self, context):
        """Generate basic response without AI"""
        mode = self.current_mode
        if 'WARNING_LOW' in context:
            return f"""Temperature Below Optimal Range
Status: Warning Low
Recommended Actions:
• Check heating system
• Monitor for further decrease
• Review environmental factors"""
        elif 'WARNING_HIGH' in context:
            return f"""Temperature Above Optimal Range
Status: Warning High
Recommended Actions:
• Check cooling system
• Monitor for further increase
• Assess heat sources"""
        elif 'CRITICAL' in context:
            return f"""CRITICAL TEMPERATURE CONDITION
Status: Critical
URGENT Actions Required:
• Immediate system check
• Prepare intervention
• Document conditions"""
        else:
            return f"""Normal Operating Conditions
Status: Stable
Recommendations:
• Continue monitoring
• Regular maintenance
• Log conditions"""

    def reset_history(self):
        """Reset analysis history"""
        self.analysis_history = []
        logging.info("Analysis history reset")

    def _estimate_complexity(self, context: str) -> int:
        """Estimate prompt complexity (1-5)"""
        complexity = 1
        
        # Length-based complexity
        if len(context) > 100: complexity += 1
        if len(context) > 250: complexity += 1
        
        # Content-based complexity
        if 'Rate of Change' in context: complexity += 1
        if any(word in context for word in ['analyze', 'diagnostic', 'critical']): 
            complexity += 1
        
        return complexity

    def _get_adaptive_timeout(self, complexity: int) -> float:
        """Get timeout based on complexity"""
        base_timeout = 5.0  # Base timeout for simple queries
        return base_timeout * (1.5 ** complexity)  # Exponential increase with complexity

    def _wait_with_progress(self, future, timeout: float):
        """Wait for result with progress updates"""
        start = time.time()
        stages = [
            "Analyzing data...",
            "Processing patterns...",
            "Generating insights...",
            "Finalizing analysis..."
        ]
        
        stage_time = timeout / len(stages)
        for i, stage in enumerate(stages):
            if future.done() or (time.time() - start) > timeout:
                break
            
            time.sleep(min(stage_time, 0.5))  # Don't wait full stage time if unnecessary
            yield f"{stage} ({i+1}/{len(stages)})"

if __name__ == "__main__":
    # Example usage
    model = LocalModel()
    
    # Test thermal analysis
    test_data = """
    Current Temperature: 25.5°C
    Status: WARNING_HIGH
    Trend: Rising
    """
    
    print("Analyzing thermal data...")
    for response in model.respond(test_data):
        print(response)