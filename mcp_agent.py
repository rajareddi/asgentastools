"""
MCP-Integrated Agent
Agent with Model Context Protocol server access
"""

from agents import Agent, function_tool
from mcp_integration import mcp_manager, mcp_tool_adapter


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
    
    3. Extended Capabilities
       - Git operations (when git server enabled)
       - Database operations (when SQL server enabled)
       - Memory operations (when memory server enabled)
    
    When performing tasks:
    1. Use appropriate MCP tools for external operations
    2. Process results and provide summaries
    3. Handle errors gracefully
    4. Report on server availability and status
    
    Available MCP Servers:
    - filesystem: File system operations
    - web: Web scraping and HTTP
    - git: Git repository management
    - sql: Database operations
    - memory: Key-value storage
    - slack: Slack integration
    - weather: Weather information
    """,
    tools=[
        read_file_via_mcp,
        write_file_via_mcp,
        list_files_via_mcp,
        fetch_url_via_mcp,
        parse_html_via_mcp
    ]
)


__all__ = ['mcp_agent']

