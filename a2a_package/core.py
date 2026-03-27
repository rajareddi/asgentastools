"""
A2A Message Broker
Core messaging system for agent-to-agent communication
"""

from datetime import datetime
from typing import Dict, List, Optional

class MessageBroker:
    """Simple message broker for agent communication"""
    
    def __init__(self):
        self.messages: List[Dict] = []
        self.conversation_history: Dict = {}
    
    def send_message(self, from_agent: str, to_agent: str, message: str, topic: str = "general") -> Dict:
        """Send a message from one agent to another"""
        msg_obj = {
            "id": len(self.messages) + 1,
            "timestamp": datetime.now().isoformat(),
            "from": from_agent,
            "to": to_agent,
            "topic": topic,
            "message": message,
            "status": "sent"
        }
        self.messages.append(msg_obj)
        
        # Store in conversation history
        conv_key = f"{from_agent}_{to_agent}_{topic}"
        if conv_key not in self.conversation_history:
            self.conversation_history[conv_key] = []
        self.conversation_history[conv_key].append(msg_obj)
        
        return msg_obj
    
    def get_messages(self, to_agent: str, topic: str = "general") -> List[Dict]:
        """Retrieve messages for an agent on a specific topic"""
        return [
            msg for msg in self.messages 
            if msg["to"] == to_agent and msg["topic"] == topic
        ]
    
    def get_conversation(self, agent1: str, agent2: str, topic: str = "general") -> List[Dict]:
        """Get full conversation between two agents"""
        conv_key = f"{agent1}_{agent2}_{topic}"
        reverse_key = f"{agent2}_{agent1}_{topic}"
        
        conversation = self.conversation_history.get(conv_key, [])
        reverse_conversation = self.conversation_history.get(reverse_key, [])
        
        all_messages = conversation + reverse_conversation
        return sorted(all_messages, key=lambda x: x["timestamp"])
    
    def clear_messages(self, to_agent: str = None, topic: str = None):
        """Clear messages optionally filtered by agent and topic"""
        if to_agent and topic:
            self.messages = [
                msg for msg in self.messages 
                if not (msg["to"] == to_agent and msg["topic"] == topic)
            ]
        elif to_agent:
            self.messages = [msg for msg in self.messages if msg["to"] != to_agent]
        else:
            self.messages = []
    
    def get_stats(self) -> Dict:
        """Get message broker statistics"""
        return {
            "total_messages": len(self.messages),
            "conversations": len(self.conversation_history),
            "topics": list(set(msg["topic"] for msg in self.messages)),
            "agents": list(set(msg["from"] for msg in self.messages) | set(msg["to"] for msg in self.messages))
        }

# Global broker instance
message_broker = MessageBroker()

