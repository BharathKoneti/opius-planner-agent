"""
Unit tests for Advanced Personalization System - Following TDD approach.

Testing user behavior analysis, adaptive AI assistance, and intelligent automation.
"""

import pytest
from unittest.mock import Mock, patch
from opius_planner.advanced.advanced_personalization import (
    UserBehaviorAnalyzer,
    AdaptiveAIAssistant,
    IntelligentAutomation,
    PersonalizationEngine,
    UserProfile,
    BehaviorPattern
)
from opius_planner.templates.template_engine import TemplateContext


class TestUserBehaviorAnalyzer:
    """Test suite for UserBehaviorAnalyzer following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = UserBehaviorAnalyzer()
    
    def test_init_loads_behavior_analyzer(self):
        """Test that analyzer initializes with behavior analysis capabilities."""
        analyzer = UserBehaviorAnalyzer()
        
        assert analyzer is not None
        assert hasattr(analyzer, 'user_sessions')
        assert hasattr(analyzer, 'behavior_patterns')
    
    def test_track_user_behavior(self):
        """Test tracking user behavior patterns."""
        user_session = {
            "user_id": "user123",
            "session_start": "2025-06-12T10:00:00",
            "actions": [
                {"action": "create_template", "category": "technical", "timestamp": "10:05:00"},
                {"action": "customize_template", "theme": "modern", "timestamp": "10:10:00"},
                {"action": "generate_plan", "complexity": "high", "timestamp": "10:15:00"}
            ],
            "preferences": {"theme": "modern", "complexity": "high"}
        }
        
        self.analyzer.track_session(user_session)
        
        # Should store session data
        sessions = self.analyzer.get_user_sessions("user123")
        assert len(sessions) == 1
        assert sessions[0]["user_id"] == "user123"
    
    def test_analyze_usage_patterns(self):
        """Test analyzing user usage patterns."""
        user_data = {
            "user_id": "user456",
            "sessions": [
                {"actions": [{"action": "create_template", "category": "technical"}]},
                {"actions": [{"action": "create_template", "category": "technical"}]},
                {"actions": [{"action": "customize_template", "theme": "modern"}]}
            ]
        }
        
        patterns = self.analyzer.analyze_patterns(user_data)
        
        assert isinstance(patterns, dict)
        assert "frequent_actions" in patterns
        assert "preferred_categories" in patterns
        assert "usage_frequency" in patterns


class TestAdaptiveAIAssistant:
    """Test suite for AdaptiveAIAssistant."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.assistant = AdaptiveAIAssistant()
    
    def test_adapt_to_user_style(self):
        """Test adapting AI responses to user style."""
        user_profile = UserProfile(
            user_id="user789",
            communication_style="concise",
            technical_level="expert",
            preferred_format="bullet_points"
        )
        
        base_response = "This is a detailed explanation of the technical implementation."
        adapted_response = self.assistant.adapt_response(base_response, user_profile)
        
        assert isinstance(adapted_response, str)
        assert len(adapted_response) <= len(base_response)  # Should be more concise
    
    def test_personalized_recommendations(self):
        """Test generating personalized recommendations."""
        user_context = {
            "user_id": "user101",
            "recent_projects": ["web_app", "mobile_app"],
            "skill_level": "intermediate",
            "time_constraints": "tight"
        }
        
        recommendations = self.assistant.generate_recommendations(user_context)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert "suggestion" in rec
            assert "confidence" in rec
            assert "personalization_reason" in rec


class TestIntelligentAutomation:
    """Test suite for IntelligentAutomation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.automation = IntelligentAutomation()
    
    def test_automate_repetitive_tasks(self):
        """Test automating repetitive user tasks."""
        user_behavior = {
            "repeated_actions": [
                {"action": "create_template", "category": "technical", "count": 15},
                {"action": "apply_theme", "theme": "modern", "count": 12}
            ]
        }
        
        automation_suggestions = self.automation.suggest_automations(user_behavior)
        
        assert isinstance(automation_suggestions, list)
        assert len(automation_suggestions) > 0
        
        for suggestion in automation_suggestions:
            assert "task" in suggestion
            assert "automation_type" in suggestion
            assert "potential_time_savings" in suggestion
    
    def test_intelligent_defaults(self):
        """Test setting intelligent defaults based on user patterns."""
        user_patterns = {
            "most_used_complexity": "high",
            "preferred_theme": "modern",
            "common_project_type": "web_application"
        }
        
        defaults = self.automation.generate_intelligent_defaults(user_patterns)
        
        assert isinstance(defaults, dict)
        assert defaults["complexity"] == "high"
        assert defaults["theme"] == "modern"


class TestPersonalizationEngine:
    """Test suite for PersonalizationEngine integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = PersonalizationEngine()
    
    def test_init_integrates_all_components(self):
        """Test that engine integrates all personalization components."""
        engine = PersonalizationEngine()
        
        assert engine is not None
        assert hasattr(engine, 'behavior_analyzer')
        assert hasattr(engine, 'ai_assistant')
        assert hasattr(engine, 'automation')
    
    def test_full_personalization_workflow(self):
        """Test complete personalization workflow."""
        user_context = {
            "user_id": "workflow_user",
            "session_data": {
                "actions": [{"action": "create_template", "category": "technical"}],
                "preferences": {"theme": "modern"}
            },
            "request": "Help me create a web application plan"
        }
        
        personalized_result = self.engine.personalize_experience(user_context)
        
        assert isinstance(personalized_result, dict)
        assert "adapted_response" in personalized_result
        assert "recommendations" in personalized_result
        assert "automation_suggestions" in personalized_result
    
    def test_learning_from_feedback(self):
        """Test learning from user feedback."""
        feedback = {
            "user_id": "feedback_user",
            "interaction_id": "int_001",
            "satisfaction": 4,
            "helpful_features": ["automated_setup", "intelligent_defaults"],
            "suggestions": "More customization options"
        }
        
        learning_result = self.engine.learn_from_feedback(feedback)
        
        assert learning_result is True
        
        # Should improve future interactions
        user_profile = self.engine.get_user_profile("feedback_user")
        assert user_profile is not None


class TestUserProfile:
    """Test suite for UserProfile data structure."""
    
    def test_create_user_profile(self):
        """Test creating a user profile."""
        profile = UserProfile(
            user_id="profile_user",
            communication_style="detailed",
            technical_level="beginner",
            preferred_format="step_by_step",
            learning_pace="slow"
        )
        
        assert profile.user_id == "profile_user"
        assert profile.communication_style == "detailed"
        assert profile.technical_level == "beginner"
    
    def test_update_profile_from_behavior(self):
        """Test updating profile based on observed behavior."""
        profile = UserProfile(user_id="adaptive_user")
        
        behavior_data = {
            "frequent_actions": ["create_template", "customize_theme"],
            "avg_session_duration": 45,  # minutes
            "help_seeking_frequency": "low"
        }
        
        profile.update_from_behavior(behavior_data)
        
        assert hasattr(profile, 'behavior_insights')
        assert profile.behavior_insights is not None


class TestBehaviorPattern:
    """Test suite for BehaviorPattern data structure."""
    
    def test_create_behavior_pattern(self):
        """Test creating a behavior pattern."""
        pattern = BehaviorPattern(
            pattern_id="pattern_001",
            user_id="pattern_user",
            pattern_type="workflow_preference",
            frequency=0.8,
            triggers=["project_start", "template_creation"],
            actions=["apply_modern_theme", "set_high_complexity"]
        )
        
        assert pattern.pattern_id == "pattern_001"
        assert pattern.frequency == 0.8
        assert "apply_modern_theme" in pattern.actions
    
    def test_pattern_matching(self):
        """Test matching behavior patterns."""
        pattern = BehaviorPattern(
            pattern_id="test_pattern",
            triggers=["create_template", "web_project"],
            confidence=0.85
        )
        
        current_context = ["create_template", "web_project", "high_complexity"]
        
        matches = pattern.matches_context(current_context)
        assert matches is True


class TestPersonalizationIntegration:
    """Integration tests for the personalization system."""
    
    def test_end_to_end_personalization(self):
        """Test complete personalization workflow."""
        engine = PersonalizationEngine()
        
        # Simulate user interaction
        user_session = {
            "user_id": "integration_user",
            "actions": [
                {"action": "create_template", "category": "technical", "success": True},
                {"action": "apply_theme", "theme": "modern", "success": True},
                {"action": "generate_plan", "complexity": "high", "success": True}
            ],
            "feedback": {"satisfaction": 5, "efficiency_rating": 4}
        }
        
        # Process the session
        result = engine.process_user_session(user_session)
        
        assert isinstance(result, dict)
        assert "user_profile_updated" in result
        assert "recommendations" in result
        assert "next_session_improvements" in result
    
    def test_cross_session_learning(self):
        """Test learning across multiple sessions."""
        engine = PersonalizationEngine()
        
        # Multiple sessions from same user
        sessions = [
            {"user_id": "learner", "preferred_complexity": "medium", "session": 1},
            {"user_id": "learner", "preferred_complexity": "high", "session": 2},
            {"user_id": "learner", "preferred_complexity": "high", "session": 3}
        ]
        
        for session in sessions:
            engine.process_user_session(session)
        
        # Should learn user's evolving preferences
        profile = engine.get_user_profile("learner")
        assert profile.preferred_complexity == "high"  # Latest preference
