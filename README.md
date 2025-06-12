# 🎯 Opius Planner Agent

> **Universal Planning Agent** - Create detailed execution plans for ANY type of task or project

A revolutionary planning agent by **Opius AI** that can generate structured, actionable plans for everything from "write a novel" to "build a React app" to "plan a wedding". Features environment-aware personalization and agentic-ready markdown output.

## ✨ Key Features

- **🌍 Universal Planning**: Handles creative, technical, business, personal, and educational tasks
- **🔧 Environment Aware**: Automatically detects your system capabilities and personalizes recommendations
- **🤖 Agentic Ready**: Generates markdown plans optimized for AI editors and automation systems
- **👥 User Friendly**: Works for complete beginners and experts alike
- **📊 Test Driven**: Built with comprehensive test coverage following TDD principles

## 🚀 Quick Start

```bash
# Install the package
pip install opius-planner-agent

# Generate a plan
opius-planner "Build a Python web application with user authentication"

# Interactive mode
opius-planner --interactive
```

## 📋 Example Use Cases

- **Creative**: "Write a science fiction novel", "Create a photography portfolio"
- **Technical**: "Build a React app with Firebase", "Set up CI/CD pipeline"
- **Business**: "Launch a SaaS product", "Create Q4 marketing strategy"
- **Personal**: "Plan a wedding", "Organize home renovation"
- **Educational**: "Learn machine learning", "Master Python programming"

## 🔧 Development Status

This project is currently in **Phase 1: Core Foundation** development.

- ✅ Project structure setup
- 🟡 Task analysis engine (TDD in progress)
- ⏳ Environment detection system
- ⏳ Template engine
- ⏳ CLI interface

## 🧪 Testing

We follow Test-Driven Development (TDD) principles:

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/opius_planner --cov-report=html
```

## 📚 Documentation

Detailed documentation is available in the `.scaffolding/` directory:

- [Implementation Plan](.scaffolding/IMPLEMENTATION_PLAN.md)
- [Implementation Tracker](.scaffolding/IMPLEMENTATION_TRACKER.md)

## 🤝 Contributing

This project follows TDD principles. When contributing:

1. Write tests first (Red)
2. Write minimal code to pass tests (Green)  
3. Refactor and improve (Refactor)
4. Update the implementation tracker

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🏢 About Opius AI

Created by Opius AI - Building the future of intelligent automation and planning.

---

**Status**: 🟡 Alpha Development | **Version**: 0.1.0 | **Test Coverage**: Target 90%+

# Opius Planner Agent 🚀

[![Tests](https://img.shields.io/badge/tests-131%20passing-brightgreen)](https://github.com/opius-planner/opius_planner_agent_alpha)
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/opius-planner/opius_planner_agent_alpha)
[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**The world's first universal planning agent** - Transform any task or project into a comprehensive, actionable plan using advanced AI-powered analysis and environment-adaptive recommendations.

## ✨ Key Features

- 🧠 **Universal Task Analysis** - Automatically categorizes and analyzes tasks across domains (Technical, Creative, Business, Personal, Educational)
- 🌍 **Environment-Adaptive Planning** - Detects your system capabilities and adapts plans accordingly
- 📝 **Agentic-Friendly Output** - Generates markdown plans optimized for AI agent processing
- 🎨 **Template-Based Customization** - Jinja2-powered templates for different project types
- 💻 **Interactive CLI** - Full command-line interface with interactive mode
- 🔧 **Extensible Architecture** - Built for easy extension and customization

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/opius_planner_agent_alpha.git
cd opius_planner_agent_alpha

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Basic Usage

#### Command Line Interface

```bash
# Generate a plan for any task
opius-planner generate "Build a Python web application with authentication"

# Save plan to file
opius-planner generate "Create a marketing strategy" --output marketing_plan.md

# Use interactive mode
opius-planner interactive

# Generate with specific options
opius-planner generate "Learn machine learning" \
  --complexity high \
  --format yaml-frontmatter \
  --agentic

# List available templates
opius-planner list-templates

# Validate an existing plan
opius-planner validate my_plan.md
```

#### Python API

```python
from opius_planner import PlannerAgent

# Create planner instance
agent = PlannerAgent()

# Generate a comprehensive plan
plan = agent.generate_plan(
    task_description="Build a React dashboard with real-time data",
    agentic=True
)

print(plan)
```

## 📋 Example Output

```markdown
# Python Web Application Development Plan

**Category**: Technical
**Complexity**: Medium
**Duration**: 2-3 weeks

## 🚀 Implementation Steps

- [ ] **Setup Development Environment** (2 hours)
  Configure Python, Flask, and development tools

- [ ] **Design Application Structure** (4 hours)  
  Plan the application architecture and database schema

- [ ] **Implement Authentication System** (1 week)
  Build user registration, login, and session management

- [ ] **Develop Core Features** (1 week)
  Build main application functionality

- [ ] **Testing & Deployment** (2 days)
  Write tests and deploy to production

## 📊 Success Criteria
- [ ] User authentication working
- [ ] Core features implemented
- [ ] Tests passing
- [ ] Successfully deployed
```

## 🏗️ Architecture

The Opius Planner Agent is built with a modular architecture following TDD principles:

### Core Components

- **TaskAnalyzer** - Analyzes and categorizes tasks across domains
- **EnvironmentDetector** - Detects system capabilities and available tools
- **PlanGenerator** - Creates adaptive execution plans
- **TemplateEngine** - Manages Jinja2-based template system
- **MarkdownGenerator** - Produces agentic-friendly markdown output
- **CLI Interface** - Click-based command-line interface

### Component Interaction Flow

```
Task Input → TaskAnalyzer → EnvironmentDetector → PlanGenerator → TemplateEngine → MarkdownGenerator → Output
```

## 🧪 Testing

We maintain **strict TDD practices** with comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/opius_planner --cov-report=html

# Run specific test suites
pytest tests/unit/test_task_analyzer.py
pytest tests/integration/test_end_to_end.py
```

### Test Statistics
- **Unit Tests**: 125 tests passing
- **Integration Tests**: 6 tests passing
- **Total Coverage**: 80%+
- **Components Covered**: All 6 core components

## 📚 Advanced Usage

### Custom Templates

Create custom templates for specific project types:

```python
from opius_planner.templates import TemplateEngine, Template
from opius_planner.core import TaskCategory, TaskComplexity

# Create custom template
custom_template = Template(
    name="my_custom_template",
    category=TaskCategory.TECHNICAL,
    complexity=TaskComplexity.MEDIUM,
    content="""# {{ project_name }}

## Overview
{{ task_description }}

## Custom Steps
{% for step in custom_steps %}
- [ ] {{ step }}
{% endfor %}
""",
    variables=["project_name", "task_description", "custom_steps"]
)

# Register template
engine = TemplateEngine()
engine.register_template(custom_template)
```

### Environment Configuration

Configure environment-specific settings:

```yaml
# config.yaml
planner:
  default_complexity: medium
  agentic_mode: true
  template_preferences:
    technical: "technical_detailed"
    creative: "creative_structured"
  
environment:
  detect_editors: true
  detect_tools: true
  cache_duration: 3600
```

### Agentic Integration

The output is optimized for AI agent processing:

```markdown
<!-- AGENTIC_METADATA:
task_type: technical
complexity: medium
estimated_hours: 40
tools_required: [Python, Git, VS Code]
-->

<!-- STEPS_START -->
- [ ] Setup Development Environment
- [ ] Implement Core Features
- [ ] Testing and Deployment
<!-- STEPS_END -->
```

## 🛠️ Development

### Project Structure

```
opius_planner_agent_alpha/
├── src/opius_planner/          # Main package
│   ├── core/                   # Core analysis components
│   ├── templates/              # Template engine
│   ├── cli/                    # Command-line interface
│   └── utils/                  # Utility functions
├── tests/                      # Test suites
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── .scaffolding/               # Project documentation
└── pyproject.toml             # Package configuration
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests following TDD practices
4. Implement your feature
5. Ensure all tests pass (`pytest`)
6. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run pre-commit hooks
pre-commit install

# Run full test suite
pytest --cov=src/opius_planner
```

## 🔮 Roadmap

### Phase 2: Advanced Features
- [ ] Multi-agent collaboration
- [ ] Real-time plan updates
- [ ] Integration with external tools
- [ ] Advanced analytics and metrics
- [ ] Plugin system
- [ ] Web interface

### Phase 3: Enterprise Features
- [ ] Team collaboration
- [ ] Advanced templates
- [ ] API integrations
- [ ] Performance optimization
- [ ] Advanced security features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Built with love using Test-Driven Development
- Powered by modern Python ecosystem
- Inspired by the need for universal planning solutions

## 📞 Support

- 📧 Email: support@opiusai.com
- 💬 Discord: [Join our community](https://discord.gg/opius-planner)
- 📖 Documentation: [Full docs](https://docs.opiusai.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/opius_planner_agent_alpha/issues)

---

**Made with ❤️ by the Opius AI Team**

*Transform your ideas into actionable plans - universally, intelligently, efficiently.*
