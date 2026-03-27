from agents import Agent, function_tool

@function_tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

@function_tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together"""
    return a * b

@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city (mock implementation)"""
    return f"The weather in {city} is sunny with 72°F"

@function_tool
def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius and Fahrenheit"""
    if from_unit.lower() == "celsius" and to_unit.lower() == "fahrenheit":
        result = (temperature * 9/5) + 32
        return f"{temperature}°C = {result:.1f}°F"
    elif from_unit.lower() == "fahrenheit" and to_unit.lower() == "celsius":
        result = (temperature - 32) * 5/9
        return f"{temperature}°F = {result:.1f}°C"
    else:
        return "Unsupported temperature conversion"

# Create an agent with custom function tools
root_agent = Agent(
    name="Function Tools Agent",
    instructions="""
    You are a helpful assistant with access to various tools.
    
    Available tools:
    - add_numbers: Add two numbers together
    - multiply_numbers: Multiply two numbers together  
    - get_weather: Get weather information for a city
    - convert_temperature: Convert between Celsius and Fahrenheit
    
    When users ask for calculations or information:
    1. Use the appropriate tool for the task
    2. Explain what you're doing
    3. Show the result clearly
    
    Always use the provided tools rather than doing calculations yourself.
    """,
    tools=[add_numbers, multiply_numbers, get_weather, convert_temperature]
)

