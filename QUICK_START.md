# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Verify Setup
```bash
python test_setup.py
```
Expected output: `3/3 tests passed`

### Step 2: Start the Service
```bash
python start_service.py
```

Wait for output:
```
🎉 Services are running!
📍 Access points:
   UI:         http://localhost:8501
   API:        http://localhost:8000
   API Docs:   http://localhost:8000/docs
```

### Step 3: Access the Service

**Option A: Web UI (Recommended)**
- Open browser: http://localhost:8501
- Select an agent
- Enter your prompt
- Click "Run Agent"

**Option B: API**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the benefits of AI?",
    "agent_type": "advanced",
    "max_turns": 5
  }'
```

**Option C: Python Client**
```bash
python example_client.py
```

## 📋 Available Agents

### 1. Advanced Orchestrator (`advanced`)
- Research specialist + Writing specialist
- Best for: Content creation, research tasks
- Example: "Write a comprehensive guide on AI in healthcare"

### 2. Function Tools (`functions`)
- Calculator + Weather + Temperature converter
- Best for: Calculations, utility tasks
- Example: "What is 42 + 8? Convert 100°F to Celsius"

## 🔧 Configuration

### Change API Port
Edit `api_server.py`:
```python
port = int(os.getenv("PORT", 8001))  # Change from 8000 to 8001
```

### Change UI Port
Edit `start_service.py`:
```bash
--server.port=8502  # Change from 8501 to 8502
```

### Use Different LLM Model
The service uses OpenRouter which supports multiple models. To change the model:

Edit `api_server.py` or `streamlit_ui.py` to pass model parameter:
```python
# Add model parameter to AsyncOpenAI
openrouter_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={"HTTP-Referer": "your-app-name"}
)
```

Available models at: https://openrouter.ai/models

## 🐳 Docker Deployment

### Build and Run
```bash
docker-compose up -d
```

### Access
- UI: http://localhost:8501
- API: http://localhost:8000

### Stop
```bash
docker-compose down
```

## ☁️ Deploy to Cloud

### AWS EC2
1. Launch Ubuntu 22.04 instance
2. Clone repository
3. Configure .env with API key
4. Run: `docker-compose up -d`
5. Setup domain with Route 53
6. Configure SSL with Let's Encrypt

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

### Google Cloud Run
```bash
gcloud run deploy agent-service \
  --source . \
  --set-env-vars OPENROUTER_API_KEY=your_key
```

### Heroku
```bash
heroku create your-app-name
heroku config:set OPENROUTER_API_KEY=your_key
git push heroku main
```

## 🔒 Important Notes

1. **Never commit .env file** - It contains your API key
2. **Use environment variables** for production
3. **Enable HTTPS** when accessing remotely
4. **Rate limiting is configured** - Don't exceed 10 req/s
5. **Container runs as non-root user** for security

## 📊 Monitoring

### View Logs
```bash
docker-compose logs -f agent-api
```

### Check Health
```bash
curl http://localhost:8000/health
```

### Monitor Resources
```bash
docker stats agent-api
```

## 🆘 Common Issues

### "Port already in use"
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### "Cannot connect to API"
- Check if API server is running: `docker-compose ps`
- Check logs: `docker-compose logs agent-api`
- Restart: `docker-compose restart agent-api`

### "API key error"
- Verify OPENROUTER_API_KEY is set: `echo $OPENROUTER_API_KEY`
- Check .env file exists
- Restart services: `docker-compose restart`

## 📚 Next Steps

1. **Customize agents** - Edit files in `agents_module/`
2. **Add new tools** - Create new function_tool decorated functions
3. **Deploy to cloud** - Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
4. **Add authentication** - Implement API key validation in FastAPI
5. **Setup monitoring** - Add logging and metrics collection

## 🔗 Resources

- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenRouter**: https://openrouter.ai/
- **OpenAI Agents**: https://openai.github.io/openai-agents-python/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://docs.streamlit.io/

## 💡 Example Prompts

### Advanced Agent
- "Research the impact of machine learning on healthcare and write a comprehensive report"
- "What are the latest trends in AI? Write about them in a casual style"
- "Analyze the benefits and drawbacks of remote work"

### Function Tools Agent
- "Calculate the sum of 123 and 456"
- "What's the weather in New York?"
- "Convert 98.6 Fahrenheit to Celsius"
- "Multiply 12 by 8 and tell me the result"

## ✅ Checklist

Before deploying to production:
- [ ] Test locally with `python start_service.py`
- [ ] Verify all agents work with example_client.py
- [ ] Configure OPENROUTER_API_KEY
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Test Docker build locally
- [ ] Configure domain and DNS
- [ ] Setup health checks
- [ ] Document API changes

---

**Happy coding! 🚀**

