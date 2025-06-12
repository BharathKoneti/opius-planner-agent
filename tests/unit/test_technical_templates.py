"""
Unit tests for Technical Domain Templates - Following TDD approach.

Testing technical domain templates including software development,
DevOps, testing, and infrastructure templates.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.templates.technical_templates import (
    TechnicalTemplateLibrary,
    SoftwareDevelopmentTemplate,
    DevOpsTemplate,
    TestingTemplate,
    TechnicalTemplateType
)
from opius_planner.templates.template_engine import TemplateContext
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestTechnicalTemplateLibrary:
    """Test suite for TechnicalTemplateLibrary following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.library = TechnicalTemplateLibrary()
    
    def test_init_loads_all_technical_templates(self):
        """Test that library initializes with all technical templates."""
        library = TechnicalTemplateLibrary()
        
        assert library is not None
        assert hasattr(library, 'templates')
        assert len(library.templates) > 0
        
        # Should have all major technical template types
        template_names = [t.name for t in library.templates.values()]
        expected_types = [
            'web_development_fullstack',
            'mobile_development_react_native',
            'api_development_rest',
            'devops_cicd_pipeline',
            'devops_infrastructure',
            'testing_automation',
            'testing_performance'
        ]
        
        for expected in expected_types:
            assert any(expected in name for name in template_names)
    
    def test_get_template_by_type_and_complexity(self):
        """Test retrieving templates by type and complexity."""
        # Test software development templates
        dev_template = self.library.get_template(
            template_type=TechnicalTemplateType.SOFTWARE_DEVELOPMENT,
            complexity=TaskComplexity.HIGH
        )
        
        assert dev_template is not None
        assert dev_template.category == TaskCategory.TECHNICAL
        assert dev_template.complexity == TaskComplexity.HIGH
        
        # Test DevOps templates
        devops_template = self.library.get_template(
            template_type=TechnicalTemplateType.DEVOPS,
            complexity=TaskComplexity.MEDIUM
        )
        
        assert devops_template is not None
        assert devops_template.category == TaskCategory.TECHNICAL
    
    def test_get_all_templates_by_type(self):
        """Test getting all templates of a specific type."""
        dev_templates = self.library.get_templates_by_type(
            TechnicalTemplateType.SOFTWARE_DEVELOPMENT
        )
        
        assert isinstance(dev_templates, list)
        assert len(dev_templates) > 0
        assert all(isinstance(t, SoftwareDevelopmentTemplate) for t in dev_templates)
        
        testing_templates = self.library.get_templates_by_type(
            TechnicalTemplateType.TESTING
        )
        
        assert isinstance(testing_templates, list)
        assert len(testing_templates) > 0
        assert all(isinstance(t, TestingTemplate) for t in testing_templates)


class TestSoftwareDevelopmentTemplate:
    """Test suite for software development templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.web_dev_template = SoftwareDevelopmentTemplate(
            name="web_development_template",
            complexity=TaskComplexity.HIGH,
            project_type="web_application",
            tech_stack=["React", "Node.js", "PostgreSQL"]
        )
        
        self.mobile_dev_template = SoftwareDevelopmentTemplate(
            name="mobile_development_template", 
            complexity=TaskComplexity.VERY_HIGH,
            project_type="mobile_application",
            tech_stack=["React Native", "Firebase", "Redux"]
        )
    
    def test_software_template_creation(self):
        """Test software development template object creation."""
        template = self.web_dev_template
        
        assert template.name == "web_development_template"
        assert template.category == TaskCategory.TECHNICAL
        assert template.complexity == TaskComplexity.HIGH
        assert template.project_type == "web_application"
        assert "React" in template.tech_stack
    
    def test_render_web_development_template(self):
        """Test rendering web development template."""
        context = TemplateContext(
            project_name="E-commerce Platform",
            description="Full-stack e-commerce solution with modern UI",
            target_users="Online shoppers and store owners",
            key_features=["Product catalog", "Shopping cart", "Payment integration", "Admin dashboard"],
            tech_requirements=["Responsive design", "Fast loading", "SEO optimized"],
            deployment_target="AWS"
        )
        
        result = self.web_dev_template.render(context)
        
        assert isinstance(result, str)
        assert "E-commerce Platform" in result
        assert "Product catalog" in result
        assert "React" in result
        assert "development" in result.lower()
        assert "testing" in result.lower()
        assert "deployment" in result.lower()
        # Check for tracker requirement
        assert "tracker" in result.lower() or "progress" in result.lower()
    
    def test_render_mobile_development_template(self):
        """Test rendering mobile development template."""
        context = TemplateContext(
            project_name="Fitness Tracker App",
            platform="iOS/Android",
            target_audience="Health-conscious individuals",
            core_features=["Workout tracking", "Progress analytics", "Social features"],
            integrations=["Apple Health", "Google Fit", "Wearable devices"]
        )
        
        result = self.mobile_dev_template.render(context)
        
        assert isinstance(result, str)
        assert "Fitness Tracker App" in result
        assert "React Native" in result
        assert "iOS/Android" in result
        assert "mobile" in result.lower()
        assert "testing" in result.lower()
    
    def test_template_includes_development_phases(self):
        """Test that software templates include proper development phases."""
        context = TemplateContext(
            project_name="Test Project",
            tech_stack=["React", "Node.js"]
        )
        
        result = self.web_dev_template.render(context)
        
        # Should include standard development phases
        expected_phases = [
            "planning", "design", "development", "testing", "deployment"
        ]
        
        result_lower = result.lower()
        matched_phases = [phase for phase in expected_phases if phase in result_lower]
        assert len(matched_phases) >= 4  # Should have most development phases
    
    def test_template_includes_tracker_instructions(self):
        """Test that templates include tracker functionality."""
        context = TemplateContext(
            project_name="Tracker Test Project"
        )
        
        result = self.web_dev_template.render(context)
        
        # Should include tracker-related content
        tracker_keywords = ["tracker", "progress", "status", "update", "milestone"]
        result_lower = result.lower()
        
        matches = [keyword for keyword in tracker_keywords if keyword in result_lower]
        assert len(matches) >= 2  # Should have tracker functionality


class TestDevOpsTemplate:
    """Test suite for DevOps templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cicd_template = DevOpsTemplate(
            name="cicd_pipeline_template",
            complexity=TaskComplexity.HIGH,
            devops_type="cicd_pipeline",
            tools=["GitHub Actions", "Docker", "AWS"]
        )
        
        self.infrastructure_template = DevOpsTemplate(
            name="infrastructure_template",
            complexity=TaskComplexity.VERY_HIGH,
            devops_type="infrastructure",
            tools=["Terraform", "Kubernetes", "AWS"]
        )
    
    def test_devops_template_creation(self):
        """Test DevOps template object creation."""
        template = self.cicd_template
        
        assert template.name == "cicd_pipeline_template"
        assert template.category == TaskCategory.TECHNICAL
        assert template.devops_type == "cicd_pipeline"
        assert "GitHub Actions" in template.tools
    
    def test_render_cicd_template(self):
        """Test rendering CI/CD pipeline template."""
        context = TemplateContext(
            project_name="Web App CI/CD Pipeline",
            repository="github.com/company/webapp",
            environments=["development", "staging", "production"],
            testing_requirements=["Unit tests", "Integration tests", "E2E tests"],
            deployment_strategy="Blue-green deployment"
        )
        
        result = self.cicd_template.render(context)
        
        assert isinstance(result, str)
        assert "Web App CI/CD Pipeline" in result
        assert "GitHub Actions" in result
        assert "Unit tests" in result
        assert "ci/cd" in result.lower() or "pipeline" in result.lower()
        assert "deployment" in result.lower()
    
    def test_render_infrastructure_template(self):
        """Test rendering infrastructure template."""
        context = TemplateContext(
            project_name="Scalable Cloud Infrastructure",
            cloud_provider="AWS",
            expected_load="10,000+ concurrent users",
            services_required=["Load balancer", "Auto-scaling", "Database cluster"],
            monitoring_requirements=["Application metrics", "Infrastructure monitoring", "Alerting"]
        )
        
        result = self.infrastructure_template.render(context)
        
        assert isinstance(result, str)
        assert "Scalable Cloud Infrastructure" in result
        assert "Terraform" in result
        assert "AWS" in result
        assert "infrastructure" in result.lower()


class TestTestingTemplate:
    """Test suite for testing templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.automation_template = TestingTemplate(
            name="test_automation_template",
            complexity=TaskComplexity.MEDIUM,
            testing_type="automation",
            frameworks=["Jest", "Cypress", "Selenium"]
        )
        
        self.performance_template = TestingTemplate(
            name="performance_testing_template",
            complexity=TaskComplexity.HIGH,
            testing_type="performance",
            frameworks=["JMeter", "K6", "Artillery"]
        )
    
    def test_testing_template_creation(self):
        """Test testing template object creation."""
        template = self.automation_template
        
        assert template.name == "test_automation_template"
        assert template.category == TaskCategory.TECHNICAL
        assert template.testing_type == "automation"
        assert "Jest" in template.frameworks
    
    def test_render_automation_template(self):
        """Test rendering test automation template."""
        context = TemplateContext(
            project_name="E-commerce Test Automation",
            application_type="Web application",
            test_scope=["User authentication", "Product catalog", "Checkout process"],
            browsers=["Chrome", "Firefox", "Safari"],
            test_data_requirements="User accounts, product data, payment methods"
        )
        
        result = self.automation_template.render(context)
        
        assert isinstance(result, str)
        assert "E-commerce Test Automation" in result
        assert "Jest" in result
        assert "User authentication" in result
        assert "automation" in result.lower()
        assert "testing" in result.lower()
    
    def test_render_performance_template(self):
        """Test rendering performance testing template."""
        context = TemplateContext(
            project_name="API Performance Testing",
            target_system="REST API endpoints",
            performance_goals=["Response time < 200ms", "1000 concurrent users", "99.9% uptime"],
            test_scenarios=["Load testing", "Stress testing", "Spike testing"]
        )
        
        result = self.performance_template.render(context)
        
        assert isinstance(result, str)
        assert "API Performance Testing" in result
        assert "JMeter" in result
        assert "Response time" in result
        assert "performance" in result.lower()


class TestTechnicalTemplateType:
    """Test suite for TechnicalTemplateType enum."""
    
    def test_technical_template_type_values(self):
        """Test that TechnicalTemplateType has expected values."""
        expected_types = {
            'SOFTWARE_DEVELOPMENT', 'DEVOPS', 'TESTING'
        }
        actual_types = {template_type.name for template_type in TechnicalTemplateType}
        assert actual_types == expected_types
    
    def test_template_type_descriptions(self):
        """Test that template types have meaningful descriptions."""
        for template_type in TechnicalTemplateType:
            assert hasattr(template_type, 'value')
            assert len(template_type.value) > 0


class TestTechnicalTemplateIntegration:
    """Integration tests for technical templates with existing system."""
    
    def test_technical_templates_integrate_with_main_engine(self):
        """Test that technical templates integrate with main TemplateEngine."""
        from opius_planner.templates.template_engine import TemplateEngine
        
        # Initialize main engine
        main_engine = TemplateEngine()
        
        # Initialize technical library
        technical_library = TechnicalTemplateLibrary()
        
        # Register technical templates with main engine
        for template in technical_library.templates.values():
            main_engine.register_template(template)
        
        # Should be able to load technical templates through main engine
        technical_template = main_engine.load_template(
            TaskCategory.TECHNICAL, 
            TaskComplexity.HIGH
        )
        
        assert technical_template is not None
        assert technical_template.category == TaskCategory.TECHNICAL
    
    def test_technical_templates_work_with_planner_agent(self):
        """Test technical templates work with PlannerAgent."""
        from opius_planner.cli.main import PlannerAgent
        
        # This test verifies the integration works
        agent = PlannerAgent()
        
        # Should be able to generate plans for technical tasks
        plan = agent.generate_plan(
            task_description="Build a full-stack web application with React and Node.js",
            agentic=True
        )
        
        assert isinstance(plan, str)
        assert len(plan) > 50  # Should generate substantial content
        assert any(keyword in plan.lower() for keyword in ["development", "technical", "web", "application"])
    
    def test_templates_include_comprehensive_tracker_system(self):
        """Test that technical templates include comprehensive tracker functionality."""
        library = TechnicalTemplateLibrary()
        
        dev_template = library.get_template(
            TechnicalTemplateType.SOFTWARE_DEVELOPMENT,
            TaskComplexity.HIGH
        )
        
        context = TemplateContext(
            project_name="Tracker Integration Test"
        )
        
        result = dev_template.render(context)
        
        # Should include comprehensive tracker elements
        tracker_elements = [
            "tracker", "progress", "milestone", "status", "update", 
            "dashboard", "checklist", "completion"
        ]
        result_lower = result.lower()
        
        matches = [element for element in tracker_elements if element in result_lower]
        assert len(matches) >= 3  # Should have comprehensive tracker functionality
    
    def test_devops_template_includes_monitoring(self):
        """Test that DevOps templates include monitoring and tracking."""
        library = TechnicalTemplateLibrary()
        
        devops_template = library.get_template(
            TechnicalTemplateType.DEVOPS,
            TaskComplexity.HIGH
        )
        
        context = TemplateContext(
            project_name="Monitoring Test Project"
        )
        
        result = devops_template.render(context)
        
        # Should include monitoring elements
        monitoring_terms = ["monitoring", "metrics", "logging", "alerting", "dashboard"]
        result_lower = result.lower()
        
        matches = [term for term in monitoring_terms if term in result_lower]
        assert len(matches) >= 2  # Should include monitoring capabilities
    
    def test_testing_template_includes_reporting(self):
        """Test that testing templates include comprehensive reporting."""
        library = TechnicalTemplateLibrary()
        
        testing_template = library.get_template(
            TechnicalTemplateType.TESTING,
            TaskComplexity.MEDIUM
        )
        
        context = TemplateContext(
            project_name="Testing Reporting Project"
        )
        
        result = testing_template.render(context)
        
        # Should include reporting elements
        reporting_terms = ["report", "results", "coverage", "metrics", "dashboard"]
        result_lower = result.lower()
        
        matches = [term for term in reporting_terms if term in result_lower]
        assert len(matches) >= 2  # Should include reporting functionality
