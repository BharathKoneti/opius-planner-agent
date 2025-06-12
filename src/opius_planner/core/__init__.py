"""
Core components of the Opius Planner Agent.

This module contains the main planning engine components:
- TaskAnalyzer: Universal task categorization and analysis (IMPLEMENTED)
- EnvironmentDetector: System capability and tool detection (IMPLEMENTED)
- PlanGenerator: Adaptive plan creation engine (IMPLEMENTED)
- Other components will be added following TDD approach
"""

# Import only implemented components for now (TDD approach)
from .task_analyzer import TaskAnalyzer, TaskCategory, TaskComplexity
from .environment_detector import (
    EnvironmentDetector, 
    SystemInfo, 
    EditorInfo, 
    ToolInfo,
    EnvironmentCapabilities
)
from .plan_generator import (
    PlanGenerator,
    PlanStep,
    ExecutionPlan,
    PlanMetadata,
    ResourceRequirement,
    PlanningContext
)

__all__ = [
    "TaskAnalyzer",
    "TaskCategory",
    "TaskComplexity",
    "EnvironmentDetector",
    "SystemInfo",
    "EditorInfo", 
    "ToolInfo",
    "EnvironmentCapabilities",
    "PlanGenerator",
    "PlanStep",
    "ExecutionPlan",
    "PlanMetadata",
    "ResourceRequirement",
    "PlanningContext",
]
