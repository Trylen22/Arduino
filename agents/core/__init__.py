#!/usr/bin/env python3
"""
Core Agents Module
=================

Core components for the IRIS Environmental AI system.
"""

from .environmental_agent import EnvironmentalAgent
from .smart_monitor import SmartMonitor
from .message_generators import MessageGenerators
from .student_companion import StudentCompanion

__all__ = [
    'EnvironmentalAgent',
    'SmartMonitor', 
    'MessageGenerators',
    'StudentCompanion'
]
