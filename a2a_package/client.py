"""
A2A Client Module
Python client for accessing A2A communication features via REST API
"""

import requests
from typing import Optional, Dict, List

class A2AClient:
    """Client for Agent-to-Agent communication"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize A2A client"""
        self.base_url = base_url
        self.session = requests.Session()
    
    def send_message(self, from_agent: str, to_agent: str, message: str, topic: str = "general") -> Dict:
        """Send a message from one agent to another"""
        response = self.session.post(
            f"{self.base_url}/a2a/send-message",
            params={"from_agent": from_agent, "to_agent": to_agent, "message": message, "topic": topic}
        )
        response.raise_for_status()
        return response.json()
    
    def get_messages(self, agent: Optional[str] = None, topic: str = "general") -> Dict:
        """Get messages for an agent"""
        response = self.session.get(
            f"{self.base_url}/a2a/messages",
            params={"agent": agent, "topic": topic}
        )
        response.raise_for_status()
        return response.json()
    
    def get_conversation(self, agent1: str = "Coordinator", agent2: str = "Specialist", topic: str = "general") -> Dict:
        """Get conversation history between two agents"""
        response = self.session.get(
            f"{self.base_url}/a2a/conversation",
            params={"agent1": agent1, "agent2": agent2, "topic": topic}
        )
        response.raise_for_status()
        return response.json()
    
    def run_collaboration(self, prompt: str, max_turns: int = 5) -> Dict:
        """Run A2A collaboration"""
        response = self.session.post(
            f"{self.base_url}/a2a/collaborate",
            json={"prompt": prompt, "agent_type": "a2a_orchestrator", "max_turns": max_turns}
        )
        response.raise_for_status()
        return response.json()
    
    def clear_messages(self, agent: Optional[str] = None, topic: Optional[str] = None) -> Dict:
        """Clear message history"""
        response = self.session.delete(
            f"{self.base_url}/a2a/clear-messages",
            params={"agent": agent, "topic": topic}
        )
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> Dict:
        """Get API statistics"""
        response = self.session.get(f"{self.base_url}/a2a/stats")
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Close the client session"""
        self.session.close()

__all__ = ['A2AClient']

