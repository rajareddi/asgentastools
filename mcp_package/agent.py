"""
MCP Agent Module
MCP-integrated agent definition with OpenTelemetry tracing
"""

try:
    from agents import Agent, function_tool
    from mcp_package.tools import mcp_tool_adapter
    
    # Import OpenTelemetry for tracing
    try:
        from otel_config import get_tracer, set_span_attributes, add_span_event
        tracer = get_tracer(__name__)
        TRACING_ENABLED = True
    except ImportError:
        TRACING_ENABLED = False
    
    # Initialize MCP tools
    mcp_tools = mcp_tool_adapter.create_all_tools()
    
    @function_tool
    async def read_file_via_mcp(file_path: str) -> str:
        """Read file using MCP filesystem server"""
        if TRACING_ENABLED:
            with tracer.start_as_current_span("tool.read_file_via_mcp") as span:
                set_span_attributes({
                    "tool.name": "read_file_via_mcp",
                    "tool.type": "mcp_filesystem",
                    "tool.mcp.server": "filesystem",
                    "tool.mcp.operation": "read_file",
                    "tool.input.file_path": file_path
                })
                add_span_event("mcp_read_file_start", {"file_path": file_path})
                
                result = await mcp_tools['read_file'](file_path)
                
                set_span_attributes({
                    "tool.output.length": len(result) if result else 0,
                    "tool.success": True
                })
                add_span_event("mcp_read_file_complete", {"content_length": len(result) if result else 0})
                return result
        return await mcp_tools['read_file'](file_path)
    
    @function_tool
    async def write_file_via_mcp(file_path: str, content: str) -> str:
        """Write file using MCP filesystem server"""
        if TRACING_ENABLED:
            with tracer.start_as_current_span("tool.write_file_via_mcp") as span:
                set_span_attributes({
                    "tool.name": "write_file_via_mcp",
                    "tool.type": "mcp_filesystem",
                    "tool.mcp.server": "filesystem",
                    "tool.mcp.operation": "write_file",
                    "tool.input.file_path": file_path,
                    "tool.input.content_length": len(content)
                })
                add_span_event("mcp_write_file_start", {
                    "file_path": file_path,
                    "content_length": len(content)
                })
                
                result = await mcp_tools['write_file'](file_path, content)
                
                set_span_attributes({
                    "tool.success": True
                })
                add_span_event("mcp_write_file_complete", {"file_path": file_path})
                return result
        return await mcp_tools['write_file'](file_path, content)
    
    @function_tool
    async def list_files_via_mcp(directory: str) -> str:
        """List files using MCP filesystem server"""
        if TRACING_ENABLED:
            with tracer.start_as_current_span("tool.list_files_via_mcp") as span:
                set_span_attributes({
                    "tool.name": "list_files_via_mcp",
                    "tool.type": "mcp_filesystem",
                    "tool.mcp.server": "filesystem",
                    "tool.mcp.operation": "list_files",
                    "tool.input.directory": directory
                })
                add_span_event("mcp_list_files_start", {"directory": directory})
                
                result = await mcp_tools['list_files'](directory)
                
                # Count files in result
                file_count = result.count('\n') if result else 0
                set_span_attributes({
                    "tool.output.file_count": file_count,
                    "tool.output.length": len(result) if result else 0,
                    "tool.success": True
                })
                add_span_event("mcp_list_files_complete", {
                    "file_count": file_count,
                    "directory": directory
                })
                return result
        return await mcp_tools['list_files'](directory)
    
    @function_tool
    async def fetch_url_via_mcp(url: str) -> str:
        """Fetch URL using MCP web server"""
        if TRACING_ENABLED:
            with tracer.start_as_current_span("tool.fetch_url_via_mcp") as span:
                set_span_attributes({
                    "tool.name": "fetch_url_via_mcp",
                    "tool.type": "mcp_web",
                    "tool.mcp.server": "web",
                    "tool.mcp.operation": "fetch_url",
                    "tool.input.url": url,
                    "http.url": url
                })
                add_span_event("mcp_fetch_url_start", {"url": url})
                
                result = await mcp_tools['fetch_url'](url)
                
                set_span_attributes({
                    "tool.output.length": len(result) if result else 0,
                    "tool.success": True,
                    "http.response.length": len(result) if result else 0
                })
                add_span_event("mcp_fetch_url_complete", {
                    "url": url,
                    "content_length": len(result) if result else 0
                })
                return result
        return await mcp_tools['fetch_url'](url)
    
    @function_tool
    async def parse_html_via_mcp(html: str) -> str:
        """Parse HTML using MCP web server"""
        if TRACING_ENABLED:
            with tracer.start_as_current_span("tool.parse_html_via_mcp") as span:
                set_span_attributes({
                    "tool.name": "parse_html_via_mcp",
                    "tool.type": "mcp_web",
                    "tool.mcp.server": "web",
                    "tool.mcp.operation": "parse_html",
                    "tool.input.html_length": len(html)
                })
                add_span_event("mcp_parse_html_start", {"html_length": len(html)})
                
                result = await mcp_tools['parse_html'](html)
                
                set_span_attributes({
                    "tool.output.length": len(result) if result else 0,
                    "tool.success": True
                })
                add_span_event("mcp_parse_html_complete", {
                    "output_length": len(result) if result else 0
                })
                return result
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

