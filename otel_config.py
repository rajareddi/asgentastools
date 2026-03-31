"""
OpenTelemetry Configuration for Opik Self-Hosted Server
Exports traces to Opik using OTLP HTTP exporter
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class OpikTelemetryConfig:
    """Configuration for OpenTelemetry tracing to Opik"""
    
    def __init__(self):
        # Opik/OTLP Configuration
        self.otel_endpoint = os.getenv(
            'OTEL_EXPORTER_OTLP_TRACES_ENDPOINT',
            'http://localhost:5173/api/v1/private/otel/v1/traces'
        )
        self.opik_authorization = os.getenv('OPIK_AUTHORIZATION', '')
        self.opik_workspace = os.getenv('OPIK_WORKSPACE', 'default')
        self.opik_project = os.getenv('OPIK_PROJECT', 'agent-service')
        self.service_name = os.getenv('OTEL_SERVICE_NAME', 'python-agent-service')
        self.enable_console_exporter = os.getenv('OTEL_CONSOLE_EXPORTER', 'false').lower() == 'true'
        self.otel_enabled = os.getenv('OTEL_ENABLED', 'true').lower() == 'true'
        
    def get_headers(self) -> dict:
        """Get headers for OTLP exporter"""
        headers = {
            'Comet-Workspace': self.opik_workspace,
            'projectName': self.opik_project,
        }
        
        # Add authorization header if provided
        if self.opik_authorization:
            headers['Authorization'] = self.opik_authorization
            
        return headers


def setup_telemetry(app=None) -> Optional[TracerProvider]:
    """
    Setup OpenTelemetry tracing for the application
    
    Args:
        app: FastAPI application instance (optional, for auto-instrumentation)
        
    Returns:
        TracerProvider instance or None if disabled
    """
    config = OpikTelemetryConfig()
    
    if not config.otel_enabled:
        logger.info("OpenTelemetry tracing is disabled")
        return None
    
    try:
        # Create resource with service name
        resource = Resource.create({
            SERVICE_NAME: config.service_name,
            "service.version": "1.0.0",
            "deployment.environment": os.getenv("ENVIRONMENT", "development"),
        })
        
        # Create tracer provider
        tracer_provider = TracerProvider(resource=resource)
        
        # Configure OTLP HTTP exporter for Opik
        otlp_exporter = OTLPSpanExporter(
            endpoint=config.otel_endpoint,
            headers=config.get_headers(),
        )
        
        # Add OTLP batch processor
        tracer_provider.add_span_processor(
            BatchSpanProcessor(otlp_exporter)
        )
        
        # Optionally add console exporter for debugging
        if config.enable_console_exporter:
            console_exporter = ConsoleSpanExporter()
            tracer_provider.add_span_processor(
                BatchSpanProcessor(console_exporter)
            )
            logger.info("Console exporter enabled for debugging")
        
        # Set global tracer provider
        trace.set_tracer_provider(tracer_provider)
        
        # Instrument FastAPI if app is provided
        if app:
            FastAPIInstrumentor.instrument_app(app)
            logger.info("FastAPI instrumentation enabled")
        
        # Instrument requests library
        RequestsInstrumentor().instrument()
        
        logger.info(f"OpenTelemetry tracing configured successfully")
        logger.info(f"  Service: {config.service_name}")
        logger.info(f"  Endpoint: {config.otel_endpoint}")
        logger.info(f"  Workspace: {config.opik_workspace}")
        logger.info(f"  Project: {config.opik_project}")
        
        return tracer_provider
        
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")
        return None


def get_tracer(name: str = __name__):
    """
    Get a tracer instance for creating spans
    
    Args:
        name: Name of the tracer (typically __name__)
        
    Returns:
        Tracer instance
    """
    return trace.get_tracer(name)


def create_span(name: str, attributes: dict = None):
    """
    Context manager for creating a span
    
    Args:
        name: Name of the span
        attributes: Optional attributes to add to the span
        
    Example:
        with create_span("agent_execution", {"agent_type": "advanced"}):
            # Your code here
            pass
    """
    tracer = get_tracer()
    span = tracer.start_span(name)
    
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, str(value))
    
    return span


def add_span_event(event_name: str, attributes: dict = None):
    """
    Add an event to the current span
    
    Args:
        event_name: Name of the event
        attributes: Optional attributes for the event
    """
    current_span = trace.get_current_span()
    if current_span:
        current_span.add_event(event_name, attributes or {})


def set_span_attributes(attributes: dict):
    """
    Set attributes on the current span
    
    Args:
        attributes: Dictionary of attributes to set
    """
    current_span = trace.get_current_span()
    if current_span:
        for key, value in attributes.items():
            current_span.set_attribute(key, str(value))


def shutdown_telemetry():
    """Shutdown telemetry and flush pending spans"""
    try:
        tracer_provider = trace.get_tracer_provider()
        if hasattr(tracer_provider, 'shutdown'):
            tracer_provider.shutdown()
            logger.info("OpenTelemetry tracing shutdown successfully")
    except Exception as e:
        logger.error(f"Failed to shutdown OpenTelemetry: {e}")

