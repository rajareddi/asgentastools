# Quick Start: OpenTelemetry Integration with Opik

## Overview
This guide will help you quickly set up and test OpenTelemetry tracing with your self-hosted Opik server.

## Prerequisites
- Python 3.11+
- Self-hosted Opik server running (typically on port 5173)
- OPENROUTER_API_KEY configured

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `opentelemetry-api` - Core OpenTelemetry API
- `opentelemetry-sdk` - OpenTelemetry SDK
- `opentelemetry-exporter-otlp-proto-http` - OTLP HTTP exporter for Opik
- `opentelemetry-instrumentation-fastapi` - Auto-instrumentation for FastAPI
- `opentelemetry-instrumentation-requests` - Auto-instrumentation for HTTP requests

## Step 2: Configure Environment Variables

Edit your `.env` file:

```bash
# Required: OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Enable OpenTelemetry (default: true)
OTEL_ENABLED=true

# Opik server endpoint (adjust if different)
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces

# Opik workspace (default: default)
OPIK_WORKSPACE=default

# Opik project name
OPIK_PROJECT=agent-service

# Service name for telemetry
OTEL_SERVICE_NAME=python-agent-service

# Environment (development, staging, production)
ENVIRONMENT=development

# Optional: Enable console output for debugging
OTEL_CONSOLE_EXPORTER=false

# Optional: Opik authorization token (if required)
OPIK_AUTHORIZATION=
```

## Step 3: Verify Opik Server is Running

Check if your Opik server is accessible:

```bash
# Test connection
curl http://localhost:5173/api/v1/private/otel/v1/traces

# Or test with PowerShell
Invoke-WebRequest -Uri "http://localhost:5173/api/v1/private/otel/v1/traces" -Method GET
```

If Opik is running, you should get a response (may be an error about method, but confirms connectivity).

## Step 4: Start the Agent Service

```bash
python api_server.py
```

You should see log messages:

```
INFO:__main__:OpenTelemetry tracing configured successfully
INFO:__main__:  Service: python-agent-service
INFO:__main__:  Endpoint: http://localhost:5173/api/v1/private/otel/v1/traces
INFO:__main__:  Workspace: default
INFO:__main__:  Project: agent-service
INFO:__main__:FastAPI instrumentation enabled
[*] Agent API Server starting...
[*] Starting Agent API Server on 0.0.0.0:8000
```

## Step 5: Generate Test Traces

### Test 1: Simple Agent Request

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is 2+2?",
    "agent_type": "functions",
    "max_turns": 3
  }'
```

### Test 2: A2A Collaboration

```bash
curl -X POST http://localhost:8000/a2a/collaborate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain microservices architecture",
    "agent_type": "a2a_orchestrator",
    "max_turns": 5
  }'
```

### Test 3: Health Check

```bash
curl http://localhost:8000/health
```

## Step 6: View Traces in Opik

1. Open Opik UI in your browser:
   ```
   http://localhost:5173
   ```

2. Navigate to your workspace: `default`

3. Select project: `agent-service`

4. You should see traces appearing with:
   - Service name: `python-agent-service`
   - Trace spans showing the request flow
   - Attributes with agent details
   - Events marking execution phases

## Step 7: Understanding the Trace Structure

Each trace will show:

```
HTTP POST /run                           [Auto-instrumented]
├── agent_execution                      [Custom span]
│   ├── agent_selection_start            [Event]
│   ├── agent_runner                     [Custom span]
│   │   └── OpenAI API call             [If instrumented]
│   └── agent_execution_complete         [Event]
└── Response
```

### Span Attributes You'll See:

- `http.method`: POST
- `http.url`: /run
- `http.status_code`: 200
- `agent.type`: functions (or other agent type)
- `agent.max_turns`: 3
- `prompt.length`: [length of prompt]
- `result.length`: [length of result]
- `success`: true/false
- `error`: true (if error occurred)

## Troubleshooting

### Problem: No traces appearing in Opik

**Solution 1: Enable console exporter to see traces locally**

Edit `.env`:
```bash
OTEL_CONSOLE_EXPORTER=true
```

Restart the server. You should see traces printed to console.

**Solution 2: Check Opik endpoint**

Verify the endpoint URL is correct:
```bash
# Should match your Opik server
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces
```

**Solution 3: Check Opik workspace and project**

Ensure workspace and project exist in Opik:
```bash
OPIK_WORKSPACE=default
OPIK_PROJECT=agent-service
```

### Problem: OpenTelemetry import errors

**Solution: Reinstall packages**

```bash
pip uninstall opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-requests
```

### Problem: Authentication errors

**Solution: Add authorization header**

If your Opik server requires authentication, set:
```bash
OPIK_AUTHORIZATION=Bearer your-token-here
```

Or for basic auth:
```bash
OPIK_AUTHORIZATION=Basic base64-encoded-credentials
```

### Problem: Traces are delayed

**Solution: Use SimpleSpanProcessor for immediate export (debugging only)**

Edit `otel_config.py`, replace `BatchSpanProcessor` with `SimpleSpanProcessor`:

```python
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Instead of:
# tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Use:
tracer_provider.add_span_processor(SimpleSpanProcessor(otlp_exporter))
```

**Note:** This reduces performance but ensures traces are sent immediately.

## Testing with PowerShell

If you're on Windows, use these PowerShell commands:

### Test agent execution:
```powershell
$body = @{
    prompt = "What is 2+2?"
    agent_type = "functions"
    max_turns = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/run" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Test A2A collaboration:
```powershell
$body = @{
    prompt = "Explain microservices"
    agent_type = "a2a_orchestrator"
    max_turns = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/a2a/collaborate" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

## Advanced: Custom Span Creation

You can add custom spans to your own code:

```python
from otel_config import get_tracer, set_span_attributes, add_span_event

tracer = get_tracer(__name__)

def my_function():
    with tracer.start_as_current_span("my_custom_operation") as span:
        # Add attributes
        set_span_attributes({
            "operation.type": "data_processing",
            "data.size": 1024
        })
        
        # Add events
        add_span_event("processing_started")
        
        # Your code here
        result = process_data()
        
        # Mark success
        span.set_attribute("success", True)
        add_span_event("processing_completed")
        
        return result
```

## Disabling OpenTelemetry

If you want to disable tracing temporarily:

```bash
# In .env file
OTEL_ENABLED=false
```

Restart the service. The server will run without tracing.

## Production Recommendations

For production deployment:

1. **Use HTTPS endpoint:**
   ```bash
   OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://opik.your-domain.com/api/v1/private/otel/v1/traces
   ```

2. **Configure authentication:**
   ```bash
   OPIK_AUTHORIZATION=Bearer production-token
   ```

3. **Set environment:**
   ```bash
   ENVIRONMENT=production
   ```

4. **Disable console exporter:**
   ```bash
   OTEL_CONSOLE_EXPORTER=false
   ```

5. **Use production service name:**
   ```bash
   OTEL_SERVICE_NAME=python-agent-service-prod
   ```

6. **Configure sampling** (edit `otel_config.py`):
   ```python
   from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
   
   # Sample 10% of traces in production
   sampler = TraceIdRatioBased(0.1)
   tracer_provider = TracerProvider(resource=resource, sampler=sampler)
   ```

## Files Reference

- **otel_config.py** - OpenTelemetry configuration and setup
- **api_server.py** - FastAPI server with tracing integrated
- **OPIK_TELEMETRY_GUIDE.md** - Comprehensive telemetry guide
- **otel-config.yaml** - Configuration reference (documentation)
- **.env** - Environment variables

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure environment variables
3. ✅ Start Opik server
4. ✅ Start agent service
5. ✅ Generate test traces
6. ✅ View traces in Opik dashboard
7. 📊 Analyze performance and errors
8. 🔧 Add custom spans for specific operations
9. 📈 Set up alerts in Opik
10. 🚀 Deploy to production with appropriate configuration

## Support

For detailed information, see:
- `OPIK_TELEMETRY_GUIDE.md` - Complete telemetry documentation
- `otel-config.yaml` - Configuration reference
- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [Opik Documentation](https://www.comet.com/docs/opik/)

## Comparison with Java

Your Java application uses Spring Boot declarative YAML config. This Python implementation achieves the same result using:

| Aspect | Java (Spring Boot) | Python (FastAPI) |
|--------|-------------------|------------------|
| Config | YAML file | Environment variables + Code |
| Setup | Auto-configuration | Manual in `otel_config.py` |
| Instrumentation | Spring Boot Auto | OpenTelemetry SDK |
| Exporter | OTLP HTTP | OTLP HTTP (same) |
| Headers | In YAML | In Python dict |
| Result | ✅ Traces to Opik | ✅ Traces to Opik |

Both work with the same Opik backend via OTLP standard!

---

**Ready to trace! 🚀**

