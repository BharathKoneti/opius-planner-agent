"""
CLI interface for the Opius Planner Agent.

This module provides command-line interface functionality
for plan generation, template management, and interactive mode.
"""

from .main import main, PlannerAgent

__all__ = [
    "main",
    "PlannerAgent",
]
