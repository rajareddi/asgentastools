import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Runner, set_default_openai_client, set_tracing_disabled
from agent import root_agent

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

# result = Runner.run_sync(root_agent, "What time is it in Inidia and hyderabad ?")
# print(result.final_output)
result = Runner.run_sync(root_agent, "Explain about the mahatma Gandhi ?")
print(result.final_output)
