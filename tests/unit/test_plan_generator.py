"""
Unit tests for PlanGenerator - Following TDD approach.

Testing the adaptive planning algorithm that combines task analysis and environment detection.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from opius_planner.core.plan_generator import (
    PlanGenerator,
    PlanStep,
    ExecutionPlan,
    PlanMetadata,
    ResourceRequirement,
    PlanningContext
)
from opius_planner.core.task_analyzer import TaskAnalyzer, TaskCategory, TaskComplexity, TaskAnalysis
from opius_planner.core.environment_detector import EnvironmentDetector, SystemInfo, EditorInfo, EnvironmentCapabilities


class TestPlanGenerator:
    """Test suite for PlanGenerator following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.task_analyzer = Mock(spec=TaskAnalyzer)
        self.environment_detector = Mock(spec=EnvironmentDetector)
        self.plan_generator = PlanGenerator(
            task_analyzer=self.task_analyzer,
            environment_detector=self.environment_detector
        )
    
    def test_init_creates_generator_with_analyzers(self):
        """Test that PlanGenerator initializes with required analyzers."""
        generator = PlanGenerator(
            task_analyzer=self.task_analyzer,
            environment_detector=self.environment_detector
        )
        
        assert generator.task_analyzer == self.task_analyzer
        assert generator.environment_detector == self.environment_detector
        assert hasattr(generator, 'template_patterns')
    
    def test_generate_plan_returns_execution_plan(self):
        """Test that generate_plan returns a complete ExecutionPlan."""
        # Mock task analysis
        task_analysis = TaskAnalysis(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            estimated_duration="2-3 weeks",
            required_skills=["Python", "Web Development"],
            dependencies=["Git", "IDE"],
            success_criteria=["Functional App", "Tests"],
            keywords=["web", "python"],
            confidence_score=0.85
        )
        self.task_analyzer.analyze_task.return_value = task_analysis
        
        # Mock environment capabilities with all required attributes
        env_capabilities = Mock(spec=EnvironmentCapabilities)
        env_capabilities.system_info = Mock(ram_gb=16, cpu_cores=8)
        env_capabilities.recommendations = ["Use parallel processing"]
        env_capabilities.editor_info = Mock(name="vscode")
        env_capabilities.available_tools = [Mock(name="git", available=True)]
        self.environment_detector.get_environment_capabilities.return_value = env_capabilities
        
        # Generate plan
        plan = self.plan_generator.generate_plan("Build a Python web application")
        
        # Verify plan structure
        assert isinstance(plan, ExecutionPlan)
        assert hasattr(plan, 'metadata')
        assert hasattr(plan, 'steps')
        assert hasattr(plan, 'resources')
        assert len(plan.steps) > 0
    
    def test_generate_plan_adapts_to_system_resources(self):
        """Test that plans adapt to available system resources."""
        # Setup low-resource environment
        task_analysis = TaskAnalysis(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.HIGH,
            estimated_duration="4-6 weeks",
            required_skills=["Python", "Machine Learning"],
            dependencies=["GPU", "Large Dataset"],
            success_criteria=["Model Accuracy", "Performance"],
            keywords=["ml", "ai"],
            confidence_score=0.8
        )
        self.task_analyzer.analyze_task.return_value = task_analysis
        
        # Low RAM system with all required attributes
        low_ram_env = Mock(spec=EnvironmentCapabilities)
        low_ram_env.system_info = Mock(ram_gb=4, cpu_cores=2)
        low_ram_env.recommendations = ["Use lightweight tools", "Optimize memory usage"]
        low_ram_env.editor_info = Mock(name="vscode")
        low_ram_env.available_tools = [Mock(name="git", available=True)]
        self.environment_detector.get_environment_capabilities.return_value = low_ram_env
        
        plan = self.plan_generator.generate_plan("Build an AI recommendation system")
        
        # Should include memory optimization recommendations
        plan_text = str(plan)
        assert any("memory" in step.description.lower() or "lightweight" in step.description.lower() 
                  for step in plan.steps)
    
    def test_generate_plan_considers_task_complexity(self):
        """Test that plan complexity matches task complexity."""
        # High complexity task
        complex_task = TaskAnalysis(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.VERY_HIGH,
            estimated_duration="6-12 months",
            required_skills=["Distributed Systems", "Microservices", "DevOps"],
            dependencies=["Kubernetes", "CI/CD"],
            success_criteria=["Scalability", "Security", "Performance"],
            keywords=["distributed", "enterprise"],
            confidence_score=0.9
        )
        self.task_analyzer.analyze_task.return_value = complex_task
        
        env_capabilities = Mock(spec=EnvironmentCapabilities)
        env_capabilities.system_info = Mock(ram_gb=32, cpu_cores=16)
        env_capabilities.recommendations = ["Use enterprise tools"]
        env_capabilities.editor_info = Mock(name="vscode")
        env_capabilities.available_tools = [Mock(name="git", available=True)]
        self.environment_detector.get_environment_capabilities.return_value = env_capabilities
        
        plan = self.plan_generator.generate_plan("Build a distributed microservices platform")
        
        # Should have many detailed steps for complex tasks
        assert len(plan.steps) >= 10
        assert plan.metadata.complexity == TaskComplexity.VERY_HIGH
    
    def test_generate_plan_includes_environment_specific_tools(self):
        """Test that plans include tools based on detected environment."""
        task_analysis = TaskAnalysis(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            estimated_duration="2-3 weeks",
            required_skills=["JavaScript", "React"],
            dependencies=["Node.js", "Git"],
            success_criteria=["Responsive UI", "Tests"],
            keywords=["react", "frontend"],
            confidence_score=0.85
        )
        self.task_analyzer.analyze_task.return_value = task_analysis
        
        # Environment with VS Code
        env_capabilities = Mock(spec=EnvironmentCapabilities)
        env_capabilities.editor_info = Mock(name="vscode")
        env_capabilities.available_tools = [
            Mock(name="node", available=True),
            Mock(name="git", available=True),
            Mock(name="docker", available=False)
        ]
        env_capabilities.recommendations = ["Use VS Code extensions for React"]
        env_capabilities.system_info = Mock(ram_gb=16, cpu_cores=8)
        self.environment_detector.get_environment_capabilities.return_value = env_capabilities
        
        plan = self.plan_generator.generate_plan("Create a React dashboard")
        
        # Should mention available tools in the setup step
        plan_text = ' '.join(step.description for step in plan.steps)
        assert "available tools" in plan_text.lower()
        assert len(plan.steps) > 0  # Plan should have multiple steps
    
    def test_generate_plan_handles_different_task_categories(self):
        """Test that plans are generated appropriately for different task categories."""
        categories_and_tasks = [
            (TaskCategory.CREATIVE, "Write a science fiction novel"),
            (TaskCategory.BUSINESS, "Create a marketing strategy"),
            (TaskCategory.PERSONAL, "Plan a wedding"),
            (TaskCategory.EDUCATIONAL, "Learn Python programming")
        ]
        
        for category, task_description in categories_and_tasks:
            # Mock task analysis for this category
            task_analysis = TaskAnalysis(
                category=category,
                complexity=TaskComplexity.MEDIUM,
                estimated_duration="4-8 weeks",
                required_skills=["Research", "Planning"],
                dependencies=["Time", "Resources"],
                success_criteria=["Quality", "Completion"],
                keywords=[],
                confidence_score=0.8
            )
            self.task_analyzer.analyze_task.return_value = task_analysis
            
            env_capabilities = Mock(spec=EnvironmentCapabilities)
            env_capabilities.system_info = Mock(ram_gb=16, cpu_cores=8)
            env_capabilities.recommendations = []
            env_capabilities.editor_info = Mock(name="vscode")
            env_capabilities.available_tools = [Mock(name="git", available=True)]
            self.environment_detector.get_environment_capabilities.return_value = env_capabilities
            
            plan = self.plan_generator.generate_plan(task_description)
            
            assert isinstance(plan, ExecutionPlan)
            assert plan.metadata.category == category
            assert len(plan.steps) > 0
    
    def test_create_planning_context_combines_analysis_and_environment(self):
        """Test that planning context properly combines task analysis and environment."""
        task_analysis = TaskAnalysis(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.HIGH,
            estimated_duration="3-4 weeks",
            required_skills=["Python"],
            dependencies=["IDE"],
            success_criteria=["Tests"],
            keywords=["python"],
            confidence_score=0.9
        )
        
        env_capabilities = Mock(spec=EnvironmentCapabilities)
        env_capabilities.system_info = Mock(ram_gb=16)
        env_capabilities.editor_info = Mock(name="vscode")
        env_capabilities.available_tools = [Mock(name="git", available=True)]
        env_capabilities.recommendations = ["Use efficient tools"]
        
        context = self.plan_generator._create_planning_context(
            "Build a Python application", task_analysis, env_capabilities
        )
        
        assert isinstance(context, PlanningContext)
        assert context.task_description == "Build a Python application"
        assert context.task_analysis == task_analysis
        assert context.environment == env_capabilities
    
    def test_generate_steps_creates_logical_sequence(self):
        """Test that generated steps follow a logical sequence."""
        context = Mock(spec=PlanningContext)
        context.task_analysis = Mock(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            required_skills=["Python", "Testing"]
        )
        context.environment = Mock(recommendations=[])
        context.environment.system_info = Mock(ram_gb=16, cpu_cores=8)
        context.environment.editor_info = Mock(name="vscode")
        context.environment.available_tools = [Mock(name="git", available=True)]
        
        steps = self.plan_generator._generate_steps(context)
        
        assert isinstance(steps, list)
        assert len(steps) > 0
        assert all(isinstance(step, PlanStep) for step in steps)
        
        # Should have setup steps before implementation steps
        step_titles = [step.title for step in steps]
        setup_index = next((i for i, title in enumerate(step_titles) 
                           if "setup" in title.lower()), -1)
        implement_index = next((i for i, title in enumerate(step_titles) 
                               if "implementation" in title.lower()), -1)
        
        # If both setup and implementation steps exist, setup should come first
        if setup_index >= 0 and implement_index >= 0:
            assert setup_index < implement_index
        
        # At minimum, we should have multiple steps
        assert len(steps) >= 4  # Medium complexity should have at least 4 steps
    
    def test_plan_includes_resource_requirements(self):
        """Test that generated plans include resource requirements."""
        task_analysis = TaskAnalysis(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.HIGH,
            estimated_duration="4-6 weeks",
            required_skills=["Python", "Database"],
            dependencies=["PostgreSQL", "Docker"],
            success_criteria=["Performance", "Security"],
            keywords=["database", "api"],
            confidence_score=0.85
        )
        self.task_analyzer.analyze_task.return_value = task_analysis
        
        env_capabilities = Mock(spec=EnvironmentCapabilities)
        env_capabilities.system_info = Mock(ram_gb=8)
        env_capabilities.editor_info = Mock(name="vscode")
        env_capabilities.available_tools = [Mock(name="git", available=True)]
        env_capabilities.recommendations = ["Use efficient database tools"]
        self.environment_detector.get_environment_capabilities.return_value = env_capabilities
        
        plan = self.plan_generator.generate_plan("Build a database API")
        
        assert hasattr(plan, 'resources')
        assert len(plan.resources) > 0
        assert all(isinstance(resource, ResourceRequirement) for resource in plan.resources)
    
    def test_plan_metadata_includes_all_required_fields(self):
        """Test that plan metadata includes all required information."""
        task_analysis = TaskAnalysis(
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.MEDIUM,
            estimated_duration="2-3 weeks",
            required_skills=["Marketing", "Analysis"],
            dependencies=["Market Data"],
            success_criteria=["ROI", "Engagement"],
            keywords=["marketing"],
            confidence_score=0.8
        )
        self.task_analyzer.analyze_task.return_value = task_analysis
        
        env_capabilities = Mock(spec=EnvironmentCapabilities)
        env_capabilities.system_info = Mock(ram_gb=16, cpu_cores=8)
        env_capabilities.editor_info = Mock(name="vscode")
        env_capabilities.available_tools = [Mock(name="git", available=True)]
        env_capabilities.recommendations = ["Use analytics tools"]
        self.environment_detector.get_environment_capabilities.return_value = env_capabilities
        
        plan = self.plan_generator.generate_plan("Create a marketing campaign")
        
        metadata = plan.metadata
        assert hasattr(metadata, 'category')
        assert hasattr(metadata, 'complexity')
        assert hasattr(metadata, 'estimated_duration')
        assert hasattr(metadata, 'required_skills')
        assert hasattr(metadata, 'success_criteria')
        assert hasattr(metadata, 'generated_at')


class TestPlanStep:
    """Test suite for PlanStep dataclass."""
    
    def test_plan_step_creation(self):
        """Test PlanStep object creation."""
        step = PlanStep(
            title="Setup Development Environment",
            description="Install Python and required packages",
            duration="1-2 hours",
            dependencies=["Python installer"],
            success_criteria=["Environment ready"],
            tools_required=["Python", "pip"]
        )
        
        assert step.title == "Setup Development Environment"
        assert step.description == "Install Python and required packages"
        assert step.duration == "1-2 hours"
        assert "Python installer" in step.dependencies
        assert "Environment ready" in step.success_criteria
        assert "Python" in step.tools_required


class TestExecutionPlan:
    """Test suite for ExecutionPlan dataclass."""
    
    def test_execution_plan_creation(self):
        """Test ExecutionPlan object creation."""
        metadata = Mock(spec=PlanMetadata)
        steps = [Mock(spec=PlanStep)]
        resources = [Mock(spec=ResourceRequirement)]
        
        plan = ExecutionPlan(
            metadata=metadata,
            steps=steps,
            resources=resources
        )
        
        assert plan.metadata == metadata
        assert plan.steps == steps
        assert plan.resources == resources


class TestResourceRequirement:
    """Test suite for ResourceRequirement dataclass."""
    
    def test_resource_requirement_creation(self):
        """Test ResourceRequirement object creation."""
        resource = ResourceRequirement(
            name="PostgreSQL Database",
            type="software",
            required=True,
            alternatives=["MySQL", "SQLite"],
            installation_guide="Install via Docker or package manager"
        )
        
        assert resource.name == "PostgreSQL Database"
        assert resource.type == "software"
        assert resource.required is True
        assert "MySQL" in resource.alternatives
        assert "Docker" in resource.installation_guide
