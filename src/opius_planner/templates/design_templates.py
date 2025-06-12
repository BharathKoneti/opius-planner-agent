"""
Design Templates Library - Phase 2 Implementation.

Provides specialized templates for design domain tasks including
UI/UX design, graphic design, and brand identity projects.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from ..core.task_analyzer import TaskCategory, TaskComplexity
from .template_engine import Template, TemplateContext


class DesignTemplateType(Enum):
    """Types of design templates available."""
    UI_UX_DESIGN = "ui_ux_design"
    GRAPHIC_DESIGN = "graphic_design"
    BRAND_IDENTITY = "brand_identity"


@dataclass
class UIUXDesignTemplate(Template):
    """Template for UI/UX design projects."""
    design_type: str = "mobile_ui"
    platform: str = "iOS/Android"
    
    def __init__(self, name: str, complexity: TaskComplexity, design_type: str = "mobile_ui", 
                 platform: str = "iOS/Android", **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.design_type = design_type
        self.platform = platform
        # Generate content after initialization
        self.content = self._generate_ui_ux_template()
    
    def _generate_ui_ux_template(self) -> str:
        """Generate UI/UX design template content."""
        return f"""# {{{{ project_name | default("UI/UX Design Project") }}}}

**Design Type**: {self.design_type.replace('_', ' ').title()}
**Platform**: {{{{ platform | default("{self.platform}") }}}}
**Target Users**: {{{{ target_users | default("General users") }}}}

## 🎨 Design Overview

**Project Goals**: {{{{ project_goals | default("Create intuitive user experience") }}}}
**Design Style**: {{{{ design_style | default("Modern and clean") }}}}
**Key Features**: 
{{% if key_features %}}
{{% for feature in key_features %}}
- {{{{ feature }}}}
{{% endfor %}}
{{% else %}}
- Core functionality
- User-friendly interface
- Responsive design
{{% endif %}}

## 🚀 Design Process

### Phase 1: Research & Discovery (1-2 weeks)
- [ ] **User Research**
  Conduct user interviews and surveys
  
- [ ] **Competitive Analysis**
  Research existing solutions and best practices
  
- [ ] **User Personas**
  Create detailed user personas and scenarios
  
- [ ] **User Journey Mapping**
  Map user flows and identify pain points

### Phase 2: Information Architecture (3-5 days)
- [ ] **Site Map Creation**
  Define content structure and navigation
  
- [ ] **User Flow Design**
  Design optimal user pathways
  
- [ ] **Content Strategy**
  Plan content hierarchy and messaging

### Phase 3: Wireframing & Prototyping (1-2 weeks)
- [ ] **Low-Fidelity Wireframes**
  Create basic layout structures
  
- [ ] **Interactive Prototypes**
  Build clickable prototypes for testing
  
- [ ] **Usability Testing**
  Test prototypes with real users

### Phase 4: Visual Design (2-3 weeks)
- [ ] **Design System Creation**
  Establish colors, typography, components
  
- [ ] **High-Fidelity Mockups**
  Create detailed visual designs
  
- [ ] **Design Specifications**
  Document spacing, colors, and interactions

### Phase 5: Implementation Support (1 week)
- [ ] **Developer Handoff**
  Provide detailed design specifications
  
- [ ] **Design QA**
  Review implementation for design accuracy
  
- [ ] **Final Adjustments**
  Make necessary design refinements

## 📊 Success Criteria
- [ ] User research insights incorporated into design
- [ ] Wireframes approved by stakeholders
- [ ] High-fidelity designs completed
- [ ] Usability testing conducted with positive results
- [ ] Design system documented and delivered
- [ ] Developer handoff completed successfully

## 📚 Deliverables
- User research findings
- User personas and journey maps
- Wireframes and prototypes
- High-fidelity mockups
- Design system documentation
- Implementation guidelines

## 🛠️ Tools & Resources
- Design tools (Figma, Sketch, Adobe XD)
- Prototyping tools (InVision, Principle)
- User testing platforms
- Analytics and research tools

## 💡 Design Principles
{{% if design_principles %}}
{{% for principle in design_principles %}}
- {{{{ principle }}}}
{{% endfor %}}
{{% else %}}
- User-centered design
- Accessibility and inclusion
- Consistency and clarity
- Performance and efficiency
{{% endif %}}"""


@dataclass
class GraphicDesignTemplate(Template):
    """Template for graphic design projects."""
    design_type: str = "logo"
    deliverables: List[str] = field(default_factory=lambda: ["Primary design", "Variations"])
    
    def __init__(self, name: str, complexity: TaskComplexity, design_type: str = "logo", 
                 deliverables: List[str] = None, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.design_type = design_type
        self.deliverables = deliverables or ["Primary design", "Variations"]
        # Generate content after initialization
        self.content = self._generate_graphic_template()
    
    def _generate_graphic_template(self) -> str:
        """Generate graphic design template content."""
        deliverables_list = "\n".join([f"- {item}" for item in self.deliverables])
        
        return f"""# {{{{ project_name | default("Graphic Design Project") }}}}

**Design Type**: {self.design_type.replace('_', ' ').title()}
**Client**: {{{{ client_name | default("Client Name") }}}}
**Industry**: {{{{ industry | default("General") }}}}

## 🎨 Design Brief

**Project Objectives**: {{{{ project_objectives | default("Create compelling visual design") }}}}
**Target Audience**: {{{{ target_audience | default("General audience") }}}}
**Brand Personality**: 
{{% if brand_personality %}}
{{% for trait in brand_personality %}}
- {{{{ trait }}}}
{{% endfor %}}
{{% else %}}
- Professional
- Modern
- Trustworthy
{{% endif %}}

**Design Requirements**:
{{% if design_requirements %}}
{{% for requirement in design_requirements %}}
- {{{{ requirement }}}}
{{% endfor %}}
{{% else %}}
- Scalable design
- Print and digital ready
- Brand alignment
{{% endif %}}

## 🚀 Design Process

### Phase 1: Creative Brief & Research (2-3 days)
- [ ] **Client Discovery**
  Understand client needs and expectations
  
- [ ] **Market Research**
  Research industry trends and competitors
  
- [ ] **Mood Board Creation**
  Gather visual inspiration and references
  
- [ ] **Creative Strategy**
  Define design direction and approach

### Phase 2: Concept Development (1 week)
- [ ] **Initial Concepts**
  Create 3-5 diverse design concepts
  
- [ ] **Concept Refinement**
  Develop strongest concepts further
  
- [ ] **Client Presentation**
  Present concepts with rationale
  
- [ ] **Feedback Integration**
  Refine based on client feedback

### Phase 3: Design Execution (1-2 weeks)
- [ ] **Final Design Creation**
  Execute approved concept to completion
  
- [ ] **Design Variations**
  Create necessary variations and formats
  
- [ ] **Quality Assurance**
  Review designs for technical accuracy
  
- [ ] **Client Approval**
  Get final approval on all deliverables

### Phase 4: Delivery & Implementation (2-3 days)
- [ ] **File Preparation**
  Prepare files in required formats
  
- [ ] **Usage Guidelines**
  Create guidelines for proper usage
  
- [ ] **Asset Organization**
  Organize and label all design files
  
- [ ] **Final Delivery**
  Deliver complete design package

## 📊 Success Criteria
- [ ] Design meets all brief requirements
- [ ] Client approval obtained
- [ ] All deliverables completed to specification
- [ ] Files delivered in correct formats
- [ ] Usage guidelines provided
- [ ] Design is scalable and versatile

## 📚 Deliverables
{deliverables_list}
- Usage guidelines
- Source files
- Final production files

## 🛠️ Tools & Software
- Adobe Creative Suite (Illustrator, Photoshop, InDesign)
- Vector graphics software
- Color management tools
- File conversion utilities

## 💡 Design Considerations
- Brand consistency and alignment
- Scalability across different sizes
- Print and digital optimization
- Color reproduction accuracy
- Accessibility and readability"""


@dataclass
class BrandIdentityTemplate(Template):
    """Template for brand identity projects."""
    brand_scope: str = "startup"
    deliverables: List[str] = field(default_factory=lambda: ["Logo", "Brand guidelines", "Applications"])
    
    def __init__(self, name: str, complexity: TaskComplexity, brand_scope: str = "startup", 
                 deliverables: List[str] = None, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.brand_scope = brand_scope
        self.deliverables = deliverables or ["Logo", "Brand guidelines", "Applications"]
        # Generate content after initialization
        self.content = self._generate_brand_template()
    
    def _generate_brand_template(self) -> str:
        """Generate brand identity template content."""
        scope_title = self.brand_scope.replace('_', ' ').title()
        deliverables_list = "\n".join([f"- {item}" for item in self.deliverables])
        
        return f"""# {{{{ company_name | default("Brand Identity Project") }}}}

**Brand Scope**: {scope_title}
**Industry**: {{{{ industry | default("General") }}}}
**Target Market**: {{{{ target_market | default("General market") }}}}

## 🏢 Brand Strategy

**Brand Mission**: {{{{ brand_mission | default("To be defined") }}}}
**Brand Vision**: {{{{ brand_vision | default("To be defined") }}}}
**Brand Values**: 
{{% if brand_values %}}
{{% for value in brand_values %}}
- {{{{ value }}}}
{{% endfor %}}
{{% else %}}
- Quality
- Innovation
- Customer focus
{{% endif %}}

**Brand Personality**: {{{{ brand_personality | default("Professional and approachable") }}}}
**Unique Value Proposition**: {{{{ unique_value_prop | default("To be defined") }}}}

## 🚀 Brand Development Process

### Phase 1: Brand Strategy & Research (2-3 weeks)
- [ ] **Brand Audit**
  Assess current brand perception and assets
  
- [ ] **Market Research**
  Analyze industry landscape and trends
  
- [ ] **Competitive Analysis**
  Study competitor positioning and messaging
  
- [ ] **Stakeholder Interviews**
  Gather insights from key stakeholders
  
- [ ] **Brand Positioning**
  Define brand position in the market

### Phase 2: Brand Identity Development (3-4 weeks)
- [ ] **Logo Design**
  Create primary logo and variations
  
- [ ] **Color Palette**
  Develop brand color system
  
- [ ] **Typography**
  Select and define brand typefaces
  
- [ ] **Visual Elements**
  Create supporting design elements
  
- [ ] **Brand Guidelines**
  Document brand identity standards

### Phase 3: Brand Applications (2-3 weeks)
- [ ] **Stationery Design**
  Business cards, letterhead, envelopes
  
- [ ] **Digital Applications**
  Website elements, social media templates
  
- [ ] **Marketing Materials**
  Brochures, presentations, advertisements
  
- [ ] **Signage & Environmental**
  Office signage and environmental graphics

### Phase 4: Implementation & Launch (1-2 weeks)
- [ ] **Brand Manual Creation**
  Comprehensive brand guidelines document
  
- [ ] **Asset Organization**
  Organize all brand assets and files
  
- [ ] **Training Materials**
  Create brand implementation training
  
- [ ] **Launch Strategy**
  Plan brand rollout and communication

## 📊 Success Criteria
- [ ] Brand strategy clearly defined and documented
- [ ] Logo and visual identity completed
- [ ] Comprehensive brand guidelines created
- [ ] All brand applications designed
- [ ] Stakeholder approval obtained
- [ ] Implementation plan established

## 📚 Deliverables
{deliverables_list}
- Brand strategy document
- Brand guidelines manual
- Asset library and templates

## 🛠️ Tools & Resources
- Adobe Creative Suite
- Brand strategy frameworks
- Color theory resources
- Typography libraries
- Template creation tools

## 💡 Brand Considerations
**Brand Architecture**: {{{{ brand_architecture | default("Single brand approach") }}}}
**Scalability**: Design for future growth and expansion
**Flexibility**: Ensure adaptability across touchpoints
**Consistency**: Maintain coherent brand experience
**Differentiation**: Stand out in competitive landscape

## 🎯 Target Audience Analysis
**Primary Audience**: {{{{ primary_audience | default("To be defined") }}}}
**Secondary Audience**: {{{{ secondary_audience | default("To be defined") }}}}
**Audience Needs**: 
{{% if audience_needs %}}
{{% for need in audience_needs %}}
- {{{{ need }}}}
{{% endfor %}}
{{% else %}}
- Reliable products/services
- Clear communication
- Value for money
{{% endif %}}

## 📈 Brand Metrics & KPIs
- Brand awareness measurement
- Brand perception tracking
- Market share analysis
- Customer loyalty metrics
- Brand equity assessment"""


class DesignTemplateLibrary:
    """Library managing all design domain templates."""
    
    def __init__(self):
        """Initialize the design template library."""
        self.templates: Dict[str, Template] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load all default design templates."""
        # UI/UX design templates
        self.templates["ui_design_mobile"] = UIUXDesignTemplate(
            name="ui_design_mobile",
            complexity=TaskComplexity.MEDIUM,
            design_type="mobile_ui",
            platform="iOS/Android"
        )
        
        self.templates["ui_design_web"] = UIUXDesignTemplate(
            name="ui_design_web",
            complexity=TaskComplexity.MEDIUM,
            design_type="web_ui",
            platform="Web"
        )
        
        self.templates["ux_research_user_journey"] = UIUXDesignTemplate(
            name="ux_research_user_journey",
            complexity=TaskComplexity.HIGH,
            design_type="web_ux",
            platform="Web"
        )
        
        # Graphic design templates
        self.templates["graphic_design_logo"] = GraphicDesignTemplate(
            name="graphic_design_logo",
            complexity=TaskComplexity.MEDIUM,
            design_type="logo",
            deliverables=["Primary logo", "Logo variations", "Usage guidelines"]
        )
        
        self.templates["graphic_design_poster"] = GraphicDesignTemplate(
            name="graphic_design_poster",
            complexity=TaskComplexity.LOW,
            design_type="poster",
            deliverables=["Print-ready poster", "Digital version"]
        )
        
        # Brand identity templates
        self.templates["brand_identity_startup"] = BrandIdentityTemplate(
            name="brand_identity_startup",
            complexity=TaskComplexity.HIGH,
            brand_scope="startup",
            deliverables=["Logo suite", "Brand guidelines", "Marketing materials"]
        )
        
        self.templates["brand_identity_enterprise"] = BrandIdentityTemplate(
            name="brand_identity_enterprise",
            complexity=TaskComplexity.VERY_HIGH,
            brand_scope="enterprise",
            deliverables=["Complete brand system", "Implementation guidelines", "Training materials"]
        )
    
    def get_template(self, template_type: DesignTemplateType, 
                    complexity: TaskComplexity) -> Optional[Template]:
        """Get template by type and complexity."""
        for template in self.templates.values():
            if (hasattr(template, 'design_type') and 
                ((template_type == DesignTemplateType.UI_UX_DESIGN and 'ui' in template.design_type) or
                 (template_type == DesignTemplateType.GRAPHIC_DESIGN and template.design_type in ['logo', 'poster']) or
                 (template_type == DesignTemplateType.BRAND_IDENTITY and hasattr(template, 'brand_scope')))):
                if template.complexity == complexity:
                    return template
        
        # Return first match if exact complexity not found
        for template in self.templates.values():
            if (hasattr(template, 'design_type') and 
                ((template_type == DesignTemplateType.UI_UX_DESIGN and 'ui' in template.design_type) or
                 (template_type == DesignTemplateType.GRAPHIC_DESIGN and template.design_type in ['logo', 'poster']) or
                 (template_type == DesignTemplateType.BRAND_IDENTITY and hasattr(template, 'brand_scope')))):
                return template
        
        return None
    
    def get_templates_by_type(self, template_type: DesignTemplateType) -> List[Template]:
        """Get all templates of a specific type."""
        result = []
        for template in self.templates.values():
            if template_type == DesignTemplateType.UI_UX_DESIGN and isinstance(template, UIUXDesignTemplate):
                result.append(template)
            elif template_type == DesignTemplateType.GRAPHIC_DESIGN and isinstance(template, GraphicDesignTemplate):
                result.append(template)
            elif template_type == DesignTemplateType.BRAND_IDENTITY and isinstance(template, BrandIdentityTemplate):
                result.append(template)
        return result
