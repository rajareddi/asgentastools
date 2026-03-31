  # Agent Service - Interactive AI Agents with OpenRouter

A complete web service for running AI agents with interactive prompts, accessible via web UI and REST API.

## 🎯 Features

- ✨ **Interactive Web UI** - Streamlit-based interface for easy agent interaction
- 🔌 **REST API** - FastAPI backend with full documentation (Swagger/ReDoc)
- 🤖 **Multiple Agents** - Advanced orchestrator + Function tools agents
- 🤝 **Agent-to-Agent (A2A) Communication** - Agents collaborate to solve problems
- 🔗 **MCP Integration** - Model Context Protocol for external service access
- 🌐 **OpenRouter Integration** - Access multiple LLM models through OpenRouter
- 📊 **OpenTelemetry Tracing** - Export traces to self-hosted Opik server
- 🐳 **Docker Support** - Easy containerization and deployment
- ☁️ **Cloud Ready** - Deploy to AWS, GCP, Azure, Heroku, etc.
- 🏗️ **Production Grade** - Nginx reverse proxy, SSL, rate limiting
- 🔒 **Secure** - Environment-based API key management, HTTPS, non-root containers

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenRouter API key:**
   ```bash
   # Create/update .env file
   echo "OPENROUTER_API_KEY=your_api_key_here" > .env
   ```

3. **Start the service:**
   ```bash
   python start_service.py
   ```

4. **Access:**
   - 🎨 **UI**: http://localhost:8501
   - 📡 **API**: http://localhost:8000
   - 📖 **API Docs**: http://localhost:8000/docs

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t agent-service:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -p 8501:8501 \
  -e OPENROUTER_API_KEY=your_api_key \
  agent-service:latest
```

## ☁️ Cloud Deployment

### AWS EC2

```bash
# See DEPLOYMENT_GUIDE.md for detailed AWS setup with:
# - EC2 instance configuration
# - Route 53 domain setup
# - Let's Encrypt SSL certificates
# - Nginx reverse proxy
```

### Google Cloud Run

```bash
gcloud run deploy agent-service \
  --source . \
  --platform managed \
  --set-env-vars OPENROUTER_API_KEY=your_api_key
```

### Heroku

```bash
heroku create your-app-name
heroku config:set OPENROUTER_API_KEY=your_api_key
git push heroku main
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions for all platforms.

## 📖 API Documentation

### Health Check
```bash
curl http://localhost:8000/health
```

### List Available Agents
```bash
curl http://localhost:8000/agents
```

### Run Agent
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Research the benefits of AI in healthcare",
    "agent_type": "advanced",
    "max_turns": 5
  }'
```

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤖 Available Agents

### Advanced Orchestrator
- **Type**: Orchestrator
- **Purpose**: Content creation with research and writing
- **Tools**: Research agent, Writing agent
- **Use**: Complex research and writing tasks

### Function Tools Agent
- **Type**: Utility
- **Purpose**: Mathematical calculations and utilities
- **Tools**: 
  - `add_numbers`: Add two numbers
  - `multiply_numbers`: Multiply two numbers
  - `get_weather`: Get weather info (mock)
  - `convert_temperature`: Convert between Celsius/Fahrenheit

## 📁 Project Structure

```
python_workspaces/
├── api_server.py              # FastAPI server
├── streamlit_ui.py            # Streamlit web interface
├── start_service.py           # Service startup script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── nginx.conf                 # Nginx reverse proxy config
├── DEPLOYMENT_GUIDE.md        # Detailed deployment guide
├── README.md                  # This file
│
├── agents_module/             # Agent definitions
│   ├── __init__.py
│   ├── advanced_agent.py      # Orchestrator agent
│   └── function_tools_agent.py # Utility agent
│
├── 3_1_function_tools/        # Original function tools examples
├── 3_3_agents_as_tools/       # Advanced agent examples
└── .env                       # Environment variables (not in git)
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your_api_key_here

# Optional Server Configuration (defaults shown)
HOST=0.0.0.0
PORT=8000
PYTHONUNBUFFERED=1

# Optional OpenTelemetry/Opik Tracing
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces
OPIK_WORKSPACE=default
OPIK_PROJECT=agent-service
OTEL_SERVICE_NAME=python-agent-service
OTEL_CONSOLE_EXPORTER=false  # Set to true for debugging
ENVIRONMENT=development
```

See `.env.example` for complete configuration options.

## 📊 Monitoring & Observability

### OpenTelemetry Integration

The service includes built-in OpenTelemetry tracing that exports to self-hosted Opik servers:

- **Automatic FastAPI instrumentation** - All HTTP requests traced
- **Custom spans** - Agent execution, A2A communication tracked
- **Error tracking** - Exceptions captured with context
- **OTLP HTTP export** - Standard protocol compatible with Opik

**Quick Setup:**

1. Configure Opik endpoint in `.env`:
   ```bash
   OTEL_ENABLED=true
   OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces
   ```

2. Start service:
   ```bash
   python api_server.py
   ```

3. View traces in Opik dashboard at `http://localhost:5173`

**Documentation:**
- `OPIK_TELEMETRY_GUIDE.md` - Comprehensive tracing guide
- `OTEL_QUICKSTART.md` - Quick start guide
- `test_otel_integration.py` - Integration test suite

### Nginx Configuration

The `nginx.conf` file includes:
- SSL/TLS support with Let's Encrypt certificates
- Rate limiting (10 req/s general, 30 req/s API)
- Security headers (HSTS, X-Frame-Options, etc.)
- HTTP/2 support
- Proxy configuration for API and UI

## 🔒 Security

- ✅ Non-root Docker container user
- ✅ Environment variable API key management
- ✅ HTTPS/SSL with rate limiting
- ✅ Security headers configured
- ✅ Container health checks
- ✅ Minimal base image (python:3.11-slim)

## 📊 Monitoring

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# Docker health
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f agent-api

# Last 100 lines with timestamps
docker-compose logs --tail=100 -f --timestamps agent-api
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

### API Connection Error
```bash
# Check if containers are running
docker-compose ps

# Restart services
docker-compose restart

# Check logs
docker-compose logs agent-api
```

### Memory Issues
```bash
# Check memory usage
docker stats agent-api

# Increase memory limit in docker-compose.yml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🔗 Resources

### External
- **OpenRouter**: https://openrouter.ai/
- **OpenAI Agents**: https://openai.github.io/openai-agents-python/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://streamlit.io/
- **Docker**: https://www.docker.com/
- **Nginx**: https://nginx.org/
- **OpenTelemetry**: https://opentelemetry.io/
- **Opik**: https://www.comet.com/docs/opik/

### Project Documentation
- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **A2A_PACKAGE_SETUP.md** - Agent-to-Agent communication setup
- **MCP_INTEGRATION_GUIDE.md** - Model Context Protocol integration
- **OPIK_TELEMETRY_GUIDE.md** - OpenTelemetry tracing guide
- **OTEL_QUICKSTART.md** - Quick start for OpenTelemetry
- **INTERVIEW_PREP.md** - Interview preparation guide
- **ARCHITECTURE.md** - System architecture details
- **ROADMAP.md** - Future development plans

## 📞 Support

For issues, questions, or suggestions:
1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review API documentation at http://localhost:8000/docs
3. Check service logs: `docker-compose logs -f`

## 🎓 Usage Examples

### Via Web UI
1. Navigate to http://localhost:8501
2. Select agent type
3. Enter prompt
4. Adjust max turns if needed
5. Click "Run Agent"
6. View results

### Via API
```bash
# Example: Research AI in healthcare
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Research the benefits of AI in healthcare",
    "agent_type": "advanced",
    "max_turns": 5
  }'
```

### Via Python
```python
import requests

response = requests.post(
    'http://localhost:8000/run',
    json={
        'prompt': 'What is 42 + 8?',
        'agent_type': 'functions',
        'max_turns': 3
    }
)

print(response.json()['result'])
```

---

**Made with ❤️ using OpenAI Agents & OpenRouter**

