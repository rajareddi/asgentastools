"""
MCP Core Module
MCPServerManager and MCPServer implementations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
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
        self.connections: Dict[str, any] = {}
    
    def register_server(self, server: MCPServer):
        """Register an MCP server"""
        self.servers[server.name] = server
        print(f"[MCP] Registered server: {server.name}")
    
    def register_built_in_servers(self):
        """Register built-in MCP servers"""
        self.register_server(MCPServer(
            name="filesystem",
            command="mcp-server-filesystem",
            args=["--root", "."],
            description="File system access and manipulation"
        ))
        
        self.register_server(MCPServer(
            name="git",
            command="mcp-server-git",
            description="Git repository operations"
        ))
        
        self.register_server(MCPServer(
            name="web",
            command="mcp-server-web",
            description="Web scraping and HTTP operations"
        ))
        
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


# Global manager instance
mcp_manager = MCPServerManager()

__all__ = ['MCPServer', 'MCPServerManager', 'mcp_manager']

