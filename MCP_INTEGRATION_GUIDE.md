# MCP (Model Context Protocol) Integration Guide

## Overview

MCP (Model Context Protocol) enables your agents to interact with external servers and services, dramatically extending their capabilities.

## 🎯 What is MCP?

MCP is a standardized protocol that allows:
- ✅ Agents to access external data sources
- ✅ Integration with specialized services
- ✅ File system operations
- ✅ Web scraping and HTTP operations
- ✅ Database operations
- ✅ Version control integration
- ✅ Cloud service access

## 📦 Available MCP Servers

### 1. Filesystem Server
```
Package: mcp-server-filesystem
Description: File system access and manipulation
Tools: read_file, write_file, list_files, create_dir, delete_file
```

### 2. Git Server
```
Package: mcp-server-git
Description: Git repository operations
Tools: clone_repo, commit, push, pull, branch, merge
```

### 3. Web Server
```
Package: mcp-server-web
Description: Web scraping and HTTP operations
Tools: fetch_url, parse_html, post_request, headers
```

### 4. SQL Server
```
Package: mcp-server-sql
Description: SQL database operations
Tools: query, insert, update, delete, schema
```

### 5. Memory Server
```
Package: mcp-server-memory
Description: In-memory data storage
Tools: store, retrieve, delete, list_keys
```

### 6. Slack Server
```
Package: mcp-server-slack
Description: Slack messaging operations
Tools: send_message, get_channels, get_users
```

### 7. Weather Server
```
Package: mcp-server-weather
Description: Weather information
Tools: get_weather, forecast, alerts
```

## 🚀 Quick Start

### 1. Install MCP Dependencies

```bash
# Install specific MCP servers
pip install mcp-server-filesystem
pip install mcp-server-git
pip install mcp-server-web
pip install mcp-server-sql

# Or install all
pip install -r requirements.txt
```

### 2. Enable MCP Servers

```python
from mcp_package import MCPConfiguration, MCPInstaller

# Create configuration
config = MCPConfiguration()

# Enable specific servers
config.enable_server("filesystem")
config.enable_server("web")
config.enable_server("git")

# Or enable all
config.enable_all_servers()

# Get enabled servers
servers = config.get_enabled_servers()
print(servers)
```

### 3. Use MCP-Integrated Agent

```python
from mcp_agent import mcp_agent
from agents import Runner

# Run agent with MCP capabilities
result = await Runner.run(
    mcp_agent,
    input="Read the README.md file and summarize it",
    max_turns=5
)

print(result.final_output)
```

## 💻 Usage Examples

### Example 1: File System Operations

```python
from mcp_agent import mcp_agent
from agents import Runner

result = await Runner.run(
    mcp_agent,
    input="List all Python files in the current directory",
    max_turns=3
)
```

### Example 2: Web Scraping

```python
result = await Runner.run(
    mcp_agent,
    input="Fetch https://example.com and extract the main content",
    max_turns=3
)
```

### Example 3: Git Operations

```python
result = await Runner.run(
    mcp_agent,
    input="Clone the repository and check recent commits",
    max_turns=5
)
```

## 🔧 Configuration

### Using mcp_integration.py

```python
from mcp_integration import MCPServerManager, MCPToolAdapter

# Create manager
manager = MCPServerManager()

# Register built-in servers
manager.register_built_in_servers()

# Start servers
await manager.start_all_servers()

# Get status
status = manager.get_server_status()
print(status)
```

### Using mcp_package.py

```python
from mcp_package import MCPConfiguration, MCPCapabilities

# Configuration
config = MCPConfiguration()
config.enable_server("filesystem", root_dir="/path/to/files")
config.enable_server("web")

# Get capabilities
capabilities = MCPCapabilities.get_all_capabilities()
```

## 📚 Advanced Integration

### Custom MCP Tool Creation

```python
from mcp_integration import MCPToolAdapter
import mcp_integration

adapter = MCPToolAdapter(mcp_integration.mcp_manager)

# Create custom tools
async def custom_tool(param):
    """Custom tool implementation"""
    return f"Result: {param}"

adapter.tools['custom_tool'] = custom_tool
```

### MCP Server Configuration

```python
from mcp_integration import MCPServer, MCPServerManager

manager = MCPServerManager()

# Register custom server
custom_server = MCPServer(
    name="custom_service",
    command="python",
    args=["-m", "custom_mcp_server"],
    env={"API_KEY": "your_key"},
    description="Custom service"
)

manager.register_server(custom_server)
```

## 🔌 API Integration

### Enable MCP in API Server

```python
# In api_server.py
from mcp_agent import mcp_agent

@app.post("/mcp/run")
async def run_mcp_agent(request: PromptRequest):
    """Run MCP-integrated agent"""
    result = await Runner.run(
        mcp_agent,
        input=request.prompt,
        max_turns=request.max_turns
    )
    return PromptResponse(
        result=str(result.final_output),
        agent_type="mcp_agent",
        prompt=request.prompt
    )
```

### Streamlit UI with MCP

```python
# In streamlit_ui.py
import streamlit as st

st.subheader("MCP-Integrated Agent")
mcp_prompt = st.text_area("Enter MCP task...")
mcp_agent_type = st.selectbox("Select agent", ["mcp_agent"])

if st.button("Run MCP Agent"):
    # Call API endpoint
    response = requests.post(
        f"{api_url}/mcp/run",
        json={
            "prompt": mcp_prompt,
            "agent_type": "mcp_agent",
            "max_turns": 5
        }
    )
    st.write(response.json()['result'])
```

## 🛡️ Security Considerations

### API Key Management

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Store MCP credentials in environment
MCP_FILESYSTEM_ROOT = os.getenv("MCP_FILESYSTEM_ROOT")
MCP_DATABASE_URL = os.getenv("MCP_DATABASE_URL")
MCP_SLACK_TOKEN = os.getenv("MCP_SLACK_TOKEN")
```

### Sandbox Execution

```python
# Restrict MCP filesystem operations to specific directories
config.enable_server("filesystem", root_dir="/safe/directory")
```

## 📊 Server Status Monitoring

```python
from mcp_integration import mcp_manager

# Get status
status = mcp_manager.get_server_status()

# Check specific server
if status['filesystem'] == 'running':
    print("Filesystem server is operational")
```

## ⚠️ Error Handling

```python
from mcp_agent import mcp_agent
from agents import Runner

try:
    result = await Runner.run(
        mcp_agent,
        input="Perform MCP operation",
        max_turns=3
    )
except Exception as e:
    print(f"MCP Error: {e}")
```

## 🔄 MCP Workflow

```
User Request
    ↓
Agent receives prompt
    ↓
Agent analyzes requirements
    ↓
Agent selects appropriate MCP server
    ↓
MCP Server processes request
    ↓
Agent receives result
    ↓
Agent processes and responds
    ↓
Result returned to user
```

## 📈 Performance Optimization

### Connection Pooling

```python
# Reuse server connections
mcp_manager.start_all_servers()  # Start once

# Execute multiple operations
for operation in operations:
    result = await mcp_agent.execute(operation)
```

### Caching Results

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cache_mcp_result(operation):
    """Cache MCP operation results"""
    return mcp_tool_adapter.execute(operation)
```

## 🚀 Deployment with Docker

```dockerfile
# In Dockerfile
RUN pip install mcp
RUN pip install mcp-server-filesystem
RUN pip install mcp-server-web
RUN pip install mcp-server-sql
```

## 📚 Related Documentation

- [mcp_integration.py](../mcp_integration.py) - Low-level MCP implementation
- [mcp_package.py](../mcp_package.py) - MCP configuration and utilities
- [mcp_agent.py](../mcp_agent.py) - MCP-integrated agent implementation
- [requirements.txt](../requirements.txt) - MCP dependencies

## 🤔 Troubleshooting

### MCP Server Won't Start

```python
# Check server configuration
print(mcp_manager.servers['filesystem'])

# Check processes
print(mcp_manager.processes)

# View detailed logs
mcp_manager.start_server('filesystem')  # Will print errors
```

### Tool Not Available

```python
# Check available tools
tools = mcp_tool_adapter.tools
print(f"Available tools: {list(tools.keys())}")
```

### Connection Timeout

```python
# Increase timeout
server.timeout = 30  # 30 seconds
```

## ✨ Best Practices

1. **Start servers once**: Initialize at application startup
2. **Handle errors gracefully**: Agents should handle MCP failures
3. **Cache results**: Reduce repeated MCP calls
4. **Monitor performance**: Track MCP operation times
5. **Secure credentials**: Store API keys in environment
6. **Limit scope**: Restrict filesystem and database access

## 🔮 Future Enhancements

- [ ] MCP client for agent-to-MCP communication
- [ ] Built-in caching layer
- [ ] Server clustering
- [ ] Load balancing
- [ ] Monitoring dashboard
- [ ] Performance metrics

---

**MCP Integration is ready to use!** 🎉

