"""
Template management system for the Opius Planner Agent.

This module handles template loading, processing, and customization
for different planning domains and use cases.
"""

from .template_engine import (
    TemplateEngine,
    TemplateCategory,
    Template,
    TemplateContext,
    TemplateVariable,
    TemplateError
)
from .markdown_generator import (
    MarkdownGenerator,
    MarkdownSection,
    MarkdownMetadata,
    FrontmatterFormat,
    MarkdownFormatError
)

__all__ = [
    "TemplateEngine",
    "TemplateCategory",
    "Template",
    "TemplateContext",
    "TemplateVariable",
    "TemplateError",
    "MarkdownGenerator",
    "MarkdownSection",
    "MarkdownMetadata",
    "FrontmatterFormat",
    "MarkdownFormatError",
]
