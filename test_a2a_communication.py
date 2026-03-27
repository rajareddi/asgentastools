"""
A2A Communication Testing and Examples
Demonstrates Agent-to-Agent communication capabilities
"""

import requests
import json
from typing import Dict, List

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def test_a2a_send_message():
    """Test sending messages between agents"""
    print_header("TEST 1: Send Messages Between Agents")
    
    # Coordinator sends to Specialist
    msg1 = requests.post(
        f"{BASE_URL}/a2a/send-message",
        params={
            "from_agent": "Coordinator",
            "to_agent": "Specialist",
            "message": "We need to analyze the system's scalability",
            "topic": "infrastructure"
        }
    ).json()
    
    print(f"✓ Message 1 sent:")
    print(f"  From: {msg1['message']['from']}")
    print(f"  To: {msg1['message']['to']}")
    print(f"  Message: {msg1['message']['message']}")
    
    # Specialist sends back to Coordinator
    msg2 = requests.post(
        f"{BASE_URL}/a2a/send-message",
        params={
            "from_agent": "Specialist",
            "to_agent": "Coordinator",
            "message": "Current system can handle 50K requests per minute with 99.9% uptime",
            "topic": "infrastructure"
        }
    ).json()
    
    print(f"\n✓ Message 2 sent:")
    print(f"  From: {msg2['message']['from']}")
    print(f"  To: {msg2['message']['to']}")
    print(f"  Message: {msg2['message']['message']}")

def test_a2a_get_messages():
    """Test retrieving messages"""
    print_header("TEST 2: Retrieve Messages")
    
    # Get all messages for Coordinator
    response = requests.get(
        f"{BASE_URL}/a2a/messages",
        params={"agent": "Coordinator", "topic": "infrastructure"}
    ).json()
    
    print(f"✓ Messages for Coordinator on 'infrastructure':")
    print(f"  Total: {response['count']}")
    for msg in response['messages']:
        print(f"  • {msg['from']}: {msg['message']}")

def test_a2a_get_conversation():
    """Test retrieving conversation history"""
    print_header("TEST 3: Get Conversation History")
    
    response = requests.get(
        f"{BASE_URL}/a2a/conversation",
        params={
            "agent1": "Coordinator",
            "agent2": "Specialist",
            "topic": "infrastructure"
        }
    ).json()
    
    print(f"✓ Conversation between {response['agent1']} ↔ {response['agent2']}")
    print(f"  Topic: {response['topic']}")
    print(f"  Messages: {response['message_count']}\n")
    
    for msg in response['conversation']:
        print(f"[{msg['timestamp']}]")
        print(f"  {msg['from']} → {msg['to']}: {msg['message']}")

def test_a2a_collaboration():
    """Test A2A collaboration"""
    print_header("TEST 4: A2A Collaboration")
    
    response = requests.post(
        f"{BASE_URL}/a2a/collaborate",
        json={
            "prompt": "Discuss the best practices for implementing microservices architecture",
            "agent_type": "a2a_orchestrator",
            "max_turns": 3
        }
    ).json()
    
    print(f"✓ Collaboration Result:")
    print(f"  Prompt: {response['prompt']}")
    print(f"  Agent Type: {response['agent_type']}")
    print(f"  Execution Time: {response['execution_time']:.2f}s\n")
    print(f"Result:\n{response['result'][:500]}...\n")

def test_a2a_list_agents():
    """Test listing available agents"""
    print_header("TEST 5: List Available Agents")
    
    response = requests.get(f"{BASE_URL}/agents").json()
    
    print(f"✓ Available Agents:\n")
    for agent in response['agents']:
        print(f"  • {agent['name']} ({agent['type']})")
        print(f"    {agent['description']}\n")

def test_a2a_clear_messages():
    """Test clearing messages"""
    print_header("TEST 6: Clear Messages")
    
    response = requests.delete(
        f"{BASE_URL}/a2a/clear-messages",
        params={"agent": "Coordinator", "topic": "infrastructure"}
    ).json()
    
    print(f"✓ Clear Result:")
    print(f"  Success: {response['success']}")
    print(f"  Message: {response['message']}")
    print(f"  Cleared for: Agent={response['cleared_for']['agent']}, Topic={response['cleared_for']['topic']}")

def run_full_demo():
    """Run full A2A communication demo"""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "🤖 A2A COMMUNICATION DEMO 🤖" + " " * 31 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        # Test 1: Send messages
        test_a2a_send_message()
        
        # Test 2: Get messages
        test_a2a_get_messages()
        
        # Test 3: Get conversation
        test_a2a_get_conversation()
        
        # Test 5: List agents
        test_a2a_list_agents()
        
        # Test 4: Collaboration
        test_a2a_collaboration()
        
        # Test 6: Clear messages
        test_a2a_clear_messages()
        
        # Final summary
        print_header("✨ A2A DEMO COMPLETED")
        print("""
        ✅ Successfully demonstrated:
           • Agent-to-agent messaging
           • Message retrieval
           • Conversation history
           • Multi-agent collaboration
           • Agent listing
           • Message clearing
        
        📚 Next Steps:
           • Read A2A_COMMUNICATION.md for detailed docs
           • Try the Streamlit UI at http://localhost:8501
           • Use the Python client for integrations
           • Build custom A2A workflows
        """)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_full_demo()

