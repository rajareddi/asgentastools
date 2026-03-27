"""
Example client for interacting with the Agent API
"""

import requests
import json
from typing import Optional

class AgentClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the Agent client"""
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if the API server is running"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_agents(self) -> list:
        """Get list of available agents"""
        response = self.session.get(f"{self.base_url}/agents")
        response.raise_for_status()
        return response.json()["agents"]
    
    def get_info(self) -> dict:
        """Get server information"""
        response = self.session.get(f"{self.base_url}/info")
        response.raise_for_status()
        return response.json()
    
    def run_agent(
        self,
        prompt: str,
        agent_type: str = "advanced",
        max_turns: int = 5,
        timeout: int = 300
    ) -> str:
        """
        Run an agent with the given prompt
        
        Args:
            prompt: The prompt to send to the agent
            agent_type: "advanced" or "functions"
            max_turns: Maximum number of agent iterations
            timeout: Request timeout in seconds
        
        Returns:
            The agent's response
        """
        payload = {
            "prompt": prompt,
            "agent_type": agent_type,
            "max_turns": max_turns
        }
        
        response = self.session.post(
            f"{self.base_url}/run",
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result["result"]
    
    def close(self):
        """Close the client session"""
        self.session.close()


def main():
    """Example usage"""
    print("🤖 Agent Client Example")
    print("=" * 60)
    
    # Create client
    client = AgentClient()
    
    # Check health
    print("\n1️⃣  Checking API health...")
    if client.health_check():
        print("   ✅ API is running")
    else:
        print("   ❌ API is not responding")
        print("   Start it with: python api_server.py")
        return
    
    # Get server info
    print("\n2️⃣  Server Information:")
    try:
        info = client.get_info()
        print(f"   Server: {info['server']} v{info['version']}")
        print(f"   API Base: {info['api_base']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # List agents
    print("\n3️⃣  Available Agents:")
    try:
        agents = client.list_agents()
        for agent in agents:
            print(f"   • {agent['name']}: {agent['description']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Run advanced agent
    print("\n4️⃣  Running Advanced Agent...")
    try:
        prompt = "What is the capital of France and what is its population?"
        print(f"   Prompt: {prompt}")
        print("   Running...")
        
        result = client.run_agent(prompt, agent_type="advanced", max_turns=3)
        
        print(f"\n   Response:")
        print(f"   {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Run function tools agent
    print("\n5️⃣  Running Function Tools Agent...")
    try:
        prompt = "What is 42 + 8? Also convert 32 Fahrenheit to Celsius."
        print(f"   Prompt: {prompt}")
        print("   Running...")
        
        result = client.run_agent(prompt, agent_type="functions", max_turns=3)
        
        print(f"\n   Response:")
        print(f"   {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("✨ Example complete!")
    print("\nFor more examples and usage, see README.md")
    
    client.close()


if __name__ == "__main__":
    main()

