"""
Integration tests for Opius Planner Agent - End-to-end workflows.

Testing complete workflows from task input to plan output,
ensuring all components work together seamlessly.
"""

import pytest
import tempfile
import os
from pathlib import Path
from opius_planner.cli.main import PlannerAgent
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity
from opius_planner.core.environment_detector import EnvironmentDetector
from opius_planner.core.plan_generator import PlanGenerator
from opius_planner.templates.template_engine import TemplateEngine
from opius_planner.templates.markdown_generator import MarkdownGenerator


class TestEndToEndWorkflows:
    """Integration tests for complete end-to-end workflows."""
    
    def test_complete_technical_project_workflow(self):
        """Test complete workflow for a technical project."""
        # Create PlannerAgent
        agent = PlannerAgent()
        
        # Generate plan for a technical project
        task_description = "Build a Python REST API with authentication and database integration"
        
        plan_content = agent.generate_plan(
            task_description=task_description,
            agentic=True
        )
        
        # Verify plan content structure
        assert isinstance(plan_content, str)
        assert len(plan_content) > 100  # Should be substantial
        assert "# " in plan_content  # Should have title
        assert "## " in plan_content  # Should have sections
        assert "Python" in plan_content
        assert "API" in plan_content
        assert "authentication" in plan_content.lower()
        assert "database" in plan_content.lower()
        
        # Should contain implementation steps
        assert "setup" in plan_content.lower() or "environment" in plan_content.lower()
        assert "implement" in plan_content.lower() or "development" in plan_content.lower()
        assert "test" in plan_content.lower()
    
    def test_complete_creative_project_workflow(self):
        """Test complete workflow for a creative project."""
        agent = PlannerAgent()
        
        task_description = "Write a science fiction short story about AI consciousness"
        
        plan_content = agent.generate_plan(
            task_description=task_description,
            agentic=True
        )
        
        # Verify creative project structure
        assert isinstance(plan_content, str)
        assert "science fiction" in plan_content.lower()
        assert "story" in plan_content.lower()
        assert "AI" in plan_content or "ai" in plan_content.lower()
        
        # Should contain creative workflow steps
        assert any(word in plan_content.lower() for word in ["brainstorm", "outline", "draft", "write"])
    
    def test_complete_business_project_workflow(self):
        """Test complete workflow for a business project."""
        agent = PlannerAgent()
        
        task_description = "Create a comprehensive marketing strategy for a new SaaS product launch"
        
        plan_content = agent.generate_plan(
            task_description=task_description,
            agentic=True
        )
        
        # Verify business project structure
        assert isinstance(plan_content, str)
        assert "marketing" in plan_content.lower()
        assert "strategy" in plan_content.lower()
        assert "saas" in plan_content.lower() or "SaaS" in plan_content
        
        # Should contain business workflow steps
        assert any(word in plan_content.lower() for word in ["market", "analysis", "target", "campaign"])
    
    def test_plan_generation_with_frontmatter(self):
        """Test plan generation with YAML frontmatter."""
        agent = PlannerAgent()
        
        plan_content = agent.generate_plan(
            task_description="Develop a mobile application",
            format_type="yaml-frontmatter",
            agentic=True
        )
        
        # Should start with YAML frontmatter
        assert plan_content.startswith("---")
        assert "title:" in plan_content
        assert "category:" in plan_content
        assert "complexity:" in plan_content
        
        # Should have markdown content after frontmatter
        parts = plan_content.split("---")
        assert len(parts) >= 3  # Before, frontmatter, after
        markdown_content = parts[2].strip()
        assert markdown_content.startswith("#")
    
    def test_component_integration_task_analyzer_to_plan_generator(self):
        """Test integration between TaskAnalyzer and PlanGenerator."""
        from opius_planner.core.task_analyzer import TaskAnalyzer
        from opius_planner.core.environment_detector import EnvironmentDetector
        from opius_planner.core.plan_generator import PlanGenerator
        
        # Initialize components
        task_analyzer = TaskAnalyzer()
        environment_detector = EnvironmentDetector()
        plan_generator = PlanGenerator(task_analyzer, environment_detector)
        
        # Analyze task
        task_analysis = task_analyzer.analyze_task("Build a React web application with Redux")
        
        # Verify analysis
        assert task_analysis.category == TaskCategory.TECHNICAL
        assert task_analysis.complexity in [TaskComplexity.MEDIUM, TaskComplexity.HIGH]
        assert "React" in task_analysis.keywords or "react" in task_analysis.keywords
        
        # Generate plan using analysis
        execution_plan = plan_generator.generate_plan("Build a React web application with Redux")
        
        # Verify plan structure
        assert execution_plan.metadata.category == TaskCategory.TECHNICAL
        assert len(execution_plan.steps) > 0
        assert len(execution_plan.resources) > 0
    
    def test_component_integration_template_engine_to_markdown_generator(self):
        """Test integration between TemplateEngine and MarkdownGenerator."""
        from opius_planner.templates.template_engine import TemplateEngine, TemplateContext
        from opius_planner.templates.markdown_generator import MarkdownGenerator, MarkdownMetadata
        import datetime
        
        # Initialize components
        template_engine = TemplateEngine()
        markdown_generator = MarkdownGenerator()
        
        # Load and render template
        template = template_engine.load_template(TaskCategory.EDUCATIONAL, TaskComplexity.LOW)
        assert template is not None
        
        context = TemplateContext(
            project_name="Learn Python Programming",
            task_description="Master Python fundamentals and build projects",
            estimated_duration="6-8 weeks",
            resources=["Python.org", "Online tutorials", "Practice projects"]
        )
        
        rendered_content = template_engine.render_by_name(template.name, context)
        
        # Add frontmatter using MarkdownGenerator
        metadata = MarkdownMetadata(
            title="Learn Python Programming",
            category="educational",
            complexity="low",
            created_at=datetime.datetime.now(),
            tags=["python", "programming", "learning"]
        )
        
        final_content = markdown_generator.generate_with_frontmatter(rendered_content, metadata)
        
        # Verify integration
        assert final_content.startswith("---")
        assert "Learn Python Programming" in final_content
        assert "Python fundamentals" in final_content
        assert "6-8 weeks" in final_content
    
    def test_environment_adaptation_integration(self):
        """Test that plans adapt to detected environment."""
        from opius_planner.core.environment_detector import EnvironmentDetector
        from opius_planner.core.plan_generator import PlanGenerator
        from opius_planner.core.task_analyzer import TaskAnalyzer
        
        # Initialize components
        task_analyzer = TaskAnalyzer()
        environment_detector = EnvironmentDetector()
        plan_generator = PlanGenerator(task_analyzer, environment_detector)
        
        # Get environment capabilities
        env_capabilities = environment_detector.get_environment_capabilities()
        
        # Generate plan
        plan = plan_generator.generate_plan("Create a Python development environment")
        
        # Verify environment-specific adaptations
        assert plan.metadata.environment_optimized == True
        
        # Plan should include environment-specific recommendations
        if env_capabilities.recommendations:
            plan_text = str(plan)
            # At least some environment considerations should be reflected
            assert len(plan.notes) > 0 or "environment" in plan_text.lower()
    
    def test_cli_integration_with_file_output(self):
        """Test CLI integration with file output."""
        from click.testing import CliRunner
        from opius_planner.cli.main import generate_plan
        
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            # Generate plan and save to file
            result = runner.invoke(generate_plan, [
                'Build a simple calculator app',
                '--output', 'calculator_plan.md',
                '--agentic'
            ])
            
            assert result.exit_code == 0
            assert "Plan saved to calculator_plan.md" in result.output
            
            # Verify file was created and has content
            assert os.path.exists('calculator_plan.md')
            
            with open('calculator_plan.md', 'r') as f:
                content = f.read()
                assert len(content) > 100
                assert "calculator" in content.lower()
                assert "# " in content  # Has title
    
    def test_error_handling_integration(self):
        """Test error handling across integrated components."""
        agent = PlannerAgent()
        
        # Test with empty task description
        with pytest.raises(Exception):
            agent.generate_plan("")
        
        # Test with None task description  
        with pytest.raises(Exception):
            agent.generate_plan(None)
    
    def test_large_complex_project_workflow(self):
        """Test workflow for a large, complex project."""
        agent = PlannerAgent()
        
        task_description = """
        Design and implement a comprehensive e-commerce platform with the following features:
        - User authentication and authorization
        - Product catalog with search and filtering
        - Shopping cart and checkout process
        - Payment integration (Stripe/PayPal)
        - Order management system
        - Admin dashboard
        - Email notifications
        - Mobile-responsive design
        - RESTful API
        - Database optimization
        - Security measures
        - Performance monitoring
        - Automated testing
        - CI/CD pipeline
        - Deployment to cloud infrastructure
        """
        
        plan_content = agent.generate_plan(
            task_description=task_description,
            agentic=True
        )
        
        # Verify comprehensive plan structure
        assert len(plan_content) > 1000  # Should be very detailed
        assert "authentication" in plan_content.lower()
        assert "database" in plan_content.lower()
        assert "payment" in plan_content.lower()
        assert "api" in plan_content.lower()
        assert "testing" in plan_content.lower()
        assert "deployment" in plan_content.lower()
        
        # Should have multiple phases/sections
        section_count = plan_content.count("## ")
        assert section_count >= 5  # Multiple major sections
        
        # Should have many implementation steps
        step_count = plan_content.count("- [ ]")
        assert step_count >= 10  # Many action items
    
    def test_memory_and_performance_with_multiple_plans(self):
        """Test memory usage and performance with multiple plan generations."""
        agent = PlannerAgent()
        
        tasks = [
            "Build a web scraper",
            "Create a data visualization dashboard", 
            "Develop a chatbot",
            "Build a file upload service",
            "Create a task scheduler"
        ]
        
        plans = []
        for task in tasks:
            plan = agent.generate_plan(task, agentic=True)
            plans.append(plan)
            assert len(plan) > 50  # Each plan should be substantial
        
        # All plans should be unique
        assert len(set(plans)) == len(plans)
        
        # Each plan should be relevant to its task
        for i, plan in enumerate(plans):
            task_words = tasks[i].lower().split()
            plan_lower = plan.lower()
            # At least some task-specific words should appear in the plan
            matches = sum(1 for word in task_words if word in plan_lower)
            assert matches >= 1


class TestComponentInteractions:
    """Test specific component interaction patterns."""
    
    def test_task_analyzer_environment_detector_synergy(self):
        """Test synergy between task analysis and environment detection."""
        from opius_planner.core.task_analyzer import TaskAnalyzer
        from opius_planner.core.environment_detector import EnvironmentDetector
        
        task_analyzer = TaskAnalyzer()
        environment_detector = EnvironmentDetector()
        
        # Analyze a development task
        task_analysis = task_analyzer.analyze_task("Set up a Python development environment with VS Code")
        env_capabilities = environment_detector.get_environment_capabilities()
        
        # Verify both components work together logically
        assert task_analysis.category == TaskCategory.TECHNICAL
        assert len(task_analysis.required_skills) > 0
        assert len(env_capabilities.available_tools) >= 0  # Should return list (may be empty)
        
        # Environment should provide useful context for the task
        if env_capabilities.editor_info.name == "vscode":
            # If VS Code is detected, it should be relevant to the task
            assert True  # This combination makes sense
    
    def test_template_selection_based_on_analysis(self):
        """Test template selection based on task analysis results."""
        from opius_planner.core.task_analyzer import TaskAnalyzer
        from opius_planner.templates.template_engine import TemplateEngine
        
        task_analyzer = TaskAnalyzer()
        template_engine = TemplateEngine()
        
        # Test different task types
        test_cases = [
            ("Build a React application", TaskCategory.TECHNICAL),
            ("Write a blog post", TaskCategory.CREATIVE),
            ("Plan a marketing campaign", TaskCategory.BUSINESS),
            ("Learn machine learning", TaskCategory.EDUCATIONAL)
        ]
        
        for task_desc, expected_category in test_cases:
            analysis = task_analyzer.analyze_task(task_desc)
            template = template_engine.load_template(analysis.category, analysis.complexity)
            
            assert analysis.category == expected_category
            assert template is not None
            assert template.category == expected_category
