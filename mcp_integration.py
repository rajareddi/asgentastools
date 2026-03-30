"""
MCP (Model Context Protocol) Integration for Agent Service
Enables agents to communicate with external MCP servers for extended capabilities
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
import json
import subprocess
import sys


@dataclass
class MCPServer:
    """MCP Server configuration"""
    name: str
    command: str
    args: List[str] = None
    env: Dict[str, str] = None
    description: str = ""


class MCPServerManager:
    """Manages connections to MCP servers"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        self.connections: Dict[str, Any] = {}
    
    def register_server(self, server: MCPServer):
        """Register an MCP server"""
        self.servers[server.name] = server
        print(f"[MCP] Registered server: {server.name}")
    
    def register_built_in_servers(self):
        """Register built-in MCP servers for common tasks"""
        
        # Filesystem server
        self.register_server(MCPServer(
            name="filesystem",
            command="mcp-server-filesystem",
            args=["--root", "."],
            description="File system access and manipulation"
        ))
        
        # Git server
        self.register_server(MCPServer(
            name="git",
            command="mcp-server-git",
            description="Git repository operations"
        ))
        
        # Web server
        self.register_server(MCPServer(
            name="web",
            command="mcp-server-web",
            description="Web scraping and HTTP operations"
        ))
        
        # SQL server
        self.register_server(MCPServer(
            name="sql",
            command="mcp-server-sql",
            description="SQL database operations"
        ))
    
    async def start_server(self, server_name: str) -> bool:
        """Start an MCP server"""
        if server_name not in self.servers:
            print(f"[MCP] Server not found: {server_name}")
            return False
        
        server = self.servers[server_name]
        try:
            cmd = [server.command] + (server.args or [])
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=server.env or {}
            )
            self.processes[server_name] = process
            print(f"[MCP] Started server: {server_name}")
            return True
        except Exception as e:
            print(f"[MCP] Error starting {server_name}: {e}")
            return False
    
    async def stop_server(self, server_name: str) -> bool:
        """Stop an MCP server"""
        if server_name in self.processes:
            try:
                self.processes[server_name].terminate()
                self.processes[server_name].wait(timeout=5)
                del self.processes[server_name]
                print(f"[MCP] Stopped server: {server_name}")
                return True
            except Exception as e:
                print(f"[MCP] Error stopping {server_name}: {e}")
                return False
        return False
    
    async def start_all_servers(self) -> List[str]:
        """Start all registered servers"""
        started = []
        for server_name in self.servers:
            if await self.start_server(server_name):
                started.append(server_name)
        return started
    
    async def stop_all_servers(self):
        """Stop all running servers"""
        for server_name in list(self.processes.keys()):
            await self.stop_server(server_name)
    
    def get_server_status(self) -> Dict[str, str]:
        """Get status of all servers"""
        status = {}
        for name, server in self.servers.items():
            if name in self.processes:
                process = self.processes[name]
                if process.poll() is None:
                    status[name] = "running"
                else:
                    status[name] = "stopped"
            else:
                status[name] = "not_started"
        return status


class MCPToolAdapter:
    """Adapts MCP server capabilities as agent tools"""
    
    def __init__(self, server_manager: MCPServerManager):
        self.server_manager = server_manager
        self.tools = {}
    
    def create_filesystem_tools(self):
        """Create tools for filesystem operations"""
        
        async def read_file(path: str) -> str:
            """Read file contents"""
            try:
                with open(path, 'r') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {e}"
        
        async def write_file(path: str, content: str) -> str:
            """Write file contents"""
            try:
                with open(path, 'w') as f:
                    f.write(content)
                return f"Successfully wrote to {path}"
            except Exception as e:
                return f"Error writing file: {e}"
        
        async def list_files(path: str) -> str:
            """List files in directory"""
            try:
                import os
                files = os.listdir(path)
                return "\n".join(files)
            except Exception as e:
                return f"Error listing files: {e}"
        
        self.tools['read_file'] = read_file
        self.tools['write_file'] = write_file
        self.tools['list_files'] = list_files
        return self.tools
    
    def create_web_tools(self):
        """Create tools for web operations"""
        
        async def fetch_url(url: str) -> str:
            """Fetch URL content"""
            try:
                import requests
                response = requests.get(url, timeout=10)
                return response.text[:1000]  # First 1000 chars
            except Exception as e:
                return f"Error fetching URL: {e}"
        
        async def parse_html(html: str) -> str:
            """Parse HTML and extract text"""
            try:
                from html.parser import HTMLParser
                
                class TextParser(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.text = []
                    
                    def handle_data(self, data):
                        self.text.append(data.strip())
                
                parser = TextParser()
                parser.feed(html)
                return "\n".join(parser.text)
            except Exception as e:
                return f"Error parsing HTML: {e}"
        
        self.tools['fetch_url'] = fetch_url
        self.tools['parse_html'] = parse_html
        return self.tools
    
    def create_all_tools(self) -> Dict:
        """Create all available MCP tools"""
        self.create_filesystem_tools()
        self.create_web_tools()
        return self.tools


# Global MCP manager instance
mcp_manager = MCPServerManager()
mcp_tool_adapter = MCPToolAdapter(mcp_manager)

__all__ = ['MCPServer', 'MCPServerManager', 'MCPToolAdapter', 'mcp_manager', 'mcp_tool_adapter']

