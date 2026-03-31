"""
Test OpenTelemetry Integration
Verifies that OpenTelemetry is properly configured and can export traces
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_otel_imports():
    """Test if all OpenTelemetry packages can be imported"""
    print("Testing OpenTelemetry imports...")
    
    try:
        from opentelemetry import trace
        print("✓ opentelemetry-api imported")
        
        from opentelemetry.sdk.trace import TracerProvider
        print("✓ opentelemetry-sdk imported")
        
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        print("✓ opentelemetry-exporter-otlp-proto-http imported")
        
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        print("✓ opentelemetry-instrumentation-fastapi imported")
        
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        print("✓ opentelemetry-instrumentation-requests imported")
        
        print("\n✅ All OpenTelemetry packages imported successfully\n")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}\n")
        return False


def test_otel_config():
    """Test if otel_config module works"""
    print("Testing otel_config module...")
    
    try:
        from otel_config import (
            setup_telemetry,
            shutdown_telemetry,
            get_tracer,
            set_span_attributes,
            add_span_event,
            OpikTelemetryConfig
        )
        print("✓ otel_config module imported")
        
        # Test configuration
        config = OpikTelemetryConfig()
        print(f"✓ Configuration loaded:")
        print(f"  - Service Name: {config.service_name}")
        print(f"  - OTEL Enabled: {config.otel_enabled}")
        print(f"  - Endpoint: {config.otel_endpoint}")
        print(f"  - Workspace: {config.opik_workspace}")
        print(f"  - Project: {config.opik_project}")
        
        print("\n✅ otel_config module works correctly\n")
        return True
        
    except Exception as e:
        print(f"\n❌ otel_config test failed: {e}\n")
        return False


def test_tracer_creation():
    """Test if we can create a tracer"""
    print("Testing tracer creation...")
    
    try:
        from otel_config import get_tracer
        
        tracer = get_tracer(__name__)
        print("✓ Tracer created successfully")
        
        # Test span creation (without actual export)
        with tracer.start_as_current_span("test_span") as span:
            span.set_attribute("test.attribute", "test_value")
            print("✓ Test span created and attribute set")
        
        print("\n✅ Tracer creation works correctly\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Tracer creation failed: {e}\n")
        return False


def test_environment_variables():
    """Test if required environment variables are set"""
    print("Testing environment variables...")
    
    required_vars = {
        'OPENROUTER_API_KEY': 'OpenRouter API key'
    }
    
    optional_vars = {
        'OTEL_ENABLED': 'OpenTelemetry enabled flag',
        'OTEL_EXPORTER_OTLP_TRACES_ENDPOINT': 'Opik traces endpoint',
        'OPIK_WORKSPACE': 'Opik workspace name',
        'OPIK_PROJECT': 'Opik project name',
        'OTEL_SERVICE_NAME': 'Service name for telemetry'
    }
    
    all_ok = True
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✓ {var} is set: {masked}")
        else:
            print(f"❌ {var} is NOT set ({description})")
            all_ok = False
    
    # Check optional variables
    print("\nOptional variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✓ {var} = {value}")
        else:
            print(f"⚠ {var} not set (using default) - {description}")
    
    if all_ok:
        print("\n✅ All required environment variables are set\n")
    else:
        print("\n❌ Some required environment variables are missing\n")
    
    return all_ok


def test_opik_connectivity():
    """Test connectivity to Opik server"""
    print("Testing Opik server connectivity...")
    
    endpoint = os.getenv('OTEL_EXPORTER_OTLP_TRACES_ENDPOINT', 
                         'http://localhost:5173/api/v1/private/otel/v1/traces')
    
    # Extract base URL
    base_url = endpoint.replace('/api/v1/private/otel/v1/traces', '')
    
    try:
        import requests
        
        print(f"Testing connection to: {base_url}")
        response = requests.get(base_url, timeout=5)
        
        print(f"✓ Opik server responded with status: {response.status_code}")
        print("\n✅ Opik server is accessible\n")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"⚠ Could not connect to Opik server at {base_url}")
        print("  This is OK if Opik is not running or on a different host")
        print("\n⚠ Opik connectivity test skipped\n")
        return False
        
    except Exception as e:
        print(f"⚠ Connectivity test error: {e}")
        print("\n⚠ Opik connectivity test skipped\n")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("OpenTelemetry Integration Test Suite")
    print("=" * 70)
    print()
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_otel_imports()))
    results.append(("Config Test", test_otel_config()))
    results.append(("Tracer Test", test_tracer_creation()))
    results.append(("Environment Test", test_environment_variables()))
    results.append(("Connectivity Test", test_opik_connectivity()))
    
    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! OpenTelemetry integration is ready.")
        print("\nNext steps:")
        print("1. Start your Opik server (if not running)")
        print("2. Run: python api_server.py")
        print("3. Make test requests to generate traces")
        print("4. View traces in Opik dashboard")
        return 0
    else:
        print("\n⚠ Some tests failed. Please check the output above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check your .env file has required variables")
        print("3. Verify Opik server is running (if you want to test connectivity)")
        return 1


if __name__ == "__main__":
    sys.exit(main())

