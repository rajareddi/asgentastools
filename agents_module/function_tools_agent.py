from agents import Agent, function_tool

# Import OpenTelemetry for tracing
try:
    from otel_config import get_tracer, set_span_attributes, add_span_event
    tracer = get_tracer(__name__)
    TRACING_ENABLED = True
except ImportError:
    TRACING_ENABLED = False

@function_tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.add_numbers") as span:
            set_span_attributes({
                "tool.name": "add_numbers",
                "tool.type": "calculation",
                "tool.input.a": a,
                "tool.input.b": b
            })
            result = a + b
            set_span_attributes({
                "tool.output.result": result,
                "tool.success": True
            })
            add_span_event("calculation_complete", {"result": result})
            return result
    return a + b

@function_tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.multiply_numbers") as span:
            set_span_attributes({
                "tool.name": "multiply_numbers",
                "tool.type": "calculation",
                "tool.input.a": a,
                "tool.input.b": b
            })
            result = a * b
            set_span_attributes({
                "tool.output.result": result,
                "tool.success": True
            })
            add_span_event("calculation_complete", {"result": result})
            return result
    return a * b

@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city (mock implementation)"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.get_weather") as span:
            set_span_attributes({
                "tool.name": "get_weather",
                "tool.type": "api_call",
                "tool.input.city": city
            })
            add_span_event("fetching_weather", {"city": city})
            
            result = f"The weather in {city} is sunny with 72°F"
            
            set_span_attributes({
                "tool.output.result": result,
                "tool.success": True
            })
            add_span_event("weather_fetched", {"city": city, "result": "sunny"})
            return result
    return f"The weather in {city} is sunny with 72°F"

@function_tool
def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius and Fahrenheit"""
    if TRACING_ENABLED:
        with tracer.start_as_current_span("tool.convert_temperature") as span:
            set_span_attributes({
                "tool.name": "convert_temperature",
                "tool.type": "calculation",
                "tool.input.temperature": temperature,
                "tool.input.from_unit": from_unit,
                "tool.input.to_unit": to_unit
            })
            add_span_event("temperature_conversion_start", {
                "temperature": temperature,
                "from": from_unit,
                "to": to_unit
            })
            
            if from_unit.lower() == "celsius" and to_unit.lower() == "fahrenheit":
                result_value = (temperature * 9/5) + 32
                result = f"{temperature}°C = {result_value:.1f}°F"
                set_span_attributes({
                    "tool.output.result_value": result_value,
                    "tool.output.result": result,
                    "tool.success": True
                })
            elif from_unit.lower() == "fahrenheit" and to_unit.lower() == "celsius":
                result_value = (temperature - 32) * 5/9
                result = f"{temperature}°F = {result_value:.1f}°C"
                set_span_attributes({
                    "tool.output.result_value": result_value,
                    "tool.output.result": result,
                    "tool.success": True
                })
            else:
                result = "Unsupported temperature conversion"
                set_span_attributes({
                    "tool.output.result": result,
                    "tool.success": False,
                    "tool.error": "unsupported_conversion"
                })
            
            add_span_event("temperature_conversion_complete", {"result": result})
            return result
    else:
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

