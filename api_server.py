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
from a2a_package import coordinator_agent, specialist_agent, a2a_orchestrator
from a2a_package.core import message_broker

# Import MCP agent from new package
try:
    from mcp_package import mcp_agent, mcp_agent_available
except ImportError:
    mcp_agent_available = False
    mcp_agent = None

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
    print("[*] Agent API Server starting...")
    yield
    print("[*] Agent API Server shutting down...")

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
        elif request.agent_type == "coordinator":
            agent = coordinator_agent
        elif request.agent_type == "specialist":
            agent = specialist_agent
        elif request.agent_type == "a2a_orchestrator":
            agent = a2a_orchestrator
        elif request.agent_type == "mcp":
            if not mcp_available or mcp_agent is None:
                raise HTTPException(
                    status_code=503,
                    detail="MCP agent not available. Install MCP dependencies."
                )
            agent = mcp_agent
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown agent type: {request.agent_type}. Available: advanced, functions, coordinator, specialist, a2a_orchestrator, mcp"
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
    agents = [
        {
            "name": "advanced",
            "description": "Content Creation Orchestrator - Coordinates research and writing",
            "type": "orchestrator"
        },
        {
            "name": "functions",
            "description": "Function Tools Agent - Performs calculations and utilities",
            "type": "utility"
        },
        {
            "name": "coordinator",
            "description": "Coordinator Agent - Manages agent-to-agent communication",
            "type": "a2a"
        },
        {
            "name": "specialist",
            "description": "Specialist Agent - Provides specialized expertise",
            "type": "a2a"
        },
        {
            "name": "a2a_orchestrator",
            "description": "A2A Orchestrator - Manages multi-agent workflows",
            "type": "a2a"
        }
    ]
    
    if mcp_agent_available:
        agents.append({
            "name": "mcp",
            "description": "MCP-Integrated Agent - Access external services via MCP",
            "type": "mcp"
        })
    
    return {"agents": agents}

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


# ============================================================================
# A2A (Agent-to-Agent) Communication Endpoints
# ============================================================================

@app.post("/a2a/collaborate", response_model=PromptResponse)
async def a2a_collaborate(request: PromptRequest):
    """
    Run A2A collaboration between Coordinator and Specialist agents
    
    Example prompt: "Discuss the implementation of microservices architecture"
    """
    try:
        # Use A2A orchestrator
        agent = a2a_orchestrator
        
        # Run the agent with collaboration prompt
        result = await Runner.run(
            agent,
            input=request.prompt,
            max_turns=request.max_turns
        )
        
        return PromptResponse(
            result=str(result.final_output),
            agent_type="a2a_orchestrator",
            prompt=request.prompt
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running A2A collaboration: {str(e)}"
        )

@app.get("/a2a/messages", response_model=dict)
async def get_a2a_messages(agent: str = None, topic: str = "general"):
    """
    Get message history between agents
    
    Args:
        agent: Filter by agent name (Coordinator or Specialist)
        topic: Filter by topic (default: "general")
    
    Returns:
        List of messages in conversation history
    """
    try:
        if agent:
            messages = message_broker.get_messages(agent, topic)
        else:
            messages = message_broker.messages
        
        return {
            "count": len(messages),
            "messages": messages,
            "topic": topic
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving messages: {str(e)}"
        )

@app.get("/a2a/conversation", response_model=dict)
async def get_a2a_conversation(agent1: str = "Coordinator", agent2: str = "Specialist", topic: str = "general"):
    """
    Get conversation history between two agents
    
    Args:
        agent1: First agent name (default: Coordinator)
        agent2: Second agent name (default: Specialist)
        topic: Topic filter (default: "general")
    
    Returns:
        Full conversation transcript
    """
    try:
        conversation = message_broker.get_conversation(agent1, agent2, topic)
        
        return {
            "agent1": agent1,
            "agent2": agent2,
            "topic": topic,
            "message_count": len(conversation),
            "conversation": conversation
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation: {str(e)}"
        )

@app.post("/a2a/send-message", response_model=dict)
async def send_a2a_message(from_agent: str, to_agent: str, message: str, topic: str = "general"):
    """
    Send a message between agents directly
    
    Args:
        from_agent: Sending agent (Coordinator or Specialist)
        to_agent: Receiving agent
        message: Message content
        topic: Topic for the message
    
    Returns:
        Message object with metadata
    """
    try:
        msg = message_broker.send_message(from_agent, to_agent, message, topic)
        return {
            "success": True,
            "message": msg,
            "status": "Message sent successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending message: {str(e)}"
        )

@app.delete("/a2a/clear-messages", response_model=dict)
async def clear_a2a_messages(agent: str = None, topic: str = None):
    """
    Clear A2A message history
    
    Args:
        agent: Clear messages for specific agent (optional)
        topic: Clear messages for specific topic (optional)
    
    Returns:
        Confirmation of cleared messages
    """
    try:
        message_broker.clear_messages(agent, topic)
        return {
            "success": True,
            "message": "Messages cleared successfully",
            "cleared_for": {
                "agent": agent or "all",
                "topic": topic or "all"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing messages: {str(e)}"
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"[*] Starting Agent API Server on {host}:{port}")
    print(f"[*] Access API docs at http://{host}:{port}/docs")
    print(f"[*] Access ReDoc at http://{host}:{port}/redoc")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
