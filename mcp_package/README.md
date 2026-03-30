# MCP Package

Model Context Protocol (MCP) integration for agent service.

## Structure

```
mcp_package/
├── __init__.py      - Package initialization and exports
├── core.py          - MCPServerManager and MCPServer
├── config.py        - Configuration and MCP server definitions
├── tools.py         - MCPToolAdapter
├── agent.py         - MCP-integrated agent
└── README.md        - This file
```

## Usage

### Basic Setup

```python
from mcp_package import MCPConfiguration, mcp_manager

# Configure MCP
config = MCPConfiguration()
config.enable_server("filesystem")
config.enable_server("web")

# Get enabled servers
servers = config.get_enabled_servers()
```

### Use MCP Agent

```python
from mcp_package import mcp_agent
from agents import Runner

result = await Runner.run(
    mcp_agent,
    input="Read README.md and summarize it",
    max_turns=5
)
```

### Access via API

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "List Python files",
    "agent_type": "mcp",
    "max_turns": 3
  }'
```

## Available Servers

- **filesystem**: File system operations
- **git**: Git repository operations
- **web**: Web scraping and HTTP
- **sql**: SQL database operations
- **memory**: Data storage
- **slack**: Slack messaging
- **weather**: Weather information

## Modules

### core.py
- `MCPServer`: Server configuration
- `MCPServerManager`: Manages MCP server connections
- `mcp_manager`: Global manager instance

### config.py
- `MCP_SERVERS`: Server definitions
- `MCPConfiguration`: Configuration manager
- `MCPInstaller`: Server installation
- `MCPCapabilities`: Agent capabilities

### tools.py
- `MCPToolAdapter`: Adapts MCP as agent tools
- `mcp_tool_adapter`: Global adapter instance

### agent.py
- `mcp_agent`: MCP-integrated agent
- `mcp_agent_available`: Availability flag

## Documentation

See `MCP_INTEGRATION_GUIDE.md` in project root for complete documentation.

