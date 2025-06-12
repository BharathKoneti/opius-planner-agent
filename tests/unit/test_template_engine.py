"""
Unit tests for TemplateEngine - Following TDD approach.

Testing the template structure system and Jinja2-based template engine.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from opius_planner.templates.template_engine import (
    TemplateEngine,
    TemplateCategory,
    Template,
    TemplateContext,
    TemplateVariable,
    TemplateError
)
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestTemplateEngine:
    """Test suite for TemplateEngine following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.template_engine = TemplateEngine()
    
    def test_init_creates_engine_with_default_templates(self):
        """Test that TemplateEngine initializes with default templates."""
        engine = TemplateEngine()
        assert engine is not None
        assert hasattr(engine, 'templates')
        assert hasattr(engine, 'jinja_env')
        assert len(engine.templates) > 0
    
    def test_load_template_by_category_and_complexity(self):
        """Test loading templates by category and complexity."""
        template = self.template_engine.load_template(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM
        )
        
        assert isinstance(template, Template)
        assert template.category == TaskCategory.TECHNICAL
        assert template.complexity == TaskComplexity.MEDIUM
    
    def test_render_template_with_context(self):
        """Test rendering a template with provided context."""
        context = TemplateContext(
            task_description="Build a Python web application",
            project_name="MyWebApp",
            technologies=["Python", "Flask", "PostgreSQL"],
            estimated_duration="2-3 weeks"
        )
        
        result = self.template_engine.render_template(
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            context=context
        )
        
        assert isinstance(result, str)
        assert "Python web application" in result
        assert "MyWebApp" in result
        assert "Flask" in result
    
    def test_template_contains_required_sections(self):
        """Test that rendered templates contain all required sections."""
        context = TemplateContext(
            task_description="Create a marketing campaign",
            project_name="Q4Campaign"
        )
        
        result = self.template_engine.render_template(
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.MEDIUM,
            context=context
        )
        
        # Should contain standard markdown sections
        assert "# " in result  # Title section
        assert "## " in result  # Sub-sections
        assert "**" in result or "*" in result  # Bold formatting
        assert "- " in result or "1. " in result  # Lists
    
    def test_template_variables_are_substituted(self):
        """Test that template variables are properly substituted."""
        context = TemplateContext(
            task_description="Learn Python programming",
            project_name="PythonLearning",
            estimated_duration="4 weeks",
            resources=["Python.org tutorial", "Online course", "Practice projects"]
        )
        
        result = self.template_engine.render_template(
            category=TaskCategory.EDUCATIONAL,
            complexity=TaskComplexity.LOW,
            context=context
        )
        
        assert "Learn Python programming" in result
        assert "PythonLearning" in result
        assert "4 weeks" in result
        assert "Python.org tutorial" in result
    
    def test_get_available_templates_returns_list(self):
        """Test that get_available_templates returns all available templates."""
        templates = self.template_engine.get_available_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert all(isinstance(t, Template) for t in templates)
    
    def test_filter_templates_by_category(self):
        """Test filtering templates by category."""
        technical_templates = self.template_engine.get_templates_by_category(
            TaskCategory.TECHNICAL
        )
        
        assert isinstance(technical_templates, list)
        assert len(technical_templates) > 0
        assert all(t.category == TaskCategory.TECHNICAL for t in technical_templates)
    
    def test_filter_templates_by_complexity(self):
        """Test filtering templates by complexity."""
        medium_templates = self.template_engine.get_templates_by_complexity(
            TaskComplexity.MEDIUM
        )
        
        assert isinstance(medium_templates, list)
        assert len(medium_templates) > 0
        assert all(t.complexity == TaskComplexity.MEDIUM for t in medium_templates)
    
    def test_custom_template_registration(self):
        """Test registering custom templates."""
        custom_template = Template(
            name="custom_test",
            category=TaskCategory.PERSONAL,
            complexity=TaskComplexity.LOW,
            content="# Custom Template\n{{ task_description }}",
            variables=["task_description"]
        )
        
        self.template_engine.register_template(custom_template)
        
        # Should be able to find and use the custom template
        result = self.template_engine.render_template(
            category=TaskCategory.PERSONAL,
            complexity=TaskComplexity.LOW,
            context=TemplateContext(task_description="Plan a birthday party")
        )
        
        assert "Custom Template" in result
        assert "Plan a birthday party" in result
    
    def test_template_inheritance_and_blocks(self):
        """Test template inheritance using Jinja2 blocks."""
        # This tests that our Jinja2 environment supports template inheritance
        parent_template = Template(
            name="base_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.LOW,
            content="""# {% block title %}Default Title{% endblock %}
{% block content %}Default content{% endblock %}
{% block footer %}Standard footer{% endblock %}""",
            variables=[]
        )
        
        child_template = Template(
            name="extended_template", 
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.LOW,
            content="""{% extends "base_template" %}
{% block title %}{{ project_name }} Project{% endblock %}
{% block content %}This is a {{ task_type }} project.{% endblock %}""",
            variables=["project_name", "task_type"]
        )
        
        self.template_engine.register_template(parent_template)
        self.template_engine.register_template(child_template)
        
        context = TemplateContext(
            project_name="MyApp",
            task_type="web development"
        )
        
        result = self.template_engine.render_by_name("extended_template", context)
        
        assert "MyApp Project" in result
        assert "web development project" in result
        assert "Standard footer" in result
    
    def test_template_validation(self):
        """Test template validation for required fields."""
        # Valid template should pass validation
        valid_template = Template(
            name="valid_test",
            category=TaskCategory.CREATIVE,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ title }}\n{{ description }}",
            variables=["title", "description"]
        )
        
        assert self.template_engine.validate_template(valid_template) == True
        
        # Invalid template should fail validation
        invalid_template = Template(
            name="",  # Empty name should be invalid
            category=TaskCategory.CREATIVE,
            complexity=TaskComplexity.MEDIUM,
            content="# Test",
            variables=[]
        )
        
        assert self.template_engine.validate_template(invalid_template) == False
    
    def test_template_error_handling(self):
        """Test error handling for malformed templates."""
        malformed_template = Template(
            name="malformed_test",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.LOW,
            content="# Test {{ unclosed_variable",  # Malformed Jinja2 syntax
            variables=["unclosed_variable"]
        )
        
        self.template_engine.register_template(malformed_template)
        
        context = TemplateContext(unclosed_variable="test")
        
        with pytest.raises(TemplateError):
            self.template_engine.render_by_name("malformed_test", context)
    
    def test_template_context_creation(self):
        """Test TemplateContext creation and usage."""
        context = TemplateContext(
            task_description="Build an API",
            technologies=["Python", "FastAPI"],
            duration="1 week"
        )
        
        assert context.task_description == "Build an API"
        assert context.technologies == ["Python", "FastAPI"]
        assert context.duration == "1 week"
        
        # Should be able to access as dict
        context_dict = context.to_dict()
        assert context_dict["task_description"] == "Build an API"
        assert context_dict["technologies"] == ["Python", "FastAPI"]


class TestTemplate:
    """Test suite for Template dataclass."""
    
    def test_template_creation(self):
        """Test Template object creation."""
        template = Template(
            name="test_template",
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.HIGH,
            content="# {{ project_name }}\n{{ description }}",
            variables=["project_name", "description"],
            metadata={"author": "Test", "version": "1.0"}
        )
        
        assert template.name == "test_template"
        assert template.category == TaskCategory.BUSINESS
        assert template.complexity == TaskComplexity.HIGH
        assert "project_name" in template.variables
        assert template.metadata["author"] == "Test"
    
    def test_template_extract_variables(self):
        """Test automatic variable extraction from template content."""
        content = "# {{ title }}\n{{ description }}\nDuration: {{ duration }}"
        
        template = Template(
            name="auto_vars",
            category=TaskCategory.PERSONAL,
            complexity=TaskComplexity.LOW,
            content=content,
            variables=[]  # Should be auto-populated
        )
        
        # Template should be able to extract variables automatically
        extracted_vars = template.extract_variables()
        assert "title" in extracted_vars
        assert "description" in extracted_vars
        assert "duration" in extracted_vars


class TestTemplateContext:
    """Test suite for TemplateContext."""
    
    def test_context_dict_conversion(self):
        """Test converting context to dictionary."""
        context = TemplateContext(
            name="TestProject",
            type="web_app",
            features=["auth", "api", "ui"]
        )
        
        context_dict = context.to_dict()
        
        assert isinstance(context_dict, dict)
        assert context_dict["name"] == "TestProject"
        assert context_dict["type"] == "web_app"
        assert context_dict["features"] == ["auth", "api", "ui"]
    
    def test_context_merge(self):
        """Test merging multiple contexts."""
        context1 = TemplateContext(name="Project1", type="api")
        context2 = TemplateContext(version="1.0", author="Developer")
        
        merged = context1.merge(context2)
        
        assert merged.name == "Project1"
        assert merged.type == "api"
        assert merged.version == "1.0"
        assert merged.author == "Developer"


class TestTemplateVariable:
    """Test suite for TemplateVariable dataclass."""
    
    def test_template_variable_creation(self):
        """Test TemplateVariable object creation."""
        var = TemplateVariable(
            name="project_name",
            description="Name of the project",
            required=True,
            default="MyProject",
            type="string"
        )
        
        assert var.name == "project_name"
        assert var.description == "Name of the project"
        assert var.required == True
        assert var.default == "MyProject"
        assert var.type == "string"


class TestTemplateCategory:
    """Test suite for TemplateCategory enum."""
    
    def test_template_category_values(self):
        """Test that TemplateCategory has expected values."""
        expected_categories = {
            'TECHNICAL', 'CREATIVE', 'BUSINESS', 'PERSONAL', 'EDUCATIONAL'
        }
        actual_categories = {category.name for category in TemplateCategory}
        assert actual_categories == expected_categories
