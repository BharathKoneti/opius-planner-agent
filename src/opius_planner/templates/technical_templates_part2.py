"""
Technical Templates Library - Part 2: DevOps and Testing Templates
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from ..core.task_analyzer import TaskCategory, TaskComplexity
from .template_engine import Template, TemplateContext


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

## 🔧 DevOps Implementation

### Phase 1: Infrastructure Setup
- [ ] **Cloud Environment**
  Set up cloud infrastructure
- [ ] **CI/CD Pipeline**
  Configure automated deployment pipeline
- [ ] **Monitoring**
  Implement comprehensive monitoring

## 📈 Success Criteria
- [ ] All environments running smoothly
- [ ] Automated deployments working
- [ ] Monitoring and alerting active"""


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
**Frameworks**: 
{frameworks_list}

## 📊 Testing Tracker
**Instructions for LLM**: Update test results, coverage, and progress daily.

### 📈 Test Coverage
```
Unit Tests:        [████████████████████] 95%
Integration Tests: [████████████████░░░░] 80%
E2E Tests:         [████████████░░░░░░░░] 60%
```

## 🧪 Testing Implementation

### Phase 1: Test Setup
- [ ] **Test Framework Setup**
  Configure testing frameworks and tools
- [ ] **Test Data Management**
  Set up test data and fixtures
- [ ] **Automated Testing**
  Implement automated test execution

## 📊 Success Criteria
- [ ] Test coverage above 90%
- [ ] All critical paths covered
- [ ] Automated test execution working"""
