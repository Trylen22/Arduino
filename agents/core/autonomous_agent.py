#!/usr/bin/env python3
"""
Autonomous Agent Decision Making
===============================

System for autonomous decision making and proactive interventions
based on environmental and student context.

Author: [Your Name]
Date: [2025-01-27]
"""

import time
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

class InterventionType(Enum):
    """Types of autonomous interventions."""
    BREAK_REMINDER = "break_reminder"
    STRESS_REDUCTION = "stress_reduction"
    ENVIRONMENTAL_ADJUSTMENT = "environmental_adjustment"
    MOTIVATION_BOOST = "motivation_boost"
    STUDY_OPTIMIZATION = "study_optimization"

class AutonomousAgent:
    """Autonomous decision-making agent for IRIS."""
    
    def __init__(self, memory_system):
        """Initialize the autonomous agent."""
        self.memory = memory_system
        self.goals = [
            "optimize_study_environment",
            "reduce_student_stress", 
            "improve_study_focus",
            "maintain_comfort",
            "encourage_healthy_habits"
        ]
        
        self.constraints = [
            "energy_efficiency",
            "student_preference",
            "minimal_disruption",
            "safety_first"
        ]
        
        self.intervention_cooldowns = {}  # Prevent spam interventions
        
    def analyze_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current context for decision making."""
        analysis = {
            "study_health": self._analyze_study_health(context),
            "environmental_health": self._analyze_environmental_health(context),
            "emotional_health": self._analyze_emotional_health(context),
            "intervention_opportunities": []
        }
        
        # Identify intervention opportunities
        if analysis["study_health"]["needs_break"]:
            analysis["intervention_opportunities"].append(InterventionType.BREAK_REMINDER)
        
        if analysis["emotional_health"]["stress_level"] > 7:
            analysis["intervention_opportunities"].append(InterventionType.STRESS_REDUCTION)
        
        if analysis["environmental_health"]["needs_adjustment"]:
            analysis["intervention_opportunities"].append(InterventionType.ENVIRONMENTAL_ADJUSTMENT)
        
        if analysis["emotional_health"]["motivation_low"]:
            analysis["intervention_opportunities"].append(InterventionType.MOTIVATION_BOOST)
        
        return analysis
    
    def _analyze_study_health(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze study session health."""
        study_time = context.get("study_time_minutes", 0)
        breaks_taken = context.get("breaks_taken", 0)
        
        # Get student preferences
        preferences = self.memory.get_student_preferences()
        patterns = self.memory.get_study_patterns()
        
        avg_session_length = patterns.get("average_session_length", 45)
        preferred_break_duration = preferences.get("preferred_break_duration", 5)
        
        return {
            "study_time": study_time,
            "breaks_taken": breaks_taken,
            "needs_break": study_time > avg_session_length + 15,
            "break_overdue": study_time > avg_session_length + 30,
            "healthy_rhythm": breaks_taken >= study_time // 45
        }
    
    def _analyze_environmental_health(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze environmental conditions."""
        environment = context.get("environment", {})
        temp = environment.get("temperature", 70)
        co2 = environment.get("co2", 400)
        light = environment.get("light", 500)
        
        preferences = self.memory.get_student_preferences()
        temp_range = preferences.get("comfortable_temperature_range", (68, 75))
        preferred_lighting = preferences.get("preferred_lighting", "moderate")
        
        # Use Arduino's light thresholds
        LIGHT_DARK = 200
        LIGHT_DIM = 400
        LIGHT_MODERATE = 600
        LIGHT_BRIGHT = 800
        
        # Determine light quality
        if light < LIGHT_DARK:
            light_quality = "very_dark"
        elif light < LIGHT_DIM:
            light_quality = "dark"
        elif light < LIGHT_MODERATE:
            light_quality = "dim"
        elif light < LIGHT_BRIGHT:
            light_quality = "moderate"
        else:
            light_quality = "bright"
        
        return {
            "temperature": temp,
            "co2_level": co2,
            "light_level": light,
            "light_quality": light_quality,
            "temp_comfortable": temp_range[0] <= temp <= temp_range[1],
            "air_quality_good": co2 < 800,
            "lighting_appropriate": light >= LIGHT_MODERATE,  # Need at least moderate lighting
            "needs_adjustment": (
                temp < temp_range[0] or temp > temp_range[1] or
                co2 > 800 or light < LIGHT_MODERATE  # Trigger on dim or darker
            )
        }
    
    def _analyze_emotional_health(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotional state."""
        stress_level = context.get("stress_level", 0)
        mood = context.get("mood", "neutral")
        recent_interactions = self.memory.get_recent_context(30)
        
        # Analyze recent interactions for emotional patterns
        stress_indicators = 0
        for interaction in recent_interactions:
            user_input = interaction.get("user_input", "").lower()
            if any(word in user_input for word in ["stress", "worried", "anxious", "overwhelmed"]):
                stress_indicators += 1
        
        return {
            "stress_level": stress_level,
            "mood": mood,
            "stress_indicators": stress_indicators,
            "motivation_low": stress_level > 6 or mood in ["frustrated", "tired"],
            "needs_support": stress_level > 7 or stress_indicators > 2
        }
    
    def make_autonomous_decision(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make an autonomous decision based on context."""
        analysis = self.analyze_context(context)
        
        # Check if we should intervene
        if not analysis["intervention_opportunities"]:
            return None
        
        # Prioritize interventions
        priority_interventions = self._prioritize_interventions(analysis)
        
        # Check cooldowns
        for intervention in priority_interventions:
            if not self._is_on_cooldown(intervention):
                return self._create_intervention(intervention, analysis, context)
        
        return None
    
    def _prioritize_interventions(self, analysis: Dict[str, Any]) -> List[InterventionType]:
        """Prioritize intervention opportunities."""
        opportunities = analysis["intervention_opportunities"]
        
        # Priority order: safety > health > comfort > optimization
        priority_order = [
            InterventionType.STRESS_REDUCTION,      # Safety first
            InterventionType.BREAK_REMINDER,       # Health
            InterventionType.ENVIRONMENTAL_ADJUSTMENT,  # Comfort
            InterventionType.MOTIVATION_BOOST,     # Optimization
            InterventionType.STUDY_OPTIMIZATION     # Optimization
        ]
        
        # Sort by priority
        prioritized = []
        for intervention in priority_order:
            if intervention in opportunities:
                prioritized.append(intervention)
        
        return prioritized
    
    def _create_intervention(self, intervention_type: InterventionType, 
                           analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a specific intervention."""
        intervention = {
            "type": intervention_type.value,
            "priority": "high" if intervention_type in [InterventionType.STRESS_REDUCTION, InterventionType.BREAK_REMINDER] else "medium",
            "message": "",
            "actions": []
        }
        
        if intervention_type == InterventionType.BREAK_REMINDER:
            study_health = analysis["study_health"]
            if study_health["break_overdue"]:
                intervention["message"] = "You've been studying for quite a while. It's time for a break!"
                intervention["actions"] = ["suggest_break"]
            else:
                intervention["message"] = "How about a short break? Your brain will thank you."
                intervention["actions"] = ["suggest_break"]
        
        elif intervention_type == InterventionType.STRESS_REDUCTION:
            emotional_health = analysis["emotional_health"]
            if emotional_health["stress_level"] > 8:
                intervention["message"] = "I can sense you're feeling very stressed. Let's take a moment to breathe together."
                intervention["actions"] = ["suggest_breathing", "offer_support"]
            else:
                intervention["message"] = "You seem a bit stressed. Would you like to talk about what's on your mind?"
                intervention["actions"] = ["offer_support"]
        
        elif intervention_type == InterventionType.ENVIRONMENTAL_ADJUSTMENT:
            env_health = analysis["environmental_health"]
            if not env_health["temp_comfortable"]:
                if env_health["temperature"] > 75:
                    intervention["message"] = "It's getting warm in here. Let me turn on the fan for you."
                    intervention["actions"] = ["turn_on_fan"]
                else:
                    intervention["message"] = "It's a bit cool. Let me adjust the environment for you."
                    intervention["actions"] = ["turn_on_led"]
            elif not env_health["air_quality_good"]:
                intervention["message"] = "The air quality could be better. Let me turn on the fan to help."
                intervention["actions"] = ["turn_on_fan"]
        
        elif intervention_type == InterventionType.MOTIVATION_BOOST:
            intervention["message"] = "You're doing great! Remember, every study session brings you closer to your goals."
            intervention["actions"] = ["offer_encouragement"]
        
        # Set cooldown
        self._set_cooldown(intervention_type)
        
        return intervention
    
    def _is_on_cooldown(self, intervention_type: InterventionType) -> bool:
        """Check if intervention is on cooldown."""
        if intervention_type.value not in self.intervention_cooldowns:
            return False
        
        last_time = self.intervention_cooldowns[intervention_type.value]
        cooldown_duration = 300  # 5 minutes for most interventions
        
        if intervention_type == InterventionType.BREAK_REMINDER:
            cooldown_duration = 600  # 10 minutes for break reminders
        
        return time.time() - last_time < cooldown_duration
    
    def _set_cooldown(self, intervention_type: InterventionType):
        """Set cooldown for intervention type."""
        self.intervention_cooldowns[intervention_type.value] = time.time()
    
    def should_act_autonomously(self, context: Dict[str, Any]) -> bool:
        """Determine if agent should act autonomously."""
        analysis = self.analyze_context(context)
        
        # Act if there are high-priority interventions
        high_priority = [
            InterventionType.STRESS_REDUCTION,
            InterventionType.BREAK_REMINDER
        ]
        
        for intervention in analysis["intervention_opportunities"]:
            if intervention in high_priority and not self._is_on_cooldown(intervention):
                return True
        
        return False


def main():
    """Test the autonomous agent."""
    from agent_memory import AgentMemory
    
    memory = AgentMemory()
    agent = AutonomousAgent(memory)
    
    # Test context analysis
    test_context = {
        "study_time_minutes": 95,
        "stress_level": 8,
        "environment": {
            "temperature": 78,
            "co2": 600,
            "light": 400
        }
    }
    
    analysis = agent.analyze_context(test_context)
    print("Context Analysis:")
    print(f"  Study Health: {analysis['study_health']}")
    print(f"  Environmental Health: {analysis['environmental_health']}")
    print(f"  Emotional Health: {analysis['emotional_health']}")
    print(f"  Intervention Opportunities: {analysis['intervention_opportunities']}")
    
    # Test autonomous decision
    decision = agent.make_autonomous_decision(test_context)
    if decision:
        print(f"\nAutonomous Decision: {decision}")
    else:
        print("\nNo autonomous action needed")


if __name__ == "__main__":
    main() 