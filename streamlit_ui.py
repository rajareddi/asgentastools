"""
Streamlit UI for Agent API
Interactive web interface for running agents
"""

import streamlit as st
import requests
import json
from typing import Optional
import time

# Page config
st.set_page_config(
    page_title="Agent Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
api_url = st.sidebar.text_input(
    "API Base URL",
    value="http://localhost:8000",
    help="Base URL of the Agent API server"
)

# Main title
st.title("🤖 Agent Interface")
st.markdown("Interactive interface for running AI agents with OpenRouter")

# Check API health
def check_api_health():
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Get available agents
def get_agents():
    try:
        response = requests.get(f"{api_url}/agents", timeout=5)
        if response.status_code == 200:
            return response.json()["agents"]
    except:
        pass
    return []

# Run agent
def run_agent(prompt: str, agent_type: str, max_turns: int):
    try:
        response = requests.post(
            f"{api_url}/run",
            json={
                "prompt": prompt,
                "agent_type": agent_type,
                "max_turns": max_turns
            },
            timeout=300  # 5 minute timeout for long-running agents
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to API at {api_url}. Make sure the server is running."}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout. The agent took too long to respond."}
    except Exception as e:
        return {"error": str(e)}

# Check API status
if not check_api_health():
    st.error(f"❌ Cannot connect to API at {api_url}")
    st.info("Make sure to start the API server first:")
    st.code("python api_server.py", language="bash")
    st.stop()

st.success(f"✅ Connected to API at {api_url}")

# Get server info
try:
    server_info = requests.get(f"{api_url}/info", timeout=5).json()
    with st.expander("ℹ️ Server Information"):
        st.json(server_info)
except:
    pass

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📝 Input")
    
    # Agent selection
    agents = get_agents()
    if agents:
        agent_names = [agent["name"] for agent in agents]
        agent_descriptions = {agent["name"]: f"{agent['name']} - {agent['description']}" for agent in agents}
        
        selected_agent = st.selectbox(
            "Select Agent",
            agent_names,
            format_func=lambda x: agent_descriptions.get(x, x),
            help="Choose which agent to run"
        )
    else:
        selected_agent = "advanced"
        st.warning("Could not fetch available agents")

with col2:
    st.subheader("⚙️ Settings")
    max_turns = st.slider(
        "Max Turns",
        min_value=1,
        max_value=10,
        value=5,
        help="Maximum number of agent iterations"
    )

# Prompt input
st.subheader("💬 Prompt")
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Ask the agent something...",
    height=150,
    label_visibility="collapsed"
)

# Run button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    run_button = st.button("🚀 Run Agent", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

# Run agent
if run_button:
    if not prompt.strip():
        st.error("Please enter a prompt")
    else:
        with st.spinner(f"Running {selected_agent} agent..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress
            for i in range(100):
                progress_bar.progress(i / 100)
                time.sleep(0.01)
            
            result = run_agent(prompt, selected_agent, max_turns)
            progress_bar.progress(100)
            
            # Display result
            st.subheader("📤 Result")
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.markdown("### Agent Response")
                st.write(result["result"])
                
                # Show metadata
                with st.expander("📊 Metadata"):
                    st.json({
                        "agent": result.get("agent_type"),
                        "prompt": result.get("prompt")
                    })
                
                # Copy to clipboard button
                st.code(result["result"], language="text")

# History section
st.divider()

# A2A Communication Section
st.subheader("🤝 Agent-to-Agent Communication (A2A)")

a2a_tab1, a2a_tab2, a2a_tab3 = st.tabs(["Collaborate", "Messages", "About A2A"])

with a2a_tab1:
    st.markdown("### Multi-Agent Collaboration")
    a2a_prompt = st.text_area(
        "Enter collaboration topic",
        placeholder="e.g., Discuss the implementation of microservices architecture",
        height=100,
        key="a2a_prompt"
    )
    a2a_turns = st.slider("Max Turns", 1, 10, 5, key="a2a_turns")
    
    if st.button("🚀 Start A2A Collaboration", use_container_width=True):
        if a2a_prompt.strip():
            with st.spinner("Agents collaborating..."):
                try:
                    response = requests.post(
                        f"{api_url}/a2a/collaborate",
                        json={
                            "prompt": a2a_prompt,
                            "agent_type": "a2a_orchestrator",
                            "max_turns": a2a_turns
                        },
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown("### Collaboration Result")
                        st.write(result["result"])
                    else:
                        st.error(f"Error: {response.json()}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a collaboration topic")

with a2a_tab2:
    st.markdown("### A2A Message History")
    
    col1, col2 = st.columns(2)
    with col1:
        msg_agent = st.selectbox("Filter by Agent", ["All", "Coordinator", "Specialist"])
    with col2:
        msg_topic = st.text_input("Filter by Topic", value="general")
    
    if st.button("📨 Load Messages", use_container_width=True):
        try:
            agent_param = None if msg_agent == "All" else msg_agent
            response = requests.get(
                f"{api_url}/a2a/messages",
                params={"agent": agent_param, "topic": msg_topic}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.info(f"Total messages: {data['count']}")
                
                if data['messages']:
                    for msg in data['messages']:
                        with st.expander(f"{msg['from']} → {msg['to']} ({msg['timestamp']})"):
                            st.write(msg['message'])
                else:
                    st.warning("No messages found")
            else:
                st.error("Error loading messages")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    st.markdown("### Send Direct Message")
    
    col1, col2 = st.columns(2)
    with col1:
        send_from = st.selectbox("From", ["Coordinator", "Specialist"])
        send_topic = st.text_input("Topic", value="general", key="send_topic")
    with col2:
        send_to = st.selectbox("To", ["Specialist", "Coordinator"])
    
    send_msg = st.text_area("Message", placeholder="Enter message", height=80)
    
    if st.button("✉️ Send Message", use_container_width=True):
        if send_msg.strip():
            try:
                response = requests.post(
                    f"{api_url}/a2a/send-message",
                    params={
                        "from_agent": send_from,
                        "to_agent": send_to,
                        "message": send_msg,
                        "topic": send_topic
                    }
                )
                
                if response.status_code == 200:
                    st.success("✓ Message sent successfully!")
                    st.json(response.json()["message"])
                else:
                    st.error("Error sending message")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with a2a_tab3:
    st.markdown("""
    ### What is A2A Communication?
    
    Agent-to-Agent (A2A) Communication enables intelligent agents to collaborate and solve problems together.
    
    **Three New Agents:**
    
    1. **Coordinator Agent** 🎯
       - Manages agent-to-agent communication
       - Analyzes topics and shares insights
       - Facilitates decision-making
    
    2. **Specialist Agent** 🔧
       - Provides specialized expertise
       - Responds to collaboration requests
       - Contributes domain knowledge
    
    3. **A2A Orchestrator** 🎼
       - Manages multi-agent workflows
       - Synthesizes insights from multiple agents
       - Tracks communication
    
    **Use Cases:**
    - Technical design reviews
    - Problem-solving with multiple perspectives
    - Knowledge sharing between experts
    - Collaborative decision-making
    
    **How It Works:**
    1. Send a collaboration prompt
    2. Coordinator and Specialist analyze the topic
    3. Agents communicate and exchange insights
    4. Orchestrator synthesizes results
    5. Get comprehensive analysis from multiple perspectives
    
    **Access:**
    - Use this UI for interactive collaboration
    - Use REST API for programmatic access
    - Use Python client for integrations
    
    📚 See `a2a_package/README.md` and `A2A_COMMUNICATION.md` for detailed documentation
    """)

st.divider()
st.subheader("📜 About")
st.markdown("""
This interface allows you to interact with AI agents powered by OpenRouter.

**Features:**
- 🤖 Multiple specialized agents
- 🤝 Agent-to-Agent collaboration
- 🔄 Interactive multi-turn conversations
- ⚙️ Configurable parameters
- 📊 Real-time responses

**Agents:**
- **Advanced**: Content creation orchestrator (research + writing)
- **Functions**: Function tools agent (calculations, utilities)
- **Coordinator**: A2A communication manager
- **Specialist**: Domain expertise provider
- **A2A Orchestrator**: Multi-agent workflow manager

**Getting Started:**
1. Select an agent from the dropdown
2. Enter your prompt
3. Adjust settings if needed
4. Click "Run Agent"
5. View the response

**For Collaboration:**
1. Go to "Agent-to-Agent Communication" tab
2. Enter a collaboration topic
3. Click "Start A2A Collaboration"
4. View multi-agent insights
""")

