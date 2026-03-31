# Opik Telemetry Integration Guide

## Overview

This guide explains how to export traces from the Python Agent Service to your self-hosted Opik server using OpenTelemetry.

## Architecture

```
Python Agent Service
       |
       | OpenTelemetry SDK
       |
       v
OTLP HTTP Exporter
       |
       | HTTP POST
       |
       v
Opik Self-Hosted Server
(localhost:5173/api/v1/private/otel/v1/traces)
       |
       v
   Trace Storage & Visualization
```

## Components

### 1. OpenTelemetry SDK
- **opentelemetry-api**: Core tracing API
- **opentelemetry-sdk**: SDK implementation
- **opentelemetry-exporter-otlp-proto-http**: HTTP exporter for OTLP

### 2. Auto-Instrumentation
- **opentelemetry-instrumentation-fastapi**: Automatic FastAPI tracing
- **opentelemetry-instrumentation-requests**: HTTP client tracing
- **opentelemetry-instrumentation-openai**: OpenAI API tracing (optional)

### 3. Configuration Module
- **otel_config.py**: Centralized configuration and setup

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements.txt includes:
```
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-exporter-otlp-proto-http>=1.20.0
opentelemetry-instrumentation-fastapi>=0.41b0
opentelemetry-instrumentation-requests>=0.41b0
opentelemetry-instrumentation-openai>=0.1.0
```

### Step 2: Configure Environment Variables

Update your `.env` file:

```bash
# Enable OpenTelemetry tracing
OTEL_ENABLED=true

# Opik server endpoint
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces

# Opik authentication (if required)
OPIK_AUTHORIZATION=your-auth-token-here

# Opik workspace
OPIK_WORKSPACE=default

# Opik project name
OPIK_PROJECT=agent-service

# Service name for telemetry
OTEL_SERVICE_NAME=python-agent-service

# Environment
ENVIRONMENT=development

# Enable console output for debugging (optional)
OTEL_CONSOLE_EXPORTER=false
```

### Step 3: Verify Configuration

Check that your Opik server is running:

```bash
curl http://localhost:5173/api/v1/private/otel/v1/traces
```

## Configuration Mapping: Java vs Python

### Java Spring Boot Configuration

```yaml
otel:
  file_format: "1.0-rc.2"
  resource:
    attributes:
      - name: service.name
        value: spring-boot-app
  tracer_provider:
    processors:
      - batch:
          exporter:
            otlp_http:
              endpoint: ${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT}
              headers:
                - name: Authorization
                  value: ${OPIK_AUTHORIZATION}
                - name: Comet-Workspace
                  value: ${OPIK_WORKSPACE}
                - name: projectName
                  value: ${OPIK_PROJECT}
```

### Python Equivalent Configuration

**Environment Variables (.env):**
```bash
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces
OPIK_AUTHORIZATION=your-token
OPIK_WORKSPACE=default
OPIK_PROJECT=agent-service
OTEL_SERVICE_NAME=python-agent-service
```

**Programmatic Setup (otel_config.py):**
```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Create resource
resource = Resource.create({
    SERVICE_NAME: "python-agent-service"
})

# Create tracer provider
tracer_provider = TracerProvider(resource=resource)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=endpoint,
    headers={
        'Authorization': auth_token,
        'Comet-Workspace': workspace,
        'projectName': project
    }
)

# Add batch processor
tracer_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)
```

## Usage

### Automatic Tracing

FastAPI endpoints are automatically instrumented:

```python
from otel_config import setup_telemetry

# In app startup
setup_telemetry(app)

# All endpoints automatically traced
@app.post("/run")
async def run_agent(request: PromptRequest):
    # Automatically creates span for this endpoint
    pass
```

### Manual Tracing

Add custom spans to your code:

```python
from otel_config import get_tracer, set_span_attributes, add_span_event

tracer = get_tracer(__name__)

# Create a span
with tracer.start_as_current_span("agent_execution") as span:
    # Add attributes
    set_span_attributes({
        "agent.type": "advanced",
        "agent.max_turns": 5,
    })
    
    # Add events
    add_span_event("agent_started")
    
    # Your code here
    result = await run_agent()
    
    # Record success
    span.set_attribute("success", True)
    add_span_event("agent_completed")
```

### Error Tracking

Automatically track errors in spans:

```python
with tracer.start_as_current_span("operation") as span:
    try:
        # Your code
        risky_operation()
    except Exception as e:
        # Record error
        span.set_attribute("error", True)
        span.set_attribute("error.type", type(e).__name__)
        add_span_event("error", {
            "error.message": str(e)
        })
        raise
```

## Span Hierarchy

The integration creates the following span structure:

```
HTTP POST /run                           [FastAPI auto-instrumentation]
├── agent_execution                      [Custom span]
│   ├── agent_selection_start            [Event]
│   ├── agent_runner                     [Custom span]
│   │   └── OpenAI API call              [Auto-instrumentation]
│   └── agent_execution_complete         [Event]
└── Response

HTTP POST /a2a/collaborate               [FastAPI auto-instrumentation]
├── a2a_collaboration                    [Custom span]
│   ├── a2a_execution_start              [Event]
│   ├── agent_runner                     [Custom span]
│   │   ├── Coordinator execution
│   │   └── Specialist execution
│   └── a2a_execution_complete           [Event]
└── Response
```

## Span Attributes

### Automatic Attributes (FastAPI)
- `http.method`: HTTP method (GET, POST, etc.)
- `http.url`: Request URL
- `http.status_code`: Response status
- `http.route`: FastAPI route path

### Custom Attributes (Agent Service)
- `agent.type`: Type of agent executed
- `agent.max_turns`: Maximum turns configured
- `prompt.length`: Length of user prompt
- `result.length`: Length of agent response
- `collaboration.type`: Type of A2A collaboration
- `success`: Whether operation succeeded
- `error`: Whether error occurred
- `error.type`: Exception type name

## Testing the Integration

### 1. Start the Service

```bash
python api_server.py
```

You should see:
```
INFO:__main__:OpenTelemetry tracing configured successfully
INFO:__main__:  Service: python-agent-service
INFO:__main__:  Endpoint: http://localhost:5173/api/v1/private/otel/v1/traces
INFO:__main__:  Workspace: default
INFO:__main__:  Project: agent-service
```

### 2. Make a Test Request

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is 2+2?",
    "agent_type": "functions",
    "max_turns": 3
  }'
```

### 3. Verify in Opik

1. Open Opik UI: `http://localhost:5173`
2. Navigate to your workspace: `default`
3. Select project: `agent-service`
4. View traces for the request

You should see:
- Trace with service name: `python-agent-service`
- Spans showing request flow
- Attributes with agent details
- Events marking execution phases

## Troubleshooting

### Issue: No traces appearing in Opik

**Check 1: Is OTEL enabled?**
```bash
# In .env file
OTEL_ENABLED=true
```

**Check 2: Is Opik server running?**
```bash
curl http://localhost:5173/api/v1/private/otel/v1/traces
```

**Check 3: Check logs**
```bash
# Enable console exporter
OTEL_CONSOLE_EXPORTER=true
```

Restart service and check console output.

**Check 4: Verify endpoint URL**
```bash
# Must match Opik's OTLP endpoint
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:5173/api/v1/private/otel/v1/traces
```

### Issue: Authentication errors

**Verify headers:**
```bash
# If Opik requires auth
OPIK_AUTHORIZATION=Bearer your-token-here

# Or basic auth
OPIK_AUTHORIZATION=Basic base64-encoded-credentials
```

**Check workspace and project:**
```bash
OPIK_WORKSPACE=default
OPIK_PROJECT=agent-service
```

These must exist in your Opik instance.

### Issue: Traces are incomplete

**Check batch processor configuration:**

The default configuration uses `BatchSpanProcessor` which batches spans before sending. This is efficient but may delay trace appearance.

For development/testing, you can modify `otel_config.py` to use `SimpleSpanProcessor`:

```python
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Instead of BatchSpanProcessor
tracer_provider.add_span_processor(
    SimpleSpanProcessor(otlp_exporter)
)
```

**Note**: `SimpleSpanProcessor` sends spans immediately but has performance overhead. Use only for debugging.

## Advanced Configuration

### Custom Span Processors

Add custom logic to spans:

```python
from opentelemetry.sdk.trace import SpanProcessor

class CustomSpanProcessor(SpanProcessor):
    def on_start(self, span, parent_context):
        # Called when span starts
        pass
    
    def on_end(self, span):
        # Called when span ends
        # Add custom logic here
        pass

# Add to tracer provider
tracer_provider.add_span_processor(CustomSpanProcessor())
```

### Sampling Configuration

Control which traces are exported:

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# Sample 50% of traces
sampler = TraceIdRatioBased(0.5)

tracer_provider = TracerProvider(
    resource=resource,
    sampler=sampler
)
```

### Multiple Exporters

Export to multiple backends:

```python
# OTLP to Opik
otlp_exporter = OTLPSpanExporter(endpoint=opik_endpoint)

# Console for debugging
console_exporter = ConsoleSpanExporter()

# Add both
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))
```

## Performance Considerations

### Batch Processing
- **Default**: `BatchSpanProcessor` with 512 max queue size
- **Export interval**: 5 seconds
- **Max export batch**: 512 spans

### Resource Usage
- **Memory**: ~10-50MB overhead for tracing
- **CPU**: <5% overhead for instrumentation
- **Network**: ~1-5KB per trace (depends on span count)

### Best Practices

1. **Use sampling in production**: Don't trace 100% of requests
2. **Batch exports**: Use `BatchSpanProcessor` not `SimpleSpanProcessor`
3. **Limit span attributes**: Don't add large data to spans
4. **Use events for checkpoints**: Events are lightweight
5. **Cleanup on shutdown**: Always call `shutdown_telemetry()`

## Integration with Docker

### Dockerfile

No changes needed - environment variables are passed at runtime.

### docker-compose.yml

Add Opik environment variables:

```yaml
services:
  agent-api:
    environment:
      - OTEL_ENABLED=true
      - OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://opik:5173/api/v1/private/otel/v1/traces
      - OPIK_WORKSPACE=default
      - OPIK_PROJECT=agent-service
      - OTEL_SERVICE_NAME=python-agent-service
```

If Opik runs in same Docker network:

```yaml
services:
  agent-api:
    networks:
      - monitoring
    environment:
      - OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://opik:5173/api/v1/private/otel/v1/traces
  
  opik:
    image: opik-server:latest
    ports:
      - "5173:5173"
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge
```

## Cloud Deployment

### Environment Variables for Production

```bash
# Production Opik endpoint
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://opik.your-domain.com/api/v1/private/otel/v1/traces

# Production service name
OTEL_SERVICE_NAME=python-agent-service-prod

# Production environment
ENVIRONMENT=production

# Enable authentication
OPIK_AUTHORIZATION=Bearer prod-token-here

# Production workspace
OPIK_WORKSPACE=production
OPIK_PROJECT=agent-service
```

### Security

1. **Use HTTPS**: Always use `https://` for production endpoints
2. **Secure credentials**: Use secret management (AWS Secrets Manager, etc.)
3. **Rotate tokens**: Regularly rotate `OPIK_AUTHORIZATION` tokens
4. **Network isolation**: Keep Opik in private network if possible

## Comparison with Java Implementation

| Aspect | Java Spring Boot | Python FastAPI |
|--------|------------------|----------------|
| Configuration | YAML declarative | Environment variables + Code |
| Auto-instrumentation | Spring Auto-config | Manual setup |
| Exporter | OTLP HTTP | OTLP HTTP |
| Headers | Via YAML config | Via dict in code |
| Sampling | Via YAML | Programmatic |
| Shutdown | Automatic | Manual in lifespan |

Both implementations achieve the same result and are interoperable via OTLP standard.

## API Reference

### otel_config.py Functions

#### `setup_telemetry(app=None)`
Initialize OpenTelemetry tracing.
- **Parameters**: `app` (optional) - FastAPI app for auto-instrumentation
- **Returns**: `TracerProvider` or `None`

#### `get_tracer(name)`
Get a tracer for creating spans.
- **Parameters**: `name` - Tracer name (use `__name__`)
- **Returns**: `Tracer` instance

#### `create_span(name, attributes=None)`
Create a custom span (context manager).
- **Parameters**: 
  - `name` - Span name
  - `attributes` - Optional dict of attributes
- **Returns**: Span context manager

#### `add_span_event(event_name, attributes=None)`
Add event to current span.
- **Parameters**:
  - `event_name` - Event name
  - `attributes` - Optional dict

#### `set_span_attributes(attributes)`
Set attributes on current span.
- **Parameters**: `attributes` - Dict of attributes

#### `shutdown_telemetry()`
Shutdown tracing and flush spans.

## Examples

### Example 1: Basic Agent Execution Tracing

```python
from otel_config import get_tracer, set_span_attributes, add_span_event

tracer = get_tracer(__name__)

async def execute_agent(agent_type: str, prompt: str):
    with tracer.start_as_current_span("agent_execution") as span:
        set_span_attributes({
            "agent.type": agent_type,
            "prompt": prompt[:100]  # First 100 chars
        })
        
        add_span_event("agent_started")
        
        result = await agent.run(prompt)
        
        set_span_attributes({
            "result.length": len(result),
            "success": True
        })
        
        add_span_event("agent_completed")
        
        return result
```

### Example 2: A2A Communication Tracing

```python
async def a2a_collaboration(topic: str):
    with tracer.start_as_current_span("a2a_collaboration") as span:
        set_span_attributes({"topic": topic})
        
        # Coordinator span
        with tracer.start_as_current_span("coordinator_execution"):
            coordinator_result = await coordinator.analyze(topic)
            add_span_event("coordinator_complete")
        
        # Specialist span
        with tracer.start_as_current_span("specialist_execution"):
            specialist_result = await specialist.provide_expertise(topic)
            add_span_event("specialist_complete")
        
        add_span_event("collaboration_complete")
        return {"coordinator": coordinator_result, "specialist": specialist_result}
```

### Example 3: Error Handling with Tracing

```python
async def risky_operation():
    with tracer.start_as_current_span("risky_operation") as span:
        try:
            add_span_event("operation_started")
            result = await perform_operation()
            
            span.set_attribute("success", True)
            add_span_event("operation_completed")
            return result
            
        except ValueError as e:
            span.set_attribute("error", True)
            span.set_attribute("error.type", "ValueError")
            add_span_event("error", {
                "error.message": str(e),
                "error.stack": traceback.format_exc()
            })
            raise
```

## Next Steps

1. **Monitor your traces**: Regularly check Opik dashboard
2. **Optimize sampling**: Adjust sampling rate for production
3. **Add custom spans**: Instrument critical code paths
4. **Set up alerts**: Configure Opik alerts for errors
5. **Analyze performance**: Use traces to identify bottlenecks

## Resources

- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [OTLP Specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/otlp.md)
- [Opik Documentation](https://www.comet.com/docs/opik/)
- [OpenTelemetry Configuration Schema](https://github.com/open-telemetry/opentelemetry-configuration)

## Support

For issues or questions:
1. Check Opik server logs
2. Enable console exporter for debugging
3. Verify environment variables
4. Check network connectivity to Opik server

