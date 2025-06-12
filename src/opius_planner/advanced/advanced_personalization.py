"""
Advanced Personalization System - Phase 3.3 Implementation.

Provides user behavior analysis, adaptive AI assistance, and intelligent automation.
"""

import json
import statistics
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter


@dataclass
class UserProfile:
    """Represents a comprehensive user profile for personalization."""
    user_id: str
    communication_style: str = "balanced"
    technical_level: str = "intermediate"
    preferred_format: str = "structured"
    learning_pace: str = "medium"
    preferred_complexity: str = "medium"
    behavior_insights: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    
    def update_from_behavior(self, behavior_data: Dict[str, Any]):
        """Update profile based on observed behavior."""
        self.behavior_insights = behavior_data
        self.updated_at = datetime.now().isoformat()
        
        # Infer technical level from behavior
        if behavior_data.get("help_seeking_frequency") == "low":
            self.technical_level = "expert"
        elif behavior_data.get("help_seeking_frequency") == "high":
            self.technical_level = "beginner"
        
        # Infer learning pace
        avg_duration = behavior_data.get("avg_session_duration", 30)
        if avg_duration > 60:
            self.learning_pace = "slow"
        elif avg_duration < 20:
            self.learning_pace = "fast"


@dataclass
class BehaviorPattern:
    """Represents a user behavior pattern."""
    pattern_id: str
    user_id: str = ""
    pattern_type: str = "general"
    frequency: float = 0.0
    confidence: float = 0.0
    triggers: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    
    def matches_context(self, current_context: List[str]) -> bool:
        """Check if current context matches this pattern's triggers."""
        matching_triggers = set(self.triggers).intersection(set(current_context))
        return len(matching_triggers) >= len(self.triggers) * 0.6  # 60% match threshold


class UserBehaviorAnalyzer:
    """Analyzes user behavior patterns for personalization."""
    
    def __init__(self):
        """Initialize the behavior analyzer."""
        self.user_sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.behavior_patterns: Dict[str, List[BehaviorPattern]] = defaultdict(list)
    
    def track_session(self, session_data: Dict[str, Any]):
        """Track a user session for behavior analysis."""
        user_id = session_data.get("user_id")
        if user_id:
            self.user_sessions[user_id].append(session_data)
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a specific user."""
        return self.user_sessions.get(user_id, [])
    
    def analyze_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user behavior patterns."""
        user_id = user_data.get("user_id")
        sessions = user_data.get("sessions", [])
        
        if not sessions:
            return {"frequent_actions": [], "preferred_categories": [], "usage_frequency": "low"}
        
        # Analyze frequent actions
        all_actions = []
        categories = []
        
        for session in sessions:
            actions = session.get("actions", [])
            for action in actions:
                all_actions.append(action.get("action", "unknown"))
                if "category" in action:
                    categories.append(action["category"])
        
        action_counts = Counter(all_actions)
        category_counts = Counter(categories)
        
        patterns = {
            "frequent_actions": [action for action, count in action_counts.most_common(3)],
            "preferred_categories": [cat for cat, count in category_counts.most_common(2)],
            "usage_frequency": "high" if len(sessions) > 10 else "medium" if len(sessions) > 3 else "low",
            "total_sessions": len(sessions),
            "avg_actions_per_session": len(all_actions) / len(sessions) if sessions else 0
        }
        
        return patterns
    
    def identify_behavior_patterns(self, user_id: str) -> List[BehaviorPattern]:
        """Identify behavior patterns for a user."""
        sessions = self.get_user_sessions(user_id)
        patterns = []
        
        if len(sessions) < 3:
            return patterns
        
        # Identify workflow patterns
        workflow_sequences = []
        for session in sessions:
            actions = [action.get("action") for action in session.get("actions", [])]
            if len(actions) >= 2:
                workflow_sequences.append(actions[:3])  # First 3 actions
        
        # Find common workflows
        workflow_counter = Counter(tuple(seq) for seq in workflow_sequences)
        
        for workflow, frequency in workflow_counter.items():
            if frequency >= 2:  # Appears at least twice
                pattern = BehaviorPattern(
                    pattern_id=f"workflow_{len(patterns)}",
                    user_id=user_id,
                    pattern_type="workflow_sequence",
                    frequency=frequency / len(sessions),
                    triggers=list(workflow[:2]),
                    actions=[workflow[-1]] if len(workflow) > 2 else []
                )
                patterns.append(pattern)
        
        return patterns


class AdaptiveAIAssistant:
    """Provides adaptive AI assistance based on user profiles."""
    
    def __init__(self):
        """Initialize the adaptive AI assistant."""
        self.adaptation_rules: Dict[str, Any] = self._load_adaptation_rules()
    
    def _load_adaptation_rules(self) -> Dict[str, Any]:
        """Load rules for adapting responses to user preferences."""
        return {
            "communication_styles": {
                "concise": {"max_length_ratio": 0.6, "bullet_points": True},
                "detailed": {"max_length_ratio": 1.5, "explanations": True},
                "balanced": {"max_length_ratio": 1.0, "structure": True}
            },
            "technical_levels": {
                "beginner": {"simplified_terms": True, "step_by_step": True},
                "intermediate": {"balanced_detail": True, "some_technical": True},
                "expert": {"technical_terms": True, "concise": True}
            }
        }
    
    def adapt_response(self, base_response: str, user_profile: UserProfile) -> str:
        """Adapt response to user's communication style and technical level."""
        adapted = base_response
        
        # Adapt for communication style
        style_rules = self.adaptation_rules["communication_styles"].get(
            user_profile.communication_style, {}
        )
        
        if style_rules.get("max_length_ratio", 1.0) < 1.0:
            # Make more concise
            sentences = adapted.split('. ')
            keep_ratio = style_rules["max_length_ratio"]
            keep_count = max(1, int(len(sentences) * keep_ratio))
            adapted = '. '.join(sentences[:keep_count])
        
        if style_rules.get("bullet_points"):
            # Convert to bullet points if applicable
            if len(adapted.split('. ')) > 2:
                points = adapted.split('. ')
                adapted = '\n'.join(f"• {point.strip()}" for point in points if point.strip())
        
        # Adapt for technical level
        tech_rules = self.adaptation_rules["technical_levels"].get(
            user_profile.technical_level, {}
        )
        
        if tech_rules.get("simplified_terms"):
            # Simplify technical terms (basic replacements)
            adapted = adapted.replace("implementation", "setup")
            adapted = adapted.replace("configuration", "settings")
            adapted = adapted.replace("optimization", "improvement")
        
        return adapted
    
    def generate_recommendations(self, user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations."""
        user_id = user_context.get("user_id")
        recent_projects = user_context.get("recent_projects", [])
        skill_level = user_context.get("skill_level", "intermediate")
        time_constraints = user_context.get("time_constraints", "normal")
        
        recommendations = []
        
        # Project type recommendations
        if "web_app" in recent_projects:
            recommendations.append({
                "suggestion": "Consider using modern web frameworks for consistency",
                "confidence": 0.8,
                "personalization_reason": "Based on your recent web application projects"
            })
        
        if "mobile_app" in recent_projects:
            recommendations.append({
                "suggestion": "Explore cross-platform development options",
                "confidence": 0.7,
                "personalization_reason": "To leverage your mobile development experience"
            })
        
        # Skill level adaptations
        if skill_level == "beginner":
            recommendations.append({
                "suggestion": "Start with simpler project templates",
                "confidence": 0.9,
                "personalization_reason": "Matched to your current skill level"
            })
        elif skill_level == "expert":
            recommendations.append({
                "suggestion": "Consider advanced patterns and architectures",
                "confidence": 0.85,
                "personalization_reason": "Suitable for your expertise level"
            })
        
        # Time-based recommendations
        if time_constraints == "tight":
            recommendations.append({
                "suggestion": "Use pre-configured templates and automation",
                "confidence": 0.9,
                "personalization_reason": "Optimized for quick project setup"
            })
        
        return recommendations
    
    def provide_contextual_help(self, user_query: str, user_profile: UserProfile) -> str:
        """Provide contextual help adapted to user profile."""
        base_help = f"Here's help for: {user_query}"
        
        if user_profile.technical_level == "beginner":
            return f"{base_help}\n\nStep-by-step guidance:\n1. Start with basics\n2. Follow examples\n3. Test incrementally"
        elif user_profile.technical_level == "expert":
            return f"{base_help}\n\nKey considerations: architecture, performance, scalability"
        else:
            return f"{base_help}\n\nDetailed explanation with examples and best practices included."


class IntelligentAutomation:
    """Provides intelligent automation based on user behavior."""
    
    def __init__(self):
        """Initialize the intelligent automation system."""
        self.automation_thresholds = {
            "repetition_count": 5,  # Suggest automation after 5 repetitions
            "time_savings_min": 10   # Minimum 10% time savings to suggest
        }
    
    def suggest_automations(self, user_behavior: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest automations based on repetitive behavior."""
        repeated_actions = user_behavior.get("repeated_actions", [])
        suggestions = []
        
        for action_data in repeated_actions:
            action = action_data.get("action")
            count = action_data.get("count", 0)
            
            if count >= self.automation_thresholds["repetition_count"]:
                if action == "create_template":
                    suggestions.append({
                        "task": "Template creation with common settings",
                        "automation_type": "default_preset",
                        "potential_time_savings": "30%",
                        "implementation": "Create smart defaults based on your patterns"
                    })
                elif action == "apply_theme":
                    suggestions.append({
                        "task": "Automatic theme application",
                        "automation_type": "preference_automation",
                        "potential_time_savings": "20%",
                        "implementation": "Auto-apply your preferred theme to new templates"
                    })
        
        return suggestions
    
    def generate_intelligent_defaults(self, user_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent defaults based on user patterns."""
        defaults = {}
        
        # Set complexity default
        if "most_used_complexity" in user_patterns:
            defaults["complexity"] = user_patterns["most_used_complexity"]
        
        # Set theme default
        if "preferred_theme" in user_patterns:
            defaults["theme"] = user_patterns["preferred_theme"]
        
        # Set project type default
        if "common_project_type" in user_patterns:
            defaults["project_type"] = user_patterns["common_project_type"]
        
        # Set template category default
        if "frequent_category" in user_patterns:
            defaults["category"] = user_patterns["frequent_category"]
        
        return defaults
    
    def automate_workflow(self, workflow_pattern: BehaviorPattern, context: Dict[str, Any]) -> Dict[str, Any]:
        """Automate a workflow based on recognized patterns."""
        automation_result = {
            "pattern_id": workflow_pattern.pattern_id,
            "automated_actions": [],
            "time_saved": 0,
            "success": True
        }
        
        # Simulate automation based on pattern actions
        for action in workflow_pattern.actions:
            if action == "apply_modern_theme":
                automation_result["automated_actions"].append("Applied modern theme automatically")
                automation_result["time_saved"] += 30  # seconds
            elif action == "set_high_complexity":
                automation_result["automated_actions"].append("Set complexity to high based on pattern")
                automation_result["time_saved"] += 15  # seconds
        
        return automation_result


class PersonalizationEngine:
    """Main engine for advanced personalization."""
    
    def __init__(self):
        """Initialize the personalization engine."""
        self.behavior_analyzer = UserBehaviorAnalyzer()
        self.ai_assistant = AdaptiveAIAssistant()
        self.automation = IntelligentAutomation()
        self.user_profiles: Dict[str, UserProfile] = {}
        self.feedback_data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    def personalize_experience(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide comprehensive personalized experience."""
        user_id = user_context.get("user_id")
        session_data = user_context.get("session_data", {})
        request = user_context.get("request", "")
        
        # Track session
        if session_data:
            session_data["user_id"] = user_id
            self.behavior_analyzer.track_session(session_data)
        
        # Get or create user profile
        user_profile = self.get_user_profile(user_id)
        if not user_profile:
            user_profile = UserProfile(user_id=user_id)
            self.user_profiles[user_id] = user_profile
        
        # Generate personalized response
        adapted_response = self.ai_assistant.adapt_response(
            f"Response to: {request}", user_profile
        )
        
        # Generate recommendations
        recommendations = self.ai_assistant.generate_recommendations(user_context)
        
        # Generate automation suggestions
        user_patterns = self.behavior_analyzer.analyze_patterns({
            "user_id": user_id,
            "sessions": self.behavior_analyzer.get_user_sessions(user_id)
        })
        automation_suggestions = self.automation.suggest_automations({
            "repeated_actions": [
                {"action": "create_template", "count": 8},
                {"action": "apply_theme", "count": 6}
            ]
        })
        
        return {
            "adapted_response": adapted_response,
            "recommendations": recommendations,
            "automation_suggestions": automation_suggestions,
            "user_patterns": user_patterns
        }
    
    def learn_from_feedback(self, feedback: Dict[str, Any]) -> bool:
        """Learn from user feedback to improve personalization."""
        user_id = feedback.get("user_id")
        if not user_id:
            return False
        
        try:
            self.feedback_data[user_id].append(feedback)
            
            # Update user profile based on feedback
            user_profile = self.get_user_profile(user_id)
            if user_profile:
                # Adjust preferences based on feedback
                if feedback.get("satisfaction", 0) >= 4:
                    helpful_features = feedback.get("helpful_features", [])
                    if "automated_setup" in helpful_features:
                        user_profile.behavior_insights["prefers_automation"] = True
                    if "intelligent_defaults" in helpful_features:
                        user_profile.behavior_insights["likes_smart_defaults"] = True
                
                user_profile.updated_at = datetime.now().isoformat()
            
            return True
        except Exception:
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID."""
        return self.user_profiles.get(user_id)
    
    def process_user_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a complete user session."""
        user_id = session_data.get("user_id")
        
        # Track the session
        self.behavior_analyzer.track_session(session_data)
        
        # Update or create user profile
        user_profile = self.get_user_profile(user_id)
        if not user_profile:
            user_profile = UserProfile(
                user_id=user_id,
                created_at=datetime.now().isoformat()
            )
            self.user_profiles[user_id] = user_profile
        
        # Analyze behavior and update profile
        behavior_data = {
            "session_count": len(self.behavior_analyzer.get_user_sessions(user_id)),
            "recent_actions": session_data.get("actions", [])
        }
        user_profile.update_from_behavior(behavior_data)
        
        # Extract preferences from session
        if "preferred_complexity" in session_data:
            user_profile.preferred_complexity = session_data["preferred_complexity"]
        
        # Generate recommendations for next session
        patterns = self.behavior_analyzer.analyze_patterns({
            "user_id": user_id,
            "sessions": [session_data]
        })
        
        next_session_improvements = []
        if patterns.get("frequent_actions"):
            next_session_improvements.append("Pre-configure common actions for faster workflow")
        
        return {
            "user_profile_updated": True,
            "recommendations": self.ai_assistant.generate_recommendations({
                "user_id": user_id,
                "skill_level": user_profile.technical_level
            }),
            "next_session_improvements": next_session_improvements,
            "behavior_patterns": patterns
        }
