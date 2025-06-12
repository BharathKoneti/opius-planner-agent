"""
PlanGenerator - Adaptive planning algorithm system.

This module provides intelligent plan generation capabilities that combine:
- Task analysis results (category, complexity, requirements)
- Environment detection (system capabilities, available tools)
- Resource-aware recommendations
- Structured execution plans
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

from .task_analyzer import TaskAnalyzer, TaskAnalysis, TaskCategory, TaskComplexity
from .environment_detector import EnvironmentDetector, EnvironmentCapabilities


@dataclass
class ResourceRequirement:
    """Represents a resource requirement for plan execution."""
    name: str
    type: str  # 'software', 'hardware', 'service', 'skill'
    required: bool = True
    alternatives: List[str] = field(default_factory=list)
    installation_guide: str = ""
    estimated_cost: Optional[str] = None


@dataclass
class PlanStep:
    """Represents a single step in an execution plan."""
    title: str
    description: str
    duration: str
    dependencies: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    tools_required: List[str] = field(default_factory=list)
    resources_needed: List[str] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)
    order: int = 0


@dataclass
class PlanMetadata:
    """Metadata about the generated plan."""
    category: TaskCategory
    complexity: TaskComplexity
    estimated_duration: str
    required_skills: List[str]
    success_criteria: List[str]
    generated_at: datetime.datetime
    confidence_score: float
    environment_optimized: bool = False


@dataclass
class PlanningContext:
    """Context information for plan generation."""
    task_description: str
    task_analysis: TaskAnalysis
    environment: EnvironmentCapabilities
    user_preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    """Complete execution plan with all components."""
    metadata: PlanMetadata
    steps: List[PlanStep]
    resources: List[ResourceRequirement]
    notes: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of the execution plan."""
        lines = [
            f"# {self.metadata.category.value.title()} Project Plan",
            f"**Complexity**: {self.metadata.complexity.name}",
            f"**Duration**: {self.metadata.estimated_duration}",
            "",
            "## Steps:",
        ]
        
        for i, step in enumerate(self.steps, 1):
            lines.append(f"{i}. **{step.title}** ({step.duration})")
            lines.append(f"   {step.description}")
        
        return "\n".join(lines)


class PlanGenerator:
    """Adaptive plan generation engine that combines task analysis and environment detection."""
    
    def __init__(self, task_analyzer: TaskAnalyzer = None, environment_detector: EnvironmentDetector = None):
        """Initialize the PlanGenerator with analyzers."""
        self.task_analyzer = task_analyzer or TaskAnalyzer()
        self.environment_detector = environment_detector or EnvironmentDetector()
        
        # Initialize template patterns for different categories and complexities
        self.template_patterns = self._initialize_template_patterns()
        
        # Step templates organized by category
        self.step_templates = self._initialize_step_templates()
    
    def _initialize_template_patterns(self) -> Dict[str, Any]:
        """Initialize planning patterns and templates."""
        return {
            TaskCategory.TECHNICAL: {
                TaskComplexity.LOW: {
                    'base_steps': ['setup', 'implement', 'test', 'deploy'],
                    'estimated_hours': 8
                },
                TaskComplexity.MEDIUM: {
                    'base_steps': ['setup', 'design', 'implement', 'test', 'optimize', 'deploy'],
                    'estimated_hours': 40
                },
                TaskComplexity.HIGH: {
                    'base_steps': ['research', 'architecture', 'setup', 'implement', 'test', 'optimize', 'security', 'deploy', 'monitor'],
                    'estimated_hours': 120
                },
                TaskComplexity.VERY_HIGH: {
                    'base_steps': ['research', 'requirements', 'architecture', 'prototype', 'setup', 'implement', 'test', 'optimize', 'security', 'deploy', 'monitor', 'scale'],
                    'estimated_hours': 400
                }
            },
            TaskCategory.CREATIVE: {
                TaskComplexity.LOW: {
                    'base_steps': ['brainstorm', 'outline', 'create', 'review'],
                    'estimated_hours': 6
                },
                TaskComplexity.MEDIUM: {
                    'base_steps': ['research', 'brainstorm', 'outline', 'create', 'review', 'refine'],
                    'estimated_hours': 25
                },
                TaskComplexity.HIGH: {
                    'base_steps': ['research', 'concept', 'outline', 'draft', 'review', 'revise', 'finalize'],
                    'estimated_hours': 80
                },
                TaskComplexity.VERY_HIGH: {
                    'base_steps': ['research', 'concept', 'planning', 'outline', 'draft', 'feedback', 'revise', 'polish', 'finalize'],
                    'estimated_hours': 200
                }
            },
            TaskCategory.BUSINESS: {
                TaskComplexity.LOW: {
                    'base_steps': ['research', 'analyze', 'plan', 'execute'],
                    'estimated_hours': 10
                },
                TaskComplexity.MEDIUM: {
                    'base_steps': ['market_research', 'analyze', 'strategy', 'plan', 'execute', 'measure'],
                    'estimated_hours': 30
                },
                TaskComplexity.HIGH: {
                    'base_steps': ['market_research', 'competitive_analysis', 'strategy', 'planning', 'budgeting', 'execution', 'monitoring', 'optimization'],
                    'estimated_hours': 100
                },
                TaskComplexity.VERY_HIGH: {
                    'base_steps': ['market_research', 'competitive_analysis', 'stakeholder_analysis', 'strategy', 'planning', 'budgeting', 'risk_assessment', 'execution', 'monitoring', 'optimization', 'scaling'],
                    'estimated_hours': 300
                }
            },
            TaskCategory.PERSONAL: {
                TaskComplexity.LOW: {
                    'base_steps': ['research', 'plan', 'organize', 'execute'],
                    'estimated_hours': 5
                },
                TaskComplexity.MEDIUM: {
                    'base_steps': ['research', 'budget', 'plan', 'organize', 'coordinate', 'execute'],
                    'estimated_hours': 20
                },
                TaskComplexity.HIGH: {
                    'base_steps': ['research', 'budget', 'timeline', 'vendors', 'coordination', 'execution', 'management'],
                    'estimated_hours': 60
                },
                TaskComplexity.VERY_HIGH: {
                    'base_steps': ['research', 'budget', 'timeline', 'vendors', 'logistics', 'coordination', 'backup_plans', 'execution', 'management'],
                    'estimated_hours': 150
                }
            },
            TaskCategory.EDUCATIONAL: {
                TaskComplexity.LOW: {
                    'base_steps': ['assess', 'learn', 'practice', 'review'],
                    'estimated_hours': 8
                },
                TaskComplexity.MEDIUM: {
                    'base_steps': ['assess', 'curriculum', 'learn', 'practice', 'project', 'review'],
                    'estimated_hours': 30
                },
                TaskComplexity.HIGH: {
                    'base_steps': ['assess', 'curriculum', 'foundation', 'intermediate', 'advanced', 'project', 'portfolio'],
                    'estimated_hours': 100
                },
                TaskComplexity.VERY_HIGH: {
                    'base_steps': ['assess', 'curriculum', 'foundation', 'intermediate', 'advanced', 'specialization', 'projects', 'portfolio', 'certification'],
                    'estimated_hours': 250
                }
            }
        }
    
    def _initialize_step_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize step templates for different step types."""
        return {
            'setup': {
                'title': 'Setup Development Environment',
                'description': 'Configure your development environment with necessary tools and dependencies',
                'duration': '1-2 hours'
            },
            'research': {
                'title': 'Research and Requirements Gathering',
                'description': 'Gather requirements, research best practices, and understand the problem domain',
                'duration': '2-4 hours'
            },
            'design': {
                'title': 'System Design and Architecture',
                'description': 'Design the system architecture and plan the implementation approach',
                'duration': '3-6 hours'
            },
            'implement': {
                'title': 'Implementation and Development',
                'description': 'Write the core functionality and implement the main features',
                'duration': '8-16 hours'
            },
            'test': {
                'title': 'Testing and Quality Assurance',
                'description': 'Write and run tests to ensure functionality and quality',
                'duration': '2-4 hours'
            },
            'deploy': {
                'title': 'Deployment and Launch',
                'description': 'Deploy the application and make it available for use',
                'duration': '1-3 hours'
            },
            'brainstorm': {
                'title': 'Brainstorming and Ideation',
                'description': 'Generate and explore creative ideas for the project',
                'duration': '1-2 hours'
            },
            'outline': {
                'title': 'Create Outline and Structure',
                'description': 'Develop a clear structure and outline for the creative work',
                'duration': '2-3 hours'
            },
            'create': {
                'title': 'Creative Development',
                'description': 'Develop the creative content according to the outline',
                'duration': '8-20 hours'
            }
        }
    
    def generate_plan(self, task_description: str) -> ExecutionPlan:
        """Generate a comprehensive execution plan for the given task."""
        # Analyze the task
        task_analysis = self.task_analyzer.analyze_task(task_description)
        
        # Get environment capabilities
        environment = self.environment_detector.get_environment_capabilities()
        
        # Create planning context
        context = self._create_planning_context(task_description, task_analysis, environment)
        
        # Generate plan components
        steps = self._generate_steps(context)
        resources = self._generate_resources(context)
        metadata = self._generate_metadata(context)
        notes = self._generate_notes(context)
        
        return ExecutionPlan(
            metadata=metadata,
            steps=steps,
            resources=resources,
            notes=notes
        )
    
    def _create_planning_context(self, task_description: str, task_analysis: TaskAnalysis, environment: EnvironmentCapabilities) -> PlanningContext:
        """Create planning context combining all analysis results."""
        return PlanningContext(
            task_description=task_description,
            task_analysis=task_analysis,
            environment=environment
        )
    
    def _generate_steps(self, context: PlanningContext) -> List[PlanStep]:
        """Generate plan steps based on context."""
        category = context.task_analysis.category
        complexity = context.task_analysis.complexity
        
        # Get base steps for this category and complexity
        pattern = self.template_patterns.get(category, {}).get(complexity, {})
        base_steps = pattern.get('base_steps', ['setup', 'implement', 'test'])
        
        steps = []
        for i, step_type in enumerate(base_steps):
            step_template = self.step_templates.get(step_type, {
                'title': step_type.replace('_', ' ').title(),
                'description': f'Complete the {step_type} phase of the project',
                'duration': '2-4 hours'
            })
            
            # Adapt step based on environment
            adapted_step = self._adapt_step_to_environment(step_template, context)
            
            step = PlanStep(
                title=adapted_step['title'],
                description=adapted_step['description'],
                duration=adapted_step['duration'],
                dependencies=self._get_step_dependencies(step_type, context),
                success_criteria=self._get_step_success_criteria(step_type, context),
                tools_required=self._get_step_tools(step_type, context),
                order=i + 1
            )
            
            steps.append(step)
        
        return steps
    
    def _adapt_step_to_environment(self, step_template: Dict[str, str], context: PlanningContext) -> Dict[str, str]:
        """Adapt step template to the specific environment."""
        adapted = step_template.copy()
        
        # Add environment-specific recommendations
        env_recommendations = context.environment.recommendations
        
        if any("lightweight" in rec.lower() or "memory" in rec.lower() for rec in env_recommendations):
            if "development" in adapted['description'].lower():
                adapted['description'] += " Focus on lightweight tools and memory-efficient approaches."
        
        if context.environment.editor_info and context.environment.editor_info.name != "unknown":
            editor_name = context.environment.editor_info.name
            if "setup" in adapted['title'].lower():
                adapted['description'] += f" Configure {editor_name} with appropriate extensions."
        
        # Add available tools to relevant steps
        available_tools = []
        for tool in context.environment.available_tools:
            if tool.available:
                # Handle both real ToolInfo objects and Mock objects
                tool_name = getattr(tool, 'name', 'unknown')
                # Convert Mock objects to string if needed
                if hasattr(tool_name, '_mock_name'):
                    tool_name = tool_name._mock_name or str(tool_name)
                available_tools.append(str(tool_name))
        
        if "setup" in adapted['title'].lower() and available_tools:
            tools_list = ", ".join(available_tools)
            adapted['description'] += f" Available tools: {tools_list}."
        
        return adapted
    
    def _get_step_dependencies(self, step_type: str, context: PlanningContext) -> List[str]:
        """Get dependencies for a specific step type."""
        dependencies = []
        
        if step_type == 'setup':
            dependencies.extend(['Development machine', 'Internet connection'])
            if context.environment.editor_info.name != "unknown":
                dependencies.append(f"{context.environment.editor_info.name} editor")
        elif step_type == 'implement':
            dependencies.extend(['Development environment', 'Requirements specification'])
        elif step_type == 'test':
            dependencies.extend(['Implemented code', 'Testing framework'])
        elif step_type == 'deploy':
            dependencies.extend(['Tested code', 'Deployment environment'])
        
        return dependencies
    
    def _get_step_success_criteria(self, step_type: str, context: PlanningContext) -> List[str]:
        """Get success criteria for a specific step type."""
        criteria = []
        
        if step_type == 'setup':
            criteria.extend(['Environment configured', 'Tools installed', 'Dependencies resolved'])
        elif step_type == 'implement':
            criteria.extend(['Core functionality working', 'Code follows standards'])
        elif step_type == 'test':
            criteria.extend(['All tests passing', 'Coverage targets met'])
        elif step_type == 'deploy':
            criteria.extend(['Application accessible', 'No deployment errors'])
        
        return criteria
    
    def _get_step_tools(self, step_type: str, context: PlanningContext) -> List[str]:
        """Get required tools for a specific step type."""
        tools = []
        
        # Get available tools from environment
        available_tools = []
        for tool in context.environment.available_tools:
            if tool.available:
                # Handle both real ToolInfo objects and Mock objects
                tool_name = getattr(tool, 'name', 'unknown')
                # Convert Mock objects to string if needed
                if hasattr(tool_name, '_mock_name'):
                    tool_name = tool_name._mock_name or str(tool_name)
                available_tools.append(str(tool_name))
        
        available_tools_set = set(available_tools)
        
        if step_type == 'setup':
            if 'git' in available_tools_set:
                tools.append('Git')
            if context.task_analysis.category == TaskCategory.TECHNICAL:
                tools.extend(['Package manager', 'IDE/Editor'])
        elif step_type == 'test':
            if 'pytest' in available_tools_set:
                tools.append('PyTest')
            else:
                tools.append('Testing framework')
        elif step_type == 'deploy':
            if 'docker' in available_tools_set:
                tools.append('Docker')
        
        return tools
    
    def _generate_resources(self, context: PlanningContext) -> List[ResourceRequirement]:
        """Generate resource requirements based on context."""
        resources = []
        
        # Add skill-based resources
        for skill in context.task_analysis.required_skills:
            resources.append(ResourceRequirement(
                name=f"{skill} Knowledge",
                type="skill",
                required=True,
                alternatives=[],
                installation_guide=f"Learn {skill} through tutorials and documentation"
            ))
        
        # Add tool-based resources
        for dependency in context.task_analysis.dependencies:
            resources.append(ResourceRequirement(
                name=dependency,
                type="software",
                required=True,
                alternatives=[],
                installation_guide=f"Install {dependency} according to official documentation"
            ))
        
        # Add environment-specific resources
        if context.task_analysis.category == TaskCategory.TECHNICAL:
            resources.append(ResourceRequirement(
                name="Development Environment",
                type="software",
                required=True,
                alternatives=["Local setup", "Cloud IDE", "Container"],
                installation_guide="Set up a development environment suitable for your project"
            ))
        
        return resources
    
    def _generate_metadata(self, context: PlanningContext) -> PlanMetadata:
        """Generate plan metadata."""
        return PlanMetadata(
            category=context.task_analysis.category,
            complexity=context.task_analysis.complexity,
            estimated_duration=context.task_analysis.estimated_duration,
            required_skills=context.task_analysis.required_skills,
            success_criteria=context.task_analysis.success_criteria,
            generated_at=datetime.datetime.now(),
            confidence_score=context.task_analysis.confidence_score,
            environment_optimized=True
        )
    
    def _generate_notes(self, context: PlanningContext) -> List[str]:
        """Generate helpful notes for the plan."""
        notes = []
        
        # Add environment-specific notes
        if context.environment.recommendations:
            notes.append("Environment Recommendations:")
            notes.extend([f"- {rec}" for rec in context.environment.recommendations])
        
        # Add complexity-specific notes
        if context.task_analysis.complexity == TaskComplexity.VERY_HIGH:
            notes.append("This is a very complex project. Consider breaking it into smaller phases.")
        elif context.task_analysis.complexity == TaskComplexity.LOW:
            notes.append("This is a relatively simple project that can be completed quickly.")
        
        return notes
