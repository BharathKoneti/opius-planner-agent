"""
MarkdownGenerator - Markdown formatting and agentic-friendly output system.

This module provides intelligent markdown generation capabilities including:
- Agentic-friendly markdown formatting
- YAML/TOML/JSON frontmatter support
- Structured output for AI parsing
- Execution plan to markdown conversion
"""

import re
import json
import yaml
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from jinja2 import Environment, BaseLoader, Template

from ..core.plan_generator import ExecutionPlan, PlanStep, PlanMetadata


class MarkdownFormatError(Exception):
    """Custom exception for markdown formatting errors."""
    pass


class FrontmatterFormat(Enum):
    """Supported frontmatter formats."""
    YAML = "yaml"
    TOML = "toml"
    JSON = "json"


@dataclass
class MarkdownSection:
    """Represents a section in markdown document."""
    title: str
    content: str
    level: int = 2
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_markdown(self) -> str:
        """Convert section to markdown format."""
        header = "#" * self.level + " " + self.title
        return f"{header}\n\n{self.content}\n"


@dataclass
class MarkdownMetadata:
    """Metadata for markdown documents."""
    title: str
    category: Optional[str] = None
    complexity: Optional[str] = None
    created_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def to_yaml(self) -> str:
        """Convert metadata to YAML format."""
        data = {
            "title": self.title,
            "category": self.category,
            "complexity": self.complexity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tags": self.tags
        }
        
        # Add custom fields
        data.update(self.custom_fields)
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        return yaml.dump(data, default_flow_style=False)
    
    def to_toml(self) -> str:
        """Convert metadata to TOML format."""
        lines = []
        lines.append(f'title = "{self.title}"')
        
        if self.category:
            lines.append(f'category = "{self.category}"')
        if self.complexity:
            lines.append(f'complexity = "{self.complexity}"')
        if self.created_at:
            lines.append(f'created_at = "{self.created_at.isoformat()}"')
        
        if self.tags:
            tags_str = ', '.join([f'"{tag}"' for tag in self.tags])
            lines.append(f'tags = [{tags_str}]')
        
        # Add custom fields
        for key, value in self.custom_fields.items():
            if isinstance(value, str):
                lines.append(f'{key} = "{value}"')
            elif isinstance(value, (int, float, bool)):
                lines.append(f'{key} = {value}')
            elif isinstance(value, list):
                list_str = ', '.join([f'"{item}"' for item in value])
                lines.append(f'{key} = [{list_str}]')
        
        return '\n'.join(lines)
    
    def to_json(self) -> str:
        """Convert metadata to JSON format."""
        data = {
            "title": self.title,
            "category": self.category,
            "complexity": self.complexity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tags": self.tags
        }
        
        # Add custom fields
        data.update(self.custom_fields)
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        return json.dumps(data, indent=2)


class MarkdownGenerator:
    """Markdown generation and formatting engine."""
    
    def __init__(self, agentic_mode: bool = True, frontmatter_format: FrontmatterFormat = FrontmatterFormat.YAML):
        """Initialize the MarkdownGenerator."""
        self.agentic_mode = agentic_mode
        self.frontmatter_format = frontmatter_format
        
        # Initialize Jinja2 environment for custom templates
        self.jinja_env = Environment(
            loader=BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_from_plan(self, plan: ExecutionPlan) -> str:
        """Generate markdown from an ExecutionPlan object."""
        if plan is None:
            raise MarkdownFormatError("ExecutionPlan cannot be None")
        
        sections = []
        
        # Title and overview
        title = getattr(plan.metadata, 'task_description', 'Project Plan')
        sections.append(f"# {title}\n")
        
        # Metadata section
        if hasattr(plan.metadata, 'category'):
            sections.append(f"**Category**: {plan.metadata.category.value.title()}")
        if hasattr(plan.metadata, 'complexity'):
            sections.append(f"**Complexity**: {plan.metadata.complexity.name.title()}")
        if hasattr(plan.metadata, 'estimated_duration'):
            sections.append(f"**Duration**: {plan.metadata.estimated_duration}")
        
        sections.append("")
        
        # Steps section
        if plan.steps:
            sections.append("## 🚀 Implementation Steps\n")
            
            if self.agentic_mode:
                sections.append("<!-- STEPS_START -->")
            
            for i, step in enumerate(plan.steps, 1):
                if self.agentic_mode:
                    sections.append(f"- [ ] **{step.title}** ({step.duration})")
                    sections.append(f"  {step.description}")
                else:
                    sections.append(f"### {i}. {step.title}")
                    sections.append(f"**Duration**: {step.duration}")
                    sections.append(f"{step.description}")
                sections.append("")
            
            if self.agentic_mode:
                sections.append("<!-- STEPS_END -->")
        
        # Resources section
        if plan.resources:
            sections.append("## 📋 Resources\n")
            
            if self.agentic_mode:
                sections.append("<!-- RESOURCES_START -->")
            
            for resource in plan.resources:
                req_text = " (Required)" if resource.required else " (Optional)"
                sections.append(f"- **{resource.name}**{req_text}")
                if resource.installation_guide:
                    sections.append(f"  {resource.installation_guide}")
            
            if self.agentic_mode:
                sections.append("<!-- RESOURCES_END -->")
        
        # Notes section
        if plan.notes:
            sections.append("## 📝 Notes\n")
            for note in plan.notes:
                sections.append(f"- {note}")
        
        return "\n".join(sections)
    
    def generate_with_frontmatter(self, content: str, metadata: MarkdownMetadata) -> str:
        """Generate markdown with frontmatter."""
        if not content or metadata is None:
            raise MarkdownFormatError("Content and metadata cannot be empty/None")
        
        if self.frontmatter_format == FrontmatterFormat.YAML:
            frontmatter = "---\n" + metadata.to_yaml() + "---\n\n"
        elif self.frontmatter_format == FrontmatterFormat.TOML:
            frontmatter = "+++\n" + metadata.to_toml() + "\n+++\n\n"
        elif self.frontmatter_format == FrontmatterFormat.JSON:
            frontmatter = "```json\n" + metadata.to_json() + "\n```\n\n"
        else:
            frontmatter = ""
        
        return frontmatter + content
    
    def generate_agentic_format(self, title: str, sections: List[MarkdownSection], metadata: Dict[str, Any] = None) -> str:
        """Generate agentic-friendly markdown format."""
        lines = []
        
        # Add agentic markers
        lines.append("<!-- AGENTIC_PLAN_START -->")
        lines.append(f"# {title}")
        lines.append("")
        
        # Add metadata as comments
        if metadata:
            lines.append("<!-- AGENTIC_METADATA:")
            for key, value in metadata.items():
                lines.append(f"{key}: {value}")
            lines.append("-->")
            lines.append("")
        
        # Add sections
        for section in sections:
            lines.append(f"<!-- SECTION_{section.title.upper().replace(' ', '_')}_START -->")
            lines.append(section.to_markdown())
            lines.append(f"<!-- SECTION_{section.title.upper().replace(' ', '_')}_END -->")
            lines.append("")
        
        lines.append("<!-- AGENTIC_PLAN_END -->")
        
        # Also add the expected AGENTIC: marker for backward compatibility
        result = "\n".join(lines)
        result = result.replace("<!-- AGENTIC_PLAN_START -->", "<!-- AGENTIC: plan_start -->\n<!-- AGENTIC_PLAN_START -->")
        
        return result
    
    def format_steps_as_checklist(self, steps: List[PlanStep]) -> str:
        """Format execution steps as checkboxes for agentic processing."""
        lines = []
        
        for step in steps:
            lines.append(f"- [ ] {step.title}")
            lines.append(f"  **Duration**: {step.duration}")
            lines.append(f"  {step.description}")
            lines.append("")
        
        return "\n".join(lines)
    
    def add_agentic_metadata(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add metadata comments that AI agents can parse."""
        metadata_lines = ["<!-- AGENTIC_METADATA:"]
        
        for key, value in metadata.items():
            if isinstance(value, list):
                # Format lists without quotes for the expected format
                list_str = f"[{', '.join(str(item) for item in value)}]"
                metadata_lines.append(f"{key}: {list_str}")
            else:
                metadata_lines.append(f"{key}: {value}")
        
        metadata_lines.append("-->")
        metadata_comment = "\n".join(metadata_lines)
        
        return metadata_comment + "\n\n" + content
    
    def generate_table_of_contents(self, content: str) -> str:
        """Generate table of contents from markdown content."""
        lines = content.split('\n')
        toc_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Count heading level
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                
                # Extract title
                title = line[level:].strip()
                if title:
                    # Create anchor link (GitHub style)
                    anchor = title.lower().replace(' ', '-')
                    # Replace periods with hyphens for subsection numbering
                    anchor = anchor.replace('.', '-')
                    # Remove non-alphanumeric characters except hyphens
                    anchor = re.sub(r'[^a-z0-9-]', '', anchor)
                    indent = "  " * (level - 2) if level > 1 else ""
                    toc_lines.append(f"{indent}- [{title}](#{anchor})")
        
        return "\n".join(toc_lines)
    
    def validate_syntax(self, markdown: str) -> bool:
        """Validate markdown syntax."""
        try:
            # Check for basic markdown syntax issues
            lines = markdown.split('\n')
            
            # Check for unclosed bold/italic markers
            # Count ** for bold
            bold_markers = markdown.count('**')
            if bold_markers % 2 != 0:
                return False
            
            # Count single * for italic (excluding those in **)
            text_without_bold = re.sub(r'\*\*.*?\*\*', '', markdown)
            italic_markers = text_without_bold.count('*')
            if italic_markers % 2 != 0:
                return False
            
            # Check for proper heading structure
            for line in lines:
                line = line.strip()
                if line.startswith('#') and len(line) > 1:
                    # Must have space after # (unless it's just #)
                    if not line.startswith('# ') and not line == '#':
                        # Check if it has proper format like ## Section
                        if not re.match(r'^#+\s', line):
                            return False
            
            return True
            
        except Exception:
            return False
    
    def convert_frontmatter(self, content: str, target_format: FrontmatterFormat) -> str:
        """Convert between different frontmatter formats."""
        # Extract existing frontmatter
        if content.startswith('---'):
            # YAML frontmatter
            end_pos = content.find('---', 3)
            if end_pos > 0:
                yaml_content = content[3:end_pos].strip()
                body = content[end_pos + 3:].strip()
                
                try:
                    data = yaml.safe_load(yaml_content)
                except:
                    return content
                
                # Convert to target format
                if target_format == FrontmatterFormat.TOML:
                    lines = []
                    for key, value in data.items():
                        if isinstance(value, str):
                            lines.append(f'{key} = "{value}"')
                        elif isinstance(value, list):
                            list_str = ', '.join([f'"{item}"' for item in value])
                            lines.append(f'{key} = [{list_str}]')
                        else:
                            lines.append(f'{key} = {value}')
                    
                    new_frontmatter = "+++\n" + '\n'.join(lines) + "\n+++\n\n"
                    return new_frontmatter + body
                
                elif target_format == FrontmatterFormat.JSON:
                    json_str = json.dumps(data, indent=2)
                    new_frontmatter = "```json\n" + json_str + "\n```\n\n"
                    return new_frontmatter + body
        
        return content
    
    def optimize_for_agents(self, content: str) -> str:
        """Optimize markdown for agentic/AI parsing."""
        lines = content.split('\n')
        optimized_lines = []
        
        # Add plan markers
        optimized_lines.append("<!-- PLAN_START -->")
        
        in_steps_section = False
        in_resources_section = False
        
        for line in lines:
            stripped = line.strip()
            
            # Detect sections
            if stripped.startswith('## Steps') or 'Steps' in stripped:
                in_steps_section = True
                optimized_lines.append("<!-- STEPS_START -->")
                optimized_lines.append(line)
            elif stripped.startswith('## Resources') or 'Resources' in stripped:
                in_resources_section = True
                optimized_lines.append("<!-- RESOURCES_START -->")
                optimized_lines.append(line)
            elif stripped.startswith('##'):
                # End previous sections
                if in_steps_section:
                    optimized_lines.append("<!-- STEPS_END -->")
                    in_steps_section = False
                if in_resources_section:
                    optimized_lines.append("<!-- RESOURCES_END -->")
                    in_resources_section = False
                optimized_lines.append(line)
            elif in_steps_section and re.match(r'^\d+\.', stripped):
                # Convert numbered lists to checkboxes in steps section
                checkbox_line = re.sub(r'^\d+\.\s*', '- [ ] ', stripped)
                optimized_lines.append(checkbox_line)
            else:
                optimized_lines.append(line)
        
        # Close any open sections
        if in_steps_section:
            optimized_lines.append("<!-- STEPS_END -->")
        if in_resources_section:
            optimized_lines.append("<!-- RESOURCES_END -->")
        
        optimized_lines.append("<!-- PLAN_END -->")
        
        return '\n'.join(optimized_lines)
    
    def render_custom_template(self, template_str: str, data: Dict[str, Any]) -> str:
        """Render a custom Jinja2 template with data."""
        try:
            template = self.jinja_env.from_string(template_str)
            return template.render(**data)
        except Exception as e:
            raise MarkdownFormatError(f"Template rendering error: {str(e)}")

    def format_resources(self, resources: List[Dict[str, Any]]) -> str:
        """Format resources as structured lists."""
        if not resources:
            return ""
        
        # Group resources by type
        resource_groups = {}
        for resource in resources:
            resource_type = resource.get('type', 'other')
            if resource_type not in resource_groups:
                resource_groups[resource_type] = []
            resource_groups[resource_type].append(resource)
        
        lines = ["## Required Resources", ""]
        
        for resource_type, items in resource_groups.items():
            lines.append(f"### {resource_type.title()}s")
            lines.append("")
            
            for item in items:
                name = item['name']
                required = item.get('required', True)
                req_text = "" if required else " (optional)"
                lines.append(f"- {name}{req_text}")
            
            lines.append("")
        
        return "\n".join(lines)
