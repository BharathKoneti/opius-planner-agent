"""
Unit tests for Cross-Domain Learning System - Following TDD approach.

Testing pattern recognition, success metric tracking, and recommendation improvement.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.advanced.cross_domain_learning import (
    PatternRecognitionSystem,
    SuccessMetricTracker,
    RecommendationEngine,
    CrossDomainLearner,
    LearningPattern,
    SuccessMetric
)
from opius_planner.templates.template_engine import TemplateContext
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestPatternRecognitionSystem:
    """Test suite for PatternRecognitionSystem following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.pattern_system = PatternRecognitionSystem()
    
    def test_init_loads_pattern_recognition(self):
        """Test that system initializes with pattern recognition capabilities."""
        system = PatternRecognitionSystem()
        
        assert system is not None
        assert hasattr(system, 'patterns')
        assert hasattr(system, 'pattern_database')
    
    def test_identify_patterns_in_successful_projects(self):
        """Test identifying patterns in successful projects."""
        successful_projects = [
            {
                "name": "E-commerce Platform",
                "category": "technical",
                "complexity": "high",
                "success_score": 95,
                "duration": 12,
                "team_size": 8,
                "technologies": ["React", "Node.js", "PostgreSQL"]
            },
            {
                "name": "Mobile Banking App",
                "category": "technical", 
                "complexity": "very_high",
                "success_score": 90,
                "duration": 16,
                "team_size": 12,
                "technologies": ["React Native", "Node.js", "MongoDB"]
            }
        ]
        
        patterns = self.pattern_system.identify_patterns(successful_projects)
        
        assert isinstance(patterns, list)
        assert len(patterns) > 0
        
        # Should identify common patterns
        tech_pattern = next((p for p in patterns if "Node.js" in str(p)), None)
        assert tech_pattern is not None
    
    def test_analyze_cross_domain_similarities(self):
        """Test analyzing similarities across different domains."""
        technical_project = {
            "category": "technical",
            "approach": "agile",
            "team_structure": "cross_functional",
            "success_factors": ["clear_requirements", "regular_testing"]
        }
        
        creative_project = {
            "category": "creative",
            "approach": "iterative",
            "team_structure": "collaborative",
            "success_factors": ["clear_brief", "regular_feedback"]
        }
        
        similarities = self.pattern_system.find_cross_domain_patterns(
            [technical_project, creative_project]
        )
        
        assert isinstance(similarities, dict)
        assert "common_approaches" in similarities
        assert "shared_success_factors" in similarities
    
    def test_create_learning_pattern(self):
        """Test creating a learning pattern from data."""
        pattern_data = {
            "trigger_conditions": {"complexity": "high", "team_size": ">= 8"},
            "recommended_actions": ["detailed_planning", "risk_assessment"],
            "success_probability": 0.85,
            "evidence_count": 15
        }
        
        pattern = self.pattern_system.create_pattern(
            name="high_complexity_pattern",
            data=pattern_data
        )
        
        assert isinstance(pattern, LearningPattern)
        assert pattern.name == "high_complexity_pattern"
        assert pattern.success_probability == 0.85
    
    def test_pattern_matching_for_new_projects(self):
        """Test matching patterns for new project recommendations."""
        new_project = {
            "category": "technical",
            "complexity": "high",
            "team_size": 10,
            "timeline": "6_months"
        }
        
        matched_patterns = self.pattern_system.match_patterns(new_project)
        
        assert isinstance(matched_patterns, list)
        # Should find relevant patterns based on project characteristics


class TestSuccessMetricTracker:
    """Test suite for SuccessMetricTracker."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tracker = SuccessMetricTracker()
    
    def test_track_project_success_metrics(self):
        """Test tracking success metrics for projects."""
        project_metrics = {
            "project_id": "proj_001",
            "completion_time": 10,  # weeks
            "budget_utilization": 0.95,
            "quality_score": 88,
            "stakeholder_satisfaction": 4.2,
            "technical_debt": 0.15
        }
        
        result = self.tracker.record_metrics("proj_001", project_metrics)
        
        assert result is True
        
        # Should be able to retrieve metrics
        retrieved = self.tracker.get_metrics("proj_001")
        assert retrieved is not None
        assert retrieved["quality_score"] == 88
    
    def test_calculate_success_score(self):
        """Test calculating overall success score."""
        metrics = {
            "completion_time": 8,  # under budget
            "budget_utilization": 0.90,  # under budget
            "quality_score": 92,
            "stakeholder_satisfaction": 4.5
        }
        
        success_score = self.tracker.calculate_success_score(metrics)
        
        assert isinstance(success_score, (int, float))
        assert 0 <= success_score <= 100
        assert success_score > 80  # Should be high with good metrics
    
    def test_track_recommendation_effectiveness(self):
        """Test tracking effectiveness of recommendations."""
        recommendation = {
            "id": "rec_001",
            "type": "technology_choice",
            "suggestion": "Use React for frontend",
            "confidence": 0.8
        }
        
        outcome = {
            "implemented": True,
            "success_impact": 0.15,  # 15% improvement
            "user_feedback": "positive"
        }
        
        self.tracker.track_recommendation_outcome("rec_001", recommendation, outcome)
        
        # Should update recommendation effectiveness
        effectiveness = self.tracker.get_recommendation_effectiveness("rec_001")
        assert effectiveness is not None
        assert effectiveness > 0
    
    def test_identify_success_patterns(self):
        """Test identifying patterns that lead to success."""
        # Record multiple successful projects
        successful_projects = [
            {"agile_process": True, "code_review": True, "success_score": 95},
            {"agile_process": True, "code_review": True, "success_score": 88},
            {"agile_process": False, "code_review": True, "success_score": 75}
        ]
        
        for i, project in enumerate(successful_projects):
            self.tracker.record_metrics(f"proj_{i}", project)
        
        patterns = self.tracker.identify_success_patterns()
        
        assert isinstance(patterns, list)
        # Should identify that agile + code review leads to higher success


class TestRecommendationEngine:
    """Test suite for RecommendationEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = RecommendationEngine()
    
    def test_generate_recommendations_for_new_project(self):
        """Test generating recommendations for a new project."""
        project_context = {
            "name": "Customer Portal",
            "category": "technical",
            "complexity": "medium",
            "team_size": 5,
            "timeline": "3_months",
            "budget": "medium"
        }
        
        recommendations = self.engine.generate_recommendations(project_context)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Each recommendation should have required fields
        for rec in recommendations:
            assert "type" in rec
            assert "suggestion" in rec
            assert "confidence" in rec
            assert "reasoning" in rec
    
    def test_prioritize_recommendations(self):
        """Test prioritizing recommendations by importance."""
        recommendations = [
            {"type": "process", "confidence": 0.9, "impact": "high"},
            {"type": "technology", "confidence": 0.7, "impact": "medium"},
            {"type": "team", "confidence": 0.95, "impact": "high"}
        ]
        
        prioritized = self.engine.prioritize_recommendations(recommendations)
        
        assert isinstance(prioritized, list)
        assert len(prioritized) == len(recommendations)
        
        # Should be sorted by priority (confidence * impact)
        assert prioritized[0]["confidence"] >= prioritized[-1]["confidence"]
    
    def test_learn_from_feedback(self):
        """Test learning from recommendation feedback."""
        recommendation = {
            "id": "rec_002",
            "type": "process_improvement",
            "suggestion": "Implement daily standups"
        }
        
        feedback = {
            "implemented": True,
            "effectiveness": 0.8,
            "user_rating": 4,
            "comments": "Very helpful for team coordination"
        }
        
        self.engine.learn_from_feedback("rec_002", feedback)
        
        # Should improve future recommendations of similar type
        future_recs = self.engine.generate_recommendations({
            "category": "team_management",
            "team_size": 6
        })
        
        # Should include process improvements with higher confidence
        process_recs = [r for r in future_recs if r["type"] == "process"]
        assert len(process_recs) > 0
    
    def test_adapt_recommendations_to_domain(self):
        """Test adapting recommendations to specific domains."""
        technical_context = {"category": "technical", "complexity": "high"}
        creative_context = {"category": "creative", "complexity": "medium"}
        
        tech_recs = self.engine.generate_recommendations(technical_context)
        creative_recs = self.engine.generate_recommendations(creative_context)
        
        assert isinstance(tech_recs, list)
        assert isinstance(creative_recs, list)
        
        # Recommendations should be different for different domains
        tech_types = {rec["type"] for rec in tech_recs}
        creative_types = {rec["type"] for rec in creative_recs}
        
        # Should have domain-specific recommendations
        assert len(tech_types.intersection(creative_types)) < len(tech_types)


class TestCrossDomainLearner:
    """Test suite for CrossDomainLearner integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.learner = CrossDomainLearner()
    
    def test_init_integrates_all_components(self):
        """Test that learner integrates all learning components."""
        learner = CrossDomainLearner()
        
        assert learner is not None
        assert hasattr(learner, 'pattern_system')
        assert hasattr(learner, 'metric_tracker')
        assert hasattr(learner, 'recommendation_engine')
    
    def test_learn_from_project_history(self):
        """Test learning from historical project data."""
        project_history = [
            {
                "id": "hist_001",
                "category": "technical",
                "outcome": "successful",
                "metrics": {"quality": 90, "time": 10, "budget": 0.95},
                "approaches": ["agile", "tdd", "code_review"]
            },
            {
                "id": "hist_002", 
                "category": "creative",
                "outcome": "successful",
                "metrics": {"quality": 85, "time": 8, "budget": 0.90},
                "approaches": ["iterative", "user_feedback", "prototyping"]
            }
        ]
        
        learning_results = self.learner.learn_from_history(project_history)
        
        assert isinstance(learning_results, dict)
        assert "patterns_discovered" in learning_results
        assert "success_factors" in learning_results
        assert "cross_domain_insights" in learning_results
    
    def test_generate_intelligent_recommendations(self):
        """Test generating intelligent recommendations based on learning."""
        new_project = {
            "name": "AI-Powered Analytics Dashboard",
            "category": "technical",
            "complexity": "very_high",
            "team_size": 8,
            "timeline": "6_months",
            "stakeholders": ["executives", "analysts", "IT_team"]
        }
        
        recommendations = self.learner.generate_intelligent_recommendations(new_project)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Should include learned insights
        for rec in recommendations:
            assert "confidence" in rec
            assert "evidence_strength" in rec
            assert rec["confidence"] > 0
    
    def test_continuous_learning_loop(self):
        """Test continuous learning from new project outcomes."""
        # Initial learning state
        initial_patterns = len(self.learner.get_known_patterns())
        
        # Add new successful project
        new_project_outcome = {
            "id": "new_001",
            "category": "business",
            "success_score": 92,
            "innovative_approaches": ["design_thinking", "lean_startup"],
            "lessons_learned": ["early_user_validation", "rapid_iteration"]
        }
        
        self.learner.integrate_new_learning(new_project_outcome)
        
        # Should have learned new patterns
        updated_patterns = len(self.learner.get_known_patterns())
        assert updated_patterns >= initial_patterns
    
    def test_cross_domain_knowledge_transfer(self):
        """Test transferring knowledge between domains."""
        # Business domain success pattern
        business_pattern = {
            "domain": "business",
            "pattern": "stakeholder_engagement",
            "success_rate": 0.85,
            "applications": ["regular_updates", "feedback_loops"]
        }
        
        # Test if pattern can be applied to technical domain
        technical_application = self.learner.transfer_knowledge(
            source_domain="business",
            target_domain="technical", 
            pattern=business_pattern
        )
        
        assert technical_application is not None
        assert "adapted_approach" in technical_application
        assert "confidence" in technical_application


class TestLearningPattern:
    """Test suite for LearningPattern data structure."""
    
    def test_create_learning_pattern(self):
        """Test creating a learning pattern."""
        pattern = LearningPattern(
            name="agile_success_pattern",
            trigger_conditions={"methodology": "agile", "team_size": ">= 5"},
            recommended_actions=["daily_standups", "sprint_planning", "retrospectives"],
            success_probability=0.88,
            evidence_count=25,
            domains=["technical", "business"]
        )
        
        assert pattern.name == "agile_success_pattern"
        assert pattern.success_probability == 0.88
        assert "technical" in pattern.domains
    
    def test_pattern_applicability_check(self):
        """Test checking if pattern applies to a context."""
        pattern = LearningPattern(
            name="test_pattern",
            trigger_conditions={"complexity": "high", "team_size": ">= 8"}
        )
        
        matching_context = {"complexity": "high", "team_size": 10}
        non_matching_context = {"complexity": "low", "team_size": 3}
        
        assert pattern.applies_to(matching_context) is True
        assert pattern.applies_to(non_matching_context) is False


class TestSuccessMetric:
    """Test suite for SuccessMetric data structure."""
    
    def test_create_success_metric(self):
        """Test creating a success metric."""
        metric = SuccessMetric(
            name="delivery_time",
            value=8.5,
            target=10.0,
            unit="weeks",
            weight=0.3
        )
        
        assert metric.name == "delivery_time"
        assert metric.value == 8.5
        assert metric.achieved_target() is True  # 8.5 < 10.0
    
    def test_metric_performance_calculation(self):
        """Test calculating metric performance."""
        metric = SuccessMetric(
            name="quality_score",
            value=92,
            target=85,
            unit="percentage"
        )
        
        performance = metric.calculate_performance()
        assert isinstance(performance, float)
        assert performance > 1.0  # Exceeded target
