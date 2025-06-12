"""
Unit tests for CLI - Following TDD approach.

Testing the Click-based command-line interface and interactive mode.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from opius_planner.cli.main import (
    main,
    generate_plan,
    interactive_mode,
    list_templates,
    validate_plan
)
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestCLIMain:
    """Test suite for main CLI functionality following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()
    
    def test_cli_main_command_exists(self):
        """Test that main CLI command exists and shows help."""
        result = self.runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "Opius Planner Agent" in result.output
        assert "Universal planning agent" in result.output
    
    def test_generate_plan_command_basic_usage(self):
        """Test basic plan generation command."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            # Mock the agent and its methods
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Test Plan\n\nThis is a test plan."
            
            result = self.runner.invoke(generate_plan, [
                'Build a Python web application'
            ])
            
            assert result.exit_code == 0
            assert "Test Plan" in result.output
            mock_instance.generate_plan.assert_called_once()
    
    def test_generate_plan_with_output_file(self):
        """Test generating plan and saving to file."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Test Plan\n\nContent"
            
            with self.runner.isolated_filesystem():
                result = self.runner.invoke(generate_plan, [
                    'Build a React app',
                    '--output', 'plan.md'
                ])
                
                assert result.exit_code == 0
                assert "Plan saved to plan.md" in result.output
                
                # Check that file was created
                with open('plan.md', 'r') as f:
                    content = f.read()
                    assert "Test Plan" in content
    
    def test_generate_plan_with_template_option(self):
        """Test generating plan with specific template."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Technical Plan\n\nContent"
            
            result = self.runner.invoke(generate_plan, [
                'Build an API',
                '--template', 'technical',
                '--complexity', 'medium'
            ])
            
            assert result.exit_code == 0
            assert "Technical Plan" in result.output
    
    def test_generate_plan_with_format_options(self):
        """Test generating plan with different output formats."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Plan\n\nContent"
            
            result = self.runner.invoke(generate_plan, [
                'Create a business plan',
                '--format', 'yaml-frontmatter',
                '--agentic'
            ])
            
            assert result.exit_code == 0
    
    def test_interactive_mode_basic_flow(self):
        """Test interactive mode basic workflow."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent, \
             patch('click.prompt') as mock_prompt, \
             patch('click.confirm') as mock_confirm:
            
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Interactive Plan\n\nContent"
            
            # Mock user inputs
            mock_prompt.side_effect = [
                'Build a mobile app',  # Task description
                'technical',           # Category
                'high',               # Complexity
            ]
            mock_confirm.return_value = False  # Don't save to file
            
            result = self.runner.invoke(interactive_mode)
            
            assert result.exit_code == 0
            assert "Interactive Plan" in result.output
    
    def test_list_templates_command(self):
        """Test listing available templates."""
        with patch('opius_planner.cli.main.TemplateEngine') as mock_engine:
            mock_instance = Mock()
            mock_engine.return_value = mock_instance
            
            # Mock templates
            mock_templates = [
                Mock(name="technical_low", category=TaskCategory.TECHNICAL, complexity=TaskComplexity.LOW),
                Mock(name="creative_medium", category=TaskCategory.CREATIVE, complexity=TaskComplexity.MEDIUM),
                Mock(name="business_high", category=TaskCategory.BUSINESS, complexity=TaskComplexity.HIGH)
            ]
            mock_instance.get_available_templates.return_value = mock_templates
            
            result = self.runner.invoke(list_templates)
            
            assert result.exit_code == 0
            assert "Available Templates:" in result.output
            assert "technical_low" in result.output
            assert "creative_medium" in result.output
            assert "business_high" in result.output
    
    def test_list_templates_with_filter(self):
        """Test listing templates with category filter."""
        with patch('opius_planner.cli.main.TemplateEngine') as mock_engine:
            mock_instance = Mock()
            mock_engine.return_value = mock_instance
            
            mock_templates = [
                Mock(name="technical_low", category=TaskCategory.TECHNICAL, complexity=TaskComplexity.LOW),
                Mock(name="technical_high", category=TaskCategory.TECHNICAL, complexity=TaskComplexity.HIGH)
            ]
            mock_instance.get_templates_by_category.return_value = mock_templates
            
            result = self.runner.invoke(list_templates, ['--category', 'technical'])
            
            assert result.exit_code == 0
            assert "technical_low" in result.output
            assert "technical_high" in result.output
    
    def test_validate_plan_command(self):
        """Test plan validation command."""
        with patch('opius_planner.cli.main.MarkdownGenerator') as mock_generator:
            mock_instance = Mock()
            mock_generator.return_value = mock_instance
            mock_instance.validate_syntax.return_value = True
            
            with self.runner.isolated_filesystem():
                # Create a test plan file
                with open('test_plan.md', 'w') as f:
                    f.write("# Test Plan\n\n## Steps\n\n- [ ] Task 1\n- [ ] Task 2")
                
                result = self.runner.invoke(validate_plan, ['test_plan.md'])
                
                assert result.exit_code == 0
                assert "valid" in result.output.lower()
    
    def test_validate_plan_invalid_file(self):
        """Test validating invalid plan file."""
        with patch('opius_planner.cli.main.MarkdownGenerator') as mock_generator:
            mock_instance = Mock()
            mock_generator.return_value = mock_instance
            mock_instance.validate_syntax.return_value = False
            
            with self.runner.isolated_filesystem():
                # Create an invalid plan file
                with open('invalid_plan.md', 'w') as f:
                    f.write("# Test Plan\n\n**Bold text without closing")
                
                result = self.runner.invoke(validate_plan, ['invalid_plan.md'])
                
                assert result.exit_code == 1
                assert "invalid" in result.output.lower()
    
    def test_cli_error_handling(self):
        """Test CLI error handling for various scenarios."""
        # Test with invalid task description
        result = self.runner.invoke(generate_plan, [''])
        assert result.exit_code != 0
        
        # Test with non-existent file for validation
        result = self.runner.invoke(validate_plan, ['nonexistent.md'])
        assert result.exit_code != 0
    
    def test_cli_verbose_output(self):
        """Test CLI verbose output mode."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Verbose Plan\n\nContent"
            
            result = self.runner.invoke(generate_plan, [
                'Build a project',
                '--verbose'
            ])
            
            assert result.exit_code == 0
            assert "Verbose Plan" in result.output
    
    def test_cli_configuration_options(self):
        """Test CLI configuration options."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Config Plan\n\nContent"
            
            result = self.runner.invoke(generate_plan, [
                'Test project',
                '--config', 'custom_config.yaml'
            ])
            
            # Should not fail even if config doesn't exist (graceful degradation)
            assert result.exit_code == 0


class TestCLIHelpers:
    """Test suite for CLI helper functions."""
    
    def test_format_template_info(self):
        """Test formatting template information for display."""
        from opius_planner.cli.main import format_template_info
        
        template = Mock()
        template.name = "technical_medium"
        template.category = TaskCategory.TECHNICAL
        template.complexity = TaskComplexity.MEDIUM
        template.metadata = {"description": "Technical project template"}
        
        result = format_template_info(template)
        
        assert "technical_medium" in result
        assert "TECHNICAL" in result
        assert "MEDIUM" in result
    
    def test_parse_complexity_input(self):
        """Test parsing complexity input from user."""
        from opius_planner.cli.main import parse_complexity
        
        assert parse_complexity("low") == TaskComplexity.LOW
        assert parse_complexity("medium") == TaskComplexity.MEDIUM
        assert parse_complexity("high") == TaskComplexity.HIGH
        assert parse_complexity("very_high") == TaskComplexity.VERY_HIGH
        
        # Test case insensitive
        assert parse_complexity("LOW") == TaskComplexity.LOW
        assert parse_complexity("Medium") == TaskComplexity.MEDIUM
    
    def test_parse_category_input(self):
        """Test parsing category input from user."""
        from opius_planner.cli.main import parse_category
        
        assert parse_category("technical") == TaskCategory.TECHNICAL
        assert parse_category("creative") == TaskCategory.CREATIVE
        assert parse_category("business") == TaskCategory.BUSINESS
        assert parse_category("personal") == TaskCategory.PERSONAL
        assert parse_category("educational") == TaskCategory.EDUCATIONAL
        
        # Test case insensitive
        assert parse_category("TECHNICAL") == TaskCategory.TECHNICAL
        assert parse_category("Creative") == TaskCategory.CREATIVE
    
    def test_create_planner_agent_with_config(self):
        """Test creating PlannerAgent with configuration."""
        from opius_planner.cli.main import create_planner_agent
        
        # Test with default config
        agent = create_planner_agent()
        assert agent is not None
        
        # Test with custom config (should handle gracefully if file doesn't exist)
        agent = create_planner_agent(config_path="nonexistent.yaml")
        assert agent is not None


class TestCLIIntegration:
    """Integration tests for CLI components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_end_to_end_plan_generation(self):
        """Test complete end-to-end plan generation workflow."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            # Create a realistic mock response
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            
            mock_plan = """# Python Web Application Development Plan

## 🎯 Project Overview
Build a Python web application with Flask framework.

## 🚀 Implementation Steps

- [ ] **Setup Development Environment** (2 hours)
  Configure Python, Flask, and development tools

- [ ] **Design Application Structure** (4 hours)  
  Plan the application architecture and database schema

- [ ] **Implement Core Features** (2 weeks)
  Build the main application functionality

## 📋 Resources
- **Python** (Required)
- **Flask Framework** (Required)
- **Database** (Required)
"""
            mock_instance.generate_plan.return_value = mock_plan
            
            result = self.runner.invoke(generate_plan, [
                'Build a Python web application with Flask'
            ])
            
            assert result.exit_code == 0
            assert "Python Web Application Development Plan" in result.output
            assert "Setup Development Environment" in result.output
            assert "Flask Framework" in result.output
    
    def test_cli_with_all_options(self):
        """Test CLI with comprehensive option usage."""
        with patch('opius_planner.cli.main.PlannerAgent') as mock_agent:
            mock_instance = Mock()
            mock_agent.return_value = mock_instance
            mock_instance.generate_plan.return_value = "# Comprehensive Plan\n\nDetailed content"
            
            with self.runner.isolated_filesystem():
                result = self.runner.invoke(generate_plan, [
                    'Create a comprehensive project',
                    '--template', 'technical',
                    '--complexity', 'high',
                    '--format', 'yaml-frontmatter',
                    '--output', 'comprehensive_plan.md',
                    '--agentic',
                    '--verbose'
                ])
                
                assert result.exit_code == 0
                assert "Plan saved to comprehensive_plan.md" in result.output
