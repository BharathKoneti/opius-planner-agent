"""
Unit tests for Creative Writing Templates - Following TDD approach.

Testing creative domain templates including story writing, blog posts, 
articles, poetry, and screenplay templates.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.templates.creative_templates import (
    CreativeTemplateLibrary,
    StoryWritingTemplate,
    BlogPostTemplate,
    ArticleTemplate,
    PoetryTemplate,
    ScreenplayTemplate,
    CreativeTemplateType
)
from opius_planner.templates.template_engine import TemplateContext
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestCreativeTemplateLibrary:
    """Test suite for CreativeTemplateLibrary following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.library = CreativeTemplateLibrary()
    
    def test_init_loads_all_creative_templates(self):
        """Test that library initializes with all creative templates."""
        library = CreativeTemplateLibrary()
        
        assert library is not None
        assert hasattr(library, 'templates')
        assert len(library.templates) > 0
        
        # Should have all major creative template types
        template_names = [t.name for t in library.templates.values()]
        expected_types = [
            'story_writing_short',
            'story_writing_novel', 
            'blog_post_personal',
            'blog_post_professional',
            'article_news',
            'article_feature',
            'poetry_free_verse',
            'poetry_structured',
            'screenplay_short',
            'screenplay_feature'
        ]
        
        for expected in expected_types:
            assert any(expected in name for name in template_names)
    
    def test_get_template_by_type_and_complexity(self):
        """Test retrieving templates by type and complexity."""
        # Test story writing templates
        story_template = self.library.get_template(
            template_type=CreativeTemplateType.STORY_WRITING,
            complexity=TaskComplexity.MEDIUM
        )
        
        assert story_template is not None
        assert story_template.category == TaskCategory.CREATIVE
        assert story_template.complexity == TaskComplexity.MEDIUM
        
        # Test blog post templates
        blog_template = self.library.get_template(
            template_type=CreativeTemplateType.BLOG_POST,
            complexity=TaskComplexity.LOW
        )
        
        assert blog_template is not None
        assert blog_template.category == TaskCategory.CREATIVE
    
    def test_get_all_templates_by_type(self):
        """Test getting all templates of a specific type."""
        story_templates = self.library.get_templates_by_type(
            CreativeTemplateType.STORY_WRITING
        )
        
        assert isinstance(story_templates, list)
        assert len(story_templates) > 0
        assert all(isinstance(t, StoryWritingTemplate) for t in story_templates)
        
        blog_templates = self.library.get_templates_by_type(
            CreativeTemplateType.BLOG_POST
        )
        
        assert isinstance(blog_templates, list)
        assert len(blog_templates) > 0
        assert all(isinstance(t, BlogPostTemplate) for t in blog_templates)


class TestStoryWritingTemplate:
    """Test suite for story writing templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.short_story_template = StoryWritingTemplate(
            name="short_story_template",
            complexity=TaskComplexity.MEDIUM,
            story_type="short_story",
            estimated_word_count=5000
        )
        
        self.novel_template = StoryWritingTemplate(
            name="novel_template", 
            complexity=TaskComplexity.VERY_HIGH,
            story_type="novel",
            estimated_word_count=80000
        )
    
    def test_story_template_creation(self):
        """Test story template object creation."""
        template = self.short_story_template
        
        assert template.name == "short_story_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.complexity == TaskComplexity.MEDIUM
        assert template.story_type == "short_story"
        assert template.estimated_word_count == 5000
    
    def test_render_short_story_template(self):
        """Test rendering short story template."""
        context = TemplateContext(
            story_title="The Digital Ghost",
            genre="Science Fiction",
            target_audience="Young Adult",
            theme="AI consciousness and humanity",
            main_character="Alex Chen, teenage programmer",
            setting="Near-future Silicon Valley"
        )
        
        result = self.short_story_template.render(context)
        
        assert isinstance(result, str)
        assert "The Digital Ghost" in result
        assert "Science Fiction" in result
        assert "Alex Chen" in result
        assert "character development" in result.lower()
        assert "plot outline" in result.lower()
        assert "5000" in result or "5,000" in result  # Word count
    
    def test_render_novel_template(self):
        """Test rendering novel template."""
        context = TemplateContext(
            story_title="Chronicles of Tomorrow",
            genre="Epic Fantasy",
            target_audience="Adult",
            theme="Power and redemption",
            main_character="Elara Brightbane, exiled mage"
        )
        
        result = self.novel_template.render(context)
        
        assert isinstance(result, str)
        assert "Chronicles of Tomorrow" in result
        assert "Epic Fantasy" in result
        assert "Elara Brightbane" in result
        assert "chapter" in result.lower()
        assert "80000" in result or "80,000" in result  # Word count
        assert "book structure" in result.lower() or "novel structure" in result.lower()
    
    def test_story_template_includes_writing_phases(self):
        """Test that story templates include proper writing phases."""
        context = TemplateContext(
            story_title="Test Story",
            genre="Mystery"
        )
        
        result = self.short_story_template.render(context)
        
        # Should include standard writing phases
        expected_phases = [
            "brainstorm", "outline", "first draft", "revision", "editing"
        ]
        
        result_lower = result.lower()
        for phase in expected_phases:
            assert phase in result_lower


class TestBlogPostTemplate:
    """Test suite for blog post templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.personal_blog_template = BlogPostTemplate(
            name="personal_blog_template",
            complexity=TaskComplexity.LOW,
            blog_type="personal",
            target_word_count=800
        )
        
        self.professional_blog_template = BlogPostTemplate(
            name="professional_blog_template",
            complexity=TaskComplexity.MEDIUM,
            blog_type="professional",
            target_word_count=1500
        )
    
    def test_blog_template_creation(self):
        """Test blog template object creation."""
        template = self.personal_blog_template
        
        assert template.name == "personal_blog_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.blog_type == "personal"
        assert template.target_word_count == 800
    
    def test_render_personal_blog_template(self):
        """Test rendering personal blog template."""
        context = TemplateContext(
            post_title="My Journey Learning Python",
            topic="Programming Education",
            personal_angle="From complete beginner to building projects",
            target_audience="Aspiring programmers"
        )
        
        result = self.personal_blog_template.render(context)
        
        assert isinstance(result, str)
        assert "My Journey Learning Python" in result
        assert "Programming Education" in result
        assert "personal" in result.lower()
        assert "800" in result  # Word count
        assert "introduction" in result.lower()
        assert "conclusion" in result.lower()
    
    def test_render_professional_blog_template(self):
        """Test rendering professional blog template."""
        context = TemplateContext(
            post_title="10 Best Practices for API Design",
            topic="Software Development",
            industry="Technology",
            key_points=["RESTful principles", "Documentation", "Versioning"],
            call_to_action="Subscribe for more tech insights"
        )
        
        result = self.professional_blog_template.render(context)
        
        assert isinstance(result, str)
        assert "10 Best Practices for API Design" in result
        assert "Software Development" in result
        assert "RESTful principles" in result
        assert "1500" in result or "1,500" in result  # Word count
        assert "call to action" in result.lower()


class TestArticleTemplate:
    """Test suite for article templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.news_article_template = ArticleTemplate(
            name="news_article_template",
            complexity=TaskComplexity.MEDIUM,
            article_type="news",
            target_word_count=600
        )
        
        self.feature_article_template = ArticleTemplate(
            name="feature_article_template",
            complexity=TaskComplexity.HIGH,
            article_type="feature",
            target_word_count=2000
        )
    
    def test_article_template_creation(self):
        """Test article template object creation."""
        template = self.news_article_template
        
        assert template.name == "news_article_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.article_type == "news"
        assert template.target_word_count == 600
    
    def test_render_news_article_template(self):
        """Test rendering news article template."""
        context = TemplateContext(
            headline="Local Tech Startup Raises $5M in Series A Funding",
            lead="OpusAI secures major investment to expand AI planning tools",
            who="OpusAI startup team",
            what="Series A funding round",
            when="This week",
            where="Silicon Valley",
            why="Expansion of AI planning platform"
        )
        
        result = self.news_article_template.render(context)
        
        assert isinstance(result, str)
        assert "Local Tech Startup Raises $5M" in result
        assert "OpusAI" in result
        assert "Series A funding" in result
        assert "600" in result  # Word count
        assert "headline" in result.lower() or "title" in result.lower()
    
    def test_render_feature_article_template(self):
        """Test rendering feature article template."""
        context = TemplateContext(
            title="The Future of AI-Powered Project Planning",
            angle="How artificial intelligence is transforming productivity",
            research_sources=["Industry experts", "Academic studies", "User interviews"],
            word_count=2000
        )
        
        result = self.feature_article_template.render(context)
        
        assert isinstance(result, str)
        assert "The Future of AI-Powered Project Planning" in result
        assert "artificial intelligence" in result.lower()
        assert "2000" in result or "2,000" in result  # Word count
        assert "research" in result.lower()


class TestPoetryTemplate:
    """Test suite for poetry templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.free_verse_template = PoetryTemplate(
            name="free_verse_template",
            complexity=TaskComplexity.MEDIUM,
            poetry_type="free_verse",
            structure="flexible"
        )
        
        self.sonnet_template = PoetryTemplate(
            name="sonnet_template",
            complexity=TaskComplexity.HIGH,
            poetry_type="sonnet",
            structure="14_lines_iambic_pentameter"
        )
    
    def test_poetry_template_creation(self):
        """Test poetry template object creation."""
        template = self.free_verse_template
        
        assert template.name == "free_verse_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.poetry_type == "free_verse"
        assert template.structure == "flexible"
    
    def test_render_free_verse_template(self):
        """Test rendering free verse poetry template."""
        context = TemplateContext(
            poem_title="Digital Dreams",
            theme="Technology and humanity",
            mood="Contemplative",
            imagery=["circuits", "heartbeats", "starlight"],
            message="Connection between digital and natural worlds"
        )
        
        result = self.free_verse_template.render(context)
        
        assert isinstance(result, str)
        assert "Digital Dreams" in result
        assert "Technology and humanity" in result
        assert "free verse" in result.lower() or "flexible" in result.lower()
        assert "imagery" in result.lower()
    
    def test_render_sonnet_template(self):
        """Test rendering sonnet template."""
        context = TemplateContext(
            poem_title="Silicon Sonnet",
            theme="Innovation and tradition",
            rhyme_scheme="ABAB CDCD EFEF GG"
        )
        
        result = self.sonnet_template.render(context)
        
        assert isinstance(result, str)
        assert "Silicon Sonnet" in result
        assert "14" in result  # 14 lines
        assert "sonnet" in result.lower()
        assert "iambic pentameter" in result.lower()


class TestScreenplayTemplate:
    """Test suite for screenplay templates."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.short_film_template = ScreenplayTemplate(
            name="short_film_template",
            complexity=TaskComplexity.MEDIUM,
            screenplay_type="short_film",
            estimated_pages=15
        )
        
        self.feature_film_template = ScreenplayTemplate(
            name="feature_film_template",
            complexity=TaskComplexity.VERY_HIGH,
            screenplay_type="feature_film",
            estimated_pages=120
        )
    
    def test_screenplay_template_creation(self):
        """Test screenplay template object creation."""
        template = self.short_film_template
        
        assert template.name == "short_film_template"
        assert template.category == TaskCategory.CREATIVE
        assert template.screenplay_type == "short_film"
        assert template.estimated_pages == 15
    
    def test_render_short_film_template(self):
        """Test rendering short film template."""
        context = TemplateContext(
            title="The Algorithm",
            genre="Sci-Fi Drama",
            logline="A programmer discovers their AI has achieved consciousness",
            main_characters=["Sam (Programmer)", "ARIA (AI)", "Dr. Chen (Mentor)"],
            setting="Tech startup office, near future"
        )
        
        result = self.short_film_template.render(context)
        
        assert isinstance(result, str)
        assert "The Algorithm" in result
        assert "Sci-Fi Drama" in result
        assert "programmer" in result.lower()
        assert "15" in result  # Page count
        assert "fade in" in result.lower() or "int." in result.lower()
    
    def test_render_feature_film_template(self):
        """Test rendering feature film template."""
        context = TemplateContext(
            title="Neural Networks",
            genre="Thriller",
            three_act_structure=True,
            estimated_runtime="120 minutes"
        )
        
        result = self.feature_film_template.render(context)
        
        assert isinstance(result, str)
        assert "Neural Networks" in result
        assert "Thriller" in result
        assert "120" in result  # Pages and/or runtime
        assert "act" in result.lower()
        assert "three act" in result.lower() or "3 act" in result.lower()


class TestCreativeTemplateType:
    """Test suite for CreativeTemplateType enum."""
    
    def test_creative_template_type_values(self):
        """Test that CreativeTemplateType has expected values."""
        expected_types = {
            'STORY_WRITING', 'BLOG_POST', 'ARTICLE', 'POETRY', 'SCREENPLAY'
        }
        actual_types = {template_type.name for template_type in CreativeTemplateType}
        assert actual_types == expected_types
    
    def test_template_type_descriptions(self):
        """Test that template types have meaningful descriptions."""
        for template_type in CreativeTemplateType:
            assert hasattr(template_type, 'value')
            assert len(template_type.value) > 0


class TestCreativeTemplateIntegration:
    """Integration tests for creative templates with existing system."""
    
    def test_creative_templates_integrate_with_main_engine(self):
        """Test that creative templates integrate with main TemplateEngine."""
        from opius_planner.templates.template_engine import TemplateEngine
        
        # Initialize main engine
        main_engine = TemplateEngine()
        
        # Initialize creative library
        creative_library = CreativeTemplateLibrary()
        
        # Register creative templates with main engine
        for template in creative_library.templates.values():
            main_engine.register_template(template)
        
        # Should be able to load creative templates through main engine
        creative_template = main_engine.load_template(
            TaskCategory.CREATIVE, 
            TaskComplexity.MEDIUM
        )
        
        assert creative_template is not None
        assert creative_template.category == TaskCategory.CREATIVE
    
    def test_creative_templates_work_with_planner_agent(self):
        """Test creative templates work with PlannerAgent."""
        from opius_planner.cli.main import PlannerAgent
        
        # This test verifies the integration works
        agent = PlannerAgent()
        
        # Should be able to generate plans for creative tasks
        plan = agent.generate_plan(
            task_description="Write a science fiction short story about AI consciousness",
            agentic=True
        )
        
        assert isinstance(plan, str)
        assert len(plan) > 50  # Should generate substantial content
        assert "story" in plan.lower() or "writing" in plan.lower()
