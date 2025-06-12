"""
Unit tests for TaskAnalyzer - Following TDD approach.

Testing the universal task categorization and analysis system.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.core.task_analyzer import TaskAnalyzer, TaskCategory, TaskComplexity


class TestTaskAnalyzer:
    """Test suite for TaskAnalyzer following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = TaskAnalyzer()
    
    def test_init_creates_analyzer_with_default_config(self):
        """Test that TaskAnalyzer initializes with proper defaults."""
        analyzer = TaskAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, 'categories')
        assert hasattr(analyzer, 'complexity_levels')
    
    @pytest.mark.parametrize("task_description,expected_category", [
        ("Write a novel about space exploration", TaskCategory.CREATIVE),
        ("Build a React web application", TaskCategory.TECHNICAL),
        ("Create a marketing plan for Q4", TaskCategory.BUSINESS),
        ("Plan my wedding for next summer", TaskCategory.PERSONAL),
        ("Learn Python programming", TaskCategory.EDUCATIONAL),
    ])
    def test_categorize_task_returns_correct_category(self, task_description, expected_category):
        """Test that task categorization works for different domains."""
        result = self.analyzer.categorize_task(task_description)
        assert result.category == expected_category
    
    @pytest.mark.parametrize("task_description,expected_complexity", [
        ("Write a simple to-do list", TaskComplexity.LOW),
        ("Build a React web application", TaskComplexity.MEDIUM),
        ("Create an AI-powered recommendation system", TaskComplexity.HIGH),
        ("Design and launch a space mission", TaskComplexity.VERY_HIGH),
    ])
    def test_analyze_complexity_returns_correct_level(self, task_description, expected_complexity):
        """Test that complexity analysis works correctly."""
        result = self.analyzer.analyze_complexity(task_description)
        assert result.complexity == expected_complexity
    
    def test_analyze_task_returns_comprehensive_analysis(self):
        """Test that analyze_task returns complete task analysis."""
        task_description = "Build a machine learning model to predict stock prices"
        
        result = self.analyzer.analyze_task(task_description)
        
        # Verify all required fields are present
        assert hasattr(result, 'category')
        assert hasattr(result, 'complexity')
        assert hasattr(result, 'estimated_duration')
        assert hasattr(result, 'required_skills')
        assert hasattr(result, 'dependencies')
        assert hasattr(result, 'success_criteria')
    
    def test_analyze_task_with_empty_description_raises_error(self):
        """Test that empty task description raises appropriate error."""
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            self.analyzer.analyze_task("")
    
    def test_analyze_task_with_none_description_raises_error(self):
        """Test that None task description raises appropriate error."""
        with pytest.raises(ValueError, match="Task description cannot be None"):
            self.analyzer.analyze_task(None)
    
    def test_extract_keywords_from_task_description(self):
        """Test keyword extraction from task descriptions."""
        task_description = "Build a Python web application using Flask and PostgreSQL"
        
        keywords = self.analyzer.extract_keywords(task_description)
        
        assert "Python" in keywords
        assert "web application" in keywords
        assert "Flask" in keywords
        assert "PostgreSQL" in keywords
    
    def test_identify_required_skills_from_task(self):
        """Test skill identification from task descriptions."""
        task_description = "Create a React frontend with TypeScript and unit tests"
        
        skills = self.analyzer.identify_required_skills(task_description)
        
        assert "React" in skills
        assert "TypeScript" in skills
        assert "Testing" in skills
    
    def test_estimate_duration_considers_complexity(self):
        """Test that duration estimation considers task complexity."""
        simple_task = "Create a basic HTML page"
        complex_task = "Build a distributed microservices architecture"
        
        simple_duration = self.analyzer.estimate_duration(simple_task)
        complex_duration = self.analyzer.estimate_duration(complex_task)
        
        assert complex_duration > simple_duration
    
    def test_analyze_task_caches_results_for_identical_tasks(self):
        """Test that identical task descriptions use cached results."""
        task_description = "Build a simple web scraper"
        
        # First analysis
        result1 = self.analyzer.analyze_task(task_description)
        
        # Second analysis should use cache
        with patch.object(self.analyzer, '_perform_analysis') as mock_analysis:
            result2 = self.analyzer.analyze_task(task_description)
            mock_analysis.assert_not_called()
        
        assert result1 == result2


@pytest.fixture
def sample_task_analysis():
    """Fixture providing sample task analysis for testing."""
    return {
        'category': TaskCategory.TECHNICAL,
        'complexity': TaskComplexity.MEDIUM,
        'estimated_duration': '2-3 weeks',
        'required_skills': ['Python', 'Web Development', 'Database Design'],
        'dependencies': ['Development Environment', 'Database Server'],
        'success_criteria': ['Functional Application', 'Unit Tests', 'Documentation']
    }


class TestTaskCategory:
    """Test suite for TaskCategory enum."""
    
    def test_task_category_enum_values(self):
        """Test that TaskCategory enum has all expected values."""
        expected_categories = {
            'CREATIVE', 'TECHNICAL', 'BUSINESS', 'PERSONAL', 'EDUCATIONAL'
        }
        actual_categories = {category.name for category in TaskCategory}
        assert actual_categories == expected_categories


class TestTaskComplexity:
    """Test suite for TaskComplexity enum."""
    
    def test_task_complexity_enum_values(self):
        """Test that TaskComplexity enum has all expected values."""
        expected_complexities = {
            'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'
        }
        actual_complexities = {complexity.name for complexity in TaskComplexity}
        assert actual_complexities == expected_complexities
    
    def test_complexity_ordering(self):
        """Test that complexity levels are properly ordered."""
        assert TaskComplexity.LOW < TaskComplexity.MEDIUM
        assert TaskComplexity.MEDIUM < TaskComplexity.HIGH
        assert TaskComplexity.HIGH < TaskComplexity.VERY_HIGH
