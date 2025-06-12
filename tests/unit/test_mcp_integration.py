"""
Unit tests for MCP Integration System - Following TDD approach.

Testing MCP server detection, tool recommendation system, and external service integration.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from opius_planner.advanced.mcp_integration import (
    MCPServerDetector,
    ToolRecommendationSystem,
    ExternalServiceIntegrator,
    MCPIntegrationManager,
    MCPServer,
    MCPTool
)
from opius_planner.templates.template_engine import TemplateContext
from opius_planner.core.task_analyzer import TaskCategory, TaskComplexity


class TestMCPServerDetector:
    """Test suite for MCPServerDetector following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.detector = MCPServerDetector()
    
    def test_init_loads_server_detector(self):
        """Test that detector initializes with server detection capabilities."""
        detector = MCPServerDetector()
        
        assert detector is not None
        assert hasattr(detector, 'available_servers')
        assert hasattr(detector, 'connection_manager')
    
    def test_detect_available_mcp_servers(self):
        """Test detecting available MCP servers."""
        # Mock some available servers
        with patch('opius_planner.advanced.mcp_integration.discover_mcp_servers') as mock_discover:
            mock_discover.return_value = [
                {
                    "name": "github",
                    "description": "GitHub integration server",
                    "capabilities": ["repositories", "issues", "pull_requests"],
                    "endpoint": "mcp://github-server",
                    "status": "available"
                },
                {
                    "name": "playwright",
                    "description": "Web automation server",
                    "capabilities": ["browser_automation", "testing", "screenshots"],
                    "endpoint": "mcp://playwright-server",
                    "status": "available"
                }
            ]
            
            servers = self.detector.detect_servers()
            
            assert isinstance(servers, list)
            assert len(servers) >= 2
            assert any(s["name"] == "github" for s in servers)
            assert any(s["name"] == "playwright" for s in servers)
    
    def test_check_server_compatibility(self):
        """Test checking server compatibility with project needs."""
        project_context = {
            "category": "technical",
            "requirements": ["web_development", "github_integration", "testing"],
            "complexity": "high"
        }
        
        github_server = MCPServer(
            name="github",
            capabilities=["repositories", "issues", "pull_requests"],
            description="GitHub integration"
        )
        
        compatibility = self.detector.check_compatibility(github_server, project_context)
        
        assert isinstance(compatibility, dict)
        assert "score" in compatibility
        assert "matching_capabilities" in compatibility
        assert compatibility["score"] > 0
    
    def test_prioritize_servers_by_relevance(self):
        """Test prioritizing servers by project relevance."""
        servers = [
            MCPServer(name="github", capabilities=["git", "repositories"]),
            MCPServer(name="playwright", capabilities=["browser", "testing"]),
            MCPServer(name="database", capabilities=["sql", "data_management"])
        ]
        
        project_context = {
            "category": "technical",
            "requirements": ["web_testing", "browser_automation"]
        }
        
        prioritized = self.detector.prioritize_servers(servers, project_context)
        
        assert isinstance(prioritized, list)
        assert len(prioritized) == len(servers)
        # Playwright should be prioritized for web testing
        assert prioritized[0].name == "playwright"
    
    def test_establish_server_connections(self):
        """Test establishing connections to MCP servers."""
        server = MCPServer(
            name="test_server",
            endpoint="mcp://test-server",
            capabilities=["testing"]
        )
        
        with patch('opius_planner.advanced.mcp_integration.connect_to_mcp_server') as mock_connect:
            mock_connect.return_value = {"status": "connected", "session_id": "test_123"}
            
            connection_result = self.detector.connect_to_server(server)
            
            assert connection_result is not None
            assert connection_result["status"] == "connected"


class TestToolRecommendationSystem:
    """Test suite for ToolRecommendationSystem."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.recommendation_system = ToolRecommendationSystem()
    
    def test_analyze_project_needs(self):
        """Test analyzing project needs for tool recommendations."""
        project_context = TemplateContext(
            project_name="E-commerce Platform",
            category="technical",
            requirements=["web_development", "database", "payment_processing", "testing"],
            technologies=["React", "Node.js", "PostgreSQL"]
        )
        
        needs_analysis = self.recommendation_system.analyze_needs(project_context)
        
        assert isinstance(needs_analysis, dict)
        assert "primary_needs" in needs_analysis
        assert "secondary_needs" in needs_analysis
        assert "tool_categories" in needs_analysis
    
    def test_recommend_mcp_tools(self):
        """Test recommending MCP tools based on project needs."""
        project_needs = {
            "primary_needs": ["version_control", "web_testing", "deployment"],
            "complexity": "high",
            "team_size": 8
        }
        
        available_servers = [
            MCPServer(name="github", capabilities=["git", "repositories", "ci_cd"]),
            MCPServer(name="playwright", capabilities=["browser_testing", "automation"]),
            MCPServer(name="aws", capabilities=["deployment", "infrastructure"])
        ]
        
        recommendations = self.recommendation_system.recommend_tools(
            project_needs, available_servers
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert "server" in rec
            assert "tools" in rec
            assert "relevance_score" in rec
            assert "reasoning" in rec
    
    def test_generate_integration_plan(self):
        """Test generating integration plan for recommended tools."""
        recommended_tools = [
            {
                "server": "github",
                "tools": ["create_repository", "setup_ci_cd"],
                "relevance_score": 0.9
            },
            {
                "server": "playwright",
                "tools": ["setup_testing", "create_test_suite"],
                "relevance_score": 0.8
            }
        ]
        
        integration_plan = self.recommendation_system.create_integration_plan(recommended_tools)
        
        assert isinstance(integration_plan, dict)
        assert "phases" in integration_plan
        assert "setup_order" in integration_plan
        assert "dependencies" in integration_plan
    
    def test_customize_recommendations_by_complexity(self):
        """Test customizing recommendations based on project complexity."""
        simple_project = {"complexity": "low", "team_size": 2}
        complex_project = {"complexity": "very_high", "team_size": 15}
        
        simple_recs = self.recommendation_system.customize_for_complexity(
            simple_project, ["basic_tools", "advanced_tools"]
        )
        
        complex_recs = self.recommendation_system.customize_for_complexity(
            complex_project, ["basic_tools", "advanced_tools"]
        )
        
        assert isinstance(simple_recs, list)
        assert isinstance(complex_recs, list)
        # Complex projects should get more comprehensive tooling
        assert len(complex_recs) >= len(simple_recs)


class TestExternalServiceIntegrator:
    """Test suite for ExternalServiceIntegrator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.integrator = ExternalServiceIntegrator()
    
    def test_integrate_github_services(self):
        """Test integrating GitHub services."""
        github_config = {
            "server": "github",
            "services": ["repositories", "issues", "pull_requests"],
            "project_context": {
                "name": "Test Project",
                "repository_url": "https://github.com/user/test-project"
            }
        }
        
        with patch('opius_planner.advanced.mcp_integration.call_mcp_tool') as mock_call:
            mock_call.return_value = {"status": "success", "data": "integration_complete"}
            
            integration_result = self.integrator.integrate_service(github_config)
            
            assert integration_result is not None
            assert "status" in integration_result
            assert integration_result["status"] == "success"
    
    def test_integrate_browser_automation(self):
        """Test integrating browser automation services."""
        playwright_config = {
            "server": "playwright",
            "services": ["browser_automation", "testing"],
            "test_scenarios": ["user_registration", "checkout_process"]
        }
        
        with patch('opius_planner.advanced.mcp_integration.setup_playwright_tests') as mock_setup:
            mock_setup.return_value = {"tests_created": 5, "status": "ready"}
            
            result = self.integrator.setup_browser_automation(playwright_config)
            
            assert result is not None
            assert result["tests_created"] == 5
    
    def test_integrate_aws_services(self):
        """Test integrating AWS deployment services."""
        aws_config = {
            "server": "aws",
            "services": ["deployment", "monitoring"],
            "infrastructure_requirements": {
                "compute": "medium",
                "storage": "high",
                "monitoring": True
            }
        }
        
        with patch('opius_planner.advanced.mcp_integration.setup_aws_infrastructure') as mock_aws:
            mock_aws.return_value = {"infrastructure_id": "infra_123", "status": "deployed"}
            
            result = self.integrator.setup_aws_infrastructure(aws_config)
            
            assert result is not None
            assert "infrastructure_id" in result
    
    def test_handle_integration_errors(self):
        """Test handling integration errors gracefully."""
        failing_config = {
            "server": "nonexistent_server",
            "services": ["invalid_service"]
        }
        
        result = self.integrator.integrate_service(failing_config)
        
        assert result is not None
        assert "error" in result
        assert result["status"] == "failed"
    
    def test_monitor_integration_health(self):
        """Test monitoring health of integrated services."""
        active_integrations = [
            {"server": "github", "service": "repositories", "last_check": "2025-06-12T10:00:00"},
            {"server": "playwright", "service": "testing", "last_check": "2025-06-12T09:30:00"}
        ]
        
        health_status = self.integrator.check_integration_health(active_integrations)
        
        assert isinstance(health_status, dict)
        assert "overall_status" in health_status
        assert "service_status" in health_status


class TestMCPIntegrationManager:
    """Test suite for MCPIntegrationManager integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = MCPIntegrationManager()
    
    def test_init_integrates_all_components(self):
        """Test that manager integrates all MCP components."""
        manager = MCPIntegrationManager()
        
        assert manager is not None
        assert hasattr(manager, 'server_detector')
        assert hasattr(manager, 'tool_recommender')
        assert hasattr(manager, 'service_integrator')
    
    def test_full_mcp_integration_workflow(self):
        """Test complete MCP integration workflow."""
        project_context = {
            "name": "Full Stack Web App",
            "category": "technical",
            "complexity": "high",
            "requirements": ["github_integration", "web_testing", "deployment"],
            "team_size": 6
        }
        
        with patch.multiple(
            'opius_planner.advanced.mcp_integration',
            discover_mcp_servers=Mock(return_value=[
                {"name": "github", "capabilities": ["git", "repositories"]},
                {"name": "playwright", "capabilities": ["testing", "automation"]}
            ]),
            connect_to_mcp_server=Mock(return_value={"status": "connected"}),
            call_mcp_tool=Mock(return_value={"status": "success"})
        ):
            integration_result = self.manager.integrate_project(project_context)
            
            assert isinstance(integration_result, dict)
            assert "recommended_servers" in integration_result
            assert "integration_plan" in integration_result
            assert "setup_status" in integration_result
    
    def test_adaptive_integration_based_on_feedback(self):
        """Test adaptive integration based on user feedback."""
        initial_recommendations = [
            {"server": "github", "confidence": 0.9},
            {"server": "aws", "confidence": 0.7}
        ]
        
        user_feedback = {
            "github": {"used": True, "satisfaction": 5, "effectiveness": 0.9},
            "aws": {"used": False, "reason": "too_complex"}
        }
        
        adapted_recs = self.manager.adapt_recommendations(
            initial_recommendations, user_feedback
        )
        
        assert isinstance(adapted_recs, list)
        # Should adjust future recommendations based on feedback
        github_rec = next((r for r in adapted_recs if r["server"] == "github"), None)
        assert github_rec is not None
        assert github_rec["confidence"] >= 0.9  # Should maintain or increase confidence
    
    def test_generate_mcp_enhanced_templates(self):
        """Test generating templates enhanced with MCP capabilities."""
        template_context = TemplateContext(
            project_name="MCP Enhanced Project",
            mcp_integrations=["github", "playwright", "aws"]
        )
        
        enhanced_template = self.manager.generate_enhanced_template(
            template_type="technical_project",
            context=template_context
        )
        
        assert enhanced_template is not None
        assert isinstance(enhanced_template, str)
        assert "github" in enhanced_template.lower()
        assert "mcp" in enhanced_template.lower()
    
    def test_continuous_mcp_monitoring(self):
        """Test continuous monitoring of MCP integrations."""
        active_integrations = {
            "github": {"status": "active", "last_used": "2025-06-12T10:00:00"},
            "playwright": {"status": "idle", "last_used": "2025-06-11T15:30:00"}
        }
        
        monitoring_report = self.manager.monitor_integrations(active_integrations)
        
        assert isinstance(monitoring_report, dict)
        assert "health_summary" in monitoring_report
        assert "usage_statistics" in monitoring_report
        assert "recommendations" in monitoring_report
    
    def test_integration_security_validation(self):
        """Test security validation for MCP integrations."""
        security_config = {
            "servers": ["github", "aws"],
            "permissions": ["read", "write"],
            "authentication": "oauth",
            "data_access": "project_scoped"
        }
        
        security_validation = self.manager.validate_security(security_config)
        
        assert isinstance(security_validation, dict)
        assert "security_score" in security_validation
        assert "warnings" in security_validation
        assert "recommendations" in security_validation


class TestMCPServer:
    """Test suite for MCPServer data structure."""
    
    def test_create_mcp_server(self):
        """Test creating an MCP server instance."""
        server = MCPServer(
            name="github",
            description="GitHub integration server",
            capabilities=["repositories", "issues", "pull_requests"],
            endpoint="mcp://github-server",
            version="1.0.0"
        )
        
        assert server.name == "github"
        assert "repositories" in server.capabilities
        assert server.endpoint == "mcp://github-server"
    
    def test_server_capability_matching(self):
        """Test matching server capabilities with requirements."""
        server = MCPServer(
            name="test_server",
            capabilities=["web_testing", "automation", "screenshots"]
        )
        
        requirements = ["web_testing", "automation"]
        matches = server.matches_requirements(requirements)
        
        assert matches is True
        
        unmatched_requirements = ["database", "deployment"]
        no_matches = server.matches_requirements(unmatched_requirements)
        
        assert no_matches is False


class TestMCPTool:
    """Test suite for MCPTool data structure."""
    
    def test_create_mcp_tool(self):
        """Test creating an MCP tool instance."""
        tool = MCPTool(
            name="create_repository",
            server="github",
            description="Create a new GitHub repository",
            parameters=["name", "description", "private"],
            return_type="repository_info"
        )
        
        assert tool.name == "create_repository"
        assert tool.server == "github"
        assert "name" in tool.parameters
    
    def test_tool_execution_simulation(self):
        """Test simulating tool execution."""
        tool = MCPTool(
            name="run_tests",
            server="playwright",
            description="Run browser tests"
        )
        
        # Simulate tool execution
        with patch('opius_planner.advanced.mcp_integration.execute_mcp_tool') as mock_execute:
            mock_execute.return_value = {"tests_run": 15, "passed": 14, "failed": 1}
            
            result = tool.execute({"test_suite": "e2e_tests"})
            
            assert result is not None
            assert result["tests_run"] == 15


class TestMCPIntegrationScenarios:
    """Integration tests for common MCP scenarios."""
    
    def test_web_development_mcp_stack(self):
        """Test MCP integration for web development projects."""
        project = {
            "type": "web_application",
            "technologies": ["React", "Node.js"],
            "requirements": ["github_integration", "testing", "deployment"]
        }
        
        manager = MCPIntegrationManager()
        
        with patch.multiple(
            'opius_planner.advanced.mcp_integration',
            discover_mcp_servers=Mock(return_value=[
                {"name": "github", "capabilities": ["git", "ci_cd"]},
                {"name": "playwright", "capabilities": ["testing", "browser"]},
                {"name": "aws", "capabilities": ["deployment", "hosting"]}
            ])
        ):
            mcp_stack = manager.recommend_mcp_stack(project)
            
            assert isinstance(mcp_stack, list)
            assert len(mcp_stack) >= 2
            # Should include GitHub and testing tools
            server_names = [server["name"] for server in mcp_stack]
            assert "github" in server_names
    
    def test_data_science_mcp_integration(self):
        """Test MCP integration for data science projects."""
        project = {
            "type": "data_analysis",
            "technologies": ["Python", "Jupyter"],
            "requirements": ["data_processing", "visualization", "model_deployment"]
        }
        
        manager = MCPIntegrationManager()
        recommendations = manager.recommend_for_domain(project, "data_science")
        
        assert isinstance(recommendations, list)
        # Should focus on data-related MCP servers
    
    def test_mobile_development_mcp_setup(self):
        """Test MCP integration for mobile development."""
        project = {
            "type": "mobile_application",
            "platforms": ["iOS", "Android"],
            "requirements": ["app_store_deployment", "testing", "analytics"]
        }
        
        manager = MCPIntegrationManager()
        mobile_setup = manager.setup_mobile_integration(project)
        
        assert isinstance(mobile_setup, dict)
        assert "deployment_tools" in mobile_setup
        assert "testing_tools" in mobile_setup
