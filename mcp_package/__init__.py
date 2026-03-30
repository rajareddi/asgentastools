"""
MCP (Model Context Protocol) Package
Complete MCP integration for agent service

This package consolidates all MCP-related functionality:
- Core: MCPServerManager, MCPServer
- Config: MCPConfiguration, MCPInstaller, MCPCapabilities
- Tools: MCPToolAdapter
- Agent: MCP-integrated agent
"""

__version__ = "1.0.0"
__author__ = "Agent Development Team"

# Core components
from mcp_package.core import (
    MCPServer,
    MCPServerManager,
    mcp_manager
)

# Configuration
from mcp_package.config import (
    MCP_SERVERS,
    MCPConfiguration,
    MCPInstaller,
    MCPCapabilities
)

# Tools
from mcp_package.tools import (
    MCPToolAdapter,
    mcp_tool_adapter
)

# Agent
try:
    from mcp_package.agent import mcp_agent, mcp_agent_available
except ImportError:
    mcp_agent = None
    mcp_agent_available = False

__all__ = [
    # Version
    '__version__',
    
    # Core
    'MCPServer',
    'MCPServerManager',
    'mcp_manager',
    
    # Configuration
    'MCP_SERVERS',
    'MCPConfiguration',
    'MCPInstaller',
    'MCPCapabilities',
    
    # Tools
    'MCPToolAdapter',
    'mcp_tool_adapter',
    
    # Agent
    'mcp_agent',
    'mcp_agent_available'
]

