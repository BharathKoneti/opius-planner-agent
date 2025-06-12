"""
Creative Templates Library - Phase 2 Implementation.

Provides specialized templates for creative domain tasks including
story writing, blog posts, articles, poetry, and screenplays.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from ..core.task_analyzer import TaskCategory, TaskComplexity
from .template_engine import Template, TemplateContext


class CreativeTemplateType(Enum):
    """Types of creative templates available."""
    STORY_WRITING = "story_writing"
    BLOG_POST = "blog_post"
    ARTICLE = "article"
    POETRY = "poetry"
    SCREENPLAY = "screenplay"


@dataclass
class StoryWritingTemplate(Template):
    """Template for story writing projects."""
    story_type: str = "short_story"
    estimated_word_count: int = 5000
    
    def __init__(self, name: str, complexity: TaskComplexity, story_type: str = "short_story", 
                 estimated_word_count: int = 5000, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set in post_init
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.story_type = story_type
        self.estimated_word_count = estimated_word_count
        # Generate content after initialization
        self.content = self._generate_story_template()
    
    def _generate_story_template(self) -> str:
        """Generate story writing template content."""
        return f"""# {{{{ story_title | default("Story Writing Project") }}}}

**Genre**: {{{{ genre | default("Fiction") }}}}
**Target Audience**: {{{{ target_audience | default("General") }}}}
**Estimated Word Count**: {{{{ word_count | default("{self.estimated_word_count}") }}}}

## 🤖 **LLM Memory Management Instructions**

**CRITICAL**: Before starting any creative work, create and maintain these documents for persistent memory:

#### **1. 📊 Creative Analysis Document (`creative_analysis.md`)**
Create a comprehensive analysis document and link it here: `[Creative Analysis](./creative_analysis.md)`

**Document Structure**:
```markdown
# Creative Analysis - {{{{ story_title | default("Story Writing Project") }}}}

## 🎯 Creative Vision
- **Core Theme**: [Central message or idea]
- **Genre Conventions**: [What readers expect from this genre]
- **Target Audience**: [Who will read this and what they want]
- **Unique Angle**: [What makes this story different]

## 📝 Story Analysis
- **Character Development**: [Main character arcs and growth]
- **Plot Structure**: [Beginning, middle, end analysis]
- **Conflict Analysis**: [Internal and external conflicts]
- **Setting Details**: [World-building and atmosphere]

## 🔍 Creative Strategy
- **Writing Style**: [Voice, tone, pacing decisions]
- **Research Needs**: [Background information required]
- **Creative Challenges**: [Difficult scenes or concepts]
- **Quality Standards**: [What makes this story successful]

## 🔄 Ongoing Creative Updates
[Keep updating as you develop the story]
```

#### **2. 📝 Creative Work Log (`creative_work_log.md`)**
Create a detailed creative work log and link it here: `[Creative Work Log](./creative_work_log.md)`

**Work Log Structure**:
```markdown
# Creative Work Log - {{{{ story_title | default("Story Writing Project") }}}}

## 📊 Quick Reference
- **Project Start**: [Date]
- **Current Phase**: [Brainstorming/Writing/Editing]
- **Word Count Progress**: [Current/Target words]
- **Last Creative Session**: [What was accomplished]
- **Creative Challenges**: [Current creative blocks or issues]

## 📅 Daily Creative Sessions

### [Date] - [Session Description]
**Time Spent**: [Duration]
**Phase**: [Current creative phase]
**Words Written**: [New words added]
**Scenes/Chapters Completed**:
- [Specific scene/chapter with brief description]

**Creative Discoveries**:
- [Character insights discovered]
- [Plot developments that emerged]
- [Creative solutions found]

**Creative Challenges**:
- [Writing blocks encountered]: [How addressed]
- [Character/plot problems]: [Solutions attempted]

**Next Session Plan**:
- [Specific scenes to write]
- [Character/plot issues to resolve]

## 🚫 Creative Mistakes Archive
**Purpose**: Prevent repeating creative mistakes

### [Mistake Category]
- **Issue**: [What didn't work creatively]
- **Why It Failed**: [Reason it didn't work]
- **Better Approach**: [Improved creative solution]
- **Prevention**: [How to avoid in future]
```

**Instructions for Creative Work**:
- **Start of each session**: Review analysis and previous session notes
- **Before major plot decisions**: Check analysis for character consistency
- **After creative breakthroughs**: Document insights in both files
- **When stuck**: Review work log for patterns and solutions

## 📝 Story Overview

**Theme**: {{{{ theme | default("To be determined") }}}}
**Main Character**: {{{{ main_character | default("Protagonist") }}}}
**Setting**: {{{{ setting | default("To be determined") }}}}

## 🚀 Writing Process

### Phase 1: Brainstorming & Planning (1-2 days)
- [ ] **Create Analysis Document**: Set up creative_analysis.md with vision and strategy
- [ ] **Create Work Log**: Set up creative_work_log.md for session tracking
- [ ] **Develop Core Concept**
  Define the central idea and conflict (document in analysis)
- [ ] **Character Development**
  Create detailed character profiles (update analysis with insights)
- [ ] **World Building**
  Establish setting and rules (document research needs)

### Phase 2: Story Structure (1-2 days)
- [ ] **Update Analysis**: Refine understanding based on planning
- [ ] **Create Story Outline**
  Plan beginning, middle, and end (reference analysis for consistency)
- [ ] **Plot Points Planning**
  Identify key scenes and turning points
- [ ] **Conflict Resolution**
  Plan how conflicts will be resolved

### Phase 3: Writing ({{{{ estimated_duration | default("1-2 weeks") }}}})
- [ ] **Daily Work Log Updates**: Track progress and discoveries
- [ ] **First Draft**
  Write without editing, focus on story (log insights)
- [ ] **Character Dialogue**
  Develop authentic character voices (note voice discoveries)
- [ ] **Scene Development**
  Write detailed, engaging scenes (document creative solutions)

### Phase 4: Revision & Editing (3-5 days)
- [ ] **Review Analysis & Work Log**: Check for consistency and missed opportunities
- [ ] **Content Revision**
  Review plot, character development, pacing (update analysis)
- [ ] **Line Editing**
  Improve sentence structure and flow
- [ ] **Final Proofread**
  Check grammar, spelling, formatting

## 🔄 Creative Progress Tracking
**Instructions**: Update daily with creative discoveries and progress

### {{{{ current_date | default("2025-12-15") }}}}
- **Creative Analysis**: [Creative Analysis](./creative_analysis.md) - [Document current creative understanding]
- **Work Log**: [Creative Work Log](./creative_work_log.md) - [Session summary and creative discoveries]
- **Words Written**: [Number] / {self.estimated_word_count} target
- **Creative Breakthroughs**: [Any character or plot insights]
- **Next Session**: [Specific creative goals for next session]

## 📊 Success Criteria
- [ ] Story reaches target word count ({self.estimated_word_count} words)
- [ ] Character arc is complete and satisfying
- [ ] Plot is engaging with clear resolution
- [ ] Writing style is consistent throughout
- [ ] Grammar and spelling are error-free
- [ ] Creative analysis documents show clear vision achievement

## 📚 Resources
- Writing craft books
- Character development worksheets
- Story structure guides
- Writing community feedback

## 💡 Tips
- Set daily writing goals
- Don't edit while writing first draft
- Read your dialogue aloud
- Get feedback from beta readers
- Always update your creative analysis and work log"""


@dataclass
class BlogPostTemplate(Template):
    """Template for blog post creation."""
    blog_type: str = "personal"
    target_word_count: int = 800
    
    def __init__(self, name: str, complexity: TaskComplexity, blog_type: str = "personal", 
                 target_word_count: int = 800, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.blog_type = blog_type
        self.target_word_count = target_word_count
        # Generate content after initialization
        self.content = self._generate_blog_template()
    
    def _generate_blog_template(self) -> str:
        """Generate blog post template content."""
        return f"""# {{{{ post_title | default("Blog Post Title") }}}}

**Topic**: {{{{ topic | default("General") }}}}
**Target Word Count**: {{{{ target_word_count | default("{self.target_word_count}") }}}}
**Target Audience**: {{{{ target_audience | default("General readers") }}}}

## 📝 Blog Post Planning

### Content Strategy
- [ ] **Define Your Angle**
  {{% if personal_angle %}}{{{{ personal_angle }}}}{{% else %}}What unique perspective will you bring?{{% endif %}}
  
- [ ] **Identify Key Points**
  {{% if key_points %}}
  {{% for point in key_points %}}
  - {{{{ point }}}}
  {{% endfor %}}
  {{% else %}}
  - Main point 1
  - Main point 2
  - Main point 3
  {{% endif %}}

## 🚀 Writing Process

### Phase 1: Research & Outline (1-2 hours)
- [ ] **Topic Research**
  Gather information and supporting data
  
- [ ] **Create Outline**
  Structure your main points logically
  
- [ ] **Hook Development**
  Plan engaging opening

### Phase 2: Writing (2-3 hours)
- [ ] **Write Introduction**
  Hook readers with compelling opening
  
- [ ] **Develop Body Sections**
  Expand on each main point with examples
  
- [ ] **Craft Conclusion**
  Summarize and provide call to action

### Phase 3: Editing & Optimization (30-60 minutes)
- [ ] **Content Review**
  Ensure clarity and flow
  
- [ ] **SEO Optimization**
  Add relevant keywords naturally
  
- [ ] **Final Polish**
  Check grammar and readability

## 📊 Success Criteria
- [ ] Post reaches target word count ({self.target_word_count} words)
- [ ] Content provides clear value to readers
- [ ] Writing is engaging and easy to read
- [ ] Call to action is clear and compelling
{{% if call_to_action %}}{{{{ call_to_action }}}}{{% endif %}}

## 📚 Resources
- Keyword research tools
- Grammar checking software
- Blog analytics platform
- Social media for promotion"""


@dataclass
class ArticleTemplate(Template):
    """Template for article writing."""
    article_type: str = "news"
    target_word_count: int = 600
    
    def __init__(self, name: str, complexity: TaskComplexity, article_type: str = "news", 
                 target_word_count: int = 600, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.article_type = article_type
        self.target_word_count = target_word_count
        # Generate content after initialization
        self.content = self._generate_article_template()
    
    def _generate_article_template(self) -> str:
        """Generate article template content."""
        return f"""# {{{{ headline | default("Article Headline") }}}}

**Article Type**: {{{{ article_type | default("{self.article_type}") }}}}
**Target Word Count**: {{{{ target_word_count | default("{self.target_word_count}") }}}}
**Publication**: {{{{ publication | default("TBD") }}}}

## 📰 Article Planning

### Story Elements
- [ ] **Lead/Opening**
  {{% if lead %}}{{{{ lead }}}}{{% else %}}Compelling opening paragraph{{% endif %}}
  
- [ ] **Key Information**
  - **Who**: {{{{ who | default("Key people involved") }}}}
  - **What**: {{{{ what | default("What happened") }}}}
  - **When**: {{{{ when | default("When it occurred") }}}}
  - **Where**: {{{{ where | default("Where it took place") }}}}
  - **Why**: {{{{ why | default("Why it matters") }}}}

## 🚀 Writing Process

### Phase 1: Research & Interviews (2-4 hours)
- [ ] **Source Identification**
  Find credible sources and experts
  
- [ ] **Conduct Interviews**
  Gather quotes and firsthand information
  
- [ ] **Fact Verification**
  Confirm all details and statistics

### Phase 2: Writing (2-3 hours)
- [ ] **Write Lead**
  Create compelling opening paragraph
  
- [ ] **Develop Body**
  Present information in logical order
  
- [ ] **Add Quotes**
  Include relevant expert opinions

### Phase 3: Editing & Fact-Check (1 hour)
- [ ] **Content Review**
  Ensure accuracy and completeness
  
- [ ] **Style Check**
  Follow publication guidelines
  
- [ ] **Final Proofread**
  Check grammar and attribution

## 📊 Success Criteria
- [ ] Article meets word count ({self.target_word_count} words)
- [ ] All facts are verified and accurate
- [ ] Sources are properly cited
- [ ] Writing follows publication style guide
- [ ] Story has clear news value

## 📚 Resources
{{% if research_sources %}}
{{% for source in research_sources %}}
- {{{{ source }}}}
{{% endfor %}}
{{% else %}}
- Primary sources and interviews
- Industry publications
- Expert contacts
- Fact-checking databases
{{% endif %}}"""


@dataclass  
class PoetryTemplate(Template):
    """Template for poetry creation."""
    poetry_type: str = "free_verse"
    structure: str = "flexible"
    
    def __init__(self, name: str, complexity: TaskComplexity, poetry_type: str = "free_verse", 
                 structure: str = "flexible", **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.poetry_type = poetry_type
        self.structure = structure
        # Generate content after initialization
        self.content = self._generate_poetry_template()
    
    def _generate_poetry_template(self) -> str:
        """Generate poetry template content."""
        success_criteria = ""
        if self.poetry_type == "sonnet":
            success_criteria = """- [ ] 14 lines following sonnet structure
- [ ] Consistent rhyme scheme
- [ ] Iambic pentameter maintained"""
        else:
            success_criteria = """- [ ] Poem expresses intended theme clearly
- [ ] Language is evocative and precise
- [ ] Structure serves the content"""
        
        return f"""# {{{{ poem_title | default("Poetry Project") }}}}

**Poetry Type**: {{{{ poetry_type | default("{self.poetry_type}") }}}}
**Structure**: {{{{ structure | default("{self.structure}") }}}}
**Theme**: {{{{ theme | default("To be determined") }}}}

## 🎭 Poetry Planning

### Creative Elements
- [ ] **Central Theme**
  {{{{ theme | default("What is the poem about?") }}}}
  
- [ ] **Mood/Tone**
  {{{{ mood | default("What feeling should it evoke?") }}}}
  
- [ ] **Imagery**
  {{% if imagery %}}
  {{% for image in imagery %}}
  - {{{{ image }}}}
  {{% endfor %}}
  {{% else %}}
  - Visual images
  - Sensory details
  - Metaphors/similes
  {{% endif %}}

## 🚀 Creation Process

### Phase 1: Inspiration & Planning (30-60 minutes)
- [ ] **Brainstorm Ideas**
  Collect thoughts, images, emotions
  
- [ ] **Choose Form**
  Decide on structure and style
  
- [ ] **Gather Inspiration**
  Read related poetry, observe surroundings

### Phase 2: Writing (1-2 hours)
- [ ] **First Draft**
  Write freely without editing
  
- [ ] **Experiment with Language**
  Play with word choice and sounds
  
- [ ] **Develop Imagery**
  Create vivid, meaningful pictures

### Phase 3: Revision (30-45 minutes)
- [ ] **Read Aloud**
  Listen to rhythm and flow
  
- [ ] **Refine Language**
  Choose most powerful words
  
- [ ] **Polish Structure**
  Adjust line breaks and stanzas

## 📊 Success Criteria
{success_criteria}
- [ ] Imagery is vivid and meaningful
- [ ] Overall impact is emotionally resonant

## 📚 Resources
- Poetry collections for inspiration
- Rhyming dictionary (if needed)
- Online poetry communities
- Writing prompts and exercises"""


@dataclass
class ScreenplayTemplate(Template):
    """Template for screenplay writing."""
    screenplay_type: str = "short_film"
    estimated_pages: int = 15
    
    def __init__(self, name: str, complexity: TaskComplexity, screenplay_type: str = "short_film", 
                 estimated_pages: int = 15, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.CREATIVE,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.screenplay_type = screenplay_type
        self.estimated_pages = estimated_pages
        # Generate content after initialization
        self.content = self._generate_screenplay_template()
    
    def _generate_screenplay_template(self) -> str:
        """Generate screenplay template content."""
        return f"""# {{{{ title | default("Screenplay Title") }}}}

**Genre**: {{{{ genre | default("Drama") }}}}
**Type**: {{{{ screenplay_type | default("{self.screenplay_type}") }}}}
**Estimated Pages**: {{{{ estimated_pages | default("{self.estimated_pages}") }}}}
**Runtime**: {{{{ estimated_runtime | default("15 minutes") }}}}

## 🎬 Screenplay Development

### Story Elements
- [ ] **Logline**
  {{% if logline %}}{{{{ logline }}}}{{% else %}}One sentence story summary{{% endif %}}
  
- [ ] **Main Characters**
  {{% if main_characters %}}
  {{% for character in main_characters %}}
  - {{{{ character }}}}
  {{% endfor %}}
  {{% else %}}
  - Protagonist
  - Antagonist  
  - Supporting characters
  {{% endif %}}

## 🚀 Writing Process

### Phase 1: Story Development (1-2 days)
- [ ] **Develop Premise**
  Expand logline into full concept
  
- [ ] **Character Creation**
  Develop detailed character profiles
  
- [ ] **Plot Outline**
  {{% if three_act_structure %}}Plan three-act structure{{% else %}}Create scene-by-scene outline{{% endif %}}

### Phase 2: Screenplay Writing (3-5 days)
- [ ] **Format Setup**
  Use proper screenplay formatting
  
- [ ] **Scene Writing**
  Write each scene with proper headers
  
- [ ] **Dialogue Development**
  Create authentic character voices

### Phase 3: Revision (2-3 days)
- [ ] **Structure Review**
  Ensure proper pacing and flow
  
- [ ] **Dialogue Polish**
  Refine character voices and subtext
  
- [ ] **Format Check**
  Verify industry-standard formatting

## 📊 Success Criteria
- [ ] Screenplay reaches target page count ({self.estimated_pages} pages)
- [ ] Story has clear beginning, middle, end
- [ ] Characters have distinct voices
- [ ] Formatting follows industry standards
{{% if three_act_structure %}}{{{{ three_act_structure }}}}{{% endif %}}
- [ ] Visual storytelling is emphasized

## 📚 Resources
- Screenplay formatting software
- Industry script examples
- Character development guides
- Screenwriting craft books

## 💡 Formatting Notes
- Scene headers: INT./EXT. LOCATION - TIME
- Character names in ALL CAPS when speaking
- Action lines in present tense
- One page ≈ one minute of screen time"""


class CreativeTemplateLibrary:
    """Library managing all creative domain templates."""
    
    def __init__(self):
        """Initialize the creative template library."""
        self.templates: Dict[str, Template] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load all default creative templates."""
        # Story writing templates
        self.templates["story_writing_short"] = StoryWritingTemplate(
            name="story_writing_short",
            complexity=TaskComplexity.MEDIUM,
            story_type="short_story",
            estimated_word_count=5000
        )
        
        self.templates["story_writing_novel"] = StoryWritingTemplate(
            name="story_writing_novel",
            complexity=TaskComplexity.VERY_HIGH,
            story_type="novel",
            estimated_word_count=80000
        )
        
        # Blog post templates
        self.templates["blog_post_personal"] = BlogPostTemplate(
            name="blog_post_personal",
            complexity=TaskComplexity.LOW,
            blog_type="personal",
            target_word_count=800
        )
        
        self.templates["blog_post_professional"] = BlogPostTemplate(
            name="blog_post_professional",
            complexity=TaskComplexity.MEDIUM,
            blog_type="professional",
            target_word_count=1500
        )
        
        # Article templates
        self.templates["article_news"] = ArticleTemplate(
            name="article_news",
            complexity=TaskComplexity.MEDIUM,
            article_type="news",
            target_word_count=600
        )
        
        self.templates["article_feature"] = ArticleTemplate(
            name="article_feature",
            complexity=TaskComplexity.HIGH,
            article_type="feature",
            target_word_count=2000
        )
        
        # Poetry templates
        self.templates["poetry_free_verse"] = PoetryTemplate(
            name="poetry_free_verse",
            complexity=TaskComplexity.MEDIUM,
            poetry_type="free_verse",
            structure="flexible"
        )
        
        self.templates["poetry_structured"] = PoetryTemplate(
            name="poetry_structured",
            complexity=TaskComplexity.HIGH,
            poetry_type="sonnet",
            structure="14_lines_iambic_pentameter"
        )
        
        # Screenplay templates
        self.templates["screenplay_short"] = ScreenplayTemplate(
            name="screenplay_short",
            complexity=TaskComplexity.MEDIUM,
            screenplay_type="short_film",
            estimated_pages=15
        )
        
        self.templates["screenplay_feature"] = ScreenplayTemplate(
            name="screenplay_feature",
            complexity=TaskComplexity.VERY_HIGH,
            screenplay_type="feature_film",
            estimated_pages=120
        )
    
    def get_template(self, template_type: CreativeTemplateType, 
                    complexity: TaskComplexity) -> Optional[Template]:
        """Get template by type and complexity."""
        for template in self.templates.values():
            if (hasattr(template, 'poetry_type') and template_type == CreativeTemplateType.POETRY) or \
               (hasattr(template, 'story_type') and template_type == CreativeTemplateType.STORY_WRITING) or \
               (hasattr(template, 'blog_type') and template_type == CreativeTemplateType.BLOG_POST) or \
               (hasattr(template, 'article_type') and template_type == CreativeTemplateType.ARTICLE) or \
               (hasattr(template, 'screenplay_type') and template_type == CreativeTemplateType.SCREENPLAY):
                if template.complexity == complexity:
                    return template
        
        # Return first match if exact complexity not found
        for template in self.templates.values():
            if (hasattr(template, 'poetry_type') and template_type == CreativeTemplateType.POETRY) or \
               (hasattr(template, 'story_type') and template_type == CreativeTemplateType.STORY_WRITING) or \
               (hasattr(template, 'blog_type') and template_type == CreativeTemplateType.BLOG_POST) or \
               (hasattr(template, 'article_type') and template_type == CreativeTemplateType.ARTICLE) or \
               (hasattr(template, 'screenplay_type') and template_type == CreativeTemplateType.SCREENPLAY):
                return template
        
        return None
    
    def get_templates_by_type(self, template_type: CreativeTemplateType) -> List[Template]:
        """Get all templates of a specific type."""
        result = []
        for template in self.templates.values():
            if template_type == CreativeTemplateType.STORY_WRITING and hasattr(template, 'story_type'):
                result.append(template)
            elif template_type == CreativeTemplateType.BLOG_POST and hasattr(template, 'blog_type'):
                result.append(template)
            elif template_type == CreativeTemplateType.ARTICLE and hasattr(template, 'article_type'):
                result.append(template)
            elif template_type == CreativeTemplateType.POETRY and hasattr(template, 'poetry_type'):
                result.append(template)
            elif template_type == CreativeTemplateType.SCREENPLAY and hasattr(template, 'screenplay_type'):
                result.append(template)
        return result
