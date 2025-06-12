"""
Content Generation System - Phase 2.3 Implementation.

Provides context-aware content generation, multi-format output support,
template inheritance, and quality assurance automation.
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from copy import deepcopy

from ..core.task_analyzer import TaskCategory, TaskComplexity
from .template_engine import Template, TemplateContext


class ContextAnalyzer:
    """Analyzes context to determine content generation strategy."""
    
    def analyze_context(self, context: TemplateContext) -> Dict[str, Any]:
        """Analyze context for content generation."""
        context_dict = context.to_dict()
        
        # Determine domain based on context
        domain = "business"
        if any(key in context_dict for key in ["tech_stack", "programming", "api", "database"]):
            domain = "technical"
        elif any(key in context_dict for key in ["creative", "design", "story", "content"]):
            domain = "creative"
        
        return {
            "domain": domain,
            "complexity_indicators": self._assess_complexity(context_dict),
            "content_requirements": self._determine_requirements(context_dict)
        }
    
    def _assess_complexity(self, context_dict: Dict) -> List[str]:
        """Assess complexity indicators from context."""
        indicators = []
        if context_dict.get("complexity") == "high":
            indicators.append("high_complexity")
        if len(str(context_dict.get("description", ""))) > 100:
            indicators.append("detailed_description")
        return indicators
    
    def _determine_requirements(self, context_dict: Dict) -> Dict[str, Any]:
        """Determine content requirements."""
        return {
            "sections": ["overview", "timeline", "success_criteria"],
            "detail_level": "medium",
            "special_considerations": []
        }
    
    def extract_requirements(self, context: TemplateContext) -> Dict[str, Any]:
        """Extract content requirements from context."""
        return self._determine_requirements(context.to_dict())
    
    def determine_strategy(self, context: TemplateContext) -> Dict[str, Any]:
        """Determine content generation strategy."""
        return {
            "approach": "structured",
            "focus_areas": ["main_content", "supporting_details"],
            "content_depth": "medium"
        }
    
    def analyze_stakeholders(self, context: TemplateContext) -> Dict[str, Any]:
        """Analyze stakeholder needs."""
        return {
            "primary_audience": "general",
            "communication_preferences": "clear_and_structured",
            "content_priorities": ["accuracy", "completeness"]
        }


class MultiFormatOutputManager:
    """Manages multi-format output generation."""
    
    def to_markdown(self, content: Dict[str, Any]) -> str:
        """Convert content to markdown format."""
        markdown = f"# {content.get('title', 'Untitled')}\n\n"
        
        if 'sections' in content:
            for section in content['sections']:
                markdown += f"## {section['heading']}\n{section['content']}\n\n"
        
        return markdown.strip()
    
    def to_json(self, content: Dict[str, Any]) -> str:
        """Convert content to JSON format."""
        return json.dumps(content, indent=2)
    
    def to_html(self, content: Dict[str, Any]) -> str:
        """Convert content to HTML format."""
        html = f"<html><head><title>{content.get('title', 'Document')}</title></head><body>\n"
        html += f"<h1>{content.get('title', 'Document')}</h1>\n"
        
        if 'body' in content:
            html += f"<p>{content['body']}</p>\n"
        
        html += "</body></html>"
        return html
    
    def generate_pdf_metadata(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PDF metadata for content."""
        return {
            "title": content.get('title', 'Document'),
            "metadata": {
                "author": content.get('author', 'Unknown'),
                "pages": content.get('pages', 1)
            },
            "formatting": {
                "font": "Arial",
                "size": 12
            }
        }
    
    def format_for_audience(self, content: str, audience: str) -> str:
        """Format content for different audiences."""
        if audience == "executive":
            # Simplify for executives
            return content[:len(content)//2] + "\n\n[Summary for executive audience]"
        elif audience == "developer":
            # Keep detailed for developers
            return content + "\n\n[Technical implementation details]"
        return content


class TemplateInheritanceSystem:
    """Manages template inheritance and composition."""
    
    def create_base_template(self, name: str, common_sections: List[str]) -> Template:
        """Create a base template for inheritance."""
        content = f"# {{{{ project_name | default('{name}') }}}}\n\n"
        
        for section in common_sections:
            content += f"## {section.title()}\n{{{{ {section} | default('TBD') }}}}\n\n"
        
        return Template(
            name=name,
            category=TaskCategory.BUSINESS,
            complexity=TaskComplexity.MEDIUM,
            content=content
        )
    
    def extend_template(self, base_template: Template, extension_name: str, 
                       additional_sections: Dict[str, str]) -> Template:
        """Extend a base template with additional content."""
        extended = deepcopy(base_template)
        extended.name = extension_name
        
        for section_name, section_content in additional_sections.items():
            extended.content += f"## {section_name.replace('_', ' ').title()}\n{section_content}\n\n"
        
        return extended
    
    def compose_templates(self, templates: List[Template], composition_name: str) -> Template:
        """Compose multiple templates together."""
        composed_content = ""
        
        for i, template in enumerate(templates):
            if i > 0:
                composed_content += "\n---\n\n"
            composed_content += template.content
        
        return Template(
            name=composition_name,
            category=templates[0].category if templates else TaskCategory.BUSINESS,
            complexity=templates[0].complexity if templates else TaskComplexity.MEDIUM,
            content=composed_content
        )
    
    def resolve_inheritance(self, parent: Template, child: Template, 
                           resolution_strategy: str = "child_overrides") -> Template:
        """Resolve template inheritance conflicts."""
        if resolution_strategy == "child_overrides":
            resolved = deepcopy(child)
            # Keep child content but inherit parent structure if needed
            if len(child.content) < len(parent.content):
                resolved.content = parent.content + "\n\n" + child.content
        else:
            resolved = deepcopy(parent)
        
        return resolved


class QualityAssuranceEngine:
    """Provides quality assurance for generated content."""
    
    def assess_quality(self, content: str) -> float:
        """Assess overall content quality."""
        score = 50.0  # Base score
        
        # Length check
        if len(content) > 200:
            score += 20
        
        # Structure check
        if content.count('#') >= 2:
            score += 15
        
        # Content variety check
        if len(content.split('\n')) > 5:
            score += 15
        
        return min(score, 100.0)
    
    def check_completeness(self, content: str) -> float:
        """Check content completeness."""
        completeness = 30.0  # Base score
        
        # Check for sections
        sections = content.count('##')
        completeness += min(sections * 15, 60)
        
        # Check for content depth
        if len(content) > 500:
            completeness += 10
        
        return min(completeness, 100.0)
    
    def validate_structure(self, content: str) -> float:
        """Validate content structure quality."""
        structure_score = 40.0
        
        # Check header hierarchy
        if content.startswith('#'):
            structure_score += 20
        
        # Check for proper markdown structure
        if '##' in content:
            structure_score += 20
        
        # Check for bullet points or lists
        if '-' in content or '*' in content:
            structure_score += 20
        
        return min(structure_score, 100.0)
    
    def check_consistency(self, content: str) -> float:
        """Check content consistency."""
        # Simple consistency check based on term repetition
        words = content.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only check significant words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Higher consistency if key terms are repeated appropriately
        repeated_terms = sum(1 for freq in word_freq.values() if freq > 1)
        consistency = min(repeated_terms * 10, 80) + 20
        
        return min(consistency, 100.0)
    
    def generate_improvement_suggestions(self, content: str) -> List[str]:
        """Generate automated improvement suggestions."""
        suggestions = []
        
        if not content.startswith('#'):
            suggestions.append("Add a main title with # heading")
        
        if content.count('##') < 2:
            suggestions.append("Add more section headings with ## for better structure")
        
        if len(content) < 200:
            suggestions.append("Expand content with more detailed information")
        
        if not any(char in content for char in ['-', '*', '1.']):
            suggestions.append("Add bullet points or numbered lists for better readability")
        
        return suggestions


class ContentGenerator:
    """Main content generation engine."""
    
    def __init__(self):
        """Initialize the content generator."""
        self.context_analyzer = ContextAnalyzer()
        self.output_manager = MultiFormatOutputManager()
        self.inheritance_system = TemplateInheritanceSystem()
        self.quality_engine = QualityAssuranceEngine()
    
    def generate_content(self, template_type: str, context: TemplateContext, 
                        output_format: str = "markdown", complexity: TaskComplexity = None) -> str:
        """Generate context-aware content."""
        # Analyze context
        analysis = self.context_analyzer.analyze_context(context)
        
        # Generate base content structure
        content_data = {
            "title": context.to_dict().get("project_name", "Project"),
            "sections": [
                {"heading": "Overview", "content": f"This is a {template_type} project."},
                {"heading": "Requirements", "content": "Project requirements will be defined here."},
                {"heading": "Timeline", "content": "Project timeline and milestones."}
            ]
        }
        
        # Adjust for complexity
        if complexity == TaskComplexity.VERY_HIGH:
            content_data["sections"].extend([
                {"heading": "Detailed Analysis", "content": "Comprehensive analysis section."},
                {"heading": "Risk Assessment", "content": "Risk analysis and mitigation strategies."}
            ])
        
        # Convert to requested format
        if output_format == "markdown":
            return self.output_manager.to_markdown(content_data)
        elif output_format == "json":
            return self.output_manager.to_json(content_data)
        elif output_format == "html":
            return self.output_manager.to_html(content_data)
        
        return str(content_data)
    
    def generate_with_quality_check(self, template_type: str, context: TemplateContext) -> Tuple[str, float]:
        """Generate content with quality assurance."""
        content = self.generate_content(template_type, context)
        quality_score = self.quality_engine.assess_quality(content)
        
        return content, quality_score
    
    def generate_multi_format_content(self, template_type: str, context: TemplateContext, 
                                    output_formats: List[str]) -> Dict[str, str]:
        """Generate content in multiple formats."""
        results = {}
        
        for format_name in output_formats:
            results[format_name] = self.generate_content(template_type, context, format_name)
        
        return results
