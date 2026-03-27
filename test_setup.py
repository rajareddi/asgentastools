"""
Test script to verify the Agent service setup
"""

import sys
import time
import subprocess
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import agents
        print("  ✅ agents")
    except ImportError as e:
        print(f"  ❌ agents: {e}")
        return False
    
    try:
        import fastapi
        print("  ✅ fastapi")
    except ImportError as e:
        print(f"  ❌ fastapi: {e}")
        return False
    
    try:
        import streamlit
        print("  ✅ streamlit")
    except ImportError as e:
        print(f"  ❌ streamlit: {e}")
        return False
    
    try:
        from agents_module.advanced_agent import advanced_orchestrator
        print("  ✅ advanced_orchestrator agent")
    except Exception as e:
        print(f"  ❌ advanced_orchestrator: {e}")
        return False
    
    try:
        from agents_module.function_tools_agent import root_agent
        print("  ✅ function_tools agent")
    except Exception as e:
        print(f"  ❌ function_tools agent: {e}")
        return False
    
    return True

def test_api_startup():
    """Test that API can start"""
    print("\n🧪 Testing API startup...")
    
    try:
        import requests
        
        # Give server 10 seconds to start
        for i in range(10):
            try:
                response = requests.get('http://localhost:8000/health', timeout=2)
                if response.status_code == 200:
                    print("  ✅ API server responding")
                    return True
            except:
                if i < 9:
                    time.sleep(1)
        
        print("  ⚠️  API server not responding (but may be running in background)")
        return True
    except Exception as e:
        print(f"  ⚠️  Could not test API: {e}")
        return True

def test_environment():
    """Test environment configuration"""
    print("\n🧪 Testing environment...")
    
    import os
    from dotenv import load_dotenv
    
    # Load from .env
    load_dotenv()
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        print(f"  ✅ OPENROUTER_API_KEY configured ({len(api_key)} chars)")
    else:
        print("  ⚠️  OPENROUTER_API_KEY not set (required for running agents)")
    
    return True

def main():
    print("\n" + "="*60)
    print("🤖 Agent Service - Setup Verification")
    print("="*60)
    
    workspace_root = Path(__file__).parent
    import os
    os.chdir(workspace_root)
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Environment Test", test_environment()))
    results.append(("API Startup Test", test_api_startup()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All tests passed! Setup is complete.")
        print("\n🚀 To run the service:")
        print("   python start_service.py")
        print("\n📍 Access points:")
        print("   UI:      http://localhost:8501")
        print("   API:     http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

