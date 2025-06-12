"""
Customization System - Phase 2.2 Implementation.

Provides dynamic template modification, user preferences, and validation capabilities.
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from copy import deepcopy
from jinja2 import Environment, meta, TemplateSyntaxError

from ..core.task_analyzer import TaskCategory, TaskComplexity
from .template_engine import Template, TemplateContext


@dataclass
class UserPreference:
    """Represents user preferences for template customization."""
    user_id: str
    theme: str = "default"
    include_tracker: bool = True
    default_complexity: TaskComplexity = TaskComplexity.MEDIUM
    preferred_sections: List[str] = field(default_factory=list)
    custom_colors: Dict[str, str] = field(default_factory=dict)
    template_overrides: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CustomizationRule:
    """Represents a rule for template customization."""
    name: str
    condition: Dict[str, Any]
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def matches_condition(self, context: Dict[str, Any]) -> bool:
        """Check if the rule condition matches the given context."""
        for key, expected_value in self.condition.items():
            if key not in context or context[key] != expected_value:
                return False
        return True
    
    def apply_action(self, content: str) -> str:
        """Apply the rule action to the content."""
        if self.action == "add_tracker_section":
            tracker_section = """

## 📊 Progress Tracker

**Instructions for LLM**: Update this tracker section regularly with progress, milestones, and status updates.

### 📈 Overall Progress
```
[████████████░░░░░░░░░░░░░░░░] 45% Complete
```

### 🎯 Current Status
- **Phase**: In Progress
- **Last Updated**: {{ current_date | default("Today") }}
- **Next Milestone**: {{ next_milestone | default("TBD") }}

### ✅ Completed Tasks
- [x] Project setup
- [x] Initial planning

### 🔄 In Progress
- [ ] Current development tasks
- [ ] Testing and validation

### 📅 Upcoming
- [ ] Future milestones
- [ ] Final deliverables"""
            return content + tracker_section
        
        elif self.action == "apply_theme":
            # Apply theme-specific styling
            if self.parameters.get("theme_name") == "dark":
                return content.replace("##", "🌙 ##").replace("###", "✨ ###")
            elif self.parameters.get("theme_name") == "modern":
                return content.replace("##", "🚀 ##").replace("###", "💡 ###")
        
        return content


class TemplateCustomizer:
    """Handles template customization operations."""
    
    def __init__(self):
        """Initialize the template customizer."""
        self.customization_rules: List[CustomizationRule] = []
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default customization rules."""
        # Tracker rule
        tracker_rule = CustomizationRule(
            name="add_tracker",
            condition={"include_tracker": True},
            action="add_tracker_section"
        )
        self.customization_rules.append(tracker_rule)
        
        # Theme rules
        dark_theme_rule = CustomizationRule(
            name="dark_theme",
            condition={"theme": "dark"},
            action="apply_theme",
            parameters={"theme_name": "dark"}
        )
        self.customization_rules.append(dark_theme_rule)
        
        modern_theme_rule = CustomizationRule(
            name="modern_theme",
            condition={"theme": "modern"},
            action="apply_theme",
            parameters={"theme_name": "modern"}
        )
        self.customization_rules.append(modern_theme_rule)
    
    def add_tracker(self, template: Template) -> Template:
        """Add tracker functionality to a template."""
        customized = deepcopy(template)
        
        tracker_content = """

## 📊 Progress Tracker

**Instructions for LLM**: This tracker should be continuously updated throughout the project. Maintain detailed progress tracking with visual indicators and completion percentages.

### 📈 Overall Progress
```
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░] 45% Complete
```

### 🚀 Phase Status
| Phase | Status | Progress |
|-------|--------|----------|
| Planning | ✅ Complete | 100% |
| Development | 🟡 In Progress | 60% |
| Testing | 🔴 Not Started | 0% |
| Deployment | 🔴 Not Started | 0% |

### 📌 Current Focus
- [ ] Current task 1
- [ ] Current task 2
- [x] Completed task

### 🔄 Daily Updates
**Instructions for LLM**: Update this section daily with progress, blockers, and next steps.

**{{ current_date | default("Today") }}**:
- Progress: Describe today's achievements
- Blockers: List any obstacles
- Next Steps: Plan for tomorrow"""
        
        customized.content += tracker_content
        return customized
    
    def apply_theme(self, template: Template, theme: str) -> Template:
        """Apply a theme to a template."""
        customized = deepcopy(template)
        
        if theme == "modern":
            # Modern theme with enhanced visuals
            customized.content = customized.content.replace("##", "🚀 ##")
            customized.content = customized.content.replace("###", "💡 ###")
            customized.content = customized.content.replace("- [ ]", "🔲")
            customized.content = customized.content.replace("- [x]", "✅")
            
        elif theme == "minimalist":
            # Minimalist theme - clean and simple
            customized.content = re.sub(r'#{2,3}\s*', '## ', customized.content)
            
        elif theme == "dark":
            # Dark theme with night-friendly emojis
            customized.content = customized.content.replace("##", "🌙 ##")
            customized.content = customized.content.replace("###", "✨ ###")
        
        return customized
    
    def adjust_complexity(self, content: str, complexity: TaskComplexity) -> str:
        """Adjust content based on complexity level."""
        if complexity == TaskComplexity.VERY_HIGH:
            # Add more detailed sections for very high complexity
            additional_content = """

## 🔍 Detailed Analysis
- Comprehensive requirement analysis
- Risk assessment and mitigation
- Stakeholder communication plan
- Quality assurance protocols

## 📋 Advanced Planning
- Detailed project timeline
- Resource allocation planning
- Dependency management
- Contingency planning"""
            return content + additional_content
            
        elif complexity == TaskComplexity.LOW:
            # Simplify for low complexity
            simplified = re.sub(r'\n## [^#\n]*\n[^#]*(?=\n##|\n$)', '', content)
            return simplified
        
        return content
    
    def add_custom_sections(self, template: Template, sections: List[Dict[str, str]]) -> Template:
        """Add custom sections to a template."""
        customized = deepcopy(template)
        
        for section in sections:
            section_content = f"""

## {section['title']}
{section['content']}"""
            customized.content += section_content
        
        return customized


class UserPreferenceManager:
    """Manages user preferences for template customization."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """Initialize the preference manager."""
        self.storage_path = storage_path or "user_preferences.json"
        self.preferences: Dict[str, UserPreference] = {}
        self._load_preferences()
    
    def _load_preferences(self):
        """Load preferences from storage."""
        try:
            if Path(self.storage_path).exists():
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for user_id, pref_data in data.items():
                        self.preferences[user_id] = UserPreference(**pref_data)
        except Exception:
            # If loading fails, start with empty preferences
            self.preferences = {}
    
    def _save_preferences(self):
        """Save preferences to storage."""
        try:
            data = {}
            for user_id, pref in self.preferences.items():
                data[user_id] = {
                    'user_id': pref.user_id,
                    'theme': pref.theme,
                    'include_tracker': pref.include_tracker,
                    'default_complexity': pref.default_complexity.value if hasattr(pref.default_complexity, 'value') else str(pref.default_complexity),
                    'preferred_sections': pref.preferred_sections,
                    'custom_colors': pref.custom_colors,
                    'template_overrides': pref.template_overrides
                }
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            # If saving fails, continue without persistence
            pass
    
    def save_preference(self, preference: UserPreference) -> bool:
        """Save a user preference."""
        try:
            self.preferences[preference.user_id] = preference
            self._save_preferences()
            return True
        except Exception:
            return False
    
    def get_preference(self, user_id: str) -> Optional[UserPreference]:
        """Get user preference by ID."""
        return self.preferences.get(user_id)
    
    def update_preference(self, preference: UserPreference) -> bool:
        """Update an existing user preference."""
        if preference.user_id in self.preferences:
            self.preferences[preference.user_id] = preference
            self._save_preferences()
            return True
        return False
    
    def delete_preference(self, user_id: str) -> bool:
        """Delete a user preference."""
        if user_id in self.preferences:
            del self.preferences[user_id]
            self._save_preferences()
            return True
        return False
    
    def get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences for new users."""
        return {
            "theme": "default",
            "include_tracker": True,
            "default_complexity": "medium",
            "preferred_sections": ["overview", "timeline", "success_criteria"],
            "custom_colors": {},
            "template_overrides": {}
        }


class TemplateValidator:
    """Validates templates and customizations."""
    
    def __init__(self):
        """Initialize the validator."""
        self.jinja_env = Environment()
    
    def validate_syntax(self, template: Template) -> Tuple[bool, List[str]]:
        """Validate Jinja2 template syntax."""
        errors = []
        
        try:
            # Parse the template to check for syntax errors
            self.jinja_env.parse(template.content)
            return True, []
        except TemplateSyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, errors
        except Exception as e:
            errors.append(f"Template error: {str(e)}")
            return False, errors
    
    def validate_required_variables(self, template: Template, context: TemplateContext) -> Tuple[bool, List[str]]:
        """Validate that all required variables are provided."""
        try:
            # Get all variables used in the template
            ast = self.jinja_env.parse(template.content)
            required_vars = meta.find_undeclared_variables(ast)
            
            # Check which variables are missing from context
            context_dict = context.to_dict()
            missing_vars = [var for var in required_vars if var not in context_dict]
            
            return len(missing_vars) == 0, missing_vars
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]
    
    def validate_structure(self, template: Template) -> Tuple[bool, List[str]]:
        """Validate overall template structure."""
        issues = []
        content = template.content
        
        # Check for basic structure elements
        if not content.strip().startswith('#'):
            issues.append("Template should start with a title (# header)")
        
        # Check for reasonable length
        if len(content) < 50:
            issues.append("Template content seems too short")
        
        # Check for balanced sections
        header_count = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))
        if header_count < 2:
            issues.append("Template should have multiple sections")
        
        return len(issues) == 0, issues
    
    def validate_customization_rule(self, rule: CustomizationRule) -> Tuple[bool, List[str]]:
        """Validate a customization rule."""
        errors = []
        
        # Check required fields
        if not rule.name:
            errors.append("Rule must have a name")
        
        if not rule.condition:
            errors.append("Rule must have a condition")
        
        if not rule.action:
            errors.append("Rule must have an action")
        
        # Check condition structure
        if not isinstance(rule.condition, dict):
            errors.append("Rule condition must be a dictionary")
        
        return len(errors) == 0, errors


class CustomizationEngine:
    """Main engine for template customization."""
    
    def __init__(self):
        """Initialize the customization engine."""
        self.customizer = TemplateCustomizer()
        self.preference_manager = UserPreferenceManager()
        self.validator = TemplateValidator()
    
    def customize_template(self, template: Template, user_id: str = None, 
                         customizations: Dict[str, Any] = None) -> Template:
        """Apply customizations to a template."""
        customized = deepcopy(template)
        customizations = customizations or {}
        
        # Load user preferences if user_id provided
        if user_id:
            user_prefs = self.preference_manager.get_preference(user_id)
            if user_prefs:
                # Apply user preferences
                if user_prefs.include_tracker:
                    customizations['add_tracker'] = True
                if user_prefs.theme != "default":
                    customizations['theme'] = user_prefs.theme
        
        # Apply customizations
        if customizations.get('add_tracker'):
            customized = self.customizer.add_tracker(customized)
        
        if 'theme' in customizations:
            customized = self.customizer.apply_theme(customized, customizations['theme'])
        
        if 'add_sections' in customizations:
            sections = [{"title": section.title(), "content": f"Content for {section}"} 
                       for section in customizations['add_sections']]
            customized = self.customizer.add_custom_sections(customized, sections)
        
        return customized
    
    def save_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Save user preferences."""
        try:
            # Convert complexity string to enum if needed
            complexity = preferences.get('default_complexity', 'medium')
            if isinstance(complexity, str):
                complexity_map = {
                    'low': TaskComplexity.LOW,
                    'medium': TaskComplexity.MEDIUM,
                    'high': TaskComplexity.HIGH,
                    'very_high': TaskComplexity.VERY_HIGH
                }
                complexity = complexity_map.get(complexity.lower(), TaskComplexity.MEDIUM)
            
            user_pref = UserPreference(
                user_id=user_id,
                theme=preferences.get('theme', 'default'),
                include_tracker=preferences.get('include_tracker', True),
                default_complexity=complexity,
                preferred_sections=preferences.get('preferred_sections', []),
                custom_colors=preferences.get('custom_colors', {}),
                template_overrides=preferences.get('template_overrides', {})
            )
            
            return self.preference_manager.save_preference(user_pref)
        except Exception:
            return False
    
    def load_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user preferences."""
        user_pref = self.preference_manager.get_preference(user_id)
        if user_pref:
            return {
                'theme': user_pref.theme,
                'include_tracker': user_pref.include_tracker,
                'default_complexity': user_pref.default_complexity.value if hasattr(user_pref.default_complexity, 'value') else str(user_pref.default_complexity),
                'preferred_sections': user_pref.preferred_sections,
                'custom_colors': user_pref.custom_colors,
                'template_overrides': user_pref.template_overrides
            }
        return None
    
    def validate_template(self, template: Template, context: TemplateContext = None) -> Tuple[bool, List[str]]:
        """Validate a template."""
        all_errors = []
        
        # Syntax validation
        syntax_valid, syntax_errors = self.validator.validate_syntax(template)
        if not syntax_valid:
            all_errors.extend(syntax_errors)
        
        # Structure validation
        structure_valid, structure_errors = self.validator.validate_structure(template)
        if not structure_valid:
            all_errors.extend(structure_errors)
        
        # Variable validation if context provided
        if context:
            vars_valid, missing_vars = self.validator.validate_required_variables(template, context)
            if not vars_valid:
                all_errors.extend([f"Missing variable: {var}" for var in missing_vars])
        
        return len(all_errors) == 0, all_errors
