"""
A2A Agents Module
Agent definitions for Agent-to-Agent communication
"""

from agents import Agent, Runner, function_tool
from a2a_package.core import message_broker

# Import OpenTelemetry for tracing
try:
    from otel_config import get_tracer, set_span_attributes, add_span_event
    tracer = get_tracer(__name__)
    TRACING_ENABLED = True
except ImportError:
    TRACING_ENABLED = False

# ============================================================================
# Agent 1: Coordinator Agent
# ============================================================================

@function_tool
async def agent1_send_message(to_agent: str, message: str, topic: str = "general") -> str:
    """Send a message from Coordinator to another agent"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.agent1_send_message") as span:
            set_span_attributes({
                "tool.name": "agent1_send_message",
                "tool.type": "a2a_communication",
                "tool.from_agent": "Coordinator",
                "tool.to_agent": to_agent,
                "tool.topic": topic,
                "tool.message_length": len(message)
            })
            add_span_event("sending_message", {
                "from": "Coordinator",
                "to": to_agent,
                "topic": topic
            })
            
            msg = message_broker.send_message("Coordinator", to_agent, message, topic)
            result = f"✓ Message sent to {to_agent} on topic '{topic}': {message}"
            
            set_span_attributes({
                "tool.message_id": msg.get("id", "unknown"),
                "tool.success": True
            })
            add_span_event("message_sent", {"message_id": msg.get("id")})
            return result
    
    msg = message_broker.send_message("Coordinator", to_agent, message, topic)
    return f"✓ Message sent to {to_agent} on topic '{topic}': {message}"

@function_tool
async def agent1_check_messages(topic: str = "general") -> str:
    """Check messages received by Coordinator agent"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.agent1_check_messages") as span:
            set_span_attributes({
                "tool.name": "agent1_check_messages",
                "tool.type": "a2a_communication",
                "tool.agent": "Coordinator",
                "tool.topic": topic
            })
            add_span_event("checking_messages", {"topic": topic})
            
            messages = message_broker.get_messages("Coordinator", topic)
            
            set_span_attributes({
                "tool.message_count": len(messages),
                "tool.success": True
            })
            
            if not messages:
                add_span_event("no_messages_found")
                return f"No messages for Coordinator on topic '{topic}'"
            
            msg_list = []
            for msg in messages:
                msg_list.append(f"From {msg['from']}: {msg['message']} (at {msg['timestamp']})")
            
            add_span_event("messages_retrieved", {"count": len(messages)})
            return "\n".join(msg_list)
    
    messages = message_broker.get_messages("Coordinator", topic)
    if not messages:
        return f"No messages for Coordinator on topic '{topic}'"
    
    msg_list = []
    for msg in messages:
        msg_list.append(f"From {msg['from']}: {msg['message']} (at {msg['timestamp']})")
    
    return "\n".join(msg_list)

@function_tool
async def agent1_analyze_topic(topic: str) -> str:
    """Analyze a topic and provide insights"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.agent1_analyze_topic") as span:
            set_span_attributes({
                "tool.name": "agent1_analyze_topic",
                "tool.type": "analysis",
                "tool.agent": "Coordinator",
                "tool.input.topic": topic
            })
            add_span_event("analysis_start", {"topic": topic})
            
            analysis = f"""
    Analysis of topic: {topic}
    
    Key considerations:
    1. Scope and boundaries
    2. Stakeholders involved
    3. Potential challenges
    4. Recommended approaches
    5. Expected outcomes
    
    This analysis is shared with other agents for collaborative problem-solving.
    """
            result = analysis.strip()
            
            set_span_attributes({
                "tool.output.length": len(result),
                "tool.success": True
            })
            add_span_event("analysis_complete", {"output_length": len(result)})
            return result
    
    analysis = f"""
    Analysis of topic: {topic}
    
    Key considerations:
    1. Scope and boundaries
    2. Stakeholders involved
    3. Potential challenges
    4. Recommended approaches
    5. Expected outcomes
    
    This analysis is shared with other agents for collaborative problem-solving.
    """
    return analysis.strip()

@function_tool
async def agent1_get_conversation(other_agent: str, topic: str = "general") -> str:
    """Get conversation history with another agent"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.agent1_get_conversation") as span:
            set_span_attributes({
                "tool.name": "agent1_get_conversation",
                "tool.type": "a2a_communication",
                "tool.agent1": "Coordinator",
                "tool.agent2": other_agent,
                "tool.topic": topic
            })
            add_span_event("retrieving_conversation", {
                "between": f"Coordinator and {other_agent}",
                "topic": topic
            })
            
            conversation = message_broker.get_conversation("Coordinator", other_agent, topic)
            
            set_span_attributes({
                "tool.conversation_length": len(conversation),
                "tool.success": True
            })
            
            if not conversation:
                add_span_event("no_conversation_found")
                return f"No conversation history with {other_agent} on topic '{topic}'"
            
            conv_text = f"Conversation between Coordinator and {other_agent} on '{topic}':\n\n"
            for msg in conversation:
                conv_text += f"[{msg['timestamp']}] {msg['from']} → {msg['to']}: {msg['message']}\n"
            
            add_span_event("conversation_retrieved", {"message_count": len(conversation)})
            return conv_text
    
    conversation = message_broker.get_conversation("Coordinator", other_agent, topic)
    
    if not conversation:
        return f"No conversation history with {other_agent} on topic '{topic}'"
    
    conv_text = f"Conversation between Coordinator and {other_agent} on '{topic}':\n\n"
    for msg in conversation:
        conv_text += f"[{msg['timestamp']}] {msg['from']} → {msg['to']}: {msg['message']}\n"
    
    return conv_text

coordinator_agent = Agent(
    name="Coordinator",
    instructions="""
    You are a Coordinator Agent responsible for orchestrating communication between agents.
    
    Your responsibilities:
    1. Send messages to other agents for collaboration
    2. Receive and process messages from other agents
    3. Analyze topics and share insights
    4. Maintain conversation history
    5. Facilitate decision-making through agent collaboration
    
    Tools available:
    - send_message: Send messages to other agents
    - check_messages: Check received messages
    - analyze_topic: Provide analysis on topics
    - get_conversation: Retrieve conversation history
    
    When communicating:
    - Be clear and concise
    - Reference previous conversations
    - Ask for input from collaborating agents
    - Synthesize information from multiple sources
    """,
    tools=[agent1_send_message, agent1_check_messages, agent1_analyze_topic, agent1_get_conversation]
)

# ============================================================================
# Agent 2: Specialist Agent
# ============================================================================

@function_tool
async def agent2_send_message(to_agent: str, message: str, topic: str = "general") -> str:
    """Send a message from Specialist to another agent"""
    msg = message_broker.send_message("Specialist", to_agent, message, topic)
    return f"✓ Message sent to {to_agent} on topic '{topic}': {message}"

@function_tool
async def agent2_check_messages(topic: str = "general") -> str:
    """Check messages received by Specialist agent"""
    messages = message_broker.get_messages("Specialist", topic)
    
    if not messages:
        return f"No messages for Specialist on topic '{topic}'"
    
    msg_list = []
    for msg in messages:
        msg_list.append(f"From {msg['from']}: {msg['message']} (at {msg['timestamp']})")
    
    return "\n".join(msg_list)

@function_tool
async def agent2_provide_expertise(area: str, question: str) -> str:
    """Provide specialized expertise in a specific area"""
    expertise = f"""
    Specialist Response - Area: {area}
    Question: {question}
    
    Expert Analysis:
    1. Technical Assessment
    2. Best Practices
    3. Risk Factors
    4. Recommendations
    5. Implementation Steps
    
    This specialized knowledge is available for collaborative problem-solving.
    """
    return expertise.strip()

@function_tool
async def agent2_get_conversation(other_agent: str, topic: str = "general") -> str:
    """Get conversation history with another agent"""
    conversation = message_broker.get_conversation("Specialist", other_agent, topic)
    
    if not conversation:
        return f"No conversation history with {other_agent} on topic '{topic}'"
    
    conv_text = f"Conversation between Specialist and {other_agent} on '{topic}':\n\n"
    for msg in conversation:
        conv_text += f"[{msg['timestamp']}] {msg['from']} → {msg['to']}: {msg['message']}\n"
    
    return conv_text

specialist_agent = Agent(
    name="Specialist",
    instructions="""
    You are a Specialist Agent with deep expertise in specific domains.
    
    Your responsibilities:
    1. Receive collaboration requests from other agents
    2. Provide specialized expertise and analysis
    3. Send insights and recommendations back to agents
    4. Answer technical questions
    5. Contribute to collaborative decision-making
    
    Tools available:
    - send_message: Send expertise and responses to other agents
    - check_messages: Check incoming collaboration requests
    - provide_expertise: Share specialized knowledge
    - get_conversation: Review collaboration history
    
    When collaborating:
    - Provide detailed technical analysis
    - Reference standards and best practices
    - Consider multiple perspectives
    - Offer actionable recommendations
    - Support with evidence-based insights
    """,
    tools=[agent2_send_message, agent2_check_messages, agent2_provide_expertise, agent2_get_conversation]
)

# ============================================================================
# A2A Orchestrator Agent
# ============================================================================

@function_tool
async def orchestrate_collaboration(topic: str, question: str) -> str:
    """Orchestrate collaboration between Coordinator and Specialist agents"""
    
    # Step 1: Coordinator analyzes the topic
    coordinator_analysis = await agent1_analyze_topic(topic)
    
    # Step 2: Coordinator sends to Specialist
    coord_msg = f"Please provide expertise on: {question}"
    msg1 = message_broker.send_message("Coordinator", "Specialist", coord_msg, topic)
    
    # Step 3: Specialist provides expertise
    specialist_response = await agent2_provide_expertise(topic, question)
    
    # Step 4: Specialist sends response back
    spec_msg = f"Analysis complete. Key findings: {specialist_response[:100]}..."
    msg2 = message_broker.send_message("Specialist", "Coordinator", spec_msg, topic)
    
    # Step 5: Compile collaboration result
    result = f"""
    ═══════════════════════════════════════════════════════════════
    AGENT-TO-AGENT COLLABORATION RESULT
    ═══════════════════════════════════════════════════════════════
    
    Topic: {topic}
    Question: {question}
    
    ─ Coordinator Analysis ──────────────────────────────────────
    {coordinator_analysis}
    
    ─ Specialist Expertise ──────────────────────────────────────
    {specialist_response}
    
    ─ Communication Exchange ────────────────────────────────────
    1. Coordinator → Specialist: {coord_msg}
    2. Specialist → Coordinator: {spec_msg}
    
    ═══════════════════════════════════════════════════════════════
    """
    
    return result.strip()

@function_tool
async def get_collaboration_history(topic: str = "general") -> str:
    """Get full collaboration history between agents"""
    conversation = message_broker.get_conversation("Coordinator", "Specialist", topic)
    
    if not conversation:
        return f"No collaboration history on topic '{topic}'"
    
    history = f"Agent-to-Agent Communication History - Topic: {topic}\n"
    history += "=" * 70 + "\n\n"
    
    for i, msg in enumerate(conversation, 1):
        history += f"Message {i}:\n"
        history += f"  Time: {msg['timestamp']}\n"
        history += f"  From: {msg['from']}\n"
        history += f"  To: {msg['to']}\n"
        history += f"  Message: {msg['message']}\n\n"
    
    return history

a2a_orchestrator = Agent(
    name="A2A Orchestrator",
    instructions="""
    You are an Agent-to-Agent (A2A) Orchestrator that manages collaboration between specialized agents.
    
    Your role:
    1. Facilitate communication between Coordinator and Specialist agents
    2. Orchestrate multi-agent problem-solving
    3. Track conversation history
    4. Synthesize insights from multiple agents
    5. Ensure effective collaboration
    
    Tools available:
    - orchestrate_collaboration: Run full A2A collaboration workflow
    - get_collaboration_history: Review past agent interactions
    
    Process:
    - Receive collaboration requests
    - Coordinate between agents
    - Aggregate insights
    - Return synthesized results
    
    Remember: You are facilitating agent-to-agent communication for better problem-solving.
    """,
    tools=[orchestrate_collaboration, get_collaboration_history]
)

__all__ = ['coordinator_agent', 'specialist_agent', 'a2a_orchestrator']

