"""
Opius Planner Agent - Universal Planning Agent

A revolutionary planning agent that can create detailed execution plans 
for ANY type of task or project, with environment-aware personalization.
"""

__version__ = "0.1.0"
__author__ = "Opius AI"
__email__ = "hello@opius.ai"

# Import only implemented components for now (TDD approach)
from .core.task_analyzer import TaskAnalyzer, TaskCategory, TaskComplexity

__all__ = [
    "TaskAnalyzer", 
    "TaskCategory",
    "TaskComplexity",
]
