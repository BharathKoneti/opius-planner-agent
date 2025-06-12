"""
Unit tests for Content Generation System - Following TDD approach.

Testing context-aware content generation, multi-format output support,
template inheritance, and quality assurance automation.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.templates.content_generation import (
    ContentGenerator,
    ContextAnalyzer,
    MultiFormatOutputManager,
    TemplateInheritanceSystem,
    QualityAssuranceEngine
)
from opius_planner.templates.template_engine import TemplateContext, Template
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestContentGenerator:
    """Test suite for ContentGenerator following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.generator = ContentGenerator()
    
    def test_init_loads_content_engine(self):
        """Test that generator initializes with content engine."""
        generator = ContentGenerator()
        
        assert generator is not None
        assert hasattr(generator, 'context_analyzer')
        assert hasattr(generator, 'output_manager')
        assert hasattr(generator, 'inheritance_system')
        assert hasattr(generator, 'quality_engine')
    
    def test_generate_contextual_content(self):
        """Test generating context-aware content."""
        context = TemplateContext(
            project_name="AI Chat Application",
            category="technical",
            complexity="high",
            target_users="Developers and businesses",
            key_technologies=["Python", "FastAPI", "React", "OpenAI API"]
        )
        
        content = self.generator.generate_content(
            template_type="software_development",
            context=context,
            output_format="markdown"
        )
        
        assert isinstance(content, str)
        assert "AI Chat Application" in content
        assert "Python" in content or "FastAPI" in content
        assert len(content) > 100  # Should generate substantial content
    
    def test_generate_adaptive_content_complexity(self):
        """Test that content adapts to complexity level."""
        base_context = TemplateContext(
            project_name="Test Project",
            description="A test project"
        )
        
        # Generate for different complexity levels
        simple_content = self.generator.generate_content(
            template_type="business_plan",
            context=base_context,
            complexity=TaskComplexity.LOW
        )
        
        complex_content = self.generator.generate_content(
            template_type="business_plan",
            context=base_context,
            complexity=TaskComplexity.VERY_HIGH
        )
        
        assert isinstance(simple_content, str)
        assert isinstance(complex_content, str)
        assert len(complex_content) > len(simple_content)
    
    def test_generate_with_quality_checks(self):
        """Test content generation with quality assurance."""
        context = TemplateContext(
            project_name="Quality Test Project",
            requirements=["High quality", "Well structured", "Comprehensive"]
        )
        
        content, quality_score = self.generator.generate_with_quality_check(
            template_type="technical_specification",
            context=context
        )
        
        assert isinstance(content, str)
        assert isinstance(quality_score, (int, float))
        assert 0 <= quality_score <= 100


class TestContextAnalyzer:
    """Test suite for ContextAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ContextAnalyzer()
    
    def test_analyze_project_context(self):
        """Test analyzing project context for content generation."""
        context = TemplateContext(
            project_name="E-commerce Platform",
            industry="Retail Technology",
            target_market="Online shoppers",
            business_model="B2C marketplace",
            key_features=["Product catalog", "Payment processing", "User reviews"]
        )
        
        analysis = self.analyzer.analyze_context(context)
        
        assert isinstance(analysis, dict)
        assert "domain" in analysis
        assert "complexity_indicators" in analysis
        assert "content_requirements" in analysis
        assert analysis["domain"] in ["business", "technical", "creative"]
    
    def test_extract_content_requirements(self):
        """Test extracting content requirements from context."""
        context = TemplateContext(
            project_type="mobile_app",
            platform="iOS/Android",
            timeline="3 months",
            team_size=5,
            budget="$100k"
        )
        
        requirements = self.analyzer.extract_requirements(context)
        
        assert isinstance(requirements, dict)
        assert "sections" in requirements
        assert "detail_level" in requirements
        assert "special_considerations" in requirements
    
    def test_determine_content_strategy(self):
        """Test determining content generation strategy."""
        technical_context = TemplateContext(
            category="technical",
            complexity="high",
            project_type="enterprise_software"
        )
        
        strategy = self.analyzer.determine_strategy(technical_context)
        
        assert isinstance(strategy, dict)
        assert "approach" in strategy
        assert "focus_areas" in strategy
        assert "content_depth" in strategy
    
    def test_analyze_stakeholder_needs(self):
        """Test analyzing stakeholder needs from context."""
        context = TemplateContext(
            stakeholders=["Product Manager", "Engineering Team", "End Users"],
            primary_audience="Engineering Team",
            communication_style="Technical and detailed"
        )
        
        stakeholder_analysis = self.analyzer.analyze_stakeholders(context)
        
        assert isinstance(stakeholder_analysis, dict)
        assert "primary_audience" in stakeholder_analysis
        assert "communication_preferences" in stakeholder_analysis
        assert "content_priorities" in stakeholder_analysis


class TestMultiFormatOutputManager:
    """Test suite for MultiFormatOutputManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.output_manager = MultiFormatOutputManager()
    
    def test_convert_to_markdown(self):
        """Test converting content to markdown format."""
        base_content = {
            "title": "Project Plan",
            "sections": [
                {"heading": "Overview", "content": "Project overview content"},
                {"heading": "Timeline", "content": "Timeline details"}
            ]
        }
        
        markdown = self.output_manager.to_markdown(base_content)
        
        assert isinstance(markdown, str)
        assert "# Project Plan" in markdown
        assert "## Overview" in markdown
        assert "## Timeline" in markdown
    
    def test_convert_to_json(self):
        """Test converting content to JSON format."""
        base_content = {
            "project": "Test Project",
            "phases": ["Planning", "Development", "Testing"]
        }
        
        json_output = self.output_manager.to_json(base_content)
        
        assert isinstance(json_output, str)
        # Should be valid JSON
        import json
        parsed = json.loads(json_output)
        assert parsed["project"] == "Test Project"
        assert "phases" in parsed
    
    def test_convert_to_html(self):
        """Test converting content to HTML format."""
        base_content = {
            "title": "Project Documentation",
            "body": "Main content with **bold** and *italic* text"
        }
        
        html_output = self.output_manager.to_html(base_content)
        
        assert isinstance(html_output, str)
        assert "<h1>" in html_output or "<title>" in html_output
        assert "<p>" in html_output or "<div>" in html_output
    
    def test_convert_to_pdf_metadata(self):
        """Test generating PDF metadata for content."""
        content = {
            "title": "Technical Specification",
            "author": "Development Team",
            "pages": 25
        }
        
        pdf_meta = self.output_manager.generate_pdf_metadata(content)
        
        assert isinstance(pdf_meta, dict)
        assert "title" in pdf_meta
        assert "metadata" in pdf_meta
        assert "formatting" in pdf_meta
    
    def test_format_for_different_audiences(self):
        """Test formatting content for different audiences."""
        base_content = "Technical implementation details with complex algorithms"
        
        # Format for executives
        exec_format = self.output_manager.format_for_audience(
            base_content, "executive"
        )
        
        # Format for developers
        dev_format = self.output_manager.format_for_audience(
            base_content, "developer"
        )
        
        assert isinstance(exec_format, str)
        assert isinstance(dev_format, str)
        # Executive format should be more high-level
        assert len(dev_format) >= len(exec_format)


class TestTemplateInheritanceSystem:
    """Test suite for TemplateInheritanceSystem."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.inheritance_system = TemplateInheritanceSystem()
    
    def test_create_base_template(self):
        """Test creating a base template for inheritance."""
        base_template = self.inheritance_system.create_base_template(
            name="project_base",
            common_sections=["overview", "timeline", "success_criteria"]
        )
        
        assert isinstance(base_template, Template)
        assert base_template.name == "project_base"
        assert "overview" in base_template.content.lower()
        assert "timeline" in base_template.content.lower()
    
    def test_extend_template(self):
        """Test extending a base template with specific content."""
        base_template = Template(
            name="base_template",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.MEDIUM,
            content="# {{ project_name }}\n\n## Base Section\nBase content"
        )
        
        extended = self.inheritance_system.extend_template(
            base_template=base_template,
            extension_name="technical_extension",
            additional_sections={
                "technical_requirements": "Technical requirements content",
                "architecture": "System architecture details"
            }
        )
        
        assert isinstance(extended, Template)
        assert "Base Section" in extended.content
        assert "technical_requirements" in extended.content.lower()
        assert "architecture" in extended.content.lower()
    
    def test_compose_multiple_templates(self):
        """Test composing multiple templates together."""
        template1 = Template(
            name="template1",
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.MEDIUM,
            content="# Template 1\n\nContent from template 1"
        )
        
        template2 = Template(
            name="template2", 
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.MEDIUM,
            content="# Template 2\n\nContent from template 2"
        )
        
        composed = self.inheritance_system.compose_templates(
            templates=[template1, template2],
            composition_name="composed_template"
        )
        
        assert isinstance(composed, Template)
        assert "Template 1" in composed.content
        assert "Template 2" in composed.content
        assert composed.name == "composed_template"
    
    def test_template_hierarchy_resolution(self):
        """Test resolving template hierarchy and conflicts."""
        parent_template = Template(
            name="parent",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.HIGH,
            content="# Parent\n\n## Common Section\nParent content"
        )
        
        child_template = Template(
            name="child",
            category=TaskCategory.TECHNICAL,
            complexity=TaskComplexity.HIGH,
            content="# Child\n\n## Common Section\nChild content\n\n## Child Only\nChild-specific content"
        )
        
        resolved = self.inheritance_system.resolve_inheritance(
            parent=parent_template,
            child=child_template,
            resolution_strategy="child_overrides"
        )
        
        assert isinstance(resolved, Template)
        assert "Child content" in resolved.content
        assert "Child Only" in resolved.content


class TestQualityAssuranceEngine:
    """Test suite for QualityAssuranceEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.quality_engine = QualityAssuranceEngine()
    
    def test_assess_content_quality(self):
        """Test assessing overall content quality."""
        high_quality_content = """# Professional Project Plan

## Executive Summary
This comprehensive project plan outlines the development of a modern web application.

## Technical Architecture
The system will utilize microservices architecture with containerized deployment.

## Timeline and Milestones
- Phase 1: Requirements Analysis (2 weeks)
- Phase 2: Design and Architecture (3 weeks)
- Phase 3: Development (8 weeks)
- Phase 4: Testing and QA (2 weeks)

## Success Criteria
- All functional requirements implemented
- Performance benchmarks met
- Security standards compliance achieved"""
        
        quality_score = self.quality_engine.assess_quality(high_quality_content)
        
        assert isinstance(quality_score, (int, float))
        assert 0 <= quality_score <= 100
        assert quality_score > 50  # Should be decent quality
    
    def test_check_content_completeness(self):
        """Test checking content completeness."""
        incomplete_content = "# Project\n\nBasic content"
        complete_content = """# Project Plan

## Overview
Detailed project overview

## Requirements
Comprehensive requirements

## Timeline
Detailed timeline

## Resources
Resource allocation

## Success Criteria
Clear success metrics"""
        
        incomplete_score = self.quality_engine.check_completeness(incomplete_content)
        complete_score = self.quality_engine.check_completeness(complete_content)
        
        assert isinstance(incomplete_score, (int, float))
        assert isinstance(complete_score, (int, float))
        assert complete_score > incomplete_score
    
    def test_validate_structure_quality(self):
        """Test validating content structure quality."""
        well_structured = """# Main Title

## Section 1
Content for section 1

### Subsection 1.1
Detailed content

## Section 2
Content for section 2

### Subsection 2.1
More detailed content"""
        
        poorly_structured = "Title\nSome content\nMore content\nRandom text"
        
        good_score = self.quality_engine.validate_structure(well_structured)
        poor_score = self.quality_engine.validate_structure(poorly_structured)
        
        assert isinstance(good_score, (int, float))
        assert isinstance(poor_score, (int, float))
        assert good_score > poor_score
    
    def test_check_consistency(self):
        """Test checking content consistency."""
        consistent_content = """# E-commerce Platform

## Overview
This e-commerce platform will serve online retailers.

## Features
The e-commerce platform includes:
- Product catalog management
- Shopping cart functionality
- Payment processing

## Technical Requirements
The e-commerce platform requires:
- Scalable architecture
- Secure payment processing"""
        
        consistency_score = self.quality_engine.check_consistency(consistent_content)
        
        assert isinstance(consistency_score, (int, float))
        assert 0 <= consistency_score <= 100
    
    def test_automated_improvement_suggestions(self):
        """Test generating automated improvement suggestions."""
        content_to_improve = """# project

basic content with no structure

some more text"""
        
        suggestions = self.quality_engine.generate_improvement_suggestions(content_to_improve)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        # Should suggest structural improvements
        assert any("structure" in suggestion.lower() or "heading" in suggestion.lower() 
                  for suggestion in suggestions)


class TestContentGenerationIntegration:
    """Integration tests for the content generation system."""
    
    def test_end_to_end_content_generation(self):
        """Test complete content generation workflow."""
        generator = ContentGenerator()
        
        context = TemplateContext(
            project_name="Mobile Banking App",
            category="technical",
            complexity="very_high",
            platform="iOS/Android",
            target_users="Bank customers",
            key_features=["Account management", "Money transfers", "Bill payments"],
            security_requirements=["Two-factor authentication", "Encryption", "Biometric login"]
        )
        
        # Generate content with multiple outputs
        results = generator.generate_multi_format_content(
            template_type="mobile_development",
            context=context,
            output_formats=["markdown", "json", "html"]
        )
        
        assert isinstance(results, dict)
        assert "markdown" in results
        assert "json" in results
        assert "html" in results
        
        # Each format should contain the project name
        for format_name, content in results.items():
            assert isinstance(content, str)
            assert "Mobile Banking App" in content
    
    def test_inheritance_with_quality_assurance(self):
        """Test template inheritance combined with quality assurance."""
        generator = ContentGenerator()
        inheritance_system = TemplateInheritanceSystem()
        
        # Create base template
        base_template = inheritance_system.create_base_template(
            name="software_base",
            common_sections=["overview", "requirements", "timeline"]
        )
        
        # Extend with specific content
        mobile_template = inheritance_system.extend_template(
            base_template=base_template,
            extension_name="mobile_extension",
            additional_sections={
                "platform_requirements": "iOS and Android compatibility",
                "app_store_guidelines": "Compliance with store policies"
            }
        )
        
        # Generate content and check quality
        context = TemplateContext(
            project_name="Quality Test App",
            description="Testing quality assurance integration"
        )
        
        content = mobile_template.render(context)
        quality_engine = QualityAssuranceEngine()
        quality_score = quality_engine.assess_quality(content)
        
        assert isinstance(content, str)
        assert isinstance(quality_score, (int, float))
        assert quality_score > 0
