import os
from agents import Runner, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI

from advanced_agent import advanced_orchestrator
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Disable tracing to avoid telemetry API calls
set_tracing_disabled(True)

# Set up OpenRouter OpenAI client
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openrouter_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Set the OpenRouter client as the default for agents
set_default_openai_client(openrouter_client)
result = Runner.run_sync(advanced_orchestrator, "Research the benefits of AI in healthcare.")
print(result.final_output)