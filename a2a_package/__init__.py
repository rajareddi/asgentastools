"""
A2A (Agent-to-Agent) Communication Package
Multi-agent communication and collaboration framework
"""

__version__ = "1.0.0"
__author__ = "Agent Development Team"
__description__ = "Agent-to-Agent Communication Protocol for OpenAI Agents Framework"

from a2a_package.core import MessageBroker
from a2a_package.agents import (
    coordinator_agent,
    specialist_agent,
    a2a_orchestrator
)
from a2a_package.client import A2AClient

__all__ = [
    'MessageBroker',
    'coordinator_agent',
    'specialist_agent',
    'a2a_orchestrator',
    'A2AClient'
]

