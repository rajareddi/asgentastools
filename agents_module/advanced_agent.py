from agents import Agent, Runner, function_tool

# Import OpenTelemetry for tracing
try:
    from otel_config import get_tracer, set_span_attributes, add_span_event
    tracer = get_tracer(__name__)
    TRACING_ENABLED = True
except ImportError:
    TRACING_ENABLED = False

# Define a specialized research agent
research_agent = Agent(
    name="Research Specialist",
    instructions="""
    You are a research specialist. Provide detailed, well-researched information
    on any topic with proper analysis and insights.
    """
)

# Define a writing agent
writing_agent = Agent(
    name="Writing Specialist", 
    instructions="""
    You are a professional writer. Take research information and create
    well-structured, engaging content with proper formatting.
    """
)

@function_tool
async def run_research_agent(topic: str) -> str:
    """Research a topic using the specialized research agent with custom configuration"""
    
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.run_research_agent") as span:
            set_span_attributes({
                "tool.name": "run_research_agent",
                "tool.type": "agent_runner",
                "tool.agent": "Research Specialist",
                "tool.input.topic": topic,
                "tool.max_turns": 3
            })
            add_span_event("tool_execution_start", {"topic": topic})
            
            result = await Runner.run(
                research_agent,
                input=f"Research this topic thoroughly: {topic}",
                max_turns=3
            )
            
            output = str(result.final_output)
            set_span_attributes({
                "tool.output.length": len(output),
                "tool.success": True
            })
            add_span_event("tool_execution_complete", {
                "output_length": len(output)
            })
            
            return output
    else:
        result = await Runner.run(
            research_agent,
            input=f"Research this topic thoroughly: {topic}",
            max_turns=3
        )
        return str(result.final_output)

@function_tool  
async def run_writing_agent(content: str, style: str = "professional") -> str:
    """Transform content using the specialized writing agent with custom style"""
    
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.run_writing_agent") as span:
            set_span_attributes({
                "tool.name": "run_writing_agent",
                "tool.type": "agent_runner",
                "tool.agent": "Writing Specialist",
                "tool.input.content_length": len(content),
                "tool.input.style": style,
                "tool.max_turns": 2
            })
            add_span_event("tool_execution_start", {
                "style": style,
                "content_length": len(content)
            })
            
            prompt = f"Rewrite this content in a {style} style: {content}"
            
            result = await Runner.run(
                writing_agent,
                input=prompt,
                max_turns=2
            )
            
            output = str(result.final_output)
            set_span_attributes({
                "tool.output.length": len(output),
                "tool.success": True
            })
            add_span_event("tool_execution_complete", {
                "output_length": len(output)
            })
            
            return output
    else:
        prompt = f"Rewrite this content in a {style} style: {content}"
        result = await Runner.run(
            writing_agent,
            input=prompt,
            max_turns=2
        )
        return str(result.final_output)

# Create orchestrator with custom agent tools
advanced_orchestrator = Agent(
    name="Content Creation Orchestrator",
    instructions="""
    You are a content creation orchestrator that combines research and writing expertise.
    
    You have access to:
    - Research agent: For in-depth topic research
    - Writing agent: For professional content creation
    
    When users request content:
    1. First use the research agent to gather information
    2. Then use the writing agent to create polished content
    3. You can specify writing styles (professional, casual, academic, etc.)
    
    Coordinate both agents to create comprehensive, well-written content.
    """,
    tools=[run_research_agent, run_writing_agent]
)

