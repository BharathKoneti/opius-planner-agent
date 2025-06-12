"""
MCP Integration System - Phase 3.2 Implementation.

Provides MCP server detection, tool recommendation, and external service integration.
"""

import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict


@dataclass
class MCPServer:
    """Represents an MCP server with its capabilities."""
    name: str
    description: str = ""
    capabilities: List[str] = field(default_factory=list)
    endpoint: str = ""
    version: str = "1.0.0"
    status: str = "unknown"
    
    def matches_requirements(self, requirements: List[str]) -> bool:
        """Check if server capabilities match requirements."""
        return any(req in self.capabilities for req in requirements)


@dataclass
class MCPTool:
    """Represents an MCP tool with execution capabilities."""
    name: str
    server: str
    description: str = ""
    parameters: List[str] = field(default_factory=list)
    return_type: str = "dict"
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the MCP tool with given parameters."""
        # Simulate tool execution
        return {"status": "executed", "tool": self.name, "params": params}


class MCPServerDetector:
    """Detects and manages available MCP servers."""
    
    def __init__(self):
        """Initialize the MCP server detector."""
        self.available_servers: List[MCPServer] = []
        self.connection_manager: Dict[str, Any] = {}
        self._load_known_servers()
    
    def _load_known_servers(self):
        """Load known MCP servers."""
        # Initialize with common MCP servers
        self.available_servers = [
            MCPServer(
                name="github",
                description="GitHub integration server",
                capabilities=["repositories", "issues", "pull_requests", "git", "ci_cd"],
                endpoint="mcp://github-server",
                status="available"
            ),
            MCPServer(
                name="playwright",
                description="Web automation server",
                capabilities=["browser_automation", "testing", "screenshots", "web_scraping"],
                endpoint="mcp://playwright-server",
                status="available"
            ),
            MCPServer(
                name="aws",
                description="AWS cloud services",
                capabilities=["deployment", "infrastructure", "storage", "monitoring"],
                endpoint="mcp://aws-server",
                status="available"
            )
        ]
    
    def detect_servers(self) -> List[Dict[str, Any]]:
        """Detect available MCP servers."""
        return [
            {
                "name": server.name,
                "description": server.description,
                "capabilities": server.capabilities,
                "endpoint": server.endpoint,
                "status": server.status
            }
            for server in self.available_servers
        ]
    
    def check_compatibility(self, server: MCPServer, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Check server compatibility with project needs."""
        requirements = project_context.get("requirements", [])
        
        # Calculate compatibility score
        matching_caps = [cap for cap in server.capabilities if any(req in cap for req in requirements)]
        compatibility_score = len(matching_caps) / max(len(requirements), 1)
        
        return {
            "score": min(compatibility_score * 100, 100),
            "matching_capabilities": matching_caps,
            "server_name": server.name
        }
    
    def prioritize_servers(self, servers: List[MCPServer], project_context: Dict[str, Any]) -> List[MCPServer]:
        """Prioritize servers by project relevance."""
        scored_servers = []
        
        for server in servers:
            compatibility = self.check_compatibility(server, project_context)
            scored_servers.append((server, compatibility["score"]))
        
        # Sort by compatibility score (descending)
        scored_servers.sort(key=lambda x: x[1], reverse=True)
        
        return [server for server, score in scored_servers]
    
    def connect_to_server(self, server: MCPServer) -> Dict[str, Any]:
        """Establish connection to an MCP server."""
        # Simulate connection
        connection_id = f"conn_{server.name}_{len(self.connection_manager)}"
        
        self.connection_manager[server.name] = {
            "connection_id": connection_id,
            "status": "connected",
            "server": server,
            "last_ping": "2025-06-12T15:30:00"
        }
        
        return {
            "status": "connected",
            "session_id": connection_id,
            "server": server.name
        }


class ToolRecommendationSystem:
    """Recommends MCP tools based on project analysis."""
    
    def __init__(self):
        """Initialize the tool recommendation system."""
        self.recommendation_cache: Dict[str, Any] = {}
        self.tool_database: Dict[str, List[MCPTool]] = self._build_tool_database()
    
    def _build_tool_database(self) -> Dict[str, List[MCPTool]]:
        """Build database of available MCP tools."""
        return {
            "github": [
                MCPTool("create_repository", "github", "Create new repository", ["name", "description"]),
                MCPTool("setup_ci_cd", "github", "Setup CI/CD pipeline", ["workflow_type", "triggers"]),
                MCPTool("manage_issues", "github", "Manage GitHub issues", ["action", "issue_data"])
            ],
            "playwright": [
                MCPTool("setup_testing", "playwright", "Setup browser testing", ["test_type", "browsers"]),
                MCPTool("create_test_suite", "playwright", "Create test suite", ["scenarios", "config"]),
                MCPTool("run_automation", "playwright", "Run browser automation", ["script", "options"])
            ],
            "aws": [
                MCPTool("deploy_infrastructure", "aws", "Deploy AWS infrastructure", ["template", "params"]),
                MCPTool("setup_monitoring", "aws", "Setup CloudWatch monitoring", ["resources", "alarms"]),
                MCPTool("manage_storage", "aws", "Manage S3 storage", ["buckets", "policies"])
            ]
        }
    
    def analyze_needs(self, project_context) -> Dict[str, Any]:
        """Analyze project needs for tool recommendations."""
        context_dict = project_context.to_dict() if hasattr(project_context, 'to_dict') else project_context
        
        primary_needs = []
        secondary_needs = []
        
        # Extract needs from requirements
        requirements = context_dict.get("requirements", [])
        for req in requirements:
            if any(key in req for key in ["git", "repository", "version"]):
                primary_needs.append("version_control")
            elif any(key in req for key in ["test", "automation", "browser"]):
                primary_needs.append("web_testing")
            elif any(key in req for key in ["deploy", "infrastructure", "cloud"]):
                primary_needs.append("deployment")
        
        # Extract from technologies
        technologies = context_dict.get("technologies", [])
        for tech in technologies:
            if tech.lower() in ["react", "vue", "angular"]:
                secondary_needs.append("frontend_testing")
            elif tech.lower() in ["node.js", "python", "java"]:
                secondary_needs.append("backend_deployment")
        
        return {
            "primary_needs": primary_needs,
            "secondary_needs": secondary_needs,
            "tool_categories": list(set(primary_needs + secondary_needs)),
            "complexity": context_dict.get("complexity", "medium")
        }
    
    def recommend_tools(self, project_needs: Dict[str, Any], 
                       available_servers: List[MCPServer]) -> List[Dict[str, Any]]:
        """Recommend MCP tools based on project needs."""
        recommendations = []
        
        primary_needs = project_needs.get("primary_needs", [])
        
        for server in available_servers:
            server_tools = self.tool_database.get(server.name, [])
            relevant_tools = []
            
            # Match tools to needs
            for tool in server_tools:
                relevance = 0
                for need in primary_needs:
                    if need in tool.description.lower() or need in tool.name.lower():
                        relevance += 1
                
                if relevance > 0:
                    relevant_tools.append(tool.name)
            
            if relevant_tools:
                recommendations.append({
                    "server": server.name,
                    "tools": relevant_tools,
                    "relevance_score": len(relevant_tools) / max(len(primary_needs), 1),
                    "reasoning": f"Server {server.name} provides tools for {', '.join(primary_needs[:2])}"
                })
        
        return sorted(recommendations, key=lambda x: x["relevance_score"], reverse=True)
    
    def create_integration_plan(self, recommended_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create integration plan for recommended tools."""
        phases = []
        setup_order = []
        dependencies = {}
        
        # Phase 1: Core infrastructure
        core_servers = [tool for tool in recommended_tools if tool["server"] in ["github", "aws"]]
        if core_servers:
            phases.append({
                "name": "Infrastructure Setup",
                "servers": [server["server"] for server in core_servers],
                "duration": "1-2 days"
            })
            setup_order.extend([server["server"] for server in core_servers])
        
        # Phase 2: Development tools
        dev_servers = [tool for tool in recommended_tools if tool["server"] in ["playwright"]]
        if dev_servers:
            phases.append({
                "name": "Development Tools",
                "servers": [server["server"] for server in dev_servers],
                "duration": "1 day"
            })
            setup_order.extend([server["server"] for server in dev_servers])
        
        # Set up dependencies
        if "github" in setup_order and "playwright" in setup_order:
            dependencies["playwright"] = ["github"]
        
        return {
            "phases": phases,
            "setup_order": setup_order,
            "dependencies": dependencies,
            "estimated_duration": "2-3 days"
        }
    
    def customize_for_complexity(self, project_context: Dict[str, Any], 
                                available_tools: List[str]) -> List[str]:
        """Customize recommendations based on project complexity."""
        complexity = project_context.get("complexity", "medium")
        team_size = project_context.get("team_size", 5)
        
        if complexity == "low" and team_size <= 3:
            # Simple projects need basic tools
            return [tool for tool in available_tools if "basic" in tool or "simple" in tool]
        elif complexity in ["high", "very_high"] or team_size >= 10:
            # Complex projects need comprehensive tooling
            return available_tools  # Return all tools
        else:
            # Medium complexity gets moderate tooling
            return available_tools[:len(available_tools)//2 + 1]


def discover_mcp_servers():
    """Mock function to discover MCP servers."""
    return [
        {"name": "github", "capabilities": ["git", "repositories"]},
        {"name": "playwright", "capabilities": ["testing", "automation"]}
    ]

def connect_to_mcp_server(server):
    """Mock function to connect to MCP server."""
    return {"status": "connected"}

def call_mcp_tool(tool, params):
    """Mock function to call MCP tool."""
    return {"status": "success"}

def setup_playwright_tests(config):
    """Mock function to setup Playwright tests."""
    return {"tests_created": 5, "status": "ready"}

def setup_aws_infrastructure(config):
    """Mock function to setup AWS infrastructure."""
    return {"infrastructure_id": "infra_123", "status": "deployed"}

def execute_mcp_tool(tool, params):
    """Mock function to execute MCP tool."""
    return {"status": "executed", "result": "success"}


class ExternalServiceIntegrator:
    """Integrates external services through MCP servers."""
    
    def __init__(self):
        """Initialize the external service integrator."""
        self.active_integrations: Dict[str, Any] = {}
        self.integration_history: List[Dict[str, Any]] = []
    
    def integrate_service(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate an external service based on configuration."""
        server_name = config.get("server")
        services = config.get("services", [])
        
        try:
            if server_name == "github":
                return self._integrate_github(config)
            elif server_name == "playwright":
                return self._integrate_playwright(config)
            elif server_name == "aws":
                return self._integrate_aws(config)
            else:
                return {
                    "status": "failed",
                    "error": f"Unknown server: {server_name}",
                    "server": server_name
                }
        except Exception as e:
            return {
                "status": "failed", 
                "error": str(e),
                "server": server_name
            }
    
    def _integrate_github(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate GitHub services."""
        services = config.get("services", [])
        project_context = config.get("project_context", {})
        
        integration_result = {
            "status": "success",
            "server": "github",
            "services_configured": services,
            "details": {}
        }
        
        if "repositories" in services:
            integration_result["details"]["repository"] = {
                "name": project_context.get("name", "project"),
                "url": project_context.get("repository_url", ""),
                "configured": True
            }
        
        if "issues" in services:
            integration_result["details"]["issue_tracking"] = {
                "enabled": True,
                "templates": ["bug_report", "feature_request"]
            }
        
        return integration_result
    
    def _integrate_playwright(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate Playwright services."""
        services = config.get("services", [])
        test_scenarios = config.get("test_scenarios", [])
        
        return {
            "status": "success",
            "server": "playwright",
            "services_configured": services,
            "test_scenarios": test_scenarios,
            "tests_created": len(test_scenarios),
            "browser_support": ["chromium", "firefox", "webkit"]
        }
    
    def _integrate_aws(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate AWS services."""
        services = config.get("services", [])
        infrastructure_req = config.get("infrastructure_requirements", {})
        
        return {
            "status": "success",
            "server": "aws",
            "services_configured": services,
            "infrastructure": {
                "compute": infrastructure_req.get("compute", "medium"),
                "storage": infrastructure_req.get("storage", "standard"),
                "monitoring": infrastructure_req.get("monitoring", True)
            }
        }
    
    def setup_browser_automation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Setup browser automation with Playwright."""
        return setup_playwright_tests(config)
    
    def setup_aws_infrastructure(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Setup AWS infrastructure."""
        return setup_aws_infrastructure(config)
    
    def check_integration_health(self, integrations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check health of active integrations."""
        overall_status = "healthy"
        service_status = {}
        
        for integration in integrations:
            server = integration.get("server")
            service = integration.get("service")
            last_check = integration.get("last_check")
            
            # Simple health check based on last check time
            if last_check:
                service_status[f"{server}_{service}"] = {
                    "status": "healthy",
                    "last_check": last_check
                }
            else:
                overall_status = "warning"
                service_status[f"{server}_{service}"] = {
                    "status": "unknown",
                    "last_check": "never"
                }
        
        return {
            "overall_status": overall_status,
            "service_status": service_status,
            "total_services": len(integrations)
        }


class MCPIntegrationManager:
    """Main manager for MCP integration system."""
    
    def __init__(self):
        """Initialize the MCP integration manager."""
        self.server_detector = MCPServerDetector()
        self.tool_recommender = ToolRecommendationSystem()
        self.service_integrator = ExternalServiceIntegrator()
        self.recommendation_cache: Dict[str, Any] = {}
    
    def integrate_project(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate MCP services for a project."""
        # Detect available servers
        available_servers = [
            MCPServer(**server_data) 
            for server_data in self.server_detector.detect_servers()
        ]
        
        # Analyze project needs
        project_needs = self.tool_recommender.analyze_needs(project_context)
        
        # Recommend tools
        recommendations = self.tool_recommender.recommend_tools(project_needs, available_servers)
        
        # Create integration plan
        integration_plan = self.tool_recommender.create_integration_plan(recommendations)
        
        # Setup integrations
        setup_results = []
        for rec in recommendations[:2]:  # Setup top 2 recommendations
            config = {
                "server": rec["server"],
                "services": rec["tools"],
                "project_context": project_context
            }
            result = self.service_integrator.integrate_service(config)
            setup_results.append(result)
        
        return {
            "recommended_servers": [rec["server"] for rec in recommendations],
            "integration_plan": integration_plan,
            "setup_status": setup_results,
            "project_needs": project_needs
        }
    
    def adapt_recommendations(self, initial_recommendations: List[Dict[str, Any]], 
                            user_feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Adapt recommendations based on user feedback."""
        adapted = []
        
        for rec in initial_recommendations:
            server_name = rec["server"]
            feedback = user_feedback.get(server_name, {})
            
            if feedback.get("used") and feedback.get("satisfaction", 0) >= 4:
                # Increase confidence for well-received servers
                rec["confidence"] = min(rec.get("confidence", 0.5) + 0.1, 1.0)
                adapted.append(rec)
            elif not feedback.get("used") and feedback.get("reason") != "too_complex":
                # Keep unused servers unless they were too complex
                adapted.append(rec)
        
        return adapted
    
    def generate_enhanced_template(self, template_type: str, context) -> str:
        """Generate templates enhanced with MCP capabilities."""
        context_dict = context.to_dict() if hasattr(context, 'to_dict') else context
        
        project_name = context_dict.get("project_name", "MCP Enhanced Project")
        mcp_integrations = context_dict.get("mcp_integrations", [])
        
        template = f"""# {project_name}

## MCP Integration Overview
This project leverages MCP (Model Context Protocol) servers for enhanced capabilities:

"""
        
        for integration in mcp_integrations:
            if integration == "github":
                template += "### GitHub Integration\n- Repository management\n- Issue tracking\n- CI/CD pipeline\n\n"
            elif integration == "playwright":
                template += "### Playwright Integration\n- Browser automation\n- End-to-end testing\n- Visual regression testing\n\n"
            elif integration == "aws":
                template += "### AWS Integration\n- Cloud infrastructure\n- Deployment automation\n- Monitoring and logging\n\n"
        
        template += """## MCP Setup Instructions
1. Install required MCP servers
2. Configure authentication
3. Test connections
4. Implement project-specific integrations

## Benefits of MCP Integration
- Automated workflows
- Consistent processes
- Enhanced productivity
- Reduced manual errors
"""
        
        return template
    
    def monitor_integrations(self, active_integrations: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor active MCP integrations."""
        health_summary = {
            "total_integrations": len(active_integrations),
            "active_count": sum(1 for integration in active_integrations.values() 
                              if integration.get("status") == "active"),
            "idle_count": sum(1 for integration in active_integrations.values() 
                            if integration.get("status") == "idle")
        }
        
        usage_statistics = {}
        for name, integration in active_integrations.items():
            last_used = integration.get("last_used", "never")
            usage_statistics[name] = {
                "status": integration.get("status", "unknown"),
                "last_used": last_used,
                "usage_frequency": "regular" if integration.get("status") == "active" else "occasional"
            }
        
        recommendations = []
        for name, integration in active_integrations.items():
            if integration.get("status") == "idle":
                recommendations.append(f"Consider reviewing {name} integration usage")
        
        return {
            "health_summary": health_summary,
            "usage_statistics": usage_statistics,
            "recommendations": recommendations,
            "last_monitoring_check": "2025-06-12T15:30:00"
        }
    
    def validate_security(self, security_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate security configuration for MCP integrations."""
        servers = security_config.get("servers", [])
        permissions = security_config.get("permissions", [])
        authentication = security_config.get("authentication", "")
        
        security_score = 70  # Base score
        warnings = []
        recommendations = []
        
        # Check authentication method
        if authentication == "oauth":
            security_score += 20
        elif authentication == "api_key":
            security_score += 10
            warnings.append("API key authentication has lower security than OAuth")
        else:
            warnings.append("No authentication method specified")
        
        # Check permissions
        if "write" in permissions and len(servers) > 2:
            warnings.append("Write permissions granted to multiple servers")
            recommendations.append("Review write permissions and apply principle of least privilege")
        
        # Check data access scope
        data_access = security_config.get("data_access", "")
        if data_access == "project_scoped":
            security_score += 10
        elif data_access == "full_access":
            warnings.append("Full access permissions granted")
            recommendations.append("Consider limiting to project-scoped access")
        
        return {
            "security_score": min(security_score, 100),
            "warnings": warnings,
            "recommendations": recommendations,
            "compliance_status": "acceptable" if security_score >= 70 else "needs_improvement"
        }
    
    def recommend_mcp_stack(self, project: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend MCP stack for a project type."""
        project_type = project.get("type", "general")
        requirements = project.get("requirements", [])
        
        stack = []
        
        if project_type == "web_application":
            stack.extend([
                {"name": "github", "capabilities": ["git", "ci_cd"], "priority": "high"},
                {"name": "playwright", "capabilities": ["testing", "browser"], "priority": "high"},
                {"name": "aws", "capabilities": ["deployment", "hosting"], "priority": "medium"}
            ])
        
        # Filter by requirements
        if requirements:
            stack = [server for server in stack 
                    if any(req in cap for cap in server["capabilities"] for req in requirements)]
        
        return stack
    
    def recommend_for_domain(self, project: Dict[str, Any], domain: str) -> List[Dict[str, Any]]:
        """Recommend MCP tools for specific domain."""
        recommendations = []
        
        if domain == "data_science":
            recommendations = [
                {"server": "jupyter", "tools": ["notebook_management", "kernel_management"]},
                {"server": "python", "tools": ["package_management", "environment_setup"]}
            ]
        elif domain == "mobile_development":
            recommendations = [
                {"server": "app_store", "tools": ["deployment", "metadata_management"]},
                {"server": "testing", "tools": ["device_testing", "ui_automation"]}
            ]
        
        return recommendations
    
    def setup_mobile_integration(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Setup MCP integration for mobile development."""
        platforms = project.get("platforms", [])
        requirements = project.get("requirements", [])
        
        mobile_setup = {
            "deployment_tools": [],
            "testing_tools": [],
            "analytics_tools": []
        }
        
        if "iOS" in platforms:
            mobile_setup["deployment_tools"].append("app_store_connect")
        if "Android" in platforms:
            mobile_setup["deployment_tools"].append("google_play_console")
        
        if "testing" in requirements:
            mobile_setup["testing_tools"].extend(["device_farm", "ui_automator"])
        
        if "analytics" in requirements:
            mobile_setup["analytics_tools"].extend(["firebase_analytics", "app_analytics"])
        
        return mobile_setup
