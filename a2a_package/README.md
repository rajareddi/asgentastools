# A2A Communication Package

Agent-to-Agent (A2A) Communication Protocol for OpenAI Agents Framework

## Features

- **Agent Messaging**: Direct messaging between agents
- **Conversation History**: Track all agent communications
- **Topic Filtering**: Organize messages by topics
- **Multi-Agent Orchestration**: Coordinate multiple agents
- **REST API Integration**: Full REST API support
- **Python Client**: Easy-to-use Python client
- **Message Broker**: In-memory message storage

## Installation

```bash
# From PyPI (coming soon)
pip install a2a-communication

# From source
cd a2a_package
pip install -e .
```

## Quick Start

### Python Usage

```python
from a2a_package import coordinator_agent, specialist_agent, a2a_orchestrator
from a2a_package import message_broker
from agents import Runner

# Send message
msg = message_broker.send_message(
    "Coordinator",
    "Specialist",
    "Analyze this architecture",
    topic="infrastructure"
)

# Get conversation
conversation = message_broker.get_conversation(
    "Coordinator",
    "Specialist",
    "infrastructure"
)

# Run orchestrator
result = await Runner.run(
    a2a_orchestrator,
    input="Discuss best practices for microservices",
    max_turns=5
)
```

### REST API Usage

```bash
# Send message
curl -X POST "http://localhost:8000/a2a/send-message?from_agent=Coordinator&to_agent=Specialist&message=Hello&topic=test"

# Get conversation
curl "http://localhost:8000/a2a/conversation?agent1=Coordinator&agent2=Specialist&topic=test"

# Run collaboration
curl -X POST http://localhost:8000/a2a/collaborate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Discuss microservices","agent_type":"a2a_orchestrator","max_turns":5}'
```

### Python Client

```python
from a2a_package import A2AClient

client = A2AClient()

# Send message
msg = client.send_message("Coordinator", "Specialist", "Your expertise needed")

# Get conversation
conversation = client.get_conversation(agent1="Coordinator", agent2="Specialist")

# Run collaboration
result = client.run_collaboration("Discuss best practices")

client.close()
```

## Architecture

```
┌─────────────────────────────────────┐
│  a2a_package                        │
├─────────────────────────────────────┤
│ ├── __init__.py      (Package init) │
│ ├── core.py          (MessageBroker)│
│ ├── agents.py        (A2A Agents)   │
│ ├── client.py        (REST Client)  │
│ └── setup.py         (Setup config) │
└─────────────────────────────────────┘
         ↓
    Agents Framework
         ↓
    OpenRouter API
```

## Components

### MessageBroker (core.py)
- `send_message()`: Send messages between agents
- `get_messages()`: Get messages for agent
- `get_conversation()`: Get full conversation
- `clear_messages()`: Clear message history
- `get_stats()`: Get broker statistics

### Agents (agents.py)
- **Coordinator Agent**: Manages communication and analysis
- **Specialist Agent**: Provides expertise and collaboration
- **A2A Orchestrator**: Orchestrates multi-agent workflows

### Client (client.py)
- `send_message()`: Send message via API
- `get_messages()`: Get messages via API
- `get_conversation()`: Get conversation via API
- `run_collaboration()`: Run A2A collaboration
- `clear_messages()`: Clear history via API
- `get_stats()`: Get statistics via API

## Use Cases

1. **Technical Reviews**: Coordinator + Specialist analyze designs
2. **Problem Solving**: Multi-perspective problem analysis
3. **Knowledge Sharing**: Experts contribute domain knowledge
4. **Decision Making**: Collaborative decision support

## Documentation

- [A2A_COMMUNICATION.md](../A2A_COMMUNICATION.md) - Full documentation
- [A2A_QUICK_REFERENCE.md](../A2A_QUICK_REFERENCE.md) - Quick reference
- [test_a2a_communication.py](../test_a2a_communication.py) - Examples

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=a2a_package tests/

# Run examples
python test_a2a_communication.py
```

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please see CONTRIBUTING.md

## Support

For issues and questions:
1. Check documentation
2. Review examples
3. Open an issue on GitHub
4. Check tests for usage patterns

## Version History

### 1.0.0 (2026-03-27)
- Initial release
- Core messaging system
- Three agents (Coordinator, Specialist, Orchestrator)
- REST API endpoints
- Python client
- Full documentation

---

**Built with OpenAI Agents Framework** 🚀

