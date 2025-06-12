"""
CLI Main Module - Click-based command-line interface.

This module provides the main CLI functionality including:
- Plan generation commands
- Interactive mode
- Template management
- Plan validation
"""

import os
import sys
import yaml
import click
from typing import Optional, Dict, Any
from pathlib import Path

from ..core.task_analyzer import TaskAnalyzer, TaskCategory, TaskComplexity
from ..core.environment_detector import EnvironmentDetector
from ..core.plan_generator import PlanGenerator
from ..templates.template_engine import TemplateEngine
from ..templates.markdown_generator import MarkdownGenerator, MarkdownMetadata, FrontmatterFormat


class PlannerAgent:
    """Main planner agent that orchestrates all components."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the planner agent."""
        self.config = config or {}
        
        # Initialize core components
        self.task_analyzer = TaskAnalyzer()
        self.environment_detector = EnvironmentDetector()
        self.plan_generator = PlanGenerator(
            task_analyzer=self.task_analyzer,
            environment_detector=self.environment_detector
        )
        self.template_engine = TemplateEngine()
        self.markdown_generator = MarkdownGenerator()
    
    def generate_plan(self, task_description: str, template: Optional[str] = None, 
                     complexity: Optional[TaskComplexity] = None,
                     format_type: str = "markdown", agentic: bool = False) -> str:
        """Generate a comprehensive plan for the given task."""
        # Generate the execution plan
        plan = self.plan_generator.generate_plan(task_description)
        
        # Convert to markdown
        if agentic:
            self.markdown_generator.agentic_mode = True
        
        markdown_output = self.markdown_generator.generate_from_plan(plan)
        
        # Add frontmatter if requested
        if format_type == "yaml-frontmatter":
            metadata = MarkdownMetadata(
                title=task_description,
                category=plan.metadata.category.value if plan.metadata.category else None,
                complexity=plan.metadata.complexity.name if plan.metadata.complexity else None,
                created_at=plan.metadata.generated_at,
                tags=[]
            )
            markdown_output = self.markdown_generator.generate_with_frontmatter(markdown_output, metadata)
        
        return markdown_output


def parse_category(category_str: str) -> TaskCategory:
    """Parse category string to TaskCategory enum."""
    category_map = {
        'technical': TaskCategory.TECHNICAL,
        'creative': TaskCategory.CREATIVE,
        'business': TaskCategory.BUSINESS,
        'personal': TaskCategory.PERSONAL,
        'educational': TaskCategory.EDUCATIONAL
    }
    return category_map.get(category_str.lower(), TaskCategory.TECHNICAL)


def parse_complexity(complexity_str: str) -> TaskComplexity:
    """Parse complexity string to TaskComplexity enum."""
    complexity_map = {
        'low': TaskComplexity.LOW,
        'medium': TaskComplexity.MEDIUM,
        'high': TaskComplexity.HIGH,
        'very_high': TaskComplexity.VERY_HIGH
    }
    return complexity_map.get(complexity_str.lower(), TaskComplexity.MEDIUM)


def format_template_info(template) -> str:
    """Format template information for display."""
    lines = []
    lines.append(f"  {template.name}")
    lines.append(f"    Category: {template.category.name}")
    lines.append(f"    Complexity: {template.complexity.name}")
    
    # Handle both real templates and mock objects
    if hasattr(template, 'metadata') and template.metadata and isinstance(template.metadata, dict):
        if 'description' in template.metadata:
            lines.append(f"    Description: {template.metadata['description']}")
    
    return "\n".join(lines)


def create_planner_agent(config_path: Optional[str] = None) -> PlannerAgent:
    """Create PlannerAgent with optional configuration."""
    config = {}
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except Exception:
            # Gracefully handle config loading errors
            pass
    
    return PlannerAgent(config)


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Opius Planner Agent - Universal planning agent for any task or project."""
    pass


@main.command()
@click.argument('task_description', required=True)
@click.option('--template', '-t', help='Template to use for plan generation')
@click.option('--complexity', '-c', type=click.Choice(['low', 'medium', 'high', 'very_high']), 
              help='Task complexity level')
@click.option('--format', '-f', 'format_type', type=click.Choice(['markdown', 'yaml-frontmatter']), 
              default='markdown', help='Output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--agentic', is_flag=True, help='Generate agentic-friendly output')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--config', type=click.Path(exists=False), help='Configuration file path')
def generate_plan(task_description: str, template: Optional[str], complexity: Optional[str],
                 format_type: str, output: Optional[str], agentic: bool, verbose: bool,
                 config: Optional[str]):
    """Generate a comprehensive plan for the given task description."""
    if not task_description or not task_description.strip():
        click.echo("Error: Task description cannot be empty.", err=True)
        sys.exit(1)
    
    try:
        # Create planner agent
        agent = create_planner_agent(config)
        
        if verbose:
            click.echo(f"Generating plan for: {task_description}")
            if template:
                click.echo(f"Using template: {template}")
            if complexity:
                click.echo(f"Complexity: {complexity}")
        
        # Parse complexity if provided
        complexity_enum = parse_complexity(complexity) if complexity else None
        
        # Generate plan
        plan_content = agent.generate_plan(
            task_description=task_description,
            template=template,
            complexity=complexity_enum,
            format_type=format_type,
            agentic=agentic
        )
        
        # Output plan
        if output:
            # Save to file
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(plan_content)
            
            click.echo(f"Plan saved to {output}")
            
            if verbose:
                click.echo(f"File size: {output_path.stat().st_size} bytes")
        else:
            # Print to stdout
            click.echo(plan_content)
    
    except Exception as e:
        click.echo(f"Error generating plan: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config', type=click.Path(exists=False), help='Configuration file path')
def interactive_mode(config: Optional[str]):
    """Launch interactive mode for plan generation."""
    try:
        agent = create_planner_agent(config)
        
        click.echo("🚀 Welcome to Opius Planner Agent - Interactive Mode")
        click.echo("=" * 50)
        
        # Get task description
        task_description = click.prompt("\n📝 What would you like to plan?", type=str)
        
        # Get category
        click.echo("\n📂 Available categories:")
        for category in TaskCategory:
            click.echo(f"  - {category.value}")
        
        category_input = click.prompt("Choose category", 
                                    type=click.Choice([c.value for c in TaskCategory]),
                                    default="technical")
        
        # Get complexity
        click.echo("\n🎯 Available complexity levels:")
        for complexity in TaskComplexity:
            click.echo(f"  - {complexity.name.lower()}")
        
        complexity_input = click.prompt("Choose complexity", 
                                      type=click.Choice(['low', 'medium', 'high', 'very_high']),
                                      default="medium")
        
        # Generate plan
        click.echo("\n⚡ Generating your plan...")
        
        plan_content = agent.generate_plan(
            task_description=task_description,
            complexity=parse_complexity(complexity_input),
            agentic=True  # Use agentic mode for interactive
        )
        
        # Show plan
        click.echo("\n" + "=" * 50)
        click.echo("📋 YOUR GENERATED PLAN:")
        click.echo("=" * 50)
        click.echo(plan_content)
        
        # Ask if user wants to save (use click.confirm with default=False to handle 'n' input)
        save_to_file = click.confirm("\n💾 Would you like to save this plan to a file?", default=False)
        
        if save_to_file:
            default_filename = f"{task_description.lower().replace(' ', '_')}_plan.md"
            filename = click.prompt("Enter filename", default=default_filename)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(plan_content)
            
            click.echo(f"✅ Plan saved to {filename}")
        
        click.echo("\n🎉 Thank you for using Opius Planner Agent!")
    
    except KeyboardInterrupt:
        click.echo("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--category', '-c', help='Filter templates by category')
@click.option('--complexity', help='Filter templates by complexity')
def list_templates(category: Optional[str], complexity: Optional[str]):
    """List available planning templates."""
    try:
        engine = TemplateEngine()
        
        if category:
            # Filter by category
            category_enum = parse_category(category)
            templates = engine.get_templates_by_category(category_enum)
            click.echo(f"📋 Templates for category '{category}':")
        elif complexity:
            # Filter by complexity
            complexity_enum = parse_complexity(complexity)
            templates = engine.get_templates_by_complexity(complexity_enum)
            click.echo(f"📋 Templates for complexity '{complexity}':")
        else:
            # Show all templates
            templates = engine.get_available_templates()
            click.echo("📋 Available Templates:")
        
        click.echo("=" * 40)
        
        if not templates:
            click.echo("No templates found matching the criteria.")
            return
        
        for template in templates:
            click.echo(format_template_info(template))
            click.echo()
    
    except Exception as e:
        click.echo(f"Error listing templates: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('plan_file', type=click.Path(exists=True))
def validate_plan(plan_file: str):
    """Validate a plan file for syntax and structure."""
    try:
        # Read the plan file
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Validate using MarkdownGenerator
        generator = MarkdownGenerator()
        is_valid = generator.validate_syntax(content)
        
        if is_valid:
            click.echo(f"✅ Plan file '{plan_file}' is valid!")
            sys.exit(0)
        else:
            click.echo(f"❌ Plan file '{plan_file}' has syntax issues.")
            sys.exit(1)
    
    except FileNotFoundError:
        click.echo(f"Error: File '{plan_file}' not found.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error validating plan: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
