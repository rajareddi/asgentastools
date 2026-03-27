# 🤝 A2A Communication - Quick Reference

## What's New

✨ **Agent-to-Agent Communication Protocol** - Enables intelligent agents to communicate and collaborate!

### 3 New Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| **Coordinator** | Manages communication & analysis | send_message, check_messages, analyze_topic, get_conversation |
| **Specialist** | Domain expertise & collaboration | send_message, check_messages, provide_expertise, get_conversation |
| **A2A Orchestrator** | Multi-agent workflows | orchestrate_collaboration, get_collaboration_history |

## Quick API Examples

### Send Message
```bash
curl -X POST "http://localhost:8000/a2a/send-message" \
  -G --data-urlencode "from_agent=Coordinator" \
  --data-urlencode "to_agent=Specialist" \
  --data-urlencode "message=Analyze this architecture" \
  --data-urlencode "topic=infrastructure"
```

### Get Conversation
```bash
curl "http://localhost:8000/a2a/conversation?agent1=Coordinator&agent2=Specialist&topic=infrastructure"
```

### Run Collaboration
```bash
curl -X POST http://localhost:8000/a2a/collaborate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Discuss microservices best practices",
    "agent_type": "a2a_orchestrator",
    "max_turns": 5
  }'
```

## Python Usage

```python
import requests

# Send message
msg = requests.post(
    "http://localhost:8000/a2a/send-message",
    params={
        "from_agent": "Coordinator",
        "to_agent": "Specialist",
        "message": "Your expertise needed",
        "topic": "architecture"
    }
).json()

# Get conversation
conv = requests.get(
    "http://localhost:8000/a2a/conversation",
    params={
        "agent1": "Coordinator",
        "agent2": "Specialist",
        "topic": "architecture"
    }
).json()

# Run collaboration
result = requests.post(
    "http://localhost:8000/a2a/collaborate",
    json={
        "prompt": "Discuss CI/CD pipelines",
        "agent_type": "a2a_orchestrator",
        "max_turns": 5
    }
).json()
```

## Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/a2a/collaborate` | POST | Run A2A collaboration workflow |
| `/a2a/send-message` | POST | Send message between agents |
| `/a2a/messages` | GET | Get messages for an agent |
| `/a2a/conversation` | GET | Get conversation between agents |
| `/a2a/clear-messages` | DELETE | Clear message history |
| `/agents` | GET | List all agents (including A2A) |

## Use Cases

### 🏗️ Architecture Review
1. Coordinator analyzes design
2. Specialist provides critique
3. Orchestrator synthesizes feedback

### 🔍 Problem Analysis
1. Coordinator defines problem
2. Specialist provides solutions
3. Get collaborative solution

### 📚 Knowledge Sharing
1. Coordinator asks questions
2. Specialist shares expertise
3. Learn from both perspectives

### 🎯 Decision Making
1. Both agents contribute insights
2. Orchestrator synthesizes
3. Make informed decision

## How to Use

### Via Streamlit UI
1. Go to http://localhost:8501
2. Scroll to "Agent-to-Agent Communication"
3. Choose "Collaborate" tab
4. Enter topic and click "Start A2A Collaboration"

### Via REST API
Use the curl/Python examples above

### Via Test Script
```bash
python test_a2a_communication.py
```

## Message Structure

```json
{
  "id": 1,
  "timestamp": "2026-03-27T15:30:45.123456",
  "from": "Coordinator",
  "to": "Specialist",
  "topic": "infrastructure",
  "message": "Message content",
  "status": "sent"
}
```

## API Parameters

### POST /a2a/send-message
- `from_agent` (string): Sending agent
- `to_agent` (string): Receiving agent
- `message` (string): Message content
- `topic` (string): Topic/category (default: "general")

### GET /a2a/messages
- `agent` (string, optional): Filter by agent
- `topic` (string): Topic filter (default: "general")

### GET /a2a/conversation
- `agent1` (string): First agent (default: "Coordinator")
- `agent2` (string): Second agent (default: "Specialist")
- `topic` (string): Topic (default: "general")

### POST /a2a/collaborate
- `prompt` (string): Collaboration prompt
- `agent_type` (string): Always "a2a_orchestrator"
- `max_turns` (integer): Max agent iterations (default: 5)

### DELETE /a2a/clear-messages
- `agent` (string, optional): Agent filter
- `topic` (string, optional): Topic filter

## Testing

```bash
# Test imports
python -c "from agents_module.a2a_communication import *; print('✓ OK')"

# Test A2A communication
python test_a2a_communication.py
```

## Features

✅ Agent-to-agent messaging  
✅ Conversation history tracking  
✅ Multi-agent collaboration  
✅ Message filtering by topic  
✅ Timestamp tracking  
✅ Message metadata storage  
✅ Clean message history  

## Workflow Example

```
User: "Discuss microservices architecture"
  ↓
A2A Orchestrator receives prompt
  ↓
Coordinator analyzes topic
  ↓
Coordinator sends to Specialist
  ↓
Specialist provides expertise
  ↓
Specialist sends response
  ↓
Orchestrator synthesizes insights
  ↓
User gets comprehensive analysis
```

## Files

- `agents_module/a2a_communication.py` - A2A implementation
- `A2A_COMMUNICATION.md` - Detailed documentation
- `test_a2a_communication.py` - Test suite
- Updated `api_server.py` - New A2A endpoints
- Updated `streamlit_ui.py` - A2A UI tabs

## Next Steps

1. ✅ Access A2A via Streamlit UI
2. ✅ Test with REST API
3. ✅ Try test script: `python test_a2a_communication.py`
4. 📖 Read full docs: `A2A_COMMUNICATION.md`
5. 🚀 Deploy to cloud with Docker

## Documentation

- 📖 **A2A_COMMUNICATION.md** - Complete A2A guide
- 📖 **README.md** - Main project overview
- 📖 **ARCHITECTURE.md** - System design
- 📖 **DEPLOYMENT_GUIDE.md** - Cloud deployment

---

**Start using A2A Communication today!** 🚀

