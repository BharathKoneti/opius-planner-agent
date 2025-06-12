"""
Cross-Domain Learning System - Phase 3.1 Implementation.

Provides pattern recognition, success metric tracking, and recommendation improvement
through machine learning across different project domains.
"""

import json
import statistics
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict, Counter


@dataclass
class LearningPattern:
    """Represents a learned pattern from successful projects."""
    name: str
    trigger_conditions: Dict[str, Any]
    recommended_actions: List[str] = field(default_factory=list)
    success_probability: float = 0.0
    evidence_count: int = 0
    domains: List[str] = field(default_factory=list)
    
    def applies_to(self, context: Dict[str, Any]) -> bool:
        """Check if this pattern applies to the given context."""
        for key, condition in self.trigger_conditions.items():
            if key not in context:
                return False
            
            context_value = context[key]
            
            # Handle different condition types
            if isinstance(condition, str):
                if condition.startswith(">="):
                    threshold = float(condition[2:].strip())
                    if float(context_value) < threshold:
                        return False
                elif condition.startswith("<="):
                    threshold = float(condition[2:].strip())
                    if float(context_value) > threshold:
                        return False
                elif condition != context_value:
                    return False
            elif condition != context_value:
                return False
        
        return True


@dataclass
class SuccessMetric:
    """Represents a success metric for project evaluation."""
    name: str
    value: float
    target: float = 100.0
    unit: str = ""
    weight: float = 1.0
    
    def achieved_target(self) -> bool:
        """Check if the metric achieved its target."""
        return self.value >= self.target if self.target > 0 else self.value <= abs(self.target)
    
    def calculate_performance(self) -> float:
        """Calculate performance ratio (value/target)."""
        if self.target == 0:
            return 1.0
        return self.value / self.target


class PatternRecognitionSystem:
    """Recognizes patterns in successful projects across domains."""
    
    def __init__(self):
        """Initialize the pattern recognition system."""
        self.patterns: List[LearningPattern] = []
        self.pattern_database: Dict[str, Any] = {}
        self._load_existing_patterns()
    
    def _load_existing_patterns(self):
        """Load existing patterns from storage."""
        # Initialize with some basic patterns
        self.patterns = [
            LearningPattern(
                name="agile_high_success",
                trigger_conditions={"methodology": "agile", "team_size": ">= 5"},
                recommended_actions=["daily_standups", "sprint_planning", "retrospectives"],
                success_probability=0.85,
                evidence_count=20,
                domains=["technical", "business"]
            ),
            LearningPattern(
                name="small_team_efficiency",
                trigger_conditions={"team_size": "<= 4", "complexity": "medium"},
                recommended_actions=["pair_programming", "frequent_communication", "shared_ownership"],
                success_probability=0.78,
                evidence_count=15,
                domains=["technical", "creative"]
            )
        ]
    
    def identify_patterns(self, successful_projects: List[Dict[str, Any]]) -> List[LearningPattern]:
        """Identify patterns from successful project data."""
        patterns = []
        
        # Group projects by common characteristics
        tech_groups = defaultdict(list)
        process_groups = defaultdict(list)
        
        for project in successful_projects:
            # Group by technology patterns
            if "technologies" in project:
                for tech in project["technologies"]:
                    tech_groups[tech].append(project)
            
            # Group by process patterns
            if "approach" in project:
                process_groups[project["approach"]].append(project)
        
        # Identify technology patterns
        for tech, projects in tech_groups.items():
            if len(projects) >= 2:  # Need multiple examples
                avg_success = statistics.mean(p.get("success_score", 0) for p in projects)
                if avg_success > 80:
                    pattern = LearningPattern(
                        name=f"{tech.lower()}_success_pattern",
                        trigger_conditions={"technologies": tech},
                        recommended_actions=[f"use_{tech.lower()}", "best_practices"],
                        success_probability=avg_success / 100,
                        evidence_count=len(projects),
                        domains=["technical"]
                    )
                    patterns.append(pattern)
        
        # Identify process patterns
        for process, projects in process_groups.items():
            if len(projects) >= 2:
                avg_success = statistics.mean(p.get("success_score", 0) for p in projects)
                if avg_success > 75:
                    pattern = LearningPattern(
                        name=f"{process}_process_pattern",
                        trigger_conditions={"approach": process},
                        recommended_actions=[f"implement_{process}", "follow_methodology"],
                        success_probability=avg_success / 100,
                        evidence_count=len(projects),
                        domains=["business", "technical"]
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def find_cross_domain_patterns(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find patterns that work across different domains."""
        cross_patterns = {
            "common_approaches": [],
            "shared_success_factors": []
        }
        
        # Group by domain
        domain_groups = defaultdict(list)
        for project in projects:
            domain = project.get("category", "unknown")
            domain_groups[domain].append(project)
        
        # Find common approaches across domains
        all_approaches = []
        for domain, domain_projects in domain_groups.items():
            approaches = [p.get("approach") for p in domain_projects if p.get("approach")]
            all_approaches.extend(approaches)
        
        approach_counts = Counter(all_approaches)
        cross_patterns["common_approaches"] = [
            approach for approach, count in approach_counts.items() 
            if count >= 2
        ]
        
        # Find shared success factors
        all_factors = []
        for project in projects:
            factors = project.get("success_factors", [])
            all_factors.extend(factors)
        
        factor_counts = Counter(all_factors)
        cross_patterns["shared_success_factors"] = [
            factor for factor, count in factor_counts.items()
            if count >= 2
        ]
        
        return cross_patterns
    
    def create_pattern(self, name: str, data: Dict[str, Any]) -> LearningPattern:
        """Create a learning pattern from data."""
        return LearningPattern(
            name=name,
            trigger_conditions=data.get("trigger_conditions", {}),
            recommended_actions=data.get("recommended_actions", []),
            success_probability=data.get("success_probability", 0.0),
            evidence_count=data.get("evidence_count", 0),
            domains=data.get("domains", [])
        )
    
    def match_patterns(self, project_context: Dict[str, Any]) -> List[LearningPattern]:
        """Match patterns that apply to a new project."""
        matched = []
        for pattern in self.patterns:
            if pattern.applies_to(project_context):
                matched.append(pattern)
        return matched


class SuccessMetricTracker:
    """Tracks success metrics and analyzes what leads to success."""
    
    def __init__(self):
        """Initialize the success metric tracker."""
        self.project_metrics: Dict[str, Dict[str, Any]] = {}
        self.recommendation_outcomes: Dict[str, Dict[str, Any]] = {}
    
    def record_metrics(self, project_id: str, metrics: Dict[str, Any]) -> bool:
        """Record success metrics for a project."""
        try:
            self.project_metrics[project_id] = metrics
            return True
        except Exception:
            return False
    
    def get_metrics(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific project."""
        return self.project_metrics.get(project_id)
    
    def calculate_success_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall success score from individual metrics."""
        score = 0.0
        
        # Time performance (lower is better for completion_time)
        if "completion_time" in metrics:
            time_score = max(0, 100 - (metrics["completion_time"] - 8) * 5)  # 8 weeks baseline
            score += time_score * 0.25
        
        # Budget performance (lower utilization is better)
        if "budget_utilization" in metrics:
            budget_score = (2.0 - metrics["budget_utilization"]) * 50  # 1.0 = 50%, 0.9 = 55%
            score += max(0, min(budget_score, 100)) * 0.25
        
        # Quality score (direct)
        if "quality_score" in metrics:
            score += metrics["quality_score"] * 0.3
        
        # Stakeholder satisfaction (scale 1-5 to 0-100)
        if "stakeholder_satisfaction" in metrics:
            satisfaction_score = (metrics["stakeholder_satisfaction"] - 1) * 25  # 1=0, 5=100
            score += satisfaction_score * 0.2
        
        return min(score, 100.0)
    
    def track_recommendation_outcome(self, rec_id: str, recommendation: Dict[str, Any], 
                                   outcome: Dict[str, Any]):
        """Track the outcome of a recommendation."""
        self.recommendation_outcomes[rec_id] = {
            "recommendation": recommendation,
            "outcome": outcome,
            "effectiveness": outcome.get("success_impact", 0) * 100
        }
    
    def get_recommendation_effectiveness(self, rec_id: str) -> Optional[float]:
        """Get effectiveness score for a recommendation."""
        if rec_id in self.recommendation_outcomes:
            return self.recommendation_outcomes[rec_id]["effectiveness"]
        return None
    
    def identify_success_patterns(self) -> List[Dict[str, Any]]:
        """Identify patterns that lead to success."""
        patterns = []
        
        if len(self.project_metrics) < 2:
            return patterns
        
        # Analyze common factors in successful projects
        successful_projects = []
        for project_id, metrics in self.project_metrics.items():
            success_score = self.calculate_success_score(metrics)
            if success_score > 80:
                successful_projects.append(metrics)
        
        if len(successful_projects) >= 2:
            # Find common boolean factors
            common_factors = {}
            for project in successful_projects:
                for key, value in project.items():
                    if isinstance(value, bool) and value:
                        common_factors[key] = common_factors.get(key, 0) + 1
            
            # Identify factors present in majority of successful projects
            for factor, count in common_factors.items():
                if count >= len(successful_projects) * 0.6:  # 60% threshold
                    patterns.append({
                        "factor": factor,
                        "success_correlation": count / len(successful_projects),
                        "evidence_count": count
                    })
        
        return patterns


class RecommendationEngine:
    """Generates and improves recommendations based on learning."""
    
    def __init__(self):
        """Initialize the recommendation engine."""
        self.recommendation_history: List[Dict[str, Any]] = []
        self.feedback_data: Dict[str, Any] = {}
    
    def generate_recommendations(self, project_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for a project context."""
        recommendations = []
        
        category = project_context.get("category", "general")
        complexity = project_context.get("complexity", "medium")
        team_size = project_context.get("team_size", 5)
        
        # Process recommendations
        if team_size >= 8:
            recommendations.append({
                "type": "process",
                "suggestion": "Implement structured communication protocols",
                "confidence": 0.8,
                "reasoning": "Large teams benefit from clear communication structure",
                "impact": "high"
            })
        
        # Technology recommendations
        if category == "technical":
            if complexity in ["high", "very_high"]:
                recommendations.append({
                    "type": "technology",
                    "suggestion": "Use microservices architecture for scalability",
                    "confidence": 0.75,
                    "reasoning": "High complexity projects benefit from modular architecture",
                    "impact": "high"
                })
            
            recommendations.append({
                "type": "process",
                "suggestion": "Implement continuous integration/deployment",
                "confidence": 0.85,
                "reasoning": "CI/CD improves code quality and deployment reliability",
                "impact": "medium"
            })
        
        # Team recommendations
        if team_size <= 4:
            recommendations.append({
                "type": "team",
                "suggestion": "Use pair programming for knowledge sharing",
                "confidence": 0.7,
                "reasoning": "Small teams benefit from knowledge distribution",
                "impact": "medium"
            })
        
        # Timeline recommendations
        timeline = project_context.get("timeline", "")
        if "month" in timeline and int(timeline.split("_")[0]) <= 3:
            recommendations.append({
                "type": "process",
                "suggestion": "Use rapid prototyping and frequent feedback cycles",
                "confidence": 0.8,
                "reasoning": "Short timelines require quick validation and iteration",
                "impact": "high"
            })
        
        return recommendations
    
    def prioritize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize recommendations by importance and confidence."""
        def priority_score(rec):
            confidence = rec.get("confidence", 0.5)
            impact_weight = {"high": 1.0, "medium": 0.7, "low": 0.4}
            impact = impact_weight.get(rec.get("impact", "medium"), 0.7)
            return confidence * impact
        
        return sorted(recommendations, key=priority_score, reverse=True)
    
    def learn_from_feedback(self, recommendation_id: str, feedback: Dict[str, Any]):
        """Learn from recommendation feedback to improve future suggestions."""
        self.feedback_data[recommendation_id] = feedback
        
        # Analyze feedback to improve future recommendations
        if feedback.get("implemented") and feedback.get("effectiveness", 0) > 0.7:
            # Positive feedback - increase confidence for similar recommendations
            rec_type = feedback.get("type", "unknown")
            if rec_type not in self.feedback_data:
                self.feedback_data[f"{rec_type}_confidence_boost"] = 0.1
    
    def adapt_recommendations_to_domain(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Adapt recommendations to specific domain characteristics."""
        base_recommendations = self.generate_recommendations(context)
        domain = context.get("category", "general")
        
        # Domain-specific adaptations
        if domain == "creative":
            # Add creative-specific recommendations
            base_recommendations.append({
                "type": "process",
                "suggestion": "Schedule regular creative review sessions",
                "confidence": 0.75,
                "reasoning": "Creative projects benefit from iterative feedback",
                "impact": "medium"
            })
        elif domain == "business":
            # Add business-specific recommendations
            base_recommendations.append({
                "type": "stakeholder_management",
                "suggestion": "Establish clear stakeholder communication plan",
                "confidence": 0.8,
                "reasoning": "Business projects require strong stakeholder alignment",
                "impact": "high"
            })
        
        return base_recommendations


class CrossDomainLearner:
    """Integrates all learning components for cross-domain intelligence."""
    
    def __init__(self):
        """Initialize the cross-domain learner."""
        self.pattern_system = PatternRecognitionSystem()
        self.metric_tracker = SuccessMetricTracker()
        self.recommendation_engine = RecommendationEngine()
        self.knowledge_base: Dict[str, Any] = {}
    
    def learn_from_history(self, project_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Learn from historical project data."""
        learning_results = {
            "patterns_discovered": [],
            "success_factors": [],
            "cross_domain_insights": {}
        }
        
        # Record metrics for all projects
        for project in project_history:
            if "metrics" in project:
                self.metric_tracker.record_metrics(project["id"], project["metrics"])
        
        # Discover patterns
        successful_projects = [p for p in project_history if p.get("outcome") == "successful"]
        if successful_projects:
            patterns = self.pattern_system.identify_patterns(successful_projects)
            learning_results["patterns_discovered"] = [p.name for p in patterns]
            
            # Find cross-domain patterns
            cross_patterns = self.pattern_system.find_cross_domain_patterns(successful_projects)
            learning_results["cross_domain_insights"] = cross_patterns
        
        # Identify success factors
        success_patterns = self.metric_tracker.identify_success_patterns()
        learning_results["success_factors"] = success_patterns
        
        return learning_results
    
    def generate_intelligent_recommendations(self, project_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate intelligent recommendations based on all learning."""
        # Get base recommendations
        recommendations = self.recommendation_engine.generate_recommendations(project_context)
        
        # Enhance with pattern matching
        matching_patterns = self.pattern_system.match_patterns(project_context)
        for pattern in matching_patterns:
            for action in pattern.recommended_actions:
                recommendations.append({
                    "type": "learned_pattern",
                    "suggestion": action,
                    "confidence": pattern.success_probability,
                    "reasoning": f"Based on {pattern.name} pattern with {pattern.evidence_count} examples",
                    "evidence_strength": pattern.evidence_count / 10.0,  # Normalize to 0-1
                    "impact": "high" if pattern.success_probability > 0.8 else "medium"
                })
        
        # Prioritize and return
        return self.recommendation_engine.prioritize_recommendations(recommendations)
    
    def get_known_patterns(self) -> List[LearningPattern]:
        """Get all known patterns."""
        return self.pattern_system.patterns
    
    def integrate_new_learning(self, project_outcome: Dict[str, Any]):
        """Integrate learning from a new project outcome."""
        # Record new metrics
        if "success_score" in project_outcome:
            metrics = {
                "success_score": project_outcome["success_score"],
                "innovative_approaches": project_outcome.get("innovative_approaches", []),
                "lessons_learned": project_outcome.get("lessons_learned", [])
            }
            self.metric_tracker.record_metrics(project_outcome["id"], metrics)
        
        # Create new patterns if applicable
        if project_outcome.get("success_score", 0) > 85:
            pattern_data = {
                "trigger_conditions": {"category": project_outcome.get("category", "unknown")},
                "recommended_actions": project_outcome.get("innovative_approaches", []),
                "success_probability": project_outcome.get("success_score", 0) / 100,
                "evidence_count": 1
            }
            
            new_pattern = self.pattern_system.create_pattern(
                f"new_success_pattern_{len(self.pattern_system.patterns)}",
                pattern_data
            )
            self.pattern_system.patterns.append(new_pattern)
    
    def transfer_knowledge(self, source_domain: str, target_domain: str, 
                          pattern: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transfer knowledge from one domain to another."""
        if source_domain == target_domain:
            return pattern
        
        # Simple knowledge transfer - adapt pattern to target domain
        adapted_pattern = {
            "source_domain": source_domain,
            "target_domain": target_domain,
            "original_pattern": pattern["pattern"],
            "adapted_approach": f"Apply {pattern['pattern']} principles to {target_domain} context",
            "confidence": pattern.get("success_rate", 0.5) * 0.8,  # Reduce confidence for cross-domain
            "adaptation_notes": f"Transferred from {source_domain} domain"
        }
        
        return adapted_pattern
