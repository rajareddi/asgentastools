"""
FastAPI server for the Agent framework
Provides REST API endpoints for running agents with OpenRouter
"""

import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import set_default_openai_client, set_tracing_disabled, Runner
import uvicorn

# Load environment variables
load_dotenv()

# Configure OpenRouter
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

# Disable tracing
set_tracing_disabled(True)

# Set up OpenRouter client
openrouter_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Set the default client
set_default_openai_client(openrouter_client)

# Import agents after setting up the client
from agents_module.advanced_agent import advanced_orchestrator
from agents_module.function_tools_agent import root_agent as function_tools_agent

# Request/Response models
class PromptRequest(BaseModel):
    prompt: str
    agent_type: str = "advanced"  # "advanced" or "functions"
    max_turns: int = 5

class PromptResponse(BaseModel):
    result: str
    agent_type: str
    prompt: str

class HealthResponse(BaseModel):
    status: str
    openrouter_configured: bool

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Agent API Server starting...")
    yield
    print("🛑 Agent API Server shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Agent API Server",
    description="REST API for running OpenAI agents with OpenRouter",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        openrouter_configured=bool(openrouter_api_key)
    )

@app.post("/run", response_model=PromptResponse)
async def run_agent(request: PromptRequest):
    """
    Run an agent with the provided prompt
    
    Args:
        request: PromptRequest with prompt, agent_type, and max_turns
    
    Returns:
        PromptResponse with the agent's result
    """
    try:
        # Select agent based on type
        if request.agent_type == "advanced":
            agent = advanced_orchestrator
        elif request.agent_type == "functions":
            agent = function_tools_agent
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown agent type: {request.agent_type}. Use 'advanced' or 'functions'"
            )
        
        # Run the agent
        result = await Runner.run(
            agent,
            input=request.prompt,
            max_turns=request.max_turns
        )
        
        return PromptResponse(
            result=str(result.final_output),
            agent_type=request.agent_type,
            prompt=request.prompt
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running agent: {str(e)}"
        )

@app.get("/agents", response_model=dict)
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {
                "name": "advanced",
                "description": "Content Creation Orchestrator - Coordinates research and writing",
                "type": "orchestrator"
            },
            {
                "name": "functions",
                "description": "Function Tools Agent - Performs calculations and utilities",
                "type": "utility"
            }
        ]
    }

@app.get("/info", response_model=dict)
async def get_info():
    """Get server information"""
    return {
        "server": "Agent API",
        "version": "1.0.0",
        "model": "OpenRouter (Multiple models available)",
        "api_base": "https://openrouter.ai/api/v1",
        "endpoints": {
            "health": "GET /health",
            "run_agent": "POST /run",
            "list_agents": "GET /agents",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting Agent API Server on {host}:{port}")
    print(f"Access API docs at http://{host}:{port}/docs")
    print(f"Access ReDoc at http://{host}:{port}/redoc")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

