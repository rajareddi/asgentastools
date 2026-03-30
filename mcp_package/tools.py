"""
MCP Tools Module
MCPToolAdapter and tool implementations
"""

from typing import Dict
from mcp_package.core import MCPServerManager


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
                return response.text[:1000]
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
                        if data.strip():
                            self.text.append(data.strip())
                
                parser = TextParser()
                parser.feed(html)
                return "\n".join(parser.text[:100])
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


# Global instance
from mcp_package.core import mcp_manager
mcp_tool_adapter = MCPToolAdapter(mcp_manager)

__all__ = ['MCPToolAdapter', 'mcp_tool_adapter']

