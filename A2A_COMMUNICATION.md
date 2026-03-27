# Agent-to-Agent (A2A) Communication Protocol

## Overview

The Agent-to-Agent (A2A) Communication Protocol enables intelligent agents to communicate, collaborate, and solve problems together. This is a breakthrough feature that allows agents to share information, ask for expertise, and coordinate on complex tasks.

## 🎯 What's New

### 3 New Agents

1. **Coordinator Agent**
   - Orchestrates communication between agents
   - Analyzes topics and shares insights
   - Maintains conversation history
   - Facilitates decision-making

2. **Specialist Agent**
   - Provides domain-specific expertise
   - Responds to collaboration requests
   - Contributes specialized knowledge
   - Supports collaborative problem-solving

3. **A2A Orchestrator**
   - Manages agent-to-agent workflows
   - Coordinates multi-agent collaboration
   - Synthesizes insights from multiple agents
   - Tracks communication history

### Message Broker

In-memory message system for agent communication:
- Send messages between agents
- Retrieve conversation history
- Store message metadata
- Track topics and timestamps

## 🚀 Quick Start

### Access via REST API

**List all agents:**
```bash
curl http://localhost:8000/agents
```

**Run A2A collaboration:**
```bash
curl -X POST http://localhost:8000/a2a/collaborate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Discuss microservices architecture best practices",
    "agent_type": "a2a_orchestrator",
    "max_turns": 5
  }'
```

**Send message between agents:**
```bash
curl -X POST "http://localhost:8000/a2a/send-message?from_agent=Coordinator&to_agent=Specialist&message=Analyze%20this%20system&topic=architecture"
```

**Get conversation history:**
```bash
curl "http://localhost:8000/a2a/conversation?agent1=Coordinator&agent2=Specialist&topic=architecture"
```

**View messages:**
```bash
curl "http://localhost:8000/a2a/messages?agent=Coordinator&topic=architecture"
```

**Clear message history:**
```bash
curl -X DELETE "http://localhost:8000/a2a/clear-messages?agent=Coordinator&topic=architecture"
```

## 🔧 API Endpoints

### POST /a2a/collaborate
Run full A2A collaboration workflow
- **Params**: prompt, agent_type, max_turns
- **Response**: Agent response with collaboration results

### GET /a2a/messages
Get messages for an agent
- **Params**: agent (optional), topic (default: "general")
- **Response**: List of messages with metadata

### GET /a2a/conversation
Get conversation between two agents
- **Params**: agent1, agent2, topic
- **Response**: Full conversation transcript

### POST /a2a/send-message
Send message between agents
- **Params**: from_agent, to_agent, message, topic
- **Response**: Message object with metadata

### DELETE /a2a/clear-messages
Clear message history
- **Params**: agent (optional), topic (optional)
- **Response**: Confirmation of cleared messages

## 💻 Python Usage

### Using the A2A Client

```python
from a2a_client import A2AClient

# Create client
client = A2AClient()

# Send message
msg = client.send_message(
    "Coordinator",
    "Specialist",
    "Analyze this architecture",
    topic="infrastructure"
)

# Get conversation
conversation = client.get_conversation(
    agent1="Coordinator",
    agent2="Specialist",
    topic="infrastructure"
)

# Run collaboration
result = client.run_collaboration(
    "Discuss CI/CD best practices",
    max_turns=5
)

client.close()
```

### Direct Agent Access

```python
from agents_module.a2a_communication import (
    coordinator_agent,
    specialist_agent,
    a2a_orchestrator,
    message_broker
)
from agents import Runner

# Run coordinator agent
result = await Runner.run(
    coordinator_agent,
    input="Analyze the microservices architecture",
    max_turns=3
)

# Send message programmatically
msg = message_broker.send_message(
    "Coordinator",
    "Specialist",
    "Your expertise is needed on architecture",
    topic="infrastructure"
)

# Get conversation history
conversation = message_broker.get_conversation(
    "Coordinator",
    "Specialist",
    "infrastructure"
)
```

## 📊 Use Cases

### 1. Technical Design Review
- Coordinator: Analyzes proposed design
- Specialist: Provides expert critique
- Orchestrator: Synthesizes feedback

### 2. Problem Solving
- Coordinator: Defines problem
- Specialist: Provides solutions
- Result: Collaborative solution

### 3. Knowledge Sharing
- Coordinator: Asks questions
- Specialist: Shares expertise
- Outcome: Learned insights

### 4. Decision Making
- Both agents contribute perspectives
- Orchestrator synthesizes
- Produces informed decision

## 🔄 Communication Flow

```
User Input
    ↓
Coordinator Agent
    ↓ (sends message)
Message Broker
    ↓ (stores/retrieves)
Specialist Agent
    ↓ (processes & responds)
Message Broker
    ↓ (stores response)
A2A Orchestrator
    ↓ (synthesizes)
Final Output
```

## 📈 Message Metadata

Each message includes:
- `id`: Unique message identifier
- `timestamp`: ISO timestamp of message
- `from`: Sending agent name
- `to`: Receiving agent name
- `topic`: Topic/category
- `message`: Message content
- `status`: Message status ("sent")

## 🎨 Example Workflow

```python
# 1. Coordinator analyzes topic
coordinator_analysis = await coordinator_agent.analyze_topic("microservices")

# 2. Coordinator sends to Specialist
msg1 = message_broker.send_message(
    "Coordinator",
    "Specialist",
    "Need expertise on microservices patterns"
)

# 3. Specialist provides expertise
specialist_response = await specialist_agent.provide_expertise(
    "microservices",
    "What are the best patterns?"
)

# 4. Specialist sends response
msg2 = message_broker.send_message(
    "Specialist",
    "Coordinator",
    specialist_response
)

# 5. Retrieve full conversation
conversation = message_broker.get_conversation(
    "Coordinator",
    "Specialist",
    "microservices"
)
```

## 🔐 Security Considerations

- Messages stored in memory (ephemeral)
- No authentication by default
- Add API key validation for production
- Implement message persistence with database
- Use HTTPS for remote deployments

## 🚀 Deployment

### Local Development
```bash
python start_service.py
# A2A endpoints available at http://localhost:8000/a2a/*
```

### Docker
```bash
docker-compose up -d
# Access at http://localhost:8000/a2a/*
```

### Cloud (AWS/GCP/Azure)
Follow DEPLOYMENT_GUIDE.md
A2A endpoints available at your domain

## 📝 Future Enhancements (Phase 2+)

- Message persistence with database
- Agent memory/context retention
- Multi-agent teams (3+ agents)
- Message encryption
- Rate limiting per agent
- Audit logging
- Event streaming
- WebSocket for real-time collaboration
- Agent discovery service
- Message routing policies

## 🆘 Troubleshooting

### No messages retrieved
- Verify agents have communicated
- Check topic parameter matches
- Verify agent names are correct

### Clear messages not working
- Ensure agent name is exact match
- Verify topic is correct
- Try clearing all with no parameters

### Collaboration timeout
- Increase max_turns parameter
- Check OpenRouter API status
- Review API rate limits

## 📚 Related Documentation

- README.md - Main overview
- ARCHITECTURE.md - System design
- DEPLOYMENT_GUIDE.md - Deployment
- example_client.py - API usage examples

## ✨ Summary

The A2A Communication Protocol enables:
✅ Agent-to-agent messaging
✅ Multi-agent collaboration
✅ Conversation tracking
✅ Intelligent orchestration
✅ Knowledge sharing
✅ Complex problem-solving

**Start using A2A today!** 🚀

