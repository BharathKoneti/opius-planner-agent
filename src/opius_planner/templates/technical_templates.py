"""
Technical Templates Library - Phase 2 Implementation.

Provides specialized templates for technical domain tasks including
software development, DevOps, and testing projects.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from ..core.task_analyzer import TaskCategory, TaskComplexity
from .template_engine import Template, TemplateContext


class TechnicalTemplateType(Enum):
    """Types of technical templates available."""
    SOFTWARE_DEVELOPMENT = "software_development"
    DEVOPS = "devops"
    TESTING = "testing"


@dataclass
class SoftwareDevelopmentTemplate(Template):
    """Template for software development projects."""
    project_type: str = "web_application"
    tech_stack: List[str] = field(default_factory=list)
    
    def __init__(self, name: str, complexity: TaskComplexity, project_type: str = "web_application", 
                 tech_stack: List[str] = None, **kwargs):
        # Initialize base Template with required parameters
        super().__init__(
            name=name,
            category=TaskCategory.TECHNICAL,
            complexity=complexity,
            content="",  # Will be set after initialization
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.project_type = project_type
        self.tech_stack = tech_stack or ["JavaScript", "Node.js", "React"]
        # Generate content after initialization
        self.content = self._generate_software_template()
    
    def _generate_software_template(self) -> str:
        """Generate software development template content with tracker functionality."""
        
        return f"""# {{{{ project_name | default("Software Development Project") }}}}

**Project Type**: {{{{ project_type | default("{self.project_type.replace('_', ' ').title()}") }}}}
**Description**: {{{{ description | default("A software development project") }}}}
**Target Users**: {{{{ target_users | default("General users") }}}}

## 📋 Project Overview

**Key Features**: 
{{% if key_features %}}
{{% for feature in key_features %}}
- {{{{ feature }}}}
{{% endfor %}}
{{% else %}}
- Core functionality
- User management
- Data persistence
{{% endif %}}

**Technical Requirements**:
{{% if tech_requirements %}}
{{% for req in tech_requirements %}}
- {{{{ req }}}}
{{% endfor %}}
{{% else %}}
- Responsive design
- Secure authentication
- API integration
{{% endif %}}

## 📊 Project Tracker

**Instructions for LLM**: This tracker section should be continuously updated throughout the project. Maintain detailed progress tracking with visual indicators and completion percentages.

### 📈 Overall Progress
```
[░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0% Complete
```

### 🚀 Phase Status
| Phase | Status | Progress |
|-------|--------|----------|
| Planning | 🔴 Not Started | 0% |
| Design | 🔴 Not Started | 0% |
| Development | 🔴 Not Started | 0% |
| Testing | 🔴 Not Started | 0% |
| Deployment | 🔴 Not Started | 0% |

### 📌 Current Sprint Focus
- [ ] **Project Kickoff**
  Define project scope and objectives
- [ ] **Requirements Gathering**  
  Collect detailed functional requirements
- [ ] **Technical Specification**
  Create detailed technical documentation
- [ ] **Architecture Design**
  Design system architecture and components

## 🚀 Development Process

### Phase 1: Planning & Requirements (1-2 weeks)
- [ ] **Project Kickoff**
  Define project scope and objectives
  
- [ ] **Requirements Gathering**
  Collect detailed functional requirements
  
- [ ] **Technical Specification**
  Create detailed technical documentation
  
- [ ] **Architecture Design**
  Design system architecture and components

### Phase 2: Design & Prototyping (2-3 weeks)
- [ ] **UI/UX Design**
  Create wireframes and mockups
  
- [ ] **Database Schema**
  Design data models and relationships
  
- [ ] **API Design**
  Define API endpoints and documentation
  
- [ ] **Prototype Development**
  Build functional prototype for validation

### Phase 3: Development (4-8 weeks)
- [ ] **Environment Setup**
  Configure development and staging environments
  
- [ ] **Core Functionality**
  Implement core features and logic
  
- [ ] **Frontend Development**
  Build user interface components
  
- [ ] **Backend Development**
  Implement server-side logic and APIs
  
- [ ] **Database Integration**
  Implement data persistence layer
  
- [ ] **Authentication & Security**
  Implement security measures and user auth

### Phase 4: Testing & QA (2-3 weeks)
- [ ] **Unit Testing**
  Test individual components and functions
  
- [ ] **Integration Testing**
  Test component interactions and flows
  
- [ ] **Performance Testing**
  Evaluate system performance and optimize
  
- [ ] **Security Testing**
  Identify and fix security vulnerabilities
  
- [ ] **User Acceptance Testing**
  Validate with stakeholders and users

### Phase 5: Deployment & Launch (1-2 weeks)
- [ ] **Deployment Planning**
  Prepare deployment strategy and rollback plan
  
- [ ] **Infrastructure Setup**
  Configure production environment
  
- [ ] **Deployment Automation**
  Set up CI/CD pipeline for automated deployment
  
- [ ] **Launch**
  Release to production environment
  
- [ ] **Post-Launch Monitoring**
  Monitor for issues and performance

## 📊 Success Criteria
- [ ] All key features implemented and functional
- [ ] Performance meets specified requirements
- [ ] All tests passing with >90% coverage
- [ ] Security vulnerabilities addressed
- [ ] User acceptance criteria met
- [ ] Documentation complete and accurate

## 📚 Documentation
- Technical specification
- API documentation
- User guides
- Deployment instructions
- Maintenance procedures

## 🔄 Daily Progress Updates
**Instructions for LLM**: Update this section daily with progress, blockers, and achievements. Always reference your analysis document and work log.

### {{{{ current_date | default("2025-12-15") }}}}
- **Analysis Document**: [Project Analysis](./.project-scaffolding/project_analysis.md) - Document current project understanding
- **Work Log**: [Work Log](./.project-scaffolding/work_log.md) - [Session summary and next steps]
- **Completed**: Environment setup, project structure
- **In Progress**: User authentication system (refer to analysis for approach)
- **Blockers**: None (check work log for previous issues)
- **Next Steps**: Database schema design (detailed in work log)
- **Lessons Learned**: [Document any insights for future reference]

### {{{{ current_date | default("2025-12-14") }}}}
- **Analysis Document**: [Project Analysis](./.project-scaffolding/project_analysis.md) - Initial project analysis created
- **Work Log**: [Work Log](./.project-scaffolding/work_log.md) - [Day 1 setup and planning]
- **Completed**: Project kickoff, requirements gathering
- **In Progress**: Environment setup
- **Blockers**: None
- **Next Steps**: Begin core development (priorities documented in work log)
- **Lessons Learned**: Always create analysis document before coding

**Template for New Entries**:
```markdown
### [Date]
- **Analysis Document**: [Project Analysis](./.project-scaffolding/project_analysis.md) - [What was updated in analysis]
- **Work Log**: [Work Log](./.project-scaffolding/work_log.md) - [Session summary]
- **Completed**: [Specific tasks finished with details]
- **In Progress**: [Current work with reference to analysis approach]
- **Blockers**: [Issues with links to work log for solutions attempted]
- **Next Steps**: [Priorities based on analysis and work log planning]
- **Lessons Learned**: [Key insights for future sessions]
```

## 🛠️ Tools & Resources
- Version control: Git/GitHub
- Project management: Jira/Trello
- CI/CD: Jenkins/GitHub Actions
- Monitoring: Prometheus/Grafana
- Documentation: Confluence/Markdown

## 💡 Technical Considerations
- Scalability requirements
- Security best practices
- Performance optimization
- Accessibility standards
- Testing methodology
- Deployment strategy"""


@dataclass
class DevOpsTemplate(Template):
    """Template for DevOps projects."""
    devops_type: str = "cicd_pipeline"
    tools: List[str] = field(default_factory=list)
    
    def __init__(self, name: str, complexity: TaskComplexity, devops_type: str = "cicd_pipeline", 
                 tools: List[str] = None, **kwargs):
        super().__init__(
            name=name,
            category=TaskCategory.TECHNICAL,
            complexity=complexity,
            content="",
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.devops_type = devops_type
        self.tools = tools or ["GitHub Actions", "Docker", "AWS"]
        self.content = self._generate_devops_template()
    
    def _generate_devops_template(self) -> str:
        """Generate DevOps template content with tracker functionality."""
        tools_list = "\n".join([f"- {tool}" for tool in self.tools])
        
        return f"""# {{{{ project_name | default("DevOps Project") }}}}

**DevOps Type**: {self.devops_type.replace('_', ' ').title()}
**Tools & Technologies**: 
{tools_list}

## 📊 DevOps Tracker
**Instructions for LLM**: Update this tracker daily with pipeline status, deployments, and infrastructure changes.

### 🚀 Pipeline Status
| Environment | Status | Last Deploy | Health |
|-------------|--------|-------------|--------|
| Development | ✅ Healthy | 2 hours ago | 100% |
| Staging | 🟡 Warning | 1 day ago | 85% |
| Production | ✅ Healthy | 3 days ago | 98% |

### 📈 Infrastructure Metrics
- **Uptime**: 99.9%
- **Response Time**: 150ms avg
- **Error Rate**: 0.1%

## 🔧 DevOps Implementation

### Phase 1: Infrastructure Setup (1-2 weeks)
- [ ] **Cloud Environment Setup**
  Configure cloud infrastructure and networking
- [ ] **CI/CD Pipeline Configuration**
  Set up automated build and deployment pipeline
- [ ] **Infrastructure as Code**
  Implement IaC using Terraform/CloudFormation
- [ ] **Security Configuration**
  Configure security groups, IAM, and compliance

### Phase 2: Monitoring & Alerting (1 week)
- [ ] **Application Monitoring**
  Set up APM and performance monitoring
- [ ] **Infrastructure Monitoring**
  Monitor servers, databases, and services
- [ ] **Alerting System**
  Configure alerts for critical issues
- [ ] **Logging Aggregation**
  Centralize logs from all services

### Phase 3: Optimization & Scaling (1-2 weeks)
- [ ] **Performance Optimization**
  Optimize infrastructure performance
- [ ] **Auto-scaling Configuration**
  Set up horizontal and vertical scaling
- [ ] **Cost Optimization**
  Implement cost monitoring and optimization
- [ ] **Disaster Recovery**
  Set up backup and recovery procedures

## 📊 Success Criteria
- [ ] All environments running smoothly
- [ ] Automated deployments working (< 5 min deploy time)
- [ ] Monitoring and alerting active (< 1 min response time)
- [ ] 99.9% uptime achieved
- [ ] Infrastructure costs within budget"""


@dataclass
class TestingTemplate(Template):
    """Template for testing projects."""
    testing_type: str = "automation"
    frameworks: List[str] = field(default_factory=list)
    
    def __init__(self, name: str, complexity: TaskComplexity, testing_type: str = "automation", 
                 frameworks: List[str] = None, **kwargs):
        super().__init__(
            name=name,
            category=TaskCategory.TECHNICAL,
            complexity=complexity,
            content="",
            variables=[],
            metadata=kwargs.get('metadata', {})
        )
        self.testing_type = testing_type
        self.frameworks = frameworks or ["Jest", "Cypress", "Selenium"]
        self.content = self._generate_testing_template()
    
    def _generate_testing_template(self) -> str:
        """Generate testing template content with tracker functionality."""
        frameworks_list = "\n".join([f"- {framework}" for framework in self.frameworks])
        
        return f"""# {{{{ project_name | default("Testing Project") }}}}

**Testing Type**: {self.testing_type.replace('_', ' ').title()}
**Testing Frameworks**: 
{frameworks_list}

## 📊 Testing Tracker
**Instructions for LLM**: Update test results, coverage, and progress daily.

### 📈 Test Coverage Dashboard
```
Unit Tests:        [████████████████████] 95% (475/500)
Integration Tests: [████████████████░░░░] 80% (32/40)
E2E Tests:         [████████████░░░░░░░░] 60% (18/30)
Performance Tests: [████████░░░░░░░░░░░░] 40% (4/10)
```

### 🧪 Test Execution Status
| Test Suite | Status | Last Run | Pass Rate |
|------------|--------|----------|-----------|
| Unit Tests | ✅ Passing | 10 min ago | 98% |
| Integration | ✅ Passing | 1 hour ago | 95% |
| E2E Tests | 🟡 Flaky | 2 hours ago | 85% |
| Performance | 🔴 Failing | 1 day ago | 60% |

## 🧪 Testing Implementation

### Phase 1: Test Framework Setup (1 week)
- [ ] **Testing Environment**
  Set up testing environment and dependencies
- [ ] **Test Data Management**
  Create test data fixtures and factories
- [ ] **Test Framework Configuration**
  Configure testing frameworks and tools
- [ ] **Test Reporting**
  Set up test result reporting and dashboards

### Phase 2: Test Development (2-4 weeks)
- [ ] **Unit Testing**
  Write comprehensive unit tests for all components
- [ ] **Integration Testing**
  Test component interactions and APIs
- [ ] **End-to-End Testing**
  Create user journey and workflow tests
- [ ] **Performance Testing**
  Implement load and stress testing

### Phase 3: Test Automation (1-2 weeks)
- [ ] **CI/CD Integration**
  Integrate tests into build pipeline
- [ ] **Automated Test Execution**
  Set up scheduled and triggered test runs
- [ ] **Test Result Analysis**
  Implement automated test result analysis
- [ ] **Quality Gates**
  Configure quality gates for releases

## 📊 Success Criteria
- [ ] Test coverage above 90% for all components
- [ ] All critical user paths covered by E2E tests
- [ ] Automated test execution in CI/CD pipeline
- [ ] Performance benchmarks established and monitored
- [ ] Test execution time under 15 minutes
- [ ] Flaky test rate under 5%"""


class TechnicalTemplateLibrary:
    """Library managing all technical domain templates."""
    
    def __init__(self):
        """Initialize the technical template library."""
        self.templates: Dict[str, Template] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load all default technical templates."""
        # Software development templates
        self.templates["web_development_fullstack"] = SoftwareDevelopmentTemplate(
            name="web_development_fullstack",
            complexity=TaskComplexity.HIGH,
            project_type="web_application",
            tech_stack=["React", "Node.js", "PostgreSQL", "Redis"]
        )
        
        self.templates["mobile_development_react_native"] = SoftwareDevelopmentTemplate(
            name="mobile_development_react_native",
            complexity=TaskComplexity.VERY_HIGH,
            project_type="mobile_application",
            tech_stack=["React Native", "Firebase", "Redux", "TypeScript"]
        )
        
        self.templates["api_development_rest"] = SoftwareDevelopmentTemplate(
            name="api_development_rest",
            complexity=TaskComplexity.MEDIUM,
            project_type="api_service",
            tech_stack=["FastAPI", "Python", "PostgreSQL", "Docker"]
        )
        
        # DevOps templates
        self.templates["devops_cicd_pipeline"] = DevOpsTemplate(
            name="devops_cicd_pipeline",
            complexity=TaskComplexity.HIGH,
            devops_type="cicd_pipeline",
            tools=["GitHub Actions", "Docker", "AWS", "Terraform"]
        )
        
        self.templates["devops_infrastructure"] = DevOpsTemplate(
            name="devops_infrastructure",
            complexity=TaskComplexity.VERY_HIGH,
            devops_type="infrastructure",
            tools=["Terraform", "Kubernetes", "AWS", "Prometheus"]
        )
        
        # Testing templates
        self.templates["testing_automation"] = TestingTemplate(
            name="testing_automation",
            complexity=TaskComplexity.MEDIUM,
            testing_type="automation",
            frameworks=["Jest", "Cypress", "Selenium", "TestCafe"]
        )
        
        self.templates["testing_performance"] = TestingTemplate(
            name="testing_performance",
            complexity=TaskComplexity.HIGH,
            testing_type="performance",
            frameworks=["JMeter", "K6", "Artillery", "Locust"]
        )
    
    def get_template(self, template_type: TechnicalTemplateType, 
                    complexity: TaskComplexity) -> Optional[Template]:
        """Get template by type and complexity."""
        for template in self.templates.values():
            if (template_type == TechnicalTemplateType.SOFTWARE_DEVELOPMENT and 
                isinstance(template, SoftwareDevelopmentTemplate) and
                template.complexity == complexity):
                return template
            elif (template_type == TechnicalTemplateType.DEVOPS and 
                  isinstance(template, DevOpsTemplate) and
                  template.complexity == complexity):
                return template
            elif (template_type == TechnicalTemplateType.TESTING and 
                  isinstance(template, TestingTemplate) and
                  template.complexity == complexity):
                return template
        
        # Return first match if exact complexity not found
        for template in self.templates.values():
            if (template_type == TechnicalTemplateType.SOFTWARE_DEVELOPMENT and 
                isinstance(template, SoftwareDevelopmentTemplate)):
                return template
            elif (template_type == TechnicalTemplateType.DEVOPS and 
                  isinstance(template, DevOpsTemplate)):
                return template
            elif (template_type == TechnicalTemplateType.TESTING and 
                  isinstance(template, TestingTemplate)):
                return template
        
        return None
    
    def get_templates_by_type(self, template_type: TechnicalTemplateType) -> List[Template]:
        """Get all templates of a specific type."""
        result = []
        for template in self.templates.values():
            if (template_type == TechnicalTemplateType.SOFTWARE_DEVELOPMENT and 
                isinstance(template, SoftwareDevelopmentTemplate)):
                result.append(template)
            elif (template_type == TechnicalTemplateType.DEVOPS and 
                  isinstance(template, DevOpsTemplate)):
                result.append(template)
            elif (template_type == TechnicalTemplateType.TESTING and 
                  isinstance(template, TestingTemplate)):
                result.append(template)
        return result
