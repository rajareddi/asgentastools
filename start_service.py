"""
Startup script for running the Agent service with API and UI
Starts the FastAPI server and Streamlit UI
"""

import subprocess
import os
import sys
import time
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['fastapi', 'uvicorn', 'streamlit', 'requests', 'agents']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ All dependencies installed")

def start_services():
    """Start both API server and Streamlit UI"""
    
    print("🚀 Starting Agent Service...")
    print("=" * 60)
    
    # Get the workspace root directory
    workspace_root = Path(__file__).parent
    os.chdir(workspace_root)
    
    # Set environment variables
    os.environ['HOST'] = '0.0.0.0'
    os.environ['PORT'] = '8000'
    
    # Start API server in background
    print("\n📡 Starting API Server on port 8000...")
    api_process = subprocess.Popen(
        [sys.executable, 'api_server.py'],
        cwd=workspace_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for API to start
    time.sleep(3)
    
    # Check if API is running
    try:
        import requests
        for i in range(5):
            try:
                response = requests.get('http://localhost:8000/health', timeout=2)
                if response.status_code == 200:
                    print("✅ API Server is running on http://localhost:8000")
                    break
            except:
                if i < 4:
                    time.sleep(2)
    except:
        pass
    
    # Start Streamlit UI
    print("\n🎨 Starting Streamlit UI on port 8501...")
    print("   Open browser: http://localhost:8501")
    
    streamlit_process = subprocess.Popen(
        [sys.executable, '-m', 'streamlit', 'run', 'streamlit_ui.py', 
         '--server.port=8501', '--server.address=localhost'],
        cwd=workspace_root
    )
    
    print("\n" + "=" * 60)
    print("🎉 Services are running!")
    print("=" * 60)
    print("\n📍 Access points:")
    print("   UI:         http://localhost:8501")
    print("   API:        http://localhost:8000")
    print("   API Docs:   http://localhost:8000/docs")
    print("   API ReDoc:  http://localhost:8000/redoc")
    print("\n💡 Press Ctrl+C to stop all services")
    print("=" * 60 + "\n")
    
    try:
        # Wait for processes
        api_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        api_process.terminate()
        streamlit_process.terminate()
        time.sleep(2)
        print("✅ Services stopped")

if __name__ == "__main__":
    try:
        check_dependencies()
        start_services()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

