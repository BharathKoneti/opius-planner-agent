"""
Unit tests for MarkdownGenerator - Following TDD approach.

Testing markdown formatting, agentic-friendly output format, and metadata support.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from opius_planner.templates.markdown_generator import (
    MarkdownGenerator,
    MarkdownSection,
    MarkdownMetadata,
    FrontmatterFormat,
    MarkdownFormatError
)
from opius_planner.core.plan_generator import ExecutionPlan, PlanMetadata, PlanStep
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestMarkdownGenerator:
    """Test suite for MarkdownGenerator following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.markdown_generator = MarkdownGenerator()
    
    def test_init_creates_generator_with_default_config(self):
        """Test that MarkdownGenerator initializes with proper defaults."""
        generator = MarkdownGenerator()
        assert generator is not None
        assert hasattr(generator, 'frontmatter_format')
        assert hasattr(generator, 'agentic_mode')
        assert generator.agentic_mode is True  # Default should be agentic-friendly
    
    def test_generate_markdown_from_execution_plan(self):
        """Test generating markdown from an ExecutionPlan object."""
        # Create mock execution plan
        metadata = Mock(spec=PlanMetadata)
        metadata.category = TaskCategory.TECHNICAL
        metadata.complexity = TaskComplexity.MEDIUM
        metadata.estimated_duration = "2-3 weeks"
        metadata.generated_at = datetime(2024, 1, 1, 12, 0, 0)
        
        steps = [
            Mock(spec=PlanStep, title="Setup Environment", description="Configure development setup", duration="2 hours"),
            Mock(spec=PlanStep, title="Implement Core", description="Build main functionality", duration="1 week")
        ]
        
        plan = Mock(spec=ExecutionPlan)
        plan.metadata = metadata
        plan.steps = steps
        plan.resources = []
        plan.notes = ["This is a test plan"]
        
        result = self.markdown_generator.generate_from_plan(plan)
        
        assert isinstance(result, str)
        assert "# " in result  # Should have title
        assert "Setup Environment" in result
        assert "Implement Core" in result
        assert "2-3 weeks" in result
    
    def test_generate_markdown_with_frontmatter(self):
        """Test generating markdown with YAML frontmatter."""
        metadata = MarkdownMetadata(
            title="Test Project Plan",
            category="technical",
            complexity="medium",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            tags=["python", "web", "api"]
        )
        
        content = "# Test Plan\n\nThis is a test plan."
        
        result = self.markdown_generator.generate_with_frontmatter(content, metadata)
        
        assert result.startswith("---")
        assert "title: Test Project Plan" in result
        assert "category: technical" in result
        assert "tags:" in result
        assert "- python" in result
        assert "# Test Plan" in result
    
    def test_generate_agentic_friendly_format(self):
        """Test generating agentic-friendly markdown format."""
        sections = [
            MarkdownSection(title="Overview", content="Project overview", level=2),
            MarkdownSection(title="Steps", content="Implementation steps", level=2),
            MarkdownSection(title="Resources", content="Required resources", level=2)
        ]
        
        result = self.markdown_generator.generate_agentic_format(
            title="AI-Friendly Project Plan",
            sections=sections,
            metadata={"complexity": "medium", "duration": "2 weeks"}
        )
        
        assert "# AI-Friendly Project Plan" in result
        assert "## Overview" in result
        assert "## Steps" in result
        assert "## Resources" in result
        # Should include agentic markers
        assert "<!-- AGENTIC:" in result or "**AGENTIC:" in result
    
    def test_format_execution_steps_as_checklist(self):
        """Test formatting execution steps as checkboxes for agentic processing."""
        steps = [
            Mock(spec=PlanStep, title="Setup", description="Setup environment", duration="1 hour"),
            Mock(spec=PlanStep, title="Development", description="Write code", duration="1 week"),
            Mock(spec=PlanStep, title="Testing", description="Run tests", duration="1 day")
        ]
        
        result = self.markdown_generator.format_steps_as_checklist(steps)
        
        assert "- [ ] Setup" in result
        assert "- [ ] Development" in result  
        assert "- [ ] Testing" in result
        assert "Setup environment" in result
        assert "1 hour" in result
    
    def test_add_metadata_comments_for_agents(self):
        """Test adding metadata comments that AI agents can parse."""
        content = "# Test Plan\n\nContent here."
        metadata = {
            "task_type": "technical",
            "complexity": "medium", 
            "tools_required": ["Python", "Git"],
            "estimated_hours": 40
        }
        
        result = self.markdown_generator.add_agentic_metadata(content, metadata)
        
        assert "<!-- AGENTIC_METADATA:" in result
        assert "task_type: technical" in result
        assert "tools_required: [Python, Git]" in result
        assert "estimated_hours: 40" in result
    
    def test_generate_table_of_contents(self):
        """Test generating table of contents from markdown content."""
        content = """# Main Title
        
## Section 1
Content here.

### Subsection 1.1
More content.

## Section 2
More content.

### Subsection 2.1
Even more content.
"""
        
        toc = self.markdown_generator.generate_table_of_contents(content)
        
        assert "- [Section 1](#section-1)" in toc
        assert "  - [Subsection 1.1](#subsection-1-1)" in toc
        assert "- [Section 2](#section-2)" in toc
        assert "  - [Subsection 2.1](#subsection-2-1)" in toc
    
    def test_format_resources_as_structured_list(self):
        """Test formatting resources as structured lists."""
        resources = [
            {"name": "Python", "type": "language", "required": True},
            {"name": "VS Code", "type": "editor", "required": False},
            {"name": "PostgreSQL", "type": "database", "required": True}
        ]
        
        result = self.markdown_generator.format_resources(resources)
        
        assert "## Required Resources" in result
        assert "### Languages" in result or "**Languages**" in result
        assert "- Python" in result
        assert "### Editors" in result or "**Editors**" in result
        assert "- VS Code (optional)" in result or "VS Code" in result
    
    def test_validate_markdown_syntax(self):
        """Test markdown syntax validation."""
        valid_markdown = """# Title
        
## Section

- List item
- Another item

**Bold text** and *italic text*.
"""
        
        invalid_markdown = """# Title
        
## Section

- List item
- Another item

**Bold text and *italic text without closing tags
"""
        
        assert self.markdown_generator.validate_syntax(valid_markdown) == True
        assert self.markdown_generator.validate_syntax(invalid_markdown) == False
    
    def test_convert_to_different_frontmatter_formats(self):
        """Test converting between different frontmatter formats."""
        yaml_content = """---
title: Test Plan
category: technical
tags:
  - python
  - web
---

# Content here
"""
        
        # Convert to TOML frontmatter
        toml_result = self.markdown_generator.convert_frontmatter(
            yaml_content, 
            target_format=FrontmatterFormat.TOML
        )
        
        assert "+++" in toml_result
        assert 'title = "Test Plan"' in toml_result
        assert 'category = "technical"' in toml_result
        
        # Convert to JSON frontmatter
        json_result = self.markdown_generator.convert_frontmatter(
            yaml_content,
            target_format=FrontmatterFormat.JSON
        )
        
        assert "```json" in json_result
        assert '"title": "Test Plan"' in json_result
    
    def test_optimize_for_agentic_parsing(self):
        """Test optimizing markdown for agentic/AI parsing."""
        regular_content = """# Project Plan

This is a plan for building something.

## Steps
1. Do this
2. Do that  
3. Finish

## Resources
- Tool A
- Tool B
"""
        
        optimized = self.markdown_generator.optimize_for_agents(regular_content)
        
        # Should add structured markers
        assert "<!-- PLAN_START -->" in optimized
        assert "<!-- STEPS_START -->" in optimized
        assert "<!-- RESOURCES_START -->" in optimized
        # Should convert numbered lists to checkboxes where appropriate
        assert "- [ ]" in optimized
    
    def test_error_handling_for_invalid_input(self):
        """Test error handling for invalid input."""
        with pytest.raises(MarkdownFormatError):
            self.markdown_generator.generate_from_plan(None)
        
        with pytest.raises(MarkdownFormatError):
            self.markdown_generator.generate_with_frontmatter("", None)
    
    def test_custom_markdown_templates(self):
        """Test using custom markdown templates."""
        custom_template = """# {{ title }}

**Category**: {{ category }}
**Complexity**: {{ complexity }}

## Overview
{{ overview }}

## Action Items
{% for step in steps %}
- [ ] {{ step.title }} ({{ step.duration }})
{% endfor %}
"""
        
        data = {
            "title": "Custom Plan",
            "category": "Technical",
            "complexity": "Medium",
            "overview": "This is a custom plan",
            "steps": [
                {"title": "Setup", "duration": "1 hour"},
                {"title": "Development", "duration": "1 week"}
            ]
        }
        
        result = self.markdown_generator.render_custom_template(custom_template, data)
        
        assert "# Custom Plan" in result
        assert "**Category**: Technical" in result
        assert "- [ ] Setup (1 hour)" in result
        assert "- [ ] Development (1 week)" in result


class TestMarkdownSection:
    """Test suite for MarkdownSection dataclass."""
    
    def test_markdown_section_creation(self):
        """Test MarkdownSection object creation."""
        section = MarkdownSection(
            title="Test Section",
            content="This is test content",
            level=2,
            metadata={"type": "overview"}
        )
        
        assert section.title == "Test Section"
        assert section.content == "This is test content"
        assert section.level == 2
        assert section.metadata["type"] == "overview"
    
    def test_section_to_markdown_conversion(self):
        """Test converting section to markdown format."""
        section = MarkdownSection(
            title="Implementation Steps",
            content="1. Setup\n2. Development\n3. Testing",
            level=2
        )
        
        markdown = section.to_markdown()
        
        assert "## Implementation Steps" in markdown
        assert "1. Setup" in markdown
        assert "2. Development" in markdown


class TestMarkdownMetadata:
    """Test suite for MarkdownMetadata dataclass."""
    
    def test_metadata_creation(self):
        """Test MarkdownMetadata object creation."""
        metadata = MarkdownMetadata(
            title="Test Plan",
            category="technical",
            complexity="high",
            created_at=datetime(2024, 1, 1),
            tags=["python", "api", "testing"],
            custom_fields={"author": "AI Agent", "version": "1.0"}
        )
        
        assert metadata.title == "Test Plan"
        assert metadata.category == "technical"
        assert "python" in metadata.tags
        assert metadata.custom_fields["author"] == "AI Agent"
    
    def test_metadata_to_yaml_conversion(self):
        """Test converting metadata to YAML format."""
        metadata = MarkdownMetadata(
            title="Test Plan",
            category="business",
            tags=["marketing", "strategy"]
        )
        
        yaml_str = metadata.to_yaml()
        
        assert "title: Test Plan" in yaml_str
        assert "category: business" in yaml_str
        assert "- marketing" in yaml_str


class TestFrontmatterFormat:
    """Test suite for FrontmatterFormat enum."""
    
    def test_frontmatter_format_values(self):
        """Test that FrontmatterFormat has expected values."""
        expected_formats = {'YAML', 'TOML', 'JSON'}
        actual_formats = {fmt.name for fmt in FrontmatterFormat}
        assert actual_formats == expected_formats
