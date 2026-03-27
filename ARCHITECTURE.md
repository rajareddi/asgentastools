# System Architecture & Setup Guide

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        End Users                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Web UI     │  │  API Client  │  │  Direct API  │       │
│  │ (Streamlit)  │  │   (Python)   │  │   (REST)     │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │               │
├─────────┼─────────────────┼─────────────────┼───────────────┤
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                │
│                    ┌──────▼────────┐                        │
│                    │  Nginx Proxy  │                        │
│                    │  (SSL/TLS)    │                        │
│                    │  Rate Limit   │                        │
│                    └──────┬────────┘                        │
│                           │                                │
├───────────────────────────┼───────────────────────────────┤
│                           │                               │
│                    ┌──────▼────────┐                       │
│                    │  FastAPI      │                       │
│                    │  API Server   │                       │
│                    │  :8000        │                       │
│                    └──────┬────────┘                       │
│                           │                               │
│         ┌─────────────────┼─────────────────┐             │
│         │                 │                 │             │
│    ┌────▼────┐    ┌──────▼──────┐   ┌──────▼────┐        │
│    │Advanced │    │  Function   │   │   Health  │        │
│    │Agent    │    │  Tools      │   │   Check   │        │
│    │         │    │  Agent      │   │           │        │
│    └────┬────┘    └──────┬──────┘   └──────────┘        │
│         │                │                               │
├─────────┼────────────────┼───────────────────────────────┤
│         │                │                               │
│         └────────┬───────┘                               │
│                  │                                       │
│            ┌─────▼──────┐                                │
│            │ OpenRouter │                                │
│            │ API (LLM)  │                                │
│            └────────────┘                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 🔧 Component Details

### 1. **Frontend Layer**
- **Streamlit UI** (`streamlit_ui.py`)
  - Interactive web interface
  - Real-time response display
  - Agent selection and configuration
  - Port: 8501

- **API Documentation**
  - Swagger UI: `/docs`
  - ReDoc: `/redoc`

### 2. **API Layer**
- **FastAPI Server** (`api_server.py` or `api_server_prod.py`)
  - RESTful endpoints
  - Request validation
  - Error handling
  - Logging and monitoring
  - Port: 8000

### 3. **Proxy Layer**
- **Nginx** (`nginx.conf`)
  - SSL/TLS termination
  - Rate limiting
  - Load balancing
  - Security headers
  - HTTP compression

### 4. **Agent Layer**
- **Advanced Orchestrator** - Research + Writing agents
- **Function Tools Agent** - Utilities and calculations
- Located in `agents_module/`

### 5. **LLM Layer**
- **OpenRouter API**
  - Multi-model LLM access
  - Cost efficient
  - Fallback support

## 📁 Directory Structure

```
python_workspaces/
├── api_server.py              # Main FastAPI server
├── api_server_prod.py         # Production-grade server
├── streamlit_ui.py            # Web UI
├── start_service.py           # Service launcher
├── test_setup.py              # Setup verification
├── example_client.py          # Python client example
│
├── agents_module/
│   ├── __init__.py
│   ├── advanced_agent.py      # Orchestrator agent
│   └── function_tools_agent.py # Utility agent
│
├── 3_1_function_tools/        # Example: Function tools
├── 3_3_agents_as_tools/       # Example: Advanced agents
│
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── .dockerignore              # Docker ignore rules
│
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Docker orchestration
├── nginx.conf                 # Nginx configuration
│
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── QUICK_START.md             # Quick start guide
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
└── ARCHITECTURE.md            # This file
```

## 🚀 Deployment Modes

### Mode 1: Local Development
```bash
python start_service.py
```
- UI: http://localhost:8501
- API: http://localhost:8000
- No proxy, direct connection

### Mode 2: Docker Local
```bash
docker-compose up -d
```
- Containerized application
- Isolated environment
- Same ports as local

### Mode 3: Production Cloud
```
Cloud Provider (AWS/GCP/Azure)
    ↓
  Load Balancer
    ↓
Nginx (SSL/TLS)
    ↓
FastAPI Server
    ↓
OpenRouter API
```

## 🔐 Security Layers

### 1. **API Key Management**
- Environment variable based
- Never committed to git
- Rotation capability

### 2. **HTTPS/SSL**
- Let's Encrypt certificates
- TLS 1.2+ only
- HSTS headers

### 3. **Rate Limiting**
- General: 10 req/s
- API: 30 req/s
- Configurable per endpoint

### 4. **Container Security**
- Non-root user (UID 1000)
- Minimal base image
- Health checks

### 5. **Network Security**
- CORS configuration
- Security headers
- Firewall rules

## 📊 Data Flow

### Request Flow
```
Client Request
    ↓
Nginx (Rate Limit, SSL)
    ↓
FastAPI (Validate, Log)
    ↓
Select Agent
    ↓
OpenRouter API Call
    ↓
Process Response
    ↓
Return Result
```

### Response Time
- Typical: 5-30 seconds
- Maximum: 300 seconds (5 minutes)
- Depends on agent complexity and OpenRouter latency

## 🔄 Agent Execution Flow

```
User Prompt
    ↓
API Server Receives Request
    ↓
Initialize Agent
    ↓
Agent Turn 1
    ├─ Process Input
    ├─ Call Tools (if needed)
    ├─ Generate Response
    └─ Check if Done?
         ├─ Yes → Return
         └─ No → Next Turn
    ↓
Agent Turn 2-N
    (Same as Turn 1)
    ↓
Final Output
    ↓
Return to Client
```

## 📈 Scalability

### Horizontal Scaling
```
Load Balancer
    ├─ API Server 1
    ├─ API Server 2
    └─ API Server N
```

### Vertical Scaling
- Increase container resources
- Multi-worker processes
- Connection pooling

### Configuration
```yaml
docker-compose.yml:
  resources:
    limits:
      cpus: '4'
      memory: 8G
```

## 🔍 Monitoring & Logging

### Metrics Collected
- Total requests
- Error count
- Success rate
- Execution time
- Agent usage

### Endpoints
- `/health` - Server health
- `/stats` - Statistics
- `/info` - Server info

### Log Levels
- DEBUG: Detailed troubleshooting
- INFO: General operations
- WARNING: Issues
- ERROR: Failures

## 🔧 Configuration Options

### Environment Variables
```bash
# Required
OPENROUTER_API_KEY=sk-...

# Optional
HOST=0.0.0.0              # API host
PORT=8000                 # API port
DEBUG=False               # Debug mode
PYTHONUNBUFFERED=1        # For Docker
```

### API Configuration
```python
# In api_server.py
max_turns=5              # Default agent iterations
timeout=300              # Response timeout
rate_limit=10            # Requests per second
```

### UI Configuration
```python
# In streamlit_ui.py
page_config_layout="wide"
theme="light"
```

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
python test_setup.py
```

### Load Tests
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/health
```

## 📞 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Change port in config |
| API not responding | Check logs, restart container |
| High latency | Increase timeouts, check OpenRouter |
| Memory issues | Increase container limits |
| SSL errors | Verify certificates, check dates |

### Debug Mode
```bash
DEBUG=True python api_server.py
```

### View Logs
```bash
# Docker
docker-compose logs -f agent-api

# Python
python api_server.py 2>&1 | tee api.log
```

## 🔗 Integration Points

### OpenRouter API
- Endpoint: `https://openrouter.ai/api/v1`
- Models: 100+ LLMs available
- Docs: https://openrouter.ai/docs

### Streamlit
- Framework: Streamlit 1.46+
- Features: Real-time updates, caching
- Docs: https://docs.streamlit.io/

### FastAPI
- Framework: FastAPI 0.104+
- Features: Auto docs, validation
- Docs: https://fastapi.tiangolo.com/

## 📚 Performance Tuning

### API Server
- Workers: 4 (production)
- Connections: 100 (concurrent)
- Timeout: 300s (default)

### Nginx
- Worker connections: 1024
- Keepalive: 65s
- Buffer sizes: Optimized

### Docker
- Memory: 2-4GB recommended
- CPU: 2+ cores recommended
- Storage: 2GB minimum

## 🚀 Next Steps

1. **Read QUICK_START.md** - Get up and running
2. **Review DEPLOYMENT_GUIDE.md** - Deploy to cloud
3. **Customize agents** - Add domain-specific logic
4. **Monitor production** - Setup logging/metrics
5. **Scale infrastructure** - Add load balancing

---

**For detailed deployment, see DEPLOYMENT_GUIDE.md**

