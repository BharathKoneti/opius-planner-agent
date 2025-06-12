"""
Unit tests for Design Project Templates - Following TDD approach.

Testing design domain templates including UI/UX design, graphic design,
and brand identity templates.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.templates.design_templates import (
    DesignTemplateLibrary,
    UIUXDesignTemplate,
    GraphicDesignTemplate,
    BrandIdentityTemplate,
    DesignTemplateType
)
from opius_planner.templates.template_engine import TemplateContext
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestDesignTemplateLibrary:
    """Test suite for DesignTemplateLibrary following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.library = DesignTemplateLibrary()
    
    def test_init_loads_all_design_templates(self):
        """Test that library initializes with all design templates."""
        library = DesignTemplateLibrary()
        
        assert library is not None
        assert hasattr(library, 'templates')
        assert len(library.templates) > 0
        
        # Should have all major design template types
        template_names = [t.name for t in library.templates.values()]
        expected_types = [
            'ui_design_mobile',
            'ui_design_web', 
            'ux_research_user_journey',
            'graphic_design_logo',
            'graphic_design_poster',
            'brand_identity_startup',
            'brand_identity_enterprise'
        ]
        
        for expected in expected_types:
            assert any(expected in name for name in template_names)
    
    def test_get_template_by_type_and_complexity(self):
        """Test retrieving templates by type and complexity."""
        # Test UI/UX design templates
        ui_template = self.library.get_template(
            template_type=DesignTemplateType.UI_UX_DESIGN,
            complexity=TaskComplexity.MEDIUM
        )
        
        assert ui_template is not None
        assert ui_template.category == TaskCategory.CREATIVE
        assert ui_template.complexity == TaskComplexity.MEDIUM
        
        # Test graphic design templates
        graphic_template = self.library.get_template(
            template_type=DesignTemplateType.GRAPHIC_DESIGN,
            complexity=TaskComplexity.LOW
        )
        
        assert graphic_template is not None
        assert graphic_template.category == TaskCategory.CREATIVE
    
    def test_get_all_templates_by_type(self):
        """Test getting all templates of a specific type."""
        ui_templates = self.library.get_templates_by_type(
            DesignTemplateType.UI_UX_DESIGN
        )
        
        assert isinstance(ui_templates, list)
        assert len(ui_templates) > 0
        assert all(isinstance(t, UIUXDesignTemplate) for t in ui_templates)
        
        brand_templates = self.library.get_templates_by_type(
            DesignTemplateType.BRAND_IDENTITY
        )
        
        assert isinstance(brand_templates, list)
        assert len(brand_templates) > 0
        assert all(isinstance(t, BrandIdentityTemplate) for t in brand_templates)


class TestUIUXDesignTemplate:
    """Test suite for UI/UX design templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mobile_ui_template = UIUXDesignTemplate(
            name="mobile_ui_template",
            complexity=TaskComplexity.MEDIUM,
            design_type="mobile_ui",
            platform="iOS/Android"
        )
        
        self.web_ux_template = UIUXDesignTemplate(
            name="web_ux_template", 
            complexity=TaskComplexity.HIGH,
            design_type="web_ux",
            platform="Web"
        )
    
    def test_ui_template_creation(self):
        """Test UI/UX template object creation."""
        template = self.mobile_ui_template
        
        assert template.name == "mobile_ui_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.complexity == TaskComplexity.MEDIUM
        assert template.design_type == "mobile_ui"
        assert template.platform == "iOS/Android"
    
    def test_render_mobile_ui_template(self):
        """Test rendering mobile UI template."""
        context = TemplateContext(
            project_name="FitTracker App",
            target_users="Fitness enthusiasts aged 25-40",
            key_features=["Workout tracking", "Progress analytics", "Social sharing"],
            design_style="Modern minimalist",
            color_palette="Blue and white with green accents"
        )
        
        result = self.mobile_ui_template.render(context)
        
        assert isinstance(result, str)
        assert "FitTracker App" in result
        assert "Fitness enthusiasts" in result
        assert "Workout tracking" in result
        assert "wireframe" in result.lower() or "mockup" in result.lower()
        assert "user interface" in result.lower() or "ui" in result.lower()
        assert "mobile" in result.lower()
    
    def test_render_web_ux_template(self):
        """Test rendering web UX template."""
        context = TemplateContext(
            project_name="E-commerce Dashboard",
            target_users="Online store managers",
            user_goals=["Manage inventory", "Track sales", "Customer insights"],
            platform="Web",
            research_methods=["User interviews", "Analytics review", "Competitor analysis"]
        )
        
        result = self.web_ux_template.render(context)
        
        assert isinstance(result, str)
        assert "E-commerce Dashboard" in result
        assert "Online store managers" in result
        assert "user research" in result.lower() or "ux research" in result.lower()
        assert "user journey" in result.lower() or "user flow" in result.lower()
        assert "web" in result.lower()
    
    def test_ui_template_includes_design_phases(self):
        """Test that UI/UX templates include proper design phases."""
        context = TemplateContext(
            project_name="Test App",
            design_style="Modern"
        )
        
        result = self.mobile_ui_template.render(context)
        
        # Should include standard design phases
        expected_phases = [
            "research", "wireframe", "prototype", "visual design", "testing"
        ]
        
        result_lower = result.lower()
        matched_phases = [phase for phase in expected_phases if phase in result_lower]
        assert len(matched_phases) >= 3  # Should have most design phases


class TestGraphicDesignTemplate:
    """Test suite for graphic design templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logo_template = GraphicDesignTemplate(
            name="logo_design_template",
            complexity=TaskComplexity.MEDIUM,
            design_type="logo",
            deliverables=["Primary logo", "Logo variations", "Brand guidelines"]
        )
        
        self.poster_template = GraphicDesignTemplate(
            name="poster_design_template",
            complexity=TaskComplexity.LOW,
            design_type="poster",
            deliverables=["Print-ready poster", "Digital version"]
        )
    
    def test_graphic_template_creation(self):
        """Test graphic design template object creation."""
        template = self.logo_template
        
        assert template.name == "logo_design_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.design_type == "logo"
        assert "Primary logo" in template.deliverables
    
    def test_render_logo_template(self):
        """Test rendering logo design template."""
        context = TemplateContext(
            client_name="OpusAI",
            industry="Artificial Intelligence",
            brand_personality=["Innovative", "Trustworthy", "Forward-thinking"],
            color_preferences="Blue, white, and subtle gradients",
            logo_usage=["Website header", "Business cards", "Mobile app icon"]
        )
        
        result = self.logo_template.render(context)
        
        assert isinstance(result, str)
        assert "OpusAI" in result
        assert "Artificial Intelligence" in result
        assert "Innovative" in result
        assert "logo" in result.lower()
        assert "brand" in result.lower()
        assert "design brief" in result.lower() or "creative brief" in result.lower()
    
    def test_render_poster_template(self):
        """Test rendering poster design template."""
        context = TemplateContext(
            event_name="Tech Innovation Summit 2024",
            event_date="March 15-16, 2024",
            venue="Silicon Valley Convention Center",
            key_speakers=["Dr. Sarah Chen", "Mark Rodriguez", "Lisa Wang"],
            design_theme="Futuristic and professional"
        )
        
        result = self.poster_template.render(context)
        
        assert isinstance(result, str)
        assert "Tech Innovation Summit 2024" in result
        assert "March 15-16, 2024" in result
        assert "Dr. Sarah Chen" in result
        assert "poster" in result.lower()
        assert "design" in result.lower()


class TestBrandIdentityTemplate:
    """Test suite for brand identity templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.startup_brand_template = BrandIdentityTemplate(
            name="startup_brand_template",
            complexity=TaskComplexity.HIGH,
            brand_scope="startup",
            deliverables=["Logo suite", "Brand guidelines", "Marketing materials"]
        )
        
        self.enterprise_brand_template = BrandIdentityTemplate(
            name="enterprise_brand_template",
            complexity=TaskComplexity.VERY_HIGH,
            brand_scope="enterprise",
            deliverables=["Complete brand system", "Implementation guidelines", "Training materials"]
        )
    
    def test_brand_template_creation(self):
        """Test brand identity template object creation."""
        template = self.startup_brand_template
        
        assert template.name == "startup_brand_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.brand_scope == "startup"
        assert "Logo suite" in template.deliverables
    
    def test_render_startup_brand_template(self):
        """Test rendering startup brand template."""
        context = TemplateContext(
            company_name="EcoTech Solutions",
            industry="Sustainable Technology",
            target_market="Environmentally conscious consumers",
            brand_values=["Sustainability", "Innovation", "Transparency"],
            brand_personality="Approachable yet professional",
            competitors=["GreenTech Inc", "EcoInnovate", "SustainableTech"]
        )
        
        result = self.startup_brand_template.render(context)
        
        assert isinstance(result, str)
        assert "EcoTech Solutions" in result
        assert "Sustainable Technology" in result
        assert "Sustainability" in result
        assert "brand identity" in result.lower()
        assert "brand strategy" in result.lower() or "brand positioning" in result.lower()
    
    def test_render_enterprise_brand_template(self):
        """Test rendering enterprise brand template."""
        context = TemplateContext(
            company_name="Global Financial Corp",
            industry="Financial Services",
            market_presence="International",
            brand_architecture="Master brand with sub-brands",
            stakeholders=["Executives", "Marketing teams", "Regional offices"]
        )
        
        result = self.enterprise_brand_template.render(context)
        
        assert isinstance(result, str)
        assert "Global Financial Corp" in result
        assert "Financial Services" in result
        assert "brand architecture" in result.lower()
        assert "enterprise" in result.lower() or "corporate" in result.lower()


class TestDesignTemplateType:
    """Test suite for DesignTemplateType enum."""
    
    def test_design_template_type_values(self):
        """Test that DesignTemplateType has expected values."""
        expected_types = {
            'UI_UX_DESIGN', 'GRAPHIC_DESIGN', 'BRAND_IDENTITY'
        }
        actual_types = {template_type.name for template_type in DesignTemplateType}
        assert actual_types == expected_types
    
    def test_template_type_descriptions(self):
        """Test that template types have meaningful descriptions."""
        for template_type in DesignTemplateType:
            assert hasattr(template_type, 'value')
            assert len(template_type.value) > 0


class TestDesignTemplateIntegration:
    """Integration tests for design templates with existing system."""
    
    def test_design_templates_integrate_with_main_engine(self):
        """Test that design templates integrate with main TemplateEngine."""
        from opius_planner.templates.template_engine import TemplateEngine
        
        # Initialize main engine
        main_engine = TemplateEngine()
        
        # Initialize design library
        design_library = DesignTemplateLibrary()
        
        # Register design templates with main engine
        for template in design_library.templates.values():
            main_engine.register_template(template)
        
        # Should be able to load design templates through main engine
        design_template = main_engine.load_template(
            TaskCategory.CREATIVE, 
            TaskComplexity.MEDIUM
        )
        
        assert design_template is not None
        assert design_template.category == TaskCategory.CREATIVE
    
    def test_design_templates_work_with_planner_agent(self):
        """Test design templates work with PlannerAgent."""
        from opius_planner.cli.main import PlannerAgent
        
        # This test verifies the integration works
        agent = PlannerAgent()
        
        # Should be able to generate plans for design tasks
        plan = agent.generate_plan(
            task_description="Design a modern mobile app UI for a fitness tracking application",
            agentic=True
        )
        
        assert isinstance(plan, str)
        assert len(plan) > 50  # Should generate substantial content
        assert "design" in plan.lower() or "ui" in plan.lower()
    
    def test_design_workflow_includes_user_research(self):
        """Test that design templates include user research phases."""
        library = DesignTemplateLibrary()
        
        ui_template = library.get_template(
            DesignTemplateType.UI_UX_DESIGN,
            TaskComplexity.HIGH
        )
        
        context = TemplateContext(
            project_name="User Research Project",
            target_users="Mobile users"
        )
        
        result = ui_template.render(context)
        
        # Should include user research elements
        research_terms = ["user research", "user interview", "survey", "persona", "user journey"]
        result_lower = result.lower()
        
        matches = [term for term in research_terms if term in result_lower]
        assert len(matches) >= 2  # Should include multiple research elements
    
    def test_brand_template_includes_strategy_phase(self):
        """Test that brand templates include strategic planning."""
        library = DesignTemplateLibrary()
        
        brand_template = library.get_template(
            DesignTemplateType.BRAND_IDENTITY,
            TaskComplexity.HIGH
        )
        
        context = TemplateContext(
            company_name="Strategy Test Corp",
            industry="Technology"
        )
        
        result = brand_template.render(context)
        
        # Should include strategic elements
        strategy_terms = ["brand strategy", "positioning", "competitive analysis", "brand audit"]
        result_lower = result.lower()
        
        matches = [term for term in strategy_terms if term in result_lower]
        assert len(matches) >= 1  # Should include strategic planning
