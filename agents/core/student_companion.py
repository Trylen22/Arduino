#!/usr/bin/env python3
"""
Student Companion Module
=======================

AI companion for students that provides emotional support, study assistance,
and environmental monitoring to create optimal study conditions.

Author: [Your Name]
Date: [2025-01-27]
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from message_generators import MessageGenerators


class StudentCompanion:
    """AI companion for students with emotional intelligence and study support."""
    
    def __init__(self):
        """Initialize the student companion."""
        self.session_start = None
        self.study_time_minutes = 0
        self.break_time_minutes = 0
        self.student_mood = "neutral"
        self.stress_level = 0  # 0-10 scale
        self.conversation_history = []
        self.study_goals = []
        self.achievements = []
        self.last_interaction = None
        
        # Study session tracking
        self.current_session = {
            "start_time": None,
            "breaks_taken": 0,
            "total_study_time": 0,
            "environmental_alerts": 0,
            "stress_peaks": 0
        }
        
        # Emotional support patterns
        self.mood_patterns = {
            "stressed": ["exam", "test", "deadline", "pressure", "worried"],
            "frustrated": ["difficult", "hard", "confused", "stuck", "problem"],
            "tired": ["exhausted", "sleepy", "tired", "burned out", "drained"],
            "excited": ["excited", "happy", "great", "awesome", "progress"],
            "confident": ["confident", "ready", "prepared", "got this", "nailed it"]
        }
    
    def start_study_session(self) -> str:
        """Start a new study session."""
        self.session_start = datetime.now()
        self.current_session["start_time"] = self.session_start
        self.study_time_minutes = 0
        self.break_time_minutes = 0
        
        return MessageGenerators.get_conversation_starter()
    
    def update_study_time(self) -> None:
        """Update study time tracking."""
        if self.session_start:
            elapsed = datetime.now() - self.session_start
            self.study_time_minutes = int(elapsed.total_seconds() / 60)
            self.current_session["total_study_time"] = self.study_time_minutes
    
    def analyze_student_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze student input for mood and needs."""
        input_lower = user_input.lower()
        
        # Detect mood from keywords
        detected_mood = "neutral"
        for mood, keywords in self.mood_patterns.items():
            if any(keyword in input_lower for keyword in keywords):
                detected_mood = mood
                break
        
        # Detect stress indicators
        stress_indicators = ["stressed", "anxious", "worried", "overwhelmed", "pressure"]
        stress_level = sum(1 for indicator in stress_indicators if indicator in input_lower)
        
        # Detect study-related needs
        needs = []
        if any(word in input_lower for word in ["break", "rest", "tired"]):
            needs.append("break")
        if any(word in input_lower for word in ["help", "stuck", "confused"]):
            needs.append("help")
        if any(word in input_lower for word in ["motivation", "encouragement"]):
            needs.append("motivation")
        if any(word in input_lower for word in ["environment", "room", "temperature"]):
            needs.append("environment")
        
        return {
            "mood": detected_mood,
            "stress_level": min(stress_level * 2, 10),
            "needs": needs,
            "study_time": self.study_time_minutes
        }
    
    def generate_student_response(self, analysis: Dict[str, Any], environment: Dict[str, Any]) -> str:
        """Generate appropriate response based on student analysis and environment."""
        self.student_mood = analysis.get("mood", "neutral")
        self.stress_level = analysis.get("stress_level", 0)
        
        # Create student context
        student_context = {
            "mood": self.student_mood,
            "study_time_minutes": self.study_time_minutes,
            "stress_level": self.stress_level,
            "environment": environment
        }
        
        # Generate primary response
        if "break" in analysis.get("needs", []):
            return MessageGenerators.get_study_break_message(self.study_time_minutes, self.stress_level)
        elif self.stress_level > 6:
            return MessageGenerators.get_stress_management_message(self.stress_level)
        elif "motivation" in analysis.get("needs", []):
            return MessageGenerators.get_motivation_message(study_time=self.study_time_minutes)
        elif "environment" in analysis.get("needs", []):
            return MessageGenerators.get_environmental_comfort_message(environment)
        else:
            return MessageGenerators.get_student_support_message(student_context)
    
    def check_study_break_needed(self) -> Optional[str]:
        """Check if a study break is recommended."""
        if self.study_time_minutes > 180:  # 3 hours
            return "You've been studying for over 3 hours! Your brain needs a proper break. How about a 15-minute walk?"
        elif self.study_time_minutes > 90:  # 1.5 hours
            return f"You've been focused for {self.study_time_minutes} minutes. Time for a 5-minute break?"
        elif self.study_time_minutes > 45:  # 45 minutes
            return "You're in the zone! But remember, short breaks help you stay sharp."
        
        return None
    
    def take_break(self) -> str:
        """Handle taking a study break."""
        self.break_time_minutes = 0
        self.current_session["breaks_taken"] += 1
        
        break_messages = [
            "Great idea! Taking breaks helps your brain process what you've learned.",
            "Perfect timing! Your brain will thank you for this break.",
            "Smart move! Breaks improve your overall productivity.",
            "You deserve this break! You've been working hard."
        ]
        
        import random
        return random.choice(break_messages)
    
    def end_study_session(self) -> str:
        """End the current study session."""
        if not self.session_start:
            return "No active study session to end."
        
        session_duration = datetime.now() - self.session_start
        total_minutes = int(session_duration.total_seconds() / 60)
        
        # Generate session summary
        summary = f"Study session complete! You studied for {total_minutes} minutes"
        
        if self.current_session["breaks_taken"] > 0:
            summary += f" and took {self.current_session['breaks_taken']} breaks"
        
        summary += ". Great work!"
        
        # Reset session
        self.session_start = None
        self.study_time_minutes = 0
        self.current_session = {
            "start_time": None,
            "breaks_taken": 0,
            "total_study_time": 0,
            "environmental_alerts": 0,
            "stress_peaks": 0
        }
        
        return summary
    
    def get_study_stats(self) -> Dict[str, Any]:
        """Get current study session statistics."""
        return {
            "study_time_minutes": self.study_time_minutes,
            "break_time_minutes": self.break_time_minutes,
            "current_mood": self.student_mood,
            "stress_level": self.stress_level,
            "breaks_taken": self.current_session["breaks_taken"],
            "session_active": self.session_start is not None
        }
    
    def add_achievement(self, achievement: str) -> str:
        """Record a student achievement."""
        self.achievements.append({
            "achievement": achievement,
            "timestamp": datetime.now(),
            "study_time": self.study_time_minutes
        })
        
        return MessageGenerators.get_motivation_message(achievement, self.study_time_minutes)
    
    def get_environmental_recommendations(self, environment: Dict[str, Any]) -> List[str]:
        """Get environmental recommendations for optimal studying."""
        recommendations = []
        
        temp = environment.get('temperature', 0)
        co2 = environment.get('co2', 0)
        light = environment.get('brightness', 'Unknown')
        
        if temp > 75:
            recommendations.append("Consider turning on the fan - comfortable temperature helps focus")
        elif temp < 65:
            recommendations.append("It's a bit chilly - warm up for better concentration")
        
        if co2 > 1000:
            recommendations.append("The air is stuffy - fresh air helps your brain work better")
        
        if light == "dim":
            recommendations.append("Better lighting can reduce eye strain and help you stay alert")
        
        return recommendations
    
    def should_intervene(self) -> bool:
        """Determine if the AI should proactively intervene."""
        if not self.session_start:
            return False
        
        # Check for long study sessions without breaks
        if self.study_time_minutes > 90 and self.current_session["breaks_taken"] == 0:
            return True
        
        # Check for high stress levels
        if self.stress_level > 7:
            return True
        
        # Check for environmental issues
        if self.current_session["environmental_alerts"] > 2:
            return True
        
        return False
    
    def get_intervention_message(self, environment: Dict[str, Any]) -> Optional[str]:
        """Get a proactive intervention message."""
        if self.study_time_minutes > 90 and self.current_session["breaks_taken"] == 0:
            return "I notice you've been studying for a while without a break. How about a quick 5-minute stretch?"
        
        if self.stress_level > 7:
            return "I can sense you're feeling stressed. Want to take a moment to breathe and reset?"
        
        # Environmental interventions
        temp = environment.get('temperature', 0)
        co2 = environment.get('co2', 0)
        
        if temp > 80:
            return "The room is getting warm. Want me to turn on the fan to help you stay comfortable?"
        
        if co2 > 1200:
            return "The air quality is poor. Fresh air will help you think more clearly!"
        
        return None 