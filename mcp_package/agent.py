"""
MCP Agent Module
MCP-integrated agent definition
"""

try:
    from agents import Agent, function_tool
    from mcp_package.tools import mcp_tool_adapter
    
    # Initialize MCP tools
    mcp_tools = mcp_tool_adapter.create_all_tools()
    
    @function_tool
    async def read_file_via_mcp(file_path: str) -> str:
        """Read file using MCP filesystem server"""
        return await mcp_tools['read_file'](file_path)
    
    @function_tool
    async def write_file_via_mcp(file_path: str, content: str) -> str:
        """Write file using MCP filesystem server"""
        return await mcp_tools['write_file'](file_path, content)
    
    @function_tool
    async def list_files_via_mcp(directory: str) -> str:
        """List files using MCP filesystem server"""
        return await mcp_tools['list_files'](directory)
    
    @function_tool
    async def fetch_url_via_mcp(url: str) -> str:
        """Fetch URL using MCP web server"""
        return await mcp_tools['fetch_url'](url)
    
    @function_tool
    async def parse_html_via_mcp(html: str) -> str:
        """Parse HTML using MCP web server"""
        return await mcp_tools['parse_html'](html)
    
    # Create MCP-integrated agent
    mcp_agent = Agent(
        name="MCP-Integrated Agent",
        instructions="""
        You are an agent with access to external MCP (Model Context Protocol) servers.
        
        Your capabilities include:
        1. File System Operations (via MCP filesystem server)
           - read_file_via_mcp: Read file contents
           - write_file_via_mcp: Write to files
           - list_files_via_mcp: List directory contents
        
        2. Web Operations (via MCP web server)
           - fetch_url_via_mcp: Fetch URL content
           - parse_html_via_mcp: Parse HTML and extract text
        
        When performing tasks:
        1. Use appropriate MCP tools for external operations
        2. Process results and provide summaries
        3. Handle errors gracefully
        4. Report on server availability and status
        """,
        tools=[
            read_file_via_mcp,
            write_file_via_mcp,
            list_files_via_mcp,
            fetch_url_via_mcp,
            parse_html_via_mcp
        ]
    )
    
    mcp_agent_available = True
    
except ImportError as e:
    mcp_agent = None
    mcp_agent_available = False

__all__ = ['mcp_agent', 'mcp_agent_available']

