"""
Task Analyzer - Intelligent task categorization and analysis.

This module provides sophisticated task analysis capabilities including:
- Task categorization (Creative, Technical, Business, Personal, Educational)
- Complexity assessment (Low, Medium, High, Very High)
- Duration estimation based on complexity
- Required skills identification
- Success criteria generation
"""

import hashlib
import re
from enum import Enum, IntEnum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from functools import lru_cache


class TaskCategory(Enum):
    """Categories for different types of tasks."""
    CREATIVE = "creative"
    TECHNICAL = "technical"
    BUSINESS = "business"
    PERSONAL = "personal"
    EDUCATIONAL = "educational"


class TaskComplexity(IntEnum):
    """Complexity levels for tasks, ordered from lowest to highest."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


@dataclass
class TaskAnalysis:
    """Complete analysis results for a task."""
    category: TaskCategory
    complexity: TaskComplexity
    estimated_duration: str
    required_skills: List[str]
    dependencies: List[str]
    success_criteria: List[str]
    keywords: List[str]
    confidence_score: float


class TaskAnalyzer:
    """Universal task analysis engine."""
    
    def __init__(self):
        """Initialize the TaskAnalyzer with predefined patterns and mappings."""
        self.categories = self._initialize_category_patterns()
        self.complexity_levels = self._initialize_complexity_patterns()
        self.skill_patterns = self._initialize_skill_patterns()
        self.duration_mappings = self._initialize_duration_mappings()
        self._analysis_cache = {}
    
    def _initialize_category_patterns(self) -> Dict[TaskCategory, List[str]]:
        """Initialize keyword patterns for task categorization."""
        return {
            TaskCategory.CREATIVE: [
                'write', 'novel', 'story', 'poem', 'song', 'music', 'art', 'design',
                'creative', 'painting', 'drawing', 'photography', 'video', 'film',
                'animation', 'craft', 'sculpt', 'compose', 'choreograph'
            ],
            TaskCategory.TECHNICAL: [
                'build', 'develop', 'code', 'program', 'app', 'application', 'website',
                'software', 'system', 'database', 'api', 'framework', 'algorithm',
                'machine learning', 'ai', 'react', 'flask',
                'django', 'node', 'sql', 'docker', 'kubernetes', 'cloud', 'server'
            ],
            TaskCategory.BUSINESS: [
                'marketing', 'business', 'strategy', 'budget', 'finance',
                'sales', 'revenue', 'profit', 'market', 'customer', 'client',
                'proposal', 'presentation', 'meeting', 'team', 'management',
                'analysis', 'report', 'roi', 'kpi', 'growth', 'launch'
            ],
            TaskCategory.PERSONAL: [
                'wedding', 'vacation', 'trip', 'party', 'event', 'personal',
                'family', 'home', 'fitness', 'health', 'diet', 'exercise',
                'organize', 'clean', 'decorate', 'garden', 'hobby', 'birthday'
            ],
            TaskCategory.EDUCATIONAL: [
                'learn', 'study', 'course', 'tutorial', 'training', 'education',
                'skill', 'practice', 'master', 'understand', 'research',
                'knowledge', 'exam', 'certification', 'degree', 'lesson', 'programming'
            ]
        }
    
    def _initialize_complexity_patterns(self) -> Dict[TaskComplexity, List[str]]:
        """Initialize patterns for complexity assessment."""
        return {
            TaskComplexity.LOW: [
                'simple', 'basic', 'easy', 'quick', 'straightforward', 'minimal',
                'to-do', 'list', 'note', 'reminder', 'small', 'single'
            ],
            TaskComplexity.MEDIUM: [
                'web application', 'app', 'system', 'moderate', 'standard',
                'typical', 'regular', 'normal', 'medium', 'average'
            ],
            TaskComplexity.HIGH: [
                'complex', 'advanced', 'sophisticated', 'comprehensive',
                'machine learning', 'ai', 'ai-powered', 'distributed', 'scalable',
                'enterprise', 'large-scale', 'multi-tier', 'recommendation system'
            ],
            TaskComplexity.VERY_HIGH: [
                'space mission', 'rocket', 'nasa', 'satellite', 'orbital',
                'massive', 'revolutionary', 'breakthrough', 'cutting-edge',
                'research', 'PhD', 'dissertation', 'thesis', 'innovation'
            ]
        }
    
    def _initialize_skill_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for skill identification."""
        return {
            'Python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
            'JavaScript': ['javascript', 'js', 'node', 'nodejs', 'npm'],
            'React': ['react', 'reactjs', 'jsx', 'redux'],
            'Web Development': ['web', 'html', 'css', 'frontend', 'backend'],
            'Database Design': ['database', 'sql', 'postgresql', 'mysql', 'mongodb'],
            'Testing': ['test', 'testing', 'unit test', 'integration test', 'tdd'],
            'TypeScript': ['typescript', 'ts'],
            'DevOps': ['docker', 'kubernetes', 'ci/cd', 'deployment'],
            'Machine Learning': ['ml', 'machine learning', 'ai', 'neural', 'model'],
            'Design': ['design', 'ui', 'ux', 'graphic', 'visual'],
            'Project Management': ['project', 'management', 'agile', 'scrum'],
            'Writing': ['write', 'writing', 'content', 'documentation', 'copy']
        }
    
    def _initialize_duration_mappings(self) -> Dict[TaskComplexity, str]:
        """Initialize duration estimates based on complexity."""
        return {
            TaskComplexity.LOW: '1-3 days',
            TaskComplexity.MEDIUM: '1-2 weeks',
            TaskComplexity.HIGH: '2-6 weeks',
            TaskComplexity.VERY_HIGH: '2-6 months'
        }
    
    def categorize_task(self, task_description: str) -> TaskAnalysis:
        """Categorize a task based on its description."""
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty")
        
        task_lower = task_description.lower()
        category_scores = {}
        
        for category, patterns in self.categories.items():
            score = sum(1 for pattern in patterns if pattern in task_lower)
            if score > 0:
                category_scores[category] = score
        
        # Default to TECHNICAL if no clear match
        best_category = max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else TaskCategory.TECHNICAL
        
        return TaskAnalysis(
            category=best_category,
            complexity=TaskComplexity.MEDIUM,  # Default complexity
            estimated_duration="TBD",
            required_skills=[],
            dependencies=[],
            success_criteria=[],
            keywords=[],
            confidence_score=0.8
        )
    
    def analyze_complexity(self, task_description: str) -> TaskAnalysis:
        """Analyze the complexity level of a task."""
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty")
        
        task_lower = task_description.lower()
        complexity_scores = {}
        
        for complexity, patterns in self.complexity_levels.items():
            score = 0
            for pattern in patterns:
                # Use word boundary matching to prevent substring issues
                if re.search(r'\b' + re.escape(pattern) + r'\b', task_lower):
                    score += 1
            if score > 0:
                complexity_scores[complexity] = score
        
        # Default to MEDIUM if no clear match
        best_complexity = max(complexity_scores.items(), key=lambda x: x[1])[0] if complexity_scores else TaskComplexity.MEDIUM
        
        return TaskAnalysis(
            category=TaskCategory.TECHNICAL,  # Default category
            complexity=best_complexity,
            estimated_duration="TBD",
            required_skills=[],
            dependencies=[],
            success_criteria=[],
            keywords=[],
            confidence_score=0.8
        )
    
    def analyze_task(self, task_description: str) -> TaskAnalysis:
        """Perform comprehensive task analysis."""
        if task_description is None:
            raise ValueError("Task description cannot be None")
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty")
        
        # Check cache first
        cache_key = hashlib.md5(task_description.encode()).hexdigest()
        if cache_key in self._analysis_cache:
            return self._analysis_cache[cache_key]
        
        # Perform analysis
        result = self._perform_analysis(task_description)
        
        # Cache result
        self._analysis_cache[cache_key] = result
        
        return result
    
    def _perform_analysis(self, task_description: str) -> TaskAnalysis:
        """Internal method to perform the actual analysis."""
        task_lower = task_description.lower()
        
        # Determine category
        category = self._determine_category(task_lower)
        
        # Determine complexity
        complexity = self._determine_complexity(task_lower)
        
        # Extract other components
        keywords = self.extract_keywords(task_description)
        required_skills = self.identify_required_skills(task_description)
        dependencies = self._identify_dependencies(task_description)
        success_criteria = self._generate_success_criteria(task_description, category, complexity)
        estimated_duration = self.estimate_duration(task_description)
        
        return TaskAnalysis(
            category=category,
            complexity=complexity,
            estimated_duration=estimated_duration,
            required_skills=required_skills,
            dependencies=dependencies,
            success_criteria=success_criteria,
            keywords=keywords,
            confidence_score=0.85
        )
    
    def _determine_category(self, task_lower: str) -> TaskCategory:
        """Determine the category of a task."""
        category_scores = {}
        
        for category, patterns in self.categories.items():
            score = 0
            for pattern in patterns:
                # Use word boundary matching to prevent substring issues
                # \b ensures we match whole words only
                if re.search(r'\b' + re.escape(pattern) + r'\b', task_lower):
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        return max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else TaskCategory.TECHNICAL
    
    def _determine_complexity(self, task_lower: str) -> TaskComplexity:
        """Determine the complexity of a task."""
        complexity_scores = {}
        
        for complexity, patterns in self.complexity_levels.items():
            score = 0
            for pattern in patterns:
                # Use word boundary matching to prevent substring issues
                if re.search(r'\b' + re.escape(pattern) + r'\b', task_lower):
                    score += 1
            if score > 0:
                complexity_scores[complexity] = score
        
        return max(complexity_scores.items(), key=lambda x: x[1])[0] if complexity_scores else TaskComplexity.MEDIUM
    
    def extract_keywords(self, task_description: str) -> List[str]:
        """Extract important keywords from task description."""
        # Simple keyword extraction - in practice, this could be more sophisticated
        keywords = []
        task_lower = task_description.lower()
        
        # Look for technology keywords (case-insensitive matching, preserve original case)
        tech_keywords = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'react': 'React', 
            'flask': 'Flask',
            'postgresql': 'PostgreSQL',
            'docker': 'Docker',
            'kubernetes': 'Kubernetes'
        }
        
        for keyword_lower, keyword_proper in tech_keywords.items():
            if keyword_lower in task_lower:
                keywords.append(keyword_proper)
        
        # Look for domain-specific terms
        if 'web application' in task_lower:
            keywords.append('web application')
        if 'machine learning' in task_lower:
            keywords.append('machine learning')
        
        return keywords
    
    def identify_required_skills(self, task_description: str) -> List[str]:
        """Identify required skills from task description."""
        skills = []
        task_lower = task_description.lower()
        
        for skill, patterns in self.skill_patterns.items():
            if any(pattern in task_lower for pattern in patterns):
                skills.append(skill)
        
        return skills
    
    def _identify_dependencies(self, task_description: str) -> List[str]:
        """Identify task dependencies."""
        dependencies = []
        task_lower = task_description.lower()
        
        # Common dependencies based on task type
        if any(term in task_lower for term in ['web', 'app', 'application']):
            dependencies.extend(['Development Environment', 'Version Control'])
        
        if any(term in task_lower for term in ['database', 'sql', 'postgresql', 'mysql']):
            dependencies.append('Database Server')
        
        if 'docker' in task_lower:
            dependencies.append('Docker Environment')
        
        return dependencies
    
    def _generate_success_criteria(self, task_description: str, category: TaskCategory, complexity: TaskComplexity) -> List[str]:
        """Generate success criteria based on task analysis."""
        criteria = []
        
        if category == TaskCategory.TECHNICAL:
            criteria.extend(['Functional Application', 'Unit Tests', 'Documentation'])
            if complexity >= TaskComplexity.HIGH:
                criteria.extend(['Performance Tests', 'Security Audit'])
        
        elif category == TaskCategory.CREATIVE:
            criteria.extend(['Creative Vision Achieved', 'Quality Standards Met', 'Audience Engagement'])
        
        elif category == TaskCategory.BUSINESS:
            criteria.extend(['Business Objectives Met', 'ROI Targets Achieved', 'Stakeholder Approval'])
        
        return criteria
    
    def estimate_duration(self, task_description: str) -> str:
        """Estimate task duration based on complexity."""
        complexity = self._determine_complexity(task_description.lower())
        base_duration = self.duration_mappings[complexity]
        
        # Adjust based on specific patterns
        task_lower = task_description.lower()
        if any(term in task_lower for term in ['simple', 'basic', 'quick']):
            if complexity == TaskComplexity.MEDIUM:
                return self.duration_mappings[TaskComplexity.LOW]
        
        if any(term in task_lower for term in ['complex', 'comprehensive', 'large-scale']):
            if complexity == TaskComplexity.MEDIUM:
                return self.duration_mappings[TaskComplexity.HIGH]
        
        return base_duration
