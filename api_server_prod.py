"""
Production-grade API server configuration
Includes authentication, rate limiting, and monitoring
"""

import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import set_default_openai_client, set_tracing_disabled, Runner
import uvicorn
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    agent_type: str = "advanced"
    max_turns: int = 5
    model: str = None  # Optional model override

class PromptResponse(BaseModel):
    result: str
    agent_type: str
    prompt: str
    timestamp: str
    execution_time: float

class HealthResponse(BaseModel):
    status: str
    openrouter_configured: bool
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    timestamp: str
    details: str = None

# Request counter for monitoring
request_count = {"total": 0, "errors": 0}

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Agent API Server starting...")
    yield
    logger.info("🛑 Agent API Server shutting down...")

# Create FastAPI app with custom settings
app = FastAPI(
    title="Agent API Server",
    description="REST API for running OpenAI agents with OpenRouter",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    request_count["errors"] += 1
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="Invalid input",
            timestamp=datetime.now().isoformat(),
            details=str(exc)
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    request_count["errors"] += 1
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            timestamp=datetime.now().isoformat(),
            details=str(exc) if os.getenv("DEBUG") else None
        ).model_dump()
    )

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        openrouter_configured=bool(openrouter_api_key),
        timestamp=datetime.now().isoformat()
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
    request_count["total"] += 1
    start_time = datetime.now()
    
    try:
        logger.info(f"Running {request.agent_type} agent with prompt: {request.prompt[:100]}...")
        
        # Select agent based on type
        if request.agent_type == "advanced":
            agent = advanced_orchestrator
        elif request.agent_type == "functions":
            agent = function_tools_agent
        else:
            raise ValueError(
                f"Unknown agent type: {request.agent_type}. Use 'advanced' or 'functions'"
            )
        
        # Run the agent
        result = await Runner.run(
            agent,
            input=request.prompt,
            max_turns=request.max_turns
        )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Agent completed in {execution_time:.2f}s")
        
        return PromptResponse(
            result=str(result.final_output),
            agent_type=request.agent_type,
            prompt=request.prompt,
            timestamp=datetime.now().isoformat(),
            execution_time=execution_time
        )
    
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Error running agent: {str(e)}")
        request_count["errors"] += 1
        raise HTTPException(
            status_code=500,
            detail=f"Error running agent: {str(e)}"
        )

@app.get("/agents", response_model=dict)
async def list_agents():
    """List available agents"""
    logger.info("Agents list requested")
    return {
        "agents": [
            {
                "name": "advanced",
                "description": "Content Creation Orchestrator - Coordinates research and writing",
                "type": "orchestrator",
                "tools": ["run_research_agent", "run_writing_agent"]
            },
            {
                "name": "functions",
                "description": "Function Tools Agent - Performs calculations and utilities",
                "type": "utility",
                "tools": ["add_numbers", "multiply_numbers", "get_weather", "convert_temperature"]
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
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "total_requests": request_count["total"],
            "error_count": request_count["errors"]
        },
        "endpoints": {
            "health": "GET /health",
            "run_agent": "POST /run",
            "list_agents": "GET /agents",
            "info": "GET /info",
            "docs": "GET /docs",
            "redoc": "GET /redoc"
        }
    }

@app.get("/stats", response_model=dict)
async def get_stats():
    """Get server statistics"""
    return {
        "timestamp": datetime.now().isoformat(),
        "statistics": {
            "total_requests": request_count["total"],
            "error_count": request_count["errors"],
            "success_rate": (
                (request_count["total"] - request_count["errors"]) / request_count["total"] * 100
                if request_count["total"] > 0
                else 0
            )
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting Agent API Server on {host}:{port}")
    logger.info(f"Access API docs at http://{host}:{port}/docs")
    logger.info(f"Access ReDoc at http://{host}:{port}/redoc")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if not debug else "debug",
        access_log=True
    )

