"""
A2A Package Tests
Test suite for Agent-to-Agent communication
Located inside a2a_package for proper package testing
"""

import pytest
from a2a_package.core import MessageBroker
from a2a_package import coordinator_agent, specialist_agent, a2a_orchestrator, message_broker


class TestMessageBroker:
    """Test MessageBroker functionality"""
    
    def test_send_message(self):
        """Test sending a message"""
        broker = MessageBroker()
        msg = broker.send_message("Agent1", "Agent2", "Hello", topic="test")
        
        assert msg["from"] == "Agent1"
        assert msg["to"] == "Agent2"
        assert msg["message"] == "Hello"
        assert msg["topic"] == "test"
        assert msg["status"] == "sent"
    
    def test_get_messages(self):
        """Test retrieving messages for an agent"""
        broker = MessageBroker()
        broker.send_message("Agent1", "Agent2", "Message 1", topic="test")
        broker.send_message("Agent3", "Agent2", "Message 2", topic="test")
        
        messages = broker.get_messages("Agent2", topic="test")
        assert len(messages) == 2
    
    def test_get_conversation(self):
        """Test retrieving conversation history"""
        broker = MessageBroker()
        broker.send_message("Agent1", "Agent2", "Hello", topic="test")
        broker.send_message("Agent2", "Agent1", "Hi there", topic="test")
        
        conversation = broker.get_conversation("Agent1", "Agent2", topic="test")
        assert len(conversation) == 2
    
    def test_clear_messages(self):
        """Test clearing messages"""
        broker = MessageBroker()
        broker.send_message("Agent1", "Agent2", "Message 1", topic="test")
        broker.send_message("Agent1", "Agent3", "Message 2", topic="other")
        
        broker.clear_messages(to_agent="Agent2", topic="test")
        messages = broker.get_messages("Agent2", topic="test")
        assert len(messages) == 0
    
    def test_get_stats(self):
        """Test getting broker statistics"""
        broker = MessageBroker()
        broker.send_message("Agent1", "Agent2", "Message", topic="test")
        broker.send_message("Agent2", "Agent1", "Reply", topic="test")
        
        stats = broker.get_stats()
        assert stats["total_messages"] == 2
        assert "test" in stats["topics"]


class TestAgents:
    """Test A2A agents"""
    
    def test_coordinator_agent_exists(self):
        """Test that coordinator agent exists"""
        assert coordinator_agent is not None
        assert coordinator_agent.name == "Coordinator"
    
    def test_specialist_agent_exists(self):
        """Test that specialist agent exists"""
        assert specialist_agent is not None
        assert specialist_agent.name == "Specialist"
    
    def test_a2a_orchestrator_exists(self):
        """Test that A2A orchestrator exists"""
        assert a2a_orchestrator is not None
        assert a2a_orchestrator.name == "A2A Orchestrator"


class TestGlobalMessageBroker:
    """Test global message broker instance"""
    
    def test_global_broker_exists(self):
        """Test that global message broker exists"""
        assert message_broker is not None
    
    def test_global_broker_functionality(self):
        """Test global broker functionality"""
        msg = message_broker.send_message("Test1", "Test2", "Test message")
        assert msg is not None
        assert msg["from"] == "Test1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

