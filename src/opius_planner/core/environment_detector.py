"""
EnvironmentDetector - System capability and tool detection system.

This module provides intelligent environment analysis capabilities including:
- Hardware resource detection (RAM, CPU, storage)
- Editor detection (VS Code, Cursor, Windsurf)
- Available tool detection (Git, Docker, etc.)
- Resource-aware recommendations
"""

import os
import sys
import platform
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from functools import lru_cache
import psutil


@dataclass
class SystemInfo:
    """System hardware and software information."""
    platform: str
    ram_gb: int
    cpu_cores: int
    python_version: str
    storage_gb: Optional[int] = None
    architecture: Optional[str] = None


@dataclass
class EditorInfo:
    """Information about the detected code editor."""
    name: str
    version: Optional[str] = None
    path: Optional[str] = None
    extensions: List[str] = None
    
    def __post_init__(self):
        if self.extensions is None:
            self.extensions = []


@dataclass
class ToolInfo:
    """Information about an available development tool."""
    name: str
    version: Optional[str] = None
    path: Optional[str] = None
    available: bool = False


@dataclass
class EnvironmentCapabilities:
    """Complete environment analysis results."""
    system_info: SystemInfo
    editor_info: EditorInfo
    available_tools: List[ToolInfo]
    recommendations: List[str]


class EnvironmentDetector:
    """System environment detection and analysis engine."""
    
    def __init__(self):
        """Initialize the EnvironmentDetector."""
        self.system_info = None
        self.editor_info = None
        self.available_tools = None
        self._capabilities_cache = None
        
        # Define tools to detect
        self.detectable_tools = [
            'git', 'docker', 'node', 'npm', 'yarn', 'pip', 'pipenv',
            'conda', 'pytest', 'black', 'flake8', 'mypy', 'jupyter',
            'code', 'cursor', 'windsurf'
        ]
        
        # Define editor detection patterns
        self.editor_patterns = {
            'vscode': ['code', 'visual studio code', 'vscode'],
            'cursor': ['cursor'],
            'windsurf': ['windsurf'],
            'pycharm': ['pycharm'],
            'vim': ['vim', 'nvim'],
            'emacs': ['emacs']
        }
    
    @lru_cache(maxsize=1)
    def detect_system_info(self) -> SystemInfo:
        """Detect system hardware and software information."""
        try:
            # Get memory info
            memory = psutil.virtual_memory()
            ram_gb = int(memory.total / (1024**3))
            
            # Get CPU info
            cpu_cores = psutil.cpu_count(logical=True) or 1
            
            # Get platform info
            platform_name = platform.system().lower()
            
            # Get Python version
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            
            # Get architecture
            architecture = platform.machine()
            
            # Get storage info (optional)
            storage_gb = None
            try:
                disk_usage = psutil.disk_usage('/')
                storage_gb = int(disk_usage.total / (1024**3))
            except Exception:
                pass  # Storage detection is optional
            
            return SystemInfo(
                platform=platform_name,
                ram_gb=ram_gb,
                cpu_cores=cpu_cores,
                python_version=python_version,
                storage_gb=storage_gb,
                architecture=architecture
            )
            
        except Exception as e:
            # Fallback to reasonable defaults if detection fails
            return SystemInfo(
                platform=platform.system().lower(),
                ram_gb=8,  # Reasonable default
                cpu_cores=4,  # Reasonable default
                python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            )
    
    @lru_cache(maxsize=1)
    def detect_editor_info(self) -> EditorInfo:
        """Detect the current code editor being used."""
        try:
            # Check environment variables first
            editor_from_env = self._detect_editor_from_environment()
            if editor_from_env:
                return editor_from_env
            
            # Check running processes
            editor_from_process = self._detect_editor_from_processes()
            if editor_from_process:
                return editor_from_process
            
            # Check installed editors
            editor_from_installation = self._detect_editor_from_installation()
            if editor_from_installation:
                return editor_from_installation
            
            # Default fallback
            return EditorInfo(name="unknown")
            
        except Exception:
            return EditorInfo(name="unknown")
    
    def _detect_editor_from_environment(self) -> Optional[EditorInfo]:
        """Detect editor from environment variables."""
        # Check common editor environment variables
        env_vars = ['EDITOR', 'VISUAL', 'VSCODE_PID', 'CURSOR_PID']
        
        for env_var in env_vars:
            value = os.environ.get(env_var)
            if value:
                for editor_name, patterns in self.editor_patterns.items():
                    if any(pattern in value.lower() for pattern in patterns):
                        return EditorInfo(
                            name=editor_name,
                            path=value if os.path.exists(value) else None
                        )
        
        return None
    
    def _detect_editor_from_processes(self) -> Optional[EditorInfo]:
        """Detect editor from running processes."""
        try:
            for process in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    process_name = process.info['name'].lower()
                    for editor_name, patterns in self.editor_patterns.items():
                        if any(pattern in process_name for pattern in patterns):
                            return EditorInfo(
                                name=editor_name,
                                path=process.info.get('exe')
                            )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass
        
        return None
    
    def _detect_editor_from_installation(self) -> Optional[EditorInfo]:
        """Detect editor from installed applications."""
        # Check for common editor executables
        editor_executables = {
            'vscode': ['code'],
            'cursor': ['cursor'],
            'windsurf': ['windsurf'],
            'pycharm': ['pycharm'],
            'vim': ['vim', 'nvim'],
            'emacs': ['emacs']
        }
        
        for editor_name, executables in editor_executables.items():
            for executable in executables:
                path = shutil.which(executable)
                if path:
                    version = self._get_tool_version(executable)
                    return EditorInfo(
                        name=editor_name,
                        version=version,
                        path=path
                    )
        
        return None
    
    @lru_cache(maxsize=1)
    def detect_available_tools(self) -> List[ToolInfo]:
        """Detect available development tools."""
        tools = []
        
        for tool_name in self.detectable_tools:
            tool_path = shutil.which(tool_name)
            if tool_path:
                version = self._get_tool_version(tool_name)
                tools.append(ToolInfo(
                    name=tool_name,
                    version=version,
                    path=tool_path,
                    available=True
                ))
            else:
                tools.append(ToolInfo(
                    name=tool_name,
                    available=False
                ))
        
        return tools
    
    def _get_tool_version(self, tool_name: str) -> Optional[str]:
        """Get version information for a tool."""
        version_commands = {
            'git': ['--version'],
            'docker': ['--version'],
            'node': ['--version'],
            'npm': ['--version'],
            'python': ['--version'],
            'pip': ['--version'],
            'pytest': ['--version'],
            'code': ['--version'],
            'cursor': ['--version'],
            'windsurf': ['--version']
        }
        
        try:
            cmd_args = version_commands.get(tool_name, ['--version'])
            result = subprocess.run(
                [tool_name] + cmd_args,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Extract version from output (simple approach)
                output = result.stdout.strip()
                return output.split('\n')[0] if output else None
                
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return None
    
    def get_environment_capabilities(self) -> EnvironmentCapabilities:
        """Get complete environment analysis with recommendations."""
        if self._capabilities_cache is not None:
            return self._capabilities_cache
        
        # Detect all components
        system_info = self.detect_system_info()
        editor_info = self.detect_editor_info()
        available_tools = self.detect_available_tools()
        
        # Generate recommendations
        recommendations = self._generate_recommendations(system_info, editor_info, available_tools)
        
        # Create and cache result
        self._capabilities_cache = EnvironmentCapabilities(
            system_info=system_info,
            editor_info=editor_info,
            available_tools=available_tools,
            recommendations=recommendations
        )
        
        return self._capabilities_cache
    
    def _generate_recommendations(self, system_info: SystemInfo, editor_info: EditorInfo, available_tools: List[ToolInfo]) -> List[str]:
        """Generate environment-specific recommendations."""
        recommendations = []
        
        # Memory-based recommendations
        if system_info.ram_gb <= 4:
            recommendations.append("Consider using lightweight development tools due to limited memory")
            recommendations.append("Use memory-efficient IDEs and close unnecessary applications")
        elif system_info.ram_gb >= 16:
            recommendations.append("Your system has ample memory for resource-intensive development tools")
            recommendations.append("Consider using IDEs with advanced features like IntelliJ or VS Code with extensions")
        
        # CPU-based recommendations
        if system_info.cpu_cores == 1:
            recommendations.append("Use single-threaded build processes to avoid overwhelming your CPU")
            recommendations.append("Consider sequential rather than parallel processing approaches")
        elif system_info.cpu_cores >= 8:
            recommendations.append("Take advantage of parallel processing and multi-threaded builds")
            recommendations.append("Consider using parallel testing and build tools")
        
        # Tool-specific recommendations
        available_tool_names = {tool.name for tool in available_tools if tool.available}
        
        if 'git' not in available_tool_names:
            recommendations.append("Install Git for version control - essential for most development projects")
        
        if 'docker' in available_tool_names:
            recommendations.append("Docker is available - consider containerized development environments")
        
        if 'pytest' in available_tool_names:
            recommendations.append("PyTest is available - great for test-driven development")
        
        # Editor-specific recommendations
        if editor_info.name == "vscode":
            recommendations.append("VS Code detected - consider installing Python and testing extensions")
        elif editor_info.name == "cursor":
            recommendations.append("Cursor detected - excellent choice for AI-assisted development")
        elif editor_info.name == "unknown":
            recommendations.append("Consider installing a modern code editor like VS Code or Cursor")
        
        return recommendations
    
    def _categorize_resources(self, system_info: SystemInfo) -> str:
        """Categorize system resources for planning purposes."""
        # Simple categorization based on RAM (can be expanded)
        if system_info.ram_gb <= 4:
            return "low"
        elif system_info.ram_gb <= 8:
            return "medium"
        elif system_info.ram_gb <= 16:
            return "high"
        else:
            return "very_high"
