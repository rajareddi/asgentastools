# Tool Calling Tracing Guide

## Overview

This guide explains how **tool calling information** is captured in OpenTelemetry traces when agents execute functions.

## What Gets Traced

### Tool Execution Spans

Every tool call creates a dedicated span with detailed information:

```
agent_execution
├── agent_runner
│   ├── tool.add_numbers           ← Tool span
│   ├── tool.multiply_numbers      ← Tool span
│   └── tool.get_weather           ← Tool span
```

### Tool Span Attributes

Each tool span includes comprehensive metadata:

#### Common Attributes (All Tools)
- `tool.name` - Name of the tool function
- `tool.type` - Type of tool (calculation, api_call, agent_runner, a2a_communication, analysis)
- `tool.success` - Whether execution succeeded (true/false)
- `tool.input.*` - All input parameters
- `tool.output.*` - All output values

#### Tool-Specific Attributes

**Calculation Tools** (`add_numbers`, `multiply_numbers`):
```
tool.name: "add_numbers"
tool.type: "calculation"
tool.input.a: 5
tool.input.b: 3
tool.output.result: 8
tool.success: true
```

**API Call Tools** (`get_weather`):
```
tool.name: "get_weather"
tool.type: "api_call"
tool.input.city: "San Francisco"
tool.output.result: "The weather in San Francisco is sunny with 72°F"
tool.success: true
```

**Temperature Conversion**:
```
tool.name: "convert_temperature"
tool.type: "calculation"
tool.input.temperature: 100
tool.input.from_unit: "celsius"
tool.input.to_unit: "fahrenheit"
tool.output.result_value: 212.0
tool.output.result: "100°C = 212.0°F"
tool.success: true
```

**Agent Runner Tools** (`run_research_agent`, `run_writing_agent`):
```
tool.name: "run_research_agent"
tool.type: "agent_runner"
tool.agent: "Research Specialist"
tool.input.topic: "AI in healthcare"
tool.max_turns: 3
tool.output.length: 1542
tool.success: true
```

**A2A Communication Tools** (`agent1_send_message`, `agent1_check_messages`):
```
tool.name: "agent1_send_message"
tool.type: "a2a_communication"
tool.from_agent: "Coordinator"
tool.to_agent: "Specialist"
tool.topic: "general"
tool.message_length: 145
tool.message_id: "msg_abc123"
tool.success: true
```

### Tool Events

Each tool execution generates events marking key phases:

#### Calculation Tools
- `calculation_complete` - With result value

#### API Tools
- `fetching_weather` - Start of API call
- `weather_fetched` - Successful response

#### Temperature Conversion
- `temperature_conversion_start` - Start with parameters
- `temperature_conversion_complete` - End with result

#### Agent Runner Tools
- `tool_execution_start` - Tool begins with topic/input
- `tool_execution_complete` - Tool completes with output length

#### A2A Tools
- `sending_message` - Message send initiated
- `message_sent` - Message successfully sent
- `checking_messages` - Checking for messages
- `messages_retrieved` - Messages retrieved
- `analysis_start` - Analysis begins
- `analysis_complete` - Analysis completes

---

## Tool Tracing by Agent Type

### 1. Function Tools Agent

**Tools Traced:**
- ✅ `add_numbers` - Addition operations
- ✅ `multiply_numbers` - Multiplication operations
- ✅ `get_weather` - Weather API calls
- ✅ `convert_temperature` - Temperature conversions

**Example Trace Structure:**
```
HTTP POST /run
├── agent_execution
│   ├── agent_selection_start [event]
│   ├── agent_runner
│   │   ├── tool.add_numbers
│   │   │   ├── calculation_complete [event]
│   │   ├── tool.multiply_numbers
│   │   │   └── calculation_complete [event]
│   └── agent_execution_complete [event]
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is 5 + 3, then multiply by 2?",
    "agent_type": "functions",
    "max_turns": 3
  }'
```

**In Opik, you'll see:**
- Span: `tool.add_numbers`
  - Attributes: `tool.input.a=5`, `tool.input.b=3`, `tool.output.result=8`
  - Event: `calculation_complete` with result
- Span: `tool.multiply_numbers`
  - Attributes: `tool.input.a=8`, `tool.input.b=2`, `tool.output.result=16`
  - Event: `calculation_complete` with result

---

### 2. Advanced Orchestrator Agent

**Tools Traced:**
- ✅ `run_research_agent` - Research operations
- ✅ `run_writing_agent` - Writing operations

**Example Trace Structure:**
```
HTTP POST /run
├── agent_execution
│   ├── agent_runner
│   │   ├── tool.run_research_agent
│   │   │   ├── tool_execution_start [event]
│   │   │   └── tool_execution_complete [event]
│   │   ├── tool.run_writing_agent
│   │   │   ├── tool_execution_start [event]
│   │   │   └── tool_execution_complete [event]
│   └── agent_execution_complete [event]
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Research AI in healthcare and write a professional summary",
    "agent_type": "advanced",
    "max_turns": 5
  }'
```

**In Opik, you'll see:**
- Span: `tool.run_research_agent`
  - Attributes: `tool.agent="Research Specialist"`, `tool.input.topic="AI in healthcare"`, `tool.max_turns=3`
  - Events: `tool_execution_start`, `tool_execution_complete`
  - Output: `tool.output.length=1542`
- Span: `tool.run_writing_agent`
  - Attributes: `tool.agent="Writing Specialist"`, `tool.input.style="professional"`, `tool.max_turns=2`
  - Events: `tool_execution_start`, `tool_execution_complete`
  - Output: `tool.output.length=856`

---

### 3. A2A Coordinator & Specialist Agents

**Tools Traced:**
- ✅ `agent1_send_message` - Send messages between agents
- ✅ `agent1_check_messages` - Check received messages
- ✅ `agent1_analyze_topic` - Analyze topics
- ✅ `agent1_get_conversation` - Retrieve conversation history
- ✅ `agent2_provide_expertise` - Provide specialized knowledge
- ✅ `agent2_send_response` - Send responses

**Example Trace Structure:**
```
HTTP POST /a2a/collaborate
├── a2a_collaboration
│   ├── a2a_execution_start [event]
│   ├── agent_runner
│   │   ├── tool.agent1_send_message
│   │   │   ├── sending_message [event]
│   │   │   └── message_sent [event]
│   │   ├── tool.agent1_analyze_topic
│   │   │   ├── analysis_start [event]
│   │   │   └── analysis_complete [event]
│   │   ├── tool.agent2_check_messages
│   │   │   ├── checking_messages [event]
│   │   │   └── messages_retrieved [event]
│   │   ├── tool.agent2_provide_expertise
│   │   │   ├── providing_expertise [event]
│   │   │   └── expertise_provided [event]
│   └── a2a_execution_complete [event]
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/a2a/collaborate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Discuss microservices architecture",
    "agent_type": "a2a_orchestrator",
    "max_turns": 5
  }'
```

**In Opik, you'll see:**
- Span: `tool.agent1_send_message`
  - Attributes: `tool.from_agent="Coordinator"`, `tool.to_agent="Specialist"`, `tool.topic="general"`
  - Events: `sending_message`, `message_sent`
  - Message ID tracked
- Span: `tool.agent1_analyze_topic`
  - Attributes: `tool.agent="Coordinator"`, `tool.input.topic="microservices"`
  - Events: `analysis_start`, `analysis_complete`
  - Output length tracked
- Span: `tool.agent2_provide_expertise`
  - Attributes: `tool.agent="Specialist"`, domain details
  - Events showing expertise flow

---

## Viewing Tool Traces in Opik

### 1. Access Opik Dashboard
```
http://localhost:5173
```

### 2. Navigate to Your Project
- Workspace: `default`
- Project: `agent-service`

### 3. Select a Trace

Click on any trace to see the full execution tree.

### 4. Expand Tool Spans

Look for spans starting with `tool.` prefix:
- `tool.add_numbers`
- `tool.run_research_agent`
- `tool.agent1_send_message`

### 5. View Attributes

Each tool span shows:
- **Tags/Attributes** - All input/output parameters
- **Events** - Key execution phases
- **Timing** - Duration of tool execution
- **Status** - Success or failure

### 6. Filter by Tool Type

Use filters to find specific tool types:
```
tool.type = "calculation"
tool.type = "agent_runner"
tool.type = "a2a_communication"
```

---

## Tool Trace Examples

### Example 1: Simple Calculation

**Request:**
```json
{
  "prompt": "What is 10 + 5?",
  "agent_type": "functions",
  "max_turns": 2
}
```

**Trace in Opik:**
```
agent_execution (duration: 2.3s)
├── agent_runner (duration: 2.1s)
│   └── tool.add_numbers (duration: 0.001s)
│       Attributes:
│         tool.name: "add_numbers"
│         tool.type: "calculation"
│         tool.input.a: 10
│         tool.input.b: 5
│         tool.output.result: 15
│         tool.success: true
│       Events:
│         └── calculation_complete (result: 15)
```

### Example 2: Temperature Conversion

**Request:**
```json
{
  "prompt": "Convert 100 celsius to fahrenheit",
  "agent_type": "functions",
  "max_turns": 2
}
```

**Trace in Opik:**
```
agent_execution
├── agent_runner
│   └── tool.convert_temperature (duration: 0.002s)
│       Attributes:
│         tool.name: "convert_temperature"
│         tool.type: "calculation"
│         tool.input.temperature: 100
│         tool.input.from_unit: "celsius"
│         tool.input.to_unit: "fahrenheit"
│         tool.output.result_value: 212.0
│         tool.output.result: "100°C = 212.0°F"
│         tool.success: true
│       Events:
│         ├── temperature_conversion_start
│         └── temperature_conversion_complete
```

### Example 3: Research and Writing

**Request:**
```json
{
  "prompt": "Research quantum computing and write a summary",
  "agent_type": "advanced",
  "max_turns": 5
}
```

**Trace in Opik:**
```
agent_execution
├── agent_runner
│   ├── tool.run_research_agent (duration: 4.2s)
│   │   Attributes:
│   │     tool.name: "run_research_agent"
│   │     tool.type: "agent_runner"
│   │     tool.agent: "Research Specialist"
│   │     tool.input.topic: "quantum computing"
│   │     tool.max_turns: 3
│   │     tool.output.length: 2145
│   │     tool.success: true
│   │   Events:
│   │     ├── tool_execution_start
│   │     └── tool_execution_complete (output_length: 2145)
│   │
│   └── tool.run_writing_agent (duration: 3.8s)
│       Attributes:
│         tool.name: "run_writing_agent"
│         tool.type: "agent_runner"
│         tool.agent: "Writing Specialist"
│         tool.input.content_length: 2145
│         tool.input.style: "professional"
│         tool.max_turns: 2
│         tool.output.length: 1287
│         tool.success: true
│       Events:
│         ├── tool_execution_start
│         └── tool_execution_complete (output_length: 1287)
```

### Example 4: A2A Communication

**Request:**
```json
{
  "prompt": "Discuss cloud architecture best practices",
  "agent_type": "a2a_orchestrator",
  "max_turns": 5
}
```

**Trace in Opik:**
```
a2a_collaboration
├── agent_runner
│   ├── tool.agent1_analyze_topic (duration: 0.5s)
│   │   Attributes:
│   │     tool.name: "agent1_analyze_topic"
│   │     tool.type: "analysis"
│   │     tool.agent: "Coordinator"
│   │     tool.input.topic: "cloud architecture"
│   │     tool.output.length: 342
│   │     tool.success: true
│   │   Events:
│   │     ├── analysis_start
│   │     └── analysis_complete
│   │
│   ├── tool.agent1_send_message (duration: 0.01s)
│   │   Attributes:
│   │     tool.name: "agent1_send_message"
│   │     tool.type: "a2a_communication"
│   │     tool.from_agent: "Coordinator"
│   │     tool.to_agent: "Specialist"
│   │     tool.topic: "general"
│   │     tool.message_length: 145
│   │     tool.message_id: "msg_12345"
│   │     tool.success: true
│   │   Events:
│   │     ├── sending_message
│   │     └── message_sent
│   │
│   └── tool.agent2_check_messages (duration: 0.01s)
│       Attributes:
│         tool.name: "agent2_check_messages"
│         tool.type: "a2a_communication"
│         tool.agent: "Specialist"
│         tool.topic: "general"
│         tool.message_count: 1
│         tool.success: true
│       Events:
│         ├── checking_messages
│         └── messages_retrieved (count: 1)
```

---

### Example 5: MCP File Operations

**Request:**
```json
{
  "prompt": "Read the README.md file",
  "agent_type": "mcp",
  "max_turns": 3
}
```

**Trace in Opik:**
```
agent_execution
├── agent_runner
│   └── tool.read_file_via_mcp (duration: 0.05s)
│       Attributes:
│         tool.name: "read_file_via_mcp"
│         tool.type: "mcp_filesystem"
│         tool.mcp.server: "filesystem"
│         tool.mcp.operation: "read_file"
│         tool.input.file_path: "README.md"
│         tool.output.length: 5243
│         tool.success: true
│       Events:
│         ├── mcp_read_file_start (file_path: "README.md")
│         └── mcp_read_file_complete (content_length: 5243)
```

### Example 6: MCP Web Fetching

**Request:**
```json
{
  "prompt": "Fetch content from https://example.com and summarize it",
  "agent_type": "mcp",
  "max_turns": 5
}
```

**Trace in Opik:**
```
agent_execution
├── agent_runner
│   ├── tool.fetch_url_via_mcp (duration: 1.2s)
│   │   Attributes:
│   │     tool.name: "fetch_url_via_mcp"
│   │     tool.type: "mcp_web"
│   │     tool.mcp.server: "web"
│   │     tool.mcp.operation: "fetch_url"
│   │     tool.input.url: "https://example.com"
│   │     http.url: "https://example.com"
│   │     tool.output.length: 2048
│   │     http.response.length: 2048
│   │     tool.success: true
│   │   Events:
│   │     ├── mcp_fetch_url_start (url: "https://example.com")
│   │     └── mcp_fetch_url_complete (url: "https://example.com", content_length: 2048)
│   │
│   └── tool.parse_html_via_mcp (duration: 0.03s)
│       Attributes:
│         tool.name: "parse_html_via_mcp"
│         tool.type: "mcp_web"
│         tool.mcp.server: "web"
│         tool.mcp.operation: "parse_html"
│         tool.input.html_length: 2048
│         tool.output.length: 1234
│         tool.success: true
│       Events:
│         ├── mcp_parse_html_start (html_length: 2048)
│         └── mcp_parse_html_complete (output_length: 1234)
```

### Example 7: MCP File Writing

**Request:**
```json
{
  "prompt": "Create a summary.txt file with today's summary",
  "agent_type": "mcp",
  "max_turns": 3
}
```

**Trace in Opik:**
```
agent_execution
├── agent_runner
│   └── tool.write_file_via_mcp (duration: 0.02s)
│       Attributes:
│         tool.name: "write_file_via_mcp"
│         tool.type: "mcp_filesystem"
│         tool.mcp.server: "filesystem"
│         tool.mcp.operation: "write_file"
│         tool.input.file_path: "summary.txt"
│         tool.input.content_length: 456
│         tool.success: true
│       Events:
│         ├── mcp_write_file_start (file_path: "summary.txt", content_length: 456)
│         └── mcp_write_file_complete (file_path: "summary.txt")
```

---

## Querying Tool Traces

### Find All Tool Executions
Filter: `span.name starts with "tool."`

### Find Specific Tool
Filter: `tool.name = "add_numbers"`

### Find Failed Tools
Filter: `tool.success = false`

### Find Slow Tools
Filter: `duration > 1s AND span.name starts with "tool."`

### Find A2A Communications
Filter: `tool.type = "a2a_communication"`

### Find Agent Runner Tools
Filter: `tool.type = "agent_runner"`

### Find MCP Filesystem Operations
Filter: `tool.mcp.server = "filesystem"`

### Find MCP Web Operations
Filter: `tool.mcp.server = "web"`

### Find MCP File Reads
Filter: `tool.name = "read_file_via_mcp"`

### Find MCP URL Fetches
Filter: `tool.name = "fetch_url_via_mcp"`

### Find Large File Operations
Filter: `tool.output.length > 10000 AND tool.mcp.server = "filesystem"`

---

## Benefits of Tool Tracing

### 1. **Performance Analysis**
- See which tools are slow
- Identify bottlenecks in agent workflows
- Optimize tool implementations

### 2. **Debugging**
- See exact parameters passed to tools
- View tool outputs and results
- Track tool execution order

### 3. **Usage Analytics**
- Most frequently used tools
- Tool success/failure rates
- Average tool execution time

### 4. **Cost Analysis**
- Track LLM API calls (via agent runner tools)
- Monitor tool usage patterns
- Identify optimization opportunities

### 5. **Error Investigation**
- See which tool failed
- View error context
- Understand failure patterns

---

## Testing Tool Tracing

### Test Script

Create `test_tool_tracing.sh`:

```bash
#!/bin/bash

echo "Testing tool tracing..."

# Test 1: Simple calculation
echo -e "\n1. Testing add_numbers tool..."
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is 5 + 3?","agent_type":"functions","max_turns":2}'

# Test 2: Temperature conversion
echo -e "\n\n2. Testing convert_temperature tool..."
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Convert 100 celsius to fahrenheit","agent_type":"functions","max_turns":2}'

# Test 3: Research agent
echo -e "\n\n3. Testing run_research_agent tool..."
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Research AI trends","agent_type":"advanced","max_turns":3}'

# Test 4: A2A communication
echo -e "\n\n4. Testing A2A tools..."
curl -X POST http://localhost:8000/a2a/collaborate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Discuss microservices","agent_type":"a2a_orchestrator","max_turns":5}'

# Test 5: MCP filesystem tools
echo -e "\n\n5. Testing MCP filesystem tools..."
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"List files in the current directory","agent_type":"mcp","max_turns":3}'

# Test 6: MCP web tools
echo -e "\n\n6. Testing MCP web tools..."
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Fetch content from https://httpbin.org/html","agent_type":"mcp","max_turns":3}'

echo -e "\n\nDone! Check Opik at http://localhost:5173"
```

### PowerShell Test Script

```powershell
# test_tool_tracing.ps1

Write-Host "Testing tool tracing..." -ForegroundColor Green

# Test 1: Simple calculation
Write-Host "`n1. Testing add_numbers tool..." -ForegroundColor Yellow
$body1 = @{
    prompt = "What is 5 + 3?"
    agent_type = "functions"
    max_turns = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/run" -Method POST -ContentType "application/json" -Body $body1

# Test 2: Temperature conversion
Write-Host "`n2. Testing convert_temperature tool..." -ForegroundColor Yellow
$body2 = @{
    prompt = "Convert 100 celsius to fahrenheit"
    agent_type = "functions"
    max_turns = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/run" -Method POST -ContentType "application/json" -Body $body2

# Test 3: Research agent
Write-Host "`n3. Testing run_research_agent tool..." -ForegroundColor Yellow
$body3 = @{
    prompt = "Research AI trends"
    agent_type = "advanced"
    max_turns = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/run" -Method POST -ContentType "application/json" -Body $body3

# Test 4: MCP filesystem
Write-Host "`n4. Testing MCP filesystem tools..." -ForegroundColor Yellow
$body4 = @{
    prompt = "List files in the current directory"
    agent_type = "mcp"
    max_turns = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/run" -Method POST -ContentType "application/json" -Body $body4

# Test 5: MCP web
Write-Host "`n5. Testing MCP web tools..." -ForegroundColor Yellow
$body5 = @{
    prompt = "Fetch content from https://httpbin.org/html"
    agent_type = "mcp"
    max_turns = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/run" -Method POST -ContentType "application/json" -Body $body5

Write-Host "`nDone! Check Opik at http://localhost:5173" -ForegroundColor Green
```

---

## Summary

✅ **All tool calls are now traced** with comprehensive information:

- **Function Tools** - Calculations, weather, temperature
- **Agent Runner Tools** - Research, writing  
- **A2A Tools** - Messages, analysis, conversations
- **MCP Tools** - Filesystem operations, web fetching, HTML parsing

✅ **Each tool trace includes:**
- Tool name and type
- MCP server information (for MCP tools)
- MCP operation type (for MCP tools)
- All input parameters
- All output values
- Success/failure status
- Execution events
- Timing information

✅ **View in Opik:**
- Navigate to workspace → project
- Select trace to see tool spans
- Expand `tool.*` spans for details
- Filter by tool type or name
- Filter by MCP server: `tool.mcp.server = "filesystem"` or `tool.mcp.server = "web"`

**Now you have complete visibility into agent tool executions including MCP operations!** 🎉

