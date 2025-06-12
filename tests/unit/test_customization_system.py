"""
Unit tests for Customization System - Following TDD approach.

Testing dynamic template modification, user preferences, and validation.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.templates.customization_system import (
    CustomizationEngine,
    TemplateCustomizer,
    UserPreferenceManager,
    TemplateValidator,
    CustomizationRule,
    UserPreference
)
from opius_planner.templates.template_engine import TemplateContext, Template
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestCustomizationEngine:
    """Test suite for CustomizationEngine following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.engine = CustomizationEngine()
    
    def test_init_loads_default_customizations(self):
        """Test that engine initializes with default customizations."""
        engine = CustomizationEngine()
        
        assert engine is not None
        assert hasattr(engine, 'customizer')
        assert hasattr(engine, 'preference_manager')
        assert hasattr(engine, 'validator')
    
    def test_apply_customization_to_template(self):
        """Test applying customizations to a template."""
        # Create a basic template
        template = Template(
            name="test_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }}\n\nBasic template content"
        )
        
        # Apply customization
        customized = self.engine.customize_template(
            template=template,
            user_id="user123",
            customizations={"add_tracker": True, "theme": "modern"}
        )
        
        assert customized is not None
        assert isinstance(customized, Template)
        assert "tracker" in customized.content.lower() or "progress" in customized.content.lower()
    
    def test_save_and_load_user_preferences(self):
        """Test saving and loading user preferences."""
        user_id = "user123"
        preferences = {
            "theme": "dark",
            "include_tracker": True,
            "default_complexity": "medium",
            "preferred_format": "detailed"
        }
        
        # Save preferences
        self.engine.save_user_preferences(user_id, preferences)
        
        # Load preferences
        loaded_prefs = self.engine.load_user_preferences(user_id)
        
        assert loaded_prefs is not None
        assert loaded_prefs["theme"] == "dark"
        assert loaded_prefs["include_tracker"] is True
    
    def test_validate_customized_template(self):
        """Test template validation after customization."""
        template = Template(
            name="test_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }}\n\nTemplate with {{ undefined_var }}"
        )
        
        # Validate template
        is_valid, errors = self.engine.validate_template(template)
        
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)


class TestTemplateCustomizer:
    """Test suite for TemplateCustomizer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.customizer = TemplateCustomizer()
    
    def test_add_tracker_functionality(self):
        """Test adding tracker functionality to templates."""
        template = Template(
            name="basic_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }}\n\nBasic content"
        )
        
        customized = self.customizer.add_tracker(template)
        
        assert customized is not None
        assert "tracker" in customized.content.lower()
        assert "progress" in customized.content.lower()
        assert "status" in customized.content.lower()
    
    def test_apply_theme_customization(self):
        """Test applying different themes to templates."""
        template = Template(
            name="basic_template",
            category=TaskCategory.CREATIVE,
            complexity=TaskComplexity.LOW,
            content="# {{ project_name }}\n\nBasic content"
        )
        
        # Test modern theme
        modern_template = self.customizer.apply_theme(template, "modern")
        assert modern_template is not None
        assert len(modern_template.content) > len(template.content)
        
        # Test minimalist theme
        minimal_template = self.customizer.apply_theme(template, "minimalist")
        assert minimal_template is not None
    
    def test_customize_complexity_level(self):
        """Test customizing template based on complexity preferences."""
        base_content = "# {{ project_name }}\n\nBasic content"
        
        # Test high complexity customization
        high_complex = self.customizer.adjust_complexity(
            base_content, TaskComplexity.VERY_HIGH
        )
        
        assert isinstance(high_complex, str)
        assert len(high_complex) > len(base_content)
        
        # Test low complexity customization
        low_complex = self.customizer.adjust_complexity(
            base_content, TaskComplexity.LOW
        )
        
        assert isinstance(low_complex, str)
    
    def test_add_custom_sections(self):
        """Test adding custom sections to templates."""
        template = Template(
            name="test_template",
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }}\n\nExisting content"
        )
        
        custom_sections = [
            {"title": "Risk Assessment", "content": "Risk analysis content"},
            {"title": "Budget Planning", "content": "Budget breakdown"}
        ]
        
        customized = self.customizer.add_custom_sections(template, custom_sections)
        
        assert customized is not None
        assert "Risk Assessment" in customized.content
        assert "Budget Planning" in customized.content


class TestUserPreferenceManager:
    """Test suite for UserPreferenceManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.pref_manager = UserPreferenceManager()
    
    def test_create_user_preference(self):
        """Test creating a new user preference."""
        user_id = "user123"
        preference = UserPreference(
            user_id=user_id,
            theme="dark",
            include_tracker=True,
            default_complexity=TaskComplexity.MEDIUM,
            preferred_sections=["overview", "timeline", "resources"]
        )
        
        # Save preference
        saved = self.pref_manager.save_preference(preference)
        
        assert saved is True
        
        # Retrieve preference
        retrieved = self.pref_manager.get_preference(user_id)
        
        assert retrieved is not None
        assert retrieved.theme == "dark"
        assert retrieved.include_tracker is True
    
    def test_update_user_preference(self):
        """Test updating an existing user preference."""
        user_id = "user456"
        
        # Create initial preference
        initial_pref = UserPreference(
            user_id=user_id,
            theme="light",
            include_tracker=False
        )
        self.pref_manager.save_preference(initial_pref)
        
        # Update preference
        updated_pref = UserPreference(
            user_id=user_id,
            theme="dark",
            include_tracker=True
        )
        self.pref_manager.update_preference(updated_pref)
        
        # Verify update
        retrieved = self.pref_manager.get_preference(user_id)
        assert retrieved.theme == "dark"
        assert retrieved.include_tracker is True
    
    def test_delete_user_preference(self):
        """Test deleting a user preference."""
        user_id = "user789"
        
        # Create preference
        preference = UserPreference(user_id=user_id, theme="light")
        self.pref_manager.save_preference(preference)
        
        # Delete preference
        deleted = self.pref_manager.delete_preference(user_id)
        assert deleted is True
        
        # Verify deletion
        retrieved = self.pref_manager.get_preference(user_id)
        assert retrieved is None
    
    def test_get_default_preferences(self):
        """Test getting default preferences for new users."""
        defaults = self.pref_manager.get_default_preferences()
        
        assert isinstance(defaults, dict)
        assert "theme" in defaults
        assert "include_tracker" in defaults
        assert "default_complexity" in defaults


class TestTemplateValidator:
    """Test suite for TemplateValidator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = TemplateValidator()
    
    def test_validate_template_syntax(self):
        """Test validating template syntax."""
        # Valid template
        valid_template = Template(
            name="valid_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }}\n\n{{ description }}"
        )
        
        is_valid, errors = self.validator.validate_syntax(valid_template)
        
        assert is_valid is True
        assert len(errors) == 0
        
        # Invalid template with syntax error
        invalid_template = Template(
            name="invalid_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }\n\n{{ description }}"  # Missing closing brace
        )
        
        is_valid, errors = self.validator.validate_syntax(invalid_template)
        
        assert is_valid is False
        assert len(errors) > 0
    
    def test_validate_required_variables(self):
        """Test validating required template variables."""
        template = Template(
            name="test_template",
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.HIGH,
            content="# {{ project_name }}\n\n{{ description }}\n\n{{ timeline }}",
            variables=["project_name", "description", "timeline"]
        )
        
        # Test with all required variables
        context = TemplateContext(
            project_name="Test Project",
            description="Test description",
            timeline="2 weeks"
        )
        
        is_valid, missing = self.validator.validate_required_variables(template, context)
        
        assert is_valid is True
        assert len(missing) == 0
        
        # Test with missing variables
        incomplete_context = TemplateContext(
            project_name="Test Project"
        )
        
        is_valid, missing = self.validator.validate_required_variables(template, incomplete_context)
        
        assert is_valid is False
        assert len(missing) > 0
        assert "description" in missing
    
    def test_validate_template_structure(self):
        """Test validating overall template structure."""
        # Well-structured template
        good_template = Template(
            name="good_template",
            category=TaskCategory.CREATIVE,
            complexity=TaskComplexity.MEDIUM,
            content="""# {{ project_name }}

## Overview
{{ description }}

## Timeline
{{ timeline }}

## Success Criteria
- Criterion 1
- Criterion 2"""
        )
        
        is_valid, issues = self.validator.validate_structure(good_template)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_customization_rules(self):
        """Test validating customization rules."""
        rule = CustomizationRule(
            name="add_tracker_rule",
            condition={"include_tracker": True},
            action="add_section",
            parameters={"section_name": "Progress Tracker"}
        )
        
        is_valid, errors = self.validator.validate_customization_rule(rule)
        
        assert is_valid is True
        assert len(errors) == 0


class TestCustomizationRule:
    """Test suite for CustomizationRule."""
    
    def test_create_customization_rule(self):
        """Test creating a customization rule."""
        rule = CustomizationRule(
            name="theme_rule",
            condition={"theme": "dark"},
            action="apply_theme",
            parameters={"theme_name": "dark", "colors": {"bg": "#000", "text": "#fff"}}
        )
        
        assert rule.name == "theme_rule"
        assert rule.condition["theme"] == "dark"
        assert rule.action == "apply_theme"
        assert rule.parameters["theme_name"] == "dark"
    
    def test_evaluate_rule_condition(self):
        """Test evaluating rule conditions."""
        rule = CustomizationRule(
            name="complexity_rule",
            condition={"complexity": "high", "category": "technical"},
            action="add_detailed_sections"
        )
        
        # Test matching context
        matching_context = {"complexity": "high", "category": "technical"}
        assert rule.matches_condition(matching_context) is True
        
        # Test non-matching context
        non_matching_context = {"complexity": "low", "category": "creative"}
        assert rule.matches_condition(non_matching_context) is False
    
    def test_apply_rule_action(self):
        """Test applying rule actions."""
        rule = CustomizationRule(
            name="tracker_rule",
            condition={"include_tracker": True},
            action="add_tracker_section"
        )
        
        base_content = "# Project\n\nBasic content"
        result = rule.apply_action(base_content)
        
        assert isinstance(result, str)
        assert len(result) > len(base_content)


class TestCustomizationIntegration:
    """Integration tests for the customization system."""
    
    def test_end_to_end_customization_workflow(self):
        """Test complete customization workflow."""
        # Create customization engine
        engine = CustomizationEngine()
        
        # Create base template
        template = Template(
            name="integration_test_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.HIGH,
            content="# {{ project_name }}\n\n{{ description }}"
        )
        
        # Set user preferences
        user_id = "integration_user"
        preferences = {
            "theme": "modern",
            "include_tracker": True,
            "detailed_sections": True
        }
        engine.save_user_preferences(user_id, preferences)
        
        # Apply customizations
        customized = engine.customize_template(
            template=template,
            user_id=user_id,
            customizations={"add_sections": ["timeline", "resources"]}
        )
        
        # Validate result
        assert customized is not None
        assert isinstance(customized, Template)
        assert len(customized.content) > len(template.content)
        
        # Validate customized template
        is_valid, errors = engine.validate_template(customized)
        assert is_valid is True
        assert len(errors) == 0
