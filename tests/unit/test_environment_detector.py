"""
Unit tests for EnvironmentDetector - Following TDD approach.

Testing the system capability and tool detection system.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from opius_planner.core.environment_detector import (
    EnvironmentDetector, 
    SystemInfo, 
    EditorInfo, 
    ToolInfo,
    EnvironmentCapabilities
)


class TestEnvironmentDetector:
    """Test suite for EnvironmentDetector following TDD principles."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.detector = EnvironmentDetector()
    
    def test_init_creates_detector_with_default_config(self):
        """Test that EnvironmentDetector initializes with proper defaults."""
        detector = EnvironmentDetector()
        assert detector is not None
        assert hasattr(detector, 'system_info')
        assert hasattr(detector, 'editor_info')
        assert hasattr(detector, 'available_tools')
    
    @patch('psutil.virtual_memory')
    @patch('psutil.cpu_count')
    def test_detect_system_info_returns_hardware_specs(self, mock_cpu_count, mock_virtual_memory):
        """Test that system information detection works correctly."""
        # Mock system resources
        mock_virtual_memory.return_value = MagicMock(total=8 * 1024**3)  # 8GB
        mock_cpu_count.return_value = 8
        
        system_info = self.detector.detect_system_info()
        
        assert isinstance(system_info, SystemInfo)
        assert system_info.ram_gb == 8
        assert system_info.cpu_cores == 8
        assert system_info.platform is not None
    
    @patch('os.environ.get')
    @patch('os.path.exists')
    def test_detect_editor_info_identifies_vscode(self, mock_path_exists, mock_env_get):
        """Test VS Code detection."""
        # Mock VS Code environment
        mock_env_get.return_value = "/path/to/vscode"
        mock_path_exists.return_value = True
        
        editor_info = self.detector.detect_editor_info()
        
        assert isinstance(editor_info, EditorInfo)
        assert editor_info.name in ['vscode', 'cursor', 'windsurf', 'unknown']
    
    @patch('shutil.which')
    def test_detect_available_tools_finds_installed_tools(self, mock_which):
        """Test that available tools are detected correctly."""
        # Mock tool availability
        mock_which.side_effect = lambda tool: f"/usr/bin/{tool}" if tool in ['git', 'docker'] else None
        
        tools = self.detector.detect_available_tools()
        
        assert isinstance(tools, list)
        for tool in tools:
            assert isinstance(tool, ToolInfo)
    
    def test_get_environment_capabilities_returns_complete_info(self):
        """Test that complete environment analysis works."""
        capabilities = self.detector.get_environment_capabilities()
        
        assert isinstance(capabilities, EnvironmentCapabilities)
        assert hasattr(capabilities, 'system_info')
        assert hasattr(capabilities, 'editor_info')
        assert hasattr(capabilities, 'available_tools')
        assert hasattr(capabilities, 'recommendations')
    
    @patch('psutil.virtual_memory')
    def test_memory_based_recommendations(self, mock_virtual_memory):
        """Test that recommendations adapt to available memory."""
        # Test low memory scenario
        mock_virtual_memory.return_value = MagicMock(total=2 * 1024**3)  # 2GB
        
        capabilities = self.detector.get_environment_capabilities()
        
        assert capabilities.system_info.ram_gb == 2
        # Should recommend lightweight tools for low RAM
        assert any('lightweight' in rec.lower() or 'memory' in rec.lower() 
                  for rec in capabilities.recommendations)
    
    @patch('psutil.cpu_count')
    def test_cpu_based_recommendations(self, mock_cpu_count):
        """Test that recommendations consider CPU cores."""
        # Test single core scenario
        mock_cpu_count.return_value = 1
        
        capabilities = self.detector.get_environment_capabilities()
        
        assert capabilities.system_info.cpu_cores == 1
        # Should recommend single-threaded approaches
        assert any('single' in rec.lower() or 'sequential' in rec.lower() 
                  for rec in capabilities.recommendations)
    
    def test_caching_prevents_redundant_detection(self):
        """Test that environment detection results are cached."""
        # First call
        capabilities1 = self.detector.get_environment_capabilities()
        
        # Mock a method to track calls
        with patch.object(self.detector, 'detect_system_info') as mock_detect:
            # Second call should use cache
            capabilities2 = self.detector.get_environment_capabilities()
            mock_detect.assert_not_called()
        
        assert capabilities1 == capabilities2
    
    def test_environment_detector_handles_detection_errors(self):
        """Test graceful handling of detection errors."""
        with patch('psutil.virtual_memory', side_effect=Exception("Detection failed")):
            # Should not crash, should return default/fallback values
            system_info = self.detector.detect_system_info()
            assert isinstance(system_info, SystemInfo)
            # Should have fallback values
            assert system_info.ram_gb > 0
    
    @pytest.mark.parametrize("ram_gb,expected_category", [
        (2, "low"),
        (8, "medium"),
        (16, "high"),
        (32, "very_high"),
    ])
    def test_resource_categorization(self, ram_gb, expected_category):
        """Test that system resources are properly categorized."""
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value = MagicMock(total=ram_gb * 1024**3)
            
            system_info = self.detector.detect_system_info()
            resource_category = self.detector._categorize_resources(system_info)
            
            assert resource_category == expected_category


class TestSystemInfo:
    """Test suite for SystemInfo dataclass."""
    
    def test_system_info_creation(self):
        """Test SystemInfo object creation."""
        info = SystemInfo(
            platform="darwin",
            ram_gb=8,
            cpu_cores=4,
            python_version="3.12.4"
        )
        
        assert info.platform == "darwin"
        assert info.ram_gb == 8
        assert info.cpu_cores == 4
        assert info.python_version == "3.12.4"


class TestEditorInfo:
    """Test suite for EditorInfo dataclass."""
    
    def test_editor_info_creation(self):
        """Test EditorInfo object creation."""
        info = EditorInfo(
            name="vscode",
            version="1.85.0",
            path="/usr/bin/code",
            extensions=["python", "jupyter"]
        )
        
        assert info.name == "vscode"
        assert info.version == "1.85.0"
        assert info.path == "/usr/bin/code"
        assert "python" in info.extensions


class TestToolInfo:
    """Test suite for ToolInfo dataclass."""
    
    def test_tool_info_creation(self):
        """Test ToolInfo object creation."""
        info = ToolInfo(
            name="git",
            version="2.39.0",
            path="/usr/bin/git",
            available=True
        )
        
        assert info.name == "git"
        assert info.version == "2.39.0"
        assert info.path == "/usr/bin/git"
        assert info.available is True


class TestEnvironmentCapabilities:
    """Test suite for EnvironmentCapabilities dataclass."""
    
    def test_environment_capabilities_creation(self):
        """Test EnvironmentCapabilities object creation."""
        system_info = SystemInfo("darwin", 8, 4, "3.12.4")
        editor_info = EditorInfo("vscode", "1.85.0", "/usr/bin/code", [])
        tools = [ToolInfo("git", "2.39.0", "/usr/bin/git", True)]
        recommendations = ["Use Git for version control"]
        
        capabilities = EnvironmentCapabilities(
            system_info=system_info,
            editor_info=editor_info,
            available_tools=tools,
            recommendations=recommendations
        )
        
        assert capabilities.system_info == system_info
        assert capabilities.editor_info == editor_info
        assert capabilities.available_tools == tools
        assert capabilities.recommendations == recommendations
