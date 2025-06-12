"""
TemplateEngine - Template structure system and Jinja2-based template engine.

This module provides intelligent template management capabilities including:
- Template loading and rendering with Jinja2
- Context-aware template selection
- Template inheritance and customization
- Variable substitution and validation
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from jinja2 import Environment, BaseLoader, Template as JinjaTemplate, TemplateError as JinjaTemplateError

from ..core.task_analyzer import TaskCategory, TaskComplexity


class TemplateError(Exception):
    """Custom exception for template-related errors."""
    pass


class TemplateCategory(Enum):
    """Categories for different types of templates."""
    TECHNICAL = "technical"
    CREATIVE = "creative" 
    BUSINESS = "business"
    PERSONAL = "personal"
    EDUCATIONAL = "educational"


@dataclass
class TemplateVariable:
    """Represents a variable used in templates."""
    name: str
    description: str = ""
    required: bool = True
    default: Optional[str] = None
    type: str = "string"


@dataclass
class Template:
    """Represents a template with metadata and content."""
    name: str
    category: TaskCategory
    complexity: TaskComplexity
    content: str
    variables: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def extract_variables(self) -> List[str]:
        """Extract variables from template content using regex."""
        # Find all Jinja2 variables in the format {{ variable_name }}
        pattern = r'\{\{\s*(\w+)\s*\}\}'
        variables = re.findall(pattern, self.content)
        return list(set(variables))  # Remove duplicates
    
    def render(self, context: 'TemplateContext') -> str:
        """Render the template with the provided context."""
        from jinja2 import Environment, BaseLoader
        
        # Create a simple Jinja2 environment for this template
        env = Environment(
            loader=BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Create template from content
        template = env.from_string(self.content)
        
        # Render with context
        return template.render(**context.to_dict())


@dataclass 
class TemplateContext:
    """Context data for template rendering."""
    
    def __init__(self, **kwargs):
        """Initialize context with keyword arguments."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for Jinja2."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def merge(self, other: 'TemplateContext') -> 'TemplateContext':
        """Merge with another context, with other taking precedence."""
        merged_dict = self.to_dict()
        merged_dict.update(other.to_dict())
        return TemplateContext(**merged_dict)


class DictLoader(BaseLoader):
    """Custom Jinja2 loader that loads templates from a dictionary."""
    
    def __init__(self, templates: Dict[str, str]):
        self.templates = templates
    
    def get_source(self, environment, template):
        if template not in self.templates:
            raise JinjaTemplateError(f"Template '{template}' not found")
        
        source = self.templates[template]
        return source, None, lambda: True


class TemplateEngine:
    """Template management and rendering engine."""
    
    def __init__(self):
        """Initialize the TemplateEngine with default templates."""
        self.templates: Dict[str, Template] = {}
        self.template_content: Dict[str, str] = {}
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=DictLoader(self.template_content),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Load default templates
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load built-in default templates."""
        default_templates = [
            # Technical Templates
            Template(
                name="technical_low",
                category=TaskCategory.TECHNICAL,
                complexity=TaskComplexity.LOW,
                content="""# {{ project_name or task_description }}

## 🎯 **Project Overview**
{{ task_description }}

## 📋 **Requirements**
- Basic {{ technologies[0] if technologies else 'development' }} setup
- Simple implementation approach
- Testing framework

## 🚀 **Implementation Steps**

### 1. Setup Development Environment
- Install required tools and dependencies
- Configure your IDE/editor
- Set up version control

### 2. Core Implementation  
- Implement basic functionality
- Follow best practices and coding standards
- Write clean, readable code

### 3. Testing & Validation
- Write unit tests
- Perform manual testing
- Fix any issues found

### 4. Deployment
- Prepare for deployment
- Deploy to target environment
- Verify functionality

## 📊 **Success Criteria**
- [ ] Core functionality working
- [ ] Tests passing
- [ ] Code documented
- [ ] Successfully deployed

## ⏱️ **Estimated Duration**
{{ estimated_duration or '1-2 weeks' }}

## 🔧 **Technologies**
{% if technologies %}
{% for tech in technologies %}
- {{ tech }}
{% endfor %}
{% else %}
- To be determined based on requirements
{% endif %}
""",
                variables=["project_name", "task_description", "technologies", "estimated_duration"]
            ),
            
            Template(
                name="technical_medium",
                category=TaskCategory.TECHNICAL,
                complexity=TaskComplexity.MEDIUM,
                content="""# {{ project_name or task_description }}

## 🎯 **Project Overview**
{{ task_description }}

## 📋 **Requirements Analysis**
- Detailed requirements gathering
- System architecture design
- Technology stack selection
- Performance considerations

## 🏗️ **Architecture & Design**
- System architecture documentation
- Database design (if applicable)
- API design and documentation
- Security considerations

## 🚀 **Implementation Plan**

### Phase 1: Foundation Setup
- Development environment configuration
- Project structure creation
- Core dependencies installation
- CI/CD pipeline setup

### Phase 2: Core Development
- Core functionality implementation
- Database integration (if applicable)
- API development
- User interface development

### Phase 3: Integration & Testing
- Component integration
- Unit and integration testing
- Performance testing
- Security testing

### Phase 4: Deployment & Monitoring
- Production deployment
- Monitoring setup
- Documentation completion
- Handover and training

## 📊 **Success Criteria**
- [ ] All functional requirements met
- [ ] Performance targets achieved
- [ ] Security requirements satisfied
- [ ] Test coverage > 80%
- [ ] Production deployment successful
- [ ] Documentation complete

## ⏱️ **Timeline**
{{ estimated_duration or '2-6 weeks' }}

## 🔧 **Technology Stack**
{% if technologies %}
{% for tech in technologies %}
- {{ tech }}
{% endfor %}
{% else %}
- Frontend: To be determined
- Backend: To be determined  
- Database: To be determined
- Deployment: To be determined
{% endif %}

## 🎯 **Key Milestones**
1. Architecture design approved
2. Development environment ready
3. Core functionality complete
4. Testing phase complete
5. Production deployment
""",
                variables=["project_name", "task_description", "technologies", "estimated_duration"]
            ),
            
            # Creative Templates
            Template(
                name="creative_low",
                category=TaskCategory.CREATIVE,
                complexity=TaskComplexity.LOW,
                content="""# {{ project_name or task_description }}

## 🎨 **Creative Vision**
{{ task_description }}

## 💡 **Concept Development**
- Brainstorm initial ideas
- Define creative direction
- Gather inspiration and references
- Create mood board or style guide

## 📝 **Planning & Structure**
- Outline main components
- Plan creative workflow
- Set quality standards
- Define success metrics

## 🚀 **Creation Process**

### 1. Initial Creation
- Start with basic structure/framework
- Focus on core creative elements
- Maintain consistency with vision

### 2. Development & Refinement
- Expand and develop ideas
- Add details and polish
- Seek feedback from others

### 3. Final Review & Completion
- Review against original vision
- Make final adjustments
- Prepare for presentation/publication

## 📊 **Success Criteria**
- [ ] Creative vision achieved
- [ ] Quality standards met
- [ ] Audience engagement positive
- [ ] Project completed on time

## ⏱️ **Timeline**
{{ estimated_duration or '1-3 weeks' }}

{% if tools %}
## 🛠️ **Tools & Resources**
{% for tool in tools %}
- {{ tool }}
{% endfor %}
{% endif %}
""",
                variables=["project_name", "task_description", "estimated_duration", "tools"]
            ),
            
            # Business Templates  
            Template(
                name="business_medium",
                category=TaskCategory.BUSINESS,
                complexity=TaskComplexity.MEDIUM,
                content="""# {{ project_name or task_description }}

## 🎯 **Business Objective**
{{ task_description }}

## 📊 **Market Analysis**
- Target market identification
- Competitive landscape analysis
- Market size and opportunity assessment
- Key trends and insights

## 📋 **Strategic Planning**
- Goal setting and KPI definition
- Resource allocation planning
- Risk assessment and mitigation
- Timeline and milestone planning

## 🚀 **Execution Plan**

### Phase 1: Research & Analysis
- Market research completion
- Competitive analysis
- Stakeholder interviews
- Data collection and analysis

### Phase 2: Strategy Development
- Strategic framework creation
- Action plan development
- Resource requirement planning
- Risk mitigation strategies

### Phase 3: Implementation
- Plan execution initiation
- Progress monitoring and tracking
- Regular stakeholder updates
- Course correction as needed

### Phase 4: Evaluation & Optimization
- Performance measurement
- ROI analysis
- Lessons learned documentation
- Future recommendations

## 📊 **Key Performance Indicators**
{% if kpis %}
{% for kpi in kpis %}
- {{ kpi }}
{% endfor %}
{% else %}
- Revenue impact
- Customer acquisition/retention
- Market share growth
- Operational efficiency
{% endif %}

## ⏱️ **Timeline**
{{ estimated_duration or '4-8 weeks' }}

## 💰 **Budget Considerations**
{{ budget or 'To be determined based on scope' }}

## 🎯 **Success Metrics**
- [ ] Primary objectives achieved
- [ ] KPIs met or exceeded
- [ ] Stakeholder satisfaction high
- [ ] ROI targets achieved
- [ ] Project delivered on time and budget
""",
                variables=["project_name", "task_description", "estimated_duration", "budget", "kpis"]
            ),
            
            # Personal Templates
            Template(
                name="personal_medium",
                category=TaskCategory.PERSONAL,
                complexity=TaskComplexity.MEDIUM,
                content="""# {{ project_name or task_description }}

## 🎯 **Personal Goal**
{{ task_description }}

## 📅 **Planning & Preparation**
- Goal clarification and definition
- Resource and timeline assessment
- Potential challenge identification
- Support system activation

## 📋 **Action Plan**

### Phase 1: Foundation Setting
- Gather necessary resources
- Set up tracking systems
- Create supportive environment
- Establish routines and habits

### Phase 2: Active Implementation
- Execute planned activities
- Monitor progress regularly
- Adjust approach as needed
- Maintain motivation and focus

### Phase 3: Review & Refinement
- Assess progress against goals
- Celebrate achievements
- Learn from challenges
- Plan next steps

## 📊 **Success Indicators**
- [ ] Primary goal achieved
- [ ] Consistent progress maintained
- [ ] Personal satisfaction high
- [ ] Positive habit formation
- [ ] Learning objectives met

## ⏱️ **Timeline**
{{ estimated_duration or '2-6 weeks' }}

{% if resources %}
## 🛠️ **Resources Needed**
{% for resource in resources %}
- {{ resource }}
{% endfor %}
{% endif %}

## 💪 **Motivation & Support**
- Regular check-ins with accountability partner
- Progress tracking and celebration
- Flexibility to adapt approach
- Focus on personal growth and learning
""",
                variables=["project_name", "task_description", "estimated_duration", "resources"]
            ),
            
            # Educational Templates
            Template(
                name="educational_low",
                category=TaskCategory.EDUCATIONAL,
                complexity=TaskComplexity.LOW,
                content="""# {{ project_name or task_description }}

## 🎓 **Learning Objective**
{{ task_description }}

## 📚 **Learning Plan**
- Skill assessment and gap analysis
- Learning resource identification
- Study schedule creation
- Progress tracking setup

## 🚀 **Learning Journey**

### 1. Foundation Building
- Master basic concepts
- Complete introductory materials
- Practice fundamental skills
- Build confidence

### 2. Skill Development
- Work through practical exercises
- Apply knowledge to real projects
- Seek feedback and guidance
- Overcome learning challenges

### 3. Knowledge Integration
- Combine different concepts
- Create portfolio projects
- Share knowledge with others
- Plan continued learning

## 📊 **Learning Milestones**
- [ ] Basic concepts understood
- [ ] Practical skills developed
- [ ] Project portfolio created
- [ ] Knowledge application demonstrated
- [ ] Ready for next level

## ⏱️ **Study Timeline**
{{ estimated_duration or '2-4 weeks' }}

{% if resources %}
## 📖 **Learning Resources**
{% for resource in resources %}
- {{ resource }}
{% endfor %}
{% endif %}

## 🎯 **Practice Opportunities**
- Daily practice sessions
- Mini-projects and exercises
- Community engagement
- Knowledge sharing
""",
                variables=["project_name", "task_description", "estimated_duration", "resources"]
            )
        ]
        
        for template in default_templates:
            self.register_template(template)
    
    def register_template(self, template: Template):
        """Register a new template."""
        self.templates[template.name] = template
        self.template_content[template.name] = template.content
        
        # Update Jinja2 environment with new template
        self.jinja_env = Environment(
            loader=DictLoader(self.template_content),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def load_template(self, category: TaskCategory, complexity: TaskComplexity) -> Optional[Template]:
        """Load a template by category and complexity."""
        # Find template that matches category and complexity
        for template in self.templates.values():
            if template.category == category and template.complexity == complexity:
                return template
        
        # Fallback to category match with different complexity
        for template in self.templates.values():
            if template.category == category:
                return template
        
        # Ultimate fallback to first available template
        if self.templates:
            return list(self.templates.values())[0]
        
        return None
    
    def render_template(self, category: TaskCategory, complexity: TaskComplexity, context: TemplateContext) -> str:
        """Render a template with the provided context."""
        template = self.load_template(category, complexity)
        if not template:
            raise TemplateError(f"No template found for category {category} and complexity {complexity}")
        
        return self.render_by_name(template.name, context)
    
    def render_by_name(self, template_name: str, context: TemplateContext) -> str:
        """Render a template by name with the provided context."""
        try:
            jinja_template = self.jinja_env.get_template(template_name)
            return jinja_template.render(**context.to_dict())
        except JinjaTemplateError as e:
            raise TemplateError(f"Template rendering error: {str(e)}")
    
    def get_available_templates(self) -> List[Template]:
        """Get all available templates."""
        return list(self.templates.values())
    
    def get_templates_by_category(self, category: TaskCategory) -> List[Template]:
        """Get templates filtered by category."""
        return [t for t in self.templates.values() if t.category == category]
    
    def get_templates_by_complexity(self, complexity: TaskComplexity) -> List[Template]:
        """Get templates filtered by complexity."""
        return [t for t in self.templates.values() if t.complexity == complexity]
    
    def validate_template(self, template: Template) -> bool:
        """Validate a template for correctness."""
        # Check required fields
        if not template.name or not template.name.strip():
            return False
        
        if not template.content or not template.content.strip():
            return False
        
        # Check if template content is valid Jinja2
        try:
            self.jinja_env.from_string(template.content)
            return True
        except JinjaTemplateError:
            return False
