"""
MCP Package Module
Standalone MCP integration package for agent service
"""

import os
import sys
from typing import Dict, List, Any

# MCP Server Types
MCP_SERVERS = {
    "filesystem": {
        "description": "File system access and manipulation",
        "package": "mcp-server-filesystem",
        "tools": ["read_file", "write_file", "list_files", "create_dir"]
    },
    "git": {
        "description": "Git repository operations",
        "package": "mcp-server-git",
        "tools": ["clone_repo", "commit", "push", "pull", "branch"]
    },
    "web": {
        "description": "Web scraping and HTTP operations",
        "package": "mcp-server-web",
        "tools": ["fetch_url", "parse_html", "post_request", "headers"]
    },
    "sql": {
        "description": "SQL database operations",
        "package": "mcp-server-sql",
        "tools": ["query", "insert", "update", "delete", "schema"]
    },
    "memory": {
        "description": "In-memory data storage",
        "package": "mcp-server-memory",
        "tools": ["store", "retrieve", "delete", "list_keys"]
    },
    "slack": {
        "description": "Slack messaging operations",
        "package": "mcp-server-slack",
        "tools": ["send_message", "get_channels", "get_users"]
    },
    "weather": {
        "description": "Weather information",
        "package": "mcp-server-weather",
        "tools": ["get_weather", "forecast", "alerts"]
    }
}


class MCPConfiguration:
    """MCP Configuration manager"""
    
    def __init__(self):
        self.enabled_servers: List[str] = []
        self.server_configs: Dict[str, Dict] = {}
    
    def enable_server(self, server_type: str, **config):
        """Enable an MCP server"""
        if server_type not in MCP_SERVERS:
            raise ValueError(f"Unknown MCP server: {server_type}")
        
        self.enabled_servers.append(server_type)
        self.server_configs[server_type] = config
        return self
    
    def enable_all_servers(self):
        """Enable all available MCP servers"""
        self.enabled_servers = list(MCP_SERVERS.keys())
        return self
    
    def get_enabled_servers(self) -> Dict[str, Dict]:
        """Get configuration for enabled servers"""
        return {
            server: {
                **MCP_SERVERS[server],
                **self.server_configs.get(server, {})
            }
            for server in self.enabled_servers
        }
    
    def get_available_tools(self) -> Dict[str, List[str]]:
        """Get all available tools from enabled servers"""
        tools = {}
        for server in self.enabled_servers:
            tools[server] = MCP_SERVERS[server]["tools"]
        return tools


class MCPInstaller:
    """Install MCP servers"""
    
    @staticmethod
    def install_server(server_type: str) -> bool:
        """Install an MCP server"""
        if server_type not in MCP_SERVERS:
            print(f"Unknown server: {server_type}")
            return False
        
        package = MCP_SERVERS[server_type]["package"]
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[MCP] Installed {package}")
                return True
            else:
                print(f"[MCP] Failed to install {package}")
                return False
        except Exception as e:
            print(f"[MCP] Error installing {package}: {e}")
            return False
    
    @staticmethod
    def install_all():
        """Install all MCP servers"""
        for server_type in MCP_SERVERS:
            MCPInstaller.install_server(server_type)


class MCPCapabilities:
    """Define MCP capabilities for agents"""
    
    @staticmethod
    def get_filesystem_tools():
        """Get filesystem tools"""
        return {
            "type": "function",
            "name": "filesystem_operations",
            "description": "Perform file system operations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["read", "write", "list", "create"]},
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                }
            }
        }
    
    @staticmethod
    def get_web_tools():
        """Get web tools"""
        return {
            "type": "function",
            "name": "web_operations",
            "description": "Perform web operations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["fetch", "parse", "post"]},
                    "url": {"type": "string"},
                    "data": {"type": "object"}
                }
            }
        }
    
    @staticmethod
    def get_all_capabilities():
        """Get all MCP capabilities"""
        return {
            "filesystem": MCPCapabilities.get_filesystem_tools(),
            "web": MCPCapabilities.get_web_tools()
        }


__all__ = [
    'MCP_SERVERS',
    'MCPConfiguration',
    'MCPInstaller',
    'MCPCapabilities'
]

