# 🏗️ Architecture & Technical Design

Welcome to the Opius Planner Agent architecture documentation. This document explains how the system works and how to extend it.

## 🎯 **Core Concepts**

The Opius Planner Agent is built around **environment-aware planning** - it automatically detects your system capabilities and adapts plans accordingly.

### **Key Components**

1. **Task Analyzer** - Categorizes any task (technical, creative, business, personal)
2. **Environment Detector** - Detects your RAM, CPU, editors, and AI tools
3. **Plan Generator** - Creates adaptive execution plans
4. **Template Engine** - Manages customizable templates (Jinja2-based)
5. **CLI Interface** - Click-based command-line interface

## 🧠 **How Environment Awareness Works**

The system automatically detects and adapts to:

### **Hardware Resources**
- **RAM**: Low RAM → lighter tools (Vite vs Webpack)
- **CPU**: More cores → parallel processing recommendations
- **Storage**: Available space affects cache and build strategies

### **Editor Integration** 
- **VS Code**: Extension recommendations and workspace settings
- **Cursor**: AI-enhanced planning with Composer integration
- **Windsurf**: Agent-aware task breakdown

### **AI Tools Available**
- **GPT-4 + MCP Servers**: Full AI-assisted implementation
- **Basic LLM**: Balanced AI/manual approach  
- **No AI**: Detailed manual step-by-step guidance

## 📝 **Template System**

Templates are the core of plan generation:

```python
# Example: Technical Template Structure
class SoftwareDevelopmentTemplate(Template):
    def generate_plan(self, context):
        return f"""
        # {context.project_name}
        
        ## Environment-Specific Recommendations
        {self.get_tech_stack(context.environment)}
        
        ## Implementation Steps
        {self.get_steps(context.complexity)}
        """
```

### **Template Categories**
- **Technical**: Software development, DevOps, testing
- **Creative**: Writing, design, content creation
- **Business**: Marketing, operations, strategy
- **Personal**: Events, learning, lifestyle

## 🚀 **Example Adaptations**

### **Same Input, Different Outputs**

**Task**: "Build a React portfolio website"

**4GB RAM User Gets**:
```markdown
## Recommended Stack
- **Bundler**: Vite (lightweight)
- **Package Manager**: pnpm (memory efficient)
- **Development**: Hot reload with memory limits
```

**32GB RAM User Gets**:
```markdown
## Recommended Stack  
- **Bundler**: Webpack with parallel processing
- **Package Manager**: Yarn v3 with zero-installs
- **Development**: Multiple dev servers
```

**User with Cursor + GPT-4 Gets**:
```markdown
## AI-Enhanced Approach
- **Code Generation**: Use Cursor Composer for components
- **Styling**: AI-generated CSS with design systems
- **Testing**: AI-generated test suites
```

## 🛠️ **Contributing to Templates**

### **Adding New Templates**

1. **Create Template Class**:
```python
from ..core.template_engine import Template

class MyCustomTemplate(Template):
    def __init__(self, name, complexity):
        super().__init__(name, TaskCategory.CUSTOM, complexity)
    
    def generate_content(self, context):
        return "Your template content here"
```

2. **Register Template**:
```python
# In template library
self.templates["my_custom"] = MyCustomTemplate(
    name="my_custom",
    complexity=TaskComplexity.MEDIUM
)
```

3. **Test Template**:
```bash
opius-planner generate-plan "test my custom template" --verbose
```

### **Template Variables**

Templates use Jinja2 syntax:
- `{{ project_name }}` - Extracted from task description
- `{{ complexity }}` - Task complexity level
- `{{ tech_stack }}` - Environment-appropriate technologies
- `{% if condition %}` - Conditional content
- `{% for item in list %}` - Loops

## 🔧 **Environment Detection Details**

### **System Capabilities**
```python
{
    "ram_total": 16_000_000_000,  # 16GB
    "cpu_cores": 8,
    "editor": "cursor",
    "ai_tools": ["gpt-4", "github-copilot"],
    "languages": ["python", "javascript", "typescript"]
}
```

### **Editor-Specific Features**
- **VS Code**: Extension recommendations, debug configs
- **Cursor**: AI integration, Composer features
- **Terminal**: CLI-focused recommendations

## 📊 **Plan Enhancement System**

Plans are enhanced with:
- **Technology Stack Consistency**: No conflicting recommendations
- **Risk Assessment**: Potential issues and mitigation
- **Quality Gates**: Testing and review checkpoints
- **Implementation Guidance**: Step-by-step coding instructions

## 🧪 **Testing Architecture**

- **Unit Tests**: 125+ tests covering all components
- **Integration Tests**: End-to-end workflows
- **Template Tests**: Template generation and rendering
- **CLI Tests**: Command-line interface functionality

## 📈 **Performance Considerations**

- **Template Caching**: Frequently used templates are cached
- **Environment Caching**: System detection cached for 1 hour
- **Lazy Loading**: Templates loaded on-demand
- **Memory Efficiency**: Optimized for low-RAM systems

## 🔍 **Debugging & Troubleshooting**

### **Common Issues**
1. **Template Not Found**: Check template registration
2. **Environment Detection Fails**: Run with `--verbose` flag
3. **Plan Generation Errors**: Verify task description format

### **Debug Commands**
```bash
# Verbose output
opius-planner generate-plan "task" --verbose

# List available templates  
opius-planner list-templates

# Validate plan
opius-planner validate plan.md
```

## 🌟 **Future Architecture Plans**

- **Plugin System**: External template plugins
- **API Server**: REST API for plan generation
- **Web Interface**: Browser-based planning
- **Team Collaboration**: Shared templates and plans
- **Advanced AI**: Direct LLM API integration