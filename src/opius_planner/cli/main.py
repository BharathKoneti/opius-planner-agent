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
from ..templates.template_engine import TemplateEngine, TemplateContext
from ..templates.markdown_generator import MarkdownGenerator, MarkdownMetadata, FrontmatterFormat
from ..templates.technical_templates import TechnicalTemplateLibrary, TechnicalTemplateType
from ..templates.creative_templates import CreativeTemplateLibrary, CreativeTemplateType
from ..templates.design_templates import DesignTemplateLibrary, DesignTemplateType


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
        
        # Initialize rich template libraries
        self.technical_templates = TechnicalTemplateLibrary()
        self.creative_templates = CreativeTemplateLibrary()
        self.design_templates = DesignTemplateLibrary()
    
    def generate_plan(self, task_description: str, template: Optional[str] = None, 
                     complexity: Optional[TaskComplexity] = None,
                     format_type: str = "markdown", agentic: bool = False,
                     enhance_with_llm: bool = True) -> str:
        """Generate a comprehensive plan for the given task using rich templates."""
        
        # Analyze the task to understand category and complexity
        task_analysis = self.task_analyzer.analyze_task(task_description)
        actual_complexity = complexity or task_analysis.complexity
        
        # Try to get rich template based on task analysis
        rich_template = self._select_rich_template(task_analysis.category, actual_complexity, task_description)
        
        if rich_template:
            # Use rich template system
            context = self._create_template_context(task_description, task_analysis)
            markdown_output = rich_template.render(context)
        else:
            # Fallback to basic plan generator
            plan = self.plan_generator.generate_plan(task_description)
            
            # Convert to markdown
            if agentic:
                self.markdown_generator.agentic_mode = True
            
            markdown_output = self.markdown_generator.generate_from_plan(plan)
        
        # Enhance with LLM if requested
        if enhance_with_llm:
            markdown_output = self._enhance_plan_with_llm(markdown_output, task_description, task_analysis)
        
        # Add frontmatter if requested
        if format_type == "yaml-frontmatter":
            metadata = MarkdownMetadata(
                title=task_description,
                category=task_analysis.category.value if task_analysis.category else None,
                complexity=actual_complexity.name if actual_complexity else None,
                created_at=task_analysis.generated_at if hasattr(task_analysis, 'generated_at') else None,
                tags=[]
            )
            markdown_output = self.markdown_generator.generate_with_frontmatter(markdown_output, metadata)
        
        return markdown_output
    
    def _select_rich_template(self, category: TaskCategory, complexity: TaskComplexity, task_description: str):
        """Select appropriate rich template based on task analysis."""
        task_lower = task_description.lower()
        
        if category == TaskCategory.TECHNICAL:
            # Determine technical template type based on keywords
            if any(keyword in task_lower for keyword in ['website', 'web', 'app', 'application', 'software', 'api', 'backend', 'frontend', 'mobile']):
                return self.technical_templates.get_template(TechnicalTemplateType.SOFTWARE_DEVELOPMENT, complexity)
            elif any(keyword in task_lower for keyword in ['ci/cd', 'deployment', 'devops', 'pipeline', 'infrastructure', 'docker', 'kubernetes']):
                return self.technical_templates.get_template(TechnicalTemplateType.DEVOPS, complexity)
            elif any(keyword in task_lower for keyword in ['test', 'testing', 'qa', 'automation']):
                return self.technical_templates.get_template(TechnicalTemplateType.TESTING, complexity)
            else:
                # Default to software development for technical tasks
                return self.technical_templates.get_template(TechnicalTemplateType.SOFTWARE_DEVELOPMENT, complexity)
        
        elif category == TaskCategory.CREATIVE:
            # Determine creative template type based on keywords
            if any(keyword in task_lower for keyword in ['story', 'novel', 'fiction', 'book', 'writing']):
                return self.creative_templates.get_template(CreativeTemplateType.STORY_WRITING, complexity)
            elif any(keyword in task_lower for keyword in ['blog', 'post', 'article']):
                return self.creative_templates.get_template(CreativeTemplateType.BLOG_POST, complexity)
            elif any(keyword in task_lower for keyword in ['screenplay', 'script', 'film', 'movie']):
                return self.creative_templates.get_template(CreativeTemplateType.SCREENPLAY, complexity)
            elif any(keyword in task_lower for keyword in ['poem', 'poetry', 'verse']):
                return self.creative_templates.get_template(CreativeTemplateType.POETRY, complexity)
            else:
                # Default to story writing for creative tasks
                return self.creative_templates.get_template(CreativeTemplateType.STORY_WRITING, complexity)
        
        # For now, return None for other categories to use fallback
        # TODO: Add business, personal, educational template selection
        return None
    
    def _create_template_context(self, task_description: str, task_analysis) -> TemplateContext:
        """Create rich template context from task analysis."""
        # Extract key information from task description
        context_data = {
            'task_description': task_description,
            'project_name': self._extract_project_name(task_description),
            'description': task_description,
        }
        
        # Add technical-specific context
        if hasattr(task_analysis, 'category') and task_analysis.category == TaskCategory.TECHNICAL:
            context_data.update({
                'key_features': self._extract_features(task_description),
                'tech_requirements': self._extract_tech_requirements(task_description),
                'target_users': self._extract_target_users(task_description),
                'deployment_target': self._extract_deployment_target(task_description),
            })
        
        # Add creative-specific context
        elif hasattr(task_analysis, 'category') and task_analysis.category == TaskCategory.CREATIVE:
            context_data.update({
                'genre': self._extract_genre(task_description),
                'target_audience': self._extract_target_audience(task_description),
                'theme': self._extract_theme(task_description),
            })
        
        return TemplateContext(**context_data)
    
    def _extract_project_name(self, task_description: str) -> str:
        """Extract project name from task description."""
        desc_lower = task_description.lower()
        
        # Look for specific project type patterns
        if 'photography' in desc_lower and ('portfolio' in desc_lower or 'website' in desc_lower):
            return 'Photography Portfolio Website'
        elif 'e-commerce' in desc_lower or 'shopping' in desc_lower:
            return 'E-commerce Website'
        elif 'blog' in desc_lower and 'website' in desc_lower:
            return 'Blog Website'
        elif 'portfolio' in desc_lower and 'website' in desc_lower:
            return 'Portfolio Website'
        elif 'dashboard' in desc_lower:
            return 'Analytics Dashboard'
        elif 'api' in desc_lower and ('rest' in desc_lower or 'service' in desc_lower):
            return 'API Service'
        elif 'mobile app' in desc_lower or 'mobile application' in desc_lower:
            return 'Mobile Application'
        elif 'web app' in desc_lower or 'web application' in desc_lower:
            return 'Web Application'
        elif 'website' in desc_lower:
            return 'Website Project'
        elif 'app' in desc_lower or 'application' in desc_lower:
            return 'Application Project'
        
        # Fallback: take meaningful words, avoid "build", "create", "develop"
        words = task_description.split()
        meaningful_words = []
        skip_words = {'build', 'create', 'develop', 'make', 'design', 'implement', 'a', 'an', 'the', 'with', 'for', 'and'}
        
        for word in words:
            if word.lower() not in skip_words and len(word) > 2:
                meaningful_words.append(word.title())
                if len(meaningful_words) >= 3:  # Limit to 3 words
                    break
        
        if meaningful_words:
            return ' '.join(meaningful_words)
        
        return task_description.title()[:50]  # Fallback with length limit
    
    def _extract_features(self, task_description: str) -> list:
        """Extract key features from task description."""
        features = []
        desc_lower = task_description.lower()
        
        # Common feature keywords
        feature_keywords = {
            'authentication': 'User authentication',
            'login': 'User authentication', 
            'gallery': 'Interactive gallery',
            'booking': 'Booking system',
            'payment': 'Payment integration',
            'responsive': 'Responsive design',
            'shopping cart': 'Shopping cart',
            'dashboard': 'Analytics dashboard',
            'portfolio': 'Portfolio showcase',
        }
        
        for keyword, feature in feature_keywords.items():
            if keyword in desc_lower and feature not in features:
                features.append(feature)
        
        return features or ['Core functionality', 'User management', 'Data persistence']
    
    def _extract_tech_requirements(self, task_description: str) -> list:
        """Extract technical requirements from task description."""
        requirements = []
        desc_lower = task_description.lower()
        
        if 'responsive' in desc_lower:
            requirements.append('Responsive design')
        if 'authentication' in desc_lower or 'login' in desc_lower:
            requirements.append('Secure authentication')
        if 'api' in desc_lower:
            requirements.append('API integration')
        if 'database' in desc_lower or 'data' in desc_lower:
            requirements.append('Database management')
        
        return requirements or ['Responsive design', 'Secure authentication', 'API integration']
    
    def _extract_target_users(self, task_description: str) -> str:
        """Extract target users from task description."""
        desc_lower = task_description.lower()
        
        if 'photographer' in desc_lower:
            return 'Photography clients and visitors'
        elif 'business' in desc_lower:
            return 'Business users and clients'
        elif 'personal' in desc_lower:
            return 'Personal contacts and visitors'
        
        return 'General users'
    
    def _extract_deployment_target(self, task_description: str) -> str:
        """Extract deployment target from task description."""
        desc_lower = task_description.lower()
        
        if 'aws' in desc_lower:
            return 'AWS'
        elif 'vercel' in desc_lower:
            return 'Vercel'
        elif 'netlify' in desc_lower:
            return 'Netlify'
        elif 'heroku' in desc_lower:
            return 'Heroku'
        
        return 'Cloud provider'
    
    def _extract_genre(self, task_description: str) -> str:
        """Extract genre for creative projects."""
        desc_lower = task_description.lower()
        
        if 'fantasy' in desc_lower:
            return 'Fantasy'
        elif 'science fiction' in desc_lower or 'sci-fi' in desc_lower:
            return 'Science Fiction'
        elif 'romance' in desc_lower:
            return 'Romance'
        elif 'thriller' in desc_lower:
            return 'Thriller'
        elif 'mystery' in desc_lower:
            return 'Mystery'
        
        return 'Fiction'
    
    def _extract_target_audience(self, task_description: str) -> str:
        """Extract target audience for creative projects."""
        desc_lower = task_description.lower()
        
        if 'young adult' in desc_lower or 'ya' in desc_lower:
            return 'Young Adult'
        elif 'children' in desc_lower:
            return 'Children'
        elif 'adult' in desc_lower:
            return 'Adult'
        
        return 'General'
    
    def _extract_theme(self, task_description: str) -> str:
        """Extract theme for creative projects."""
        desc_lower = task_description.lower()
        
        if 'redemption' in desc_lower:
            return 'Redemption'
        elif 'love' in desc_lower:
            return 'Love and relationships'
        elif 'adventure' in desc_lower:
            return 'Adventure and discovery'
        elif 'power' in desc_lower:
            return 'Power and responsibility'
        
        return 'To be determined'
    
    def _enhance_plan_with_llm(self, plan_content: str, task_description: str, task_analysis) -> str:
        """Enhance the generated plan using LLM review and improvement."""
        
        enhancement_prompt = f"""
You are an expert project manager and technical architect. Please review and enhance the following project plan to make it more specific, actionable, and comprehensive.

ORIGINAL TASK: {task_description}
TASK CATEGORY: {task_analysis.category.value}
TASK COMPLEXITY: {task_analysis.complexity.name}

CURRENT PLAN:
{plan_content}

ENHANCEMENT INSTRUCTIONS:
1. **Make it more specific**: Replace generic terms with specific technologies, tools, and methods appropriate for this exact project
2. **Add missing details**: Include important technical considerations, potential challenges, and specific deliverables
3. **Improve actionability**: Make each task more concrete with clear acceptance criteria
4. **Add context-aware recommendations**: Suggest specific tools, frameworks, and approaches based on the project type
5. **Include realistic time estimates**: Provide more accurate duration estimates based on the specific requirements
6. **Add risk considerations**: Include potential risks and mitigation strategies
7. **Technology-specific guidance**: If it's a technical project, suggest appropriate tech stacks, architectures, and best practices
8. **Quality improvements**: Add specific quality gates, testing strategies, and success metrics

RULES:
- Keep the same overall structure and formatting
- Maintain all the existing sections (Project Tracker, Development Process, etc.)
- Replace generic placeholder content with specific, project-relevant details
- Add new subsections where helpful but don't remove existing ones
- Make sure recommendations are current and follow best practices
- Include specific tools and technologies where appropriate
- Add estimated durations that are realistic for the project scope

Enhanced Plan:"""

        try:
            # This is a placeholder for LLM integration
            # In a real implementation, this would call an LLM API like OpenAI, Claude, etc.
            enhanced_plan = self._call_llm_for_enhancement(enhancement_prompt)
            
            if enhanced_plan and len(enhanced_plan.strip()) > len(plan_content) * 0.8:
                # Only use enhanced plan if it's substantially improved
                return enhanced_plan
            else:
                # Fallback to manual enhancement if LLM fails
                return self._manual_plan_enhancement(plan_content, task_description, task_analysis)
        
        except Exception as e:
            # If LLM enhancement fails, use manual enhancement
            click.echo(f"LLM enhancement failed ({str(e)}), using manual enhancement", err=True)
            return self._manual_plan_enhancement(plan_content, task_description, task_analysis)
    
    def _call_llm_for_enhancement(self, prompt: str) -> str:
        """Call LLM API for plan enhancement. This is a placeholder for actual LLM integration."""
        
        # TODO: Implement actual LLM integration here
        # This could integrate with:
        # - OpenAI API (GPT-4)
        # - Anthropic Claude API
        # - Local LLM via ollama
        # - Azure OpenAI
        # etc.
        
        # For now, return None to trigger manual enhancement
        return None
    
    def _manual_plan_enhancement(self, plan_content: str, task_description: str, task_analysis) -> str:
        """Manual plan enhancement with specific improvements based on task analysis."""
        
        enhanced_plan = plan_content
        
        # Add specific technology recommendations based on project type
        if task_analysis.category == TaskCategory.TECHNICAL:
            enhanced_plan = self._add_technical_specifics(enhanced_plan, task_description)
        elif task_analysis.category == TaskCategory.CREATIVE:
            enhanced_plan = self._add_creative_specifics(enhanced_plan, task_description)
        
        # Add risk assessment section
        enhanced_plan = self._add_risk_assessment(enhanced_plan, task_description, task_analysis)
        
        # Add specific quality gates
        enhanced_plan = self._add_quality_gates(enhanced_plan, task_analysis.category)
        
        return enhanced_plan
    
    def _add_technical_specifics(self, plan: str, task_description: str) -> str:
        """Add specific technical recommendations."""
        desc_lower = task_description.lower()
        
        # Add specific tech stack recommendations
        tech_recommendations = []
        
        if 'website' in desc_lower or 'web' in desc_lower:
            if 'portfolio' in desc_lower:
                tech_recommendations.extend([
                    "**Frontend**: Next.js 14 with TypeScript for optimal SEO and performance",
                    "**Styling**: Tailwind CSS for responsive design and fast development", 
                    "**Image Optimization**: Next.js Image component with Cloudinary integration",
                    "**Hosting**: Vercel for seamless deployment and edge optimization"
                ])
            elif 'e-commerce' in desc_lower:
                tech_recommendations.extend([
                    "**Framework**: Next.js 14 with App Router for modern e-commerce architecture",
                    "**Database**: PostgreSQL with Prisma ORM for robust data management",
                    "**Payment**: Stripe integration with webhook handling",
                    "**State Management**: Zustand for cart and user state management",
                    "**Authentication**: NextAuth.js with multiple providers",
                    "**Hosting**: Vercel with Supabase for database hosting"
                ])
            else:
                tech_recommendations.extend([
                    "**Frontend**: React 18 with TypeScript for type safety",
                    "**Backend**: Node.js with Express.js or Fastify",
                    "**Database**: PostgreSQL for relational data or MongoDB for flexible schemas",
                    "**Authentication**: JWT with refresh tokens"
                ])
        
        if 'mobile' in desc_lower:
            tech_recommendations.extend([
                "**Framework**: React Native with Expo for cross-platform development",
                "**Navigation**: React Navigation v6 for smooth navigation",
                "**State Management**: Redux Toolkit with RTK Query for API calls",
                "**Push Notifications**: Expo Notifications with Firebase backend"
            ])
        
        # Insert tech recommendations
        if tech_recommendations:
            tech_section = f"""

## 🔧 **Recommended Technology Stack**

{chr(10).join(tech_recommendations)}

## 🏗️ **Architecture Considerations**
- **Security**: Implement HTTPS, input validation, and secure authentication
- **Performance**: Use CDN for static assets, implement caching strategies
- **Scalability**: Design with horizontal scaling in mind, use microservices if needed
- **Monitoring**: Implement logging, error tracking (Sentry), and performance monitoring
"""
            # Insert after Technology Stack section
            plan = plan.replace("## 📊 Project Tracker", tech_section + "\n## 📊 Project Tracker")
        
        return plan
    
    def _add_creative_specifics(self, plan: str, task_description: str) -> str:
        """Add specific creative project recommendations."""
        desc_lower = task_description.lower()
        
        if 'novel' in desc_lower or 'story' in desc_lower:
            creative_tools = """

## ✍️ **Recommended Writing Tools**
- **Writing Software**: Scrivener for organization or Google Docs for collaboration
- **Grammar**: Grammarly Premium for style and grammar checking
- **Research**: Notion for character development and world-building notes
- **Backup**: Automatic cloud sync (Google Drive, Dropbox) for version control

## 📖 **Story Development Framework**
- **Three-Act Structure**: Setup (25%), Confrontation (50%), Resolution (25%)
- **Character Arcs**: Each major character should have clear growth trajectory
- **Plot Points**: Inciting incident, plot points 1 & 2, climax, resolution
- **World-building**: Consistent rules, geography, culture, and history"""
            
            plan = plan.replace("## 📚 Resources", creative_tools + "\n## 📚 Resources")
        
        return plan
    
    def _add_risk_assessment(self, plan: str, task_description: str, task_analysis) -> str:
        """Add risk assessment and mitigation strategies."""
        
        risks = []
        
        if task_analysis.category == TaskCategory.TECHNICAL:
            risks.extend([
                "**Technical Risk**: Technology stack incompatibility → Mitigation: Proof of concept early",
                "**Security Risk**: Data breaches or vulnerabilities → Mitigation: Security audit and penetration testing",
                "**Performance Risk**: Poor app performance under load → Mitigation: Load testing and performance optimization",
                "**Integration Risk**: Third-party API failures → Mitigation: Fallback mechanisms and error handling"
            ])
            
            if task_analysis.complexity >= TaskComplexity.HIGH:
                risks.append("**Scope Creep Risk**: Requirements inflation → Mitigation: Clear change request process")
        
        elif task_analysis.category == TaskCategory.CREATIVE:
            risks.extend([
                "**Creative Block Risk**: Writer's block or lack of inspiration → Mitigation: Regular brainstorming sessions",
                "**Quality Risk**: Not meeting creative vision → Mitigation: Regular review and feedback cycles",
                "**Timeline Risk**: Creative work taking longer than expected → Mitigation: Buffer time in schedule"
            ])
        
        if risks:
            risk_section = f"""

## ⚠️ **Risk Assessment & Mitigation**

{chr(10).join([f"- {risk}" for risk in risks])}

### 🚨 **Contingency Planning**
- **Regular Risk Reviews**: Weekly assessment of identified risks
- **Escalation Process**: Clear escalation path for major blockers
- **Resource Buffer**: 20% time buffer for unexpected challenges
"""
            plan = plan.replace("## 📊 Success Criteria", risk_section + "\n## 📊 Success Criteria")
        
        return plan
    
    def _add_quality_gates(self, plan: str, category: TaskCategory) -> str:
        """Add specific quality gates and checkpoints."""
        
        if category == TaskCategory.TECHNICAL:
            quality_section = """

## 🎯 **Quality Gates & Checkpoints**

### Code Quality
- [ ] **Code Review**: All code reviewed by at least one other developer
- [ ] **Test Coverage**: Minimum 80% code coverage maintained
- [ ] **Static Analysis**: ESLint/SonarQube passing with no critical issues
- [ ] **Security Scan**: Automated security vulnerability scanning

### Performance Quality
- [ ] **Load Testing**: Application handles expected user load
- [ ] **Performance Budget**: Page load times under 3 seconds
- [ ] **Mobile Performance**: Lighthouse score > 90 for mobile
- [ ] **Accessibility**: WCAG 2.1 AA compliance verified

### Release Quality
- [ ] **User Acceptance Testing**: All user stories accepted by stakeholders
- [ ] **Browser Compatibility**: Tested on major browsers (Chrome, Firefox, Safari, Edge)
- [ ] **Documentation**: Technical and user documentation complete
- [ ] **Deployment Verification**: Production deployment tested and verified"""
            
            plan = plan.replace("## 💡 Technical Considerations", quality_section + "\n## 💡 Technical Considerations")
        
        return plan


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
@click.option('--output', '-o', type=click.Path(), help='Output file path (defaults to localtest/plan.md)')
@click.option('--agentic', is_flag=True, help='Generate agentic-friendly output')
@click.option('--enhance/--no-enhance', default=True, help='Enhance plan with LLM review (default: enabled)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--config', type=click.Path(exists=False), help='Configuration file path')
def generate_plan(task_description: str, template: Optional[str], complexity: Optional[str],
                 format_type: str, output: Optional[str], agentic: bool, enhance: bool, 
                 verbose: bool, config: Optional[str]):
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
            if enhance:
                click.echo("Plan enhancement: ENABLED")
            else:
                click.echo("Plan enhancement: DISABLED")
        
        # Parse complexity if provided
        complexity_enum = parse_complexity(complexity) if complexity else None
        
        # Generate plan
        plan_content = agent.generate_plan(
            task_description=task_description,
            template=template,
            complexity=complexity_enum,
            format_type=format_type,
            agentic=agentic,
            enhance_with_llm=enhance
        )
        
        # Determine output path
        if not output:
            # Create default filename in localtest folder
            import re
            safe_name = re.sub(r'[^\w\s-]', '', task_description.lower())
            safe_name = re.sub(r'[-\s]+', '_', safe_name)[:50]
            output = f"localtest/{safe_name}_plan.md"
        
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
                if enhance:
                    click.echo("Plan enhanced with specific recommendations and quality gates")
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
