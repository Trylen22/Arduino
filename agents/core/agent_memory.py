#!/usr/bin/env python3
"""
Agent Memory System
==================

Simple memory system for the IRIS agent to maintain context
and learn from interactions.

Author: [Your Name]
Date: [2025-01-27]
"""

import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class AgentMemory:
    """Simple memory system for the IRIS agent."""
    
    def __init__(self):
        """Initialize the memory system."""
        self.short_term = []  # Recent interactions
        self.long_term = {}   # Persistent knowledge
        self.episodic = []    # Study sessions
        self.patterns = {}    # Learned patterns
        
        # Initialize with basic knowledge
        self.long_term["student_preferences"] = {
            "preferred_break_duration": 5,
            "stress_triggers": ["exams", "deadlines", "complex_topics"],
            "comfortable_temperature_range": (68, 75),
            "preferred_lighting": "moderate"
        }
        
        self.long_term["study_patterns"] = {
            "average_session_length": 45,
            "break_frequency": 15,
            "peak_productivity_hours": [9, 14, 19],
            "stress_patterns": {}
        }
    
    def store_interaction(self, user_input: str, response: str, context: Dict[str, Any]):
        """Store a recent interaction."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": response,
            "context": context,
            "session_id": context.get("session_id", "unknown")
        }
        
        self.short_term.append(interaction)
        
        # Keep only last 50 interactions
        if len(self.short_term) > 50:
            self.short_term.pop(0)
    
    def store_study_session(self, session_data: Dict[str, Any]):
        """Store a complete study session."""
        session = {
            "timestamp": datetime.now().isoformat(),
            "duration_minutes": session_data.get("duration", 0),
            "breaks_taken": session_data.get("breaks", 0),
            "stress_level": session_data.get("stress", 0),
            "environmental_conditions": session_data.get("environment", {}),
            "productivity_score": session_data.get("productivity", 0)
        }
        
        self.episodic.append(session)
        
        # Keep only last 100 sessions
        if len(self.episodic) > 100:
            self.episodic.pop(0)
    
    def learn_patterns(self):
        """Analyze interactions to learn patterns."""
        if len(self.episodic) < 3:
            return
        
        # Analyze study patterns
        sessions = self.episodic[-10:]  # Last 10 sessions
        avg_duration = sum(s["duration_minutes"] for s in sessions) / len(sessions)
        avg_stress = sum(s["stress_level"] for s in sessions) / len(sessions)
        
        self.long_term["study_patterns"]["average_session_length"] = avg_duration
        self.long_term["study_patterns"]["average_stress_level"] = avg_stress
        
        # Learn stress triggers
        high_stress_sessions = [s for s in sessions if s["stress_level"] > 6]
        if high_stress_sessions:
            # Analyze what was happening during high stress
            pass
    
    def get_recent_context(self, minutes: int = 30) -> List[Dict[str, Any]]:
        """Get recent interactions within specified time window."""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent = []
        
        for interaction in self.short_term:
            interaction_time = datetime.fromisoformat(interaction["timestamp"])
            if interaction_time > cutoff:
                recent.append(interaction)
        
        return recent
    
    def get_student_preferences(self) -> Dict[str, Any]:
        """Get current student preferences."""
        return self.long_term.get("student_preferences", {})
    
    def get_study_patterns(self) -> Dict[str, Any]:
        """Get learned study patterns."""
        return self.long_term.get("study_patterns", {})
    
    def update_preferences(self, new_preferences: Dict[str, Any]):
        """Update student preferences based on interactions."""
        current = self.long_term.get("student_preferences", {})
        current.update(new_preferences)
        self.long_term["student_preferences"] = current
    
    def should_intervene(self, context: Dict[str, Any]) -> bool:
        """Determine if agent should proactively intervene."""
        # Check if student has been studying too long
        study_time = context.get("study_time_minutes", 0)
        if study_time > 90:
            return True
        
        # Check stress level
        stress = context.get("stress_level", 0)
        if stress > 7:
            return True
        
        # Check environmental conditions
        env = context.get("environment", {})
        temp = env.get("temperature", 0)
        if temp > 80 or temp < 60:
            return True
        
        return False
    
    def get_intervention_suggestion(self, context: Dict[str, Any]) -> Optional[str]:
        """Get a proactive intervention suggestion."""
        if not self.should_intervene(context):
            return None
        
        study_time = context.get("study_time_minutes", 0)
        stress = context.get("stress_level", 0)
        env = context.get("environment", {})
        
        if study_time > 90:
            return "You've been studying for a while. How about a 10-minute break?"
        elif stress > 7:
            return "I can sense you're feeling stressed. Let's take a moment to breathe."
        elif env.get("temperature", 0) > 80:
            return "It's getting warm in here. Let me turn on the fan for you."
        
        return None
    
    def save_memory(self, filename: str = "agent_memory.json"):
        """Save memory to file."""
        memory_data = {
            "short_term": self.short_term,
            "long_term": self.long_term,
            "episodic": self.episodic,
            "patterns": self.patterns
        }
        
        with open(filename, 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def load_memory(self, filename: str = "agent_memory.json"):
        """Load memory from file."""
        try:
            with open(filename, 'r') as f:
                memory_data = json.load(f)
            
            self.short_term = memory_data.get("short_term", [])
            self.long_term = memory_data.get("long_term", {})
            self.episodic = memory_data.get("episodic", [])
            self.patterns = memory_data.get("patterns", {})
        except FileNotFoundError:
            print("No existing memory file found. Starting fresh.")
        except Exception as e:
            print(f"Error loading memory: {e}")


def main():
    """Test the memory system."""
    memory = AgentMemory()
    
    # Test storing interactions
    context = {"session_id": "test_1", "study_time": 30}
    memory.store_interaction("I'm stressed", "Let me help you relax", context)
    
    # Test getting recent context
    recent = memory.get_recent_context(60)
    print(f"Recent interactions: {len(recent)}")
    
    # Test intervention logic
    test_context = {"study_time_minutes": 95, "stress_level": 5}
    should_intervene = memory.should_intervene(test_context)
    print(f"Should intervene: {should_intervene}")
    
    if should_intervene:
        suggestion = memory.get_intervention_suggestion(test_context)
        print(f"Intervention: {suggestion}")


if __name__ == "__main__":
    main() 