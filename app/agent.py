from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.structured_output import ToolStrategy

from app.schema import Context, ResponseFormat

SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:
- get_weather_for_location
- get_user_location

If the user asks about the weather, make sure you know the location.
"""

# ===== Tools =====
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Get user location based on user_id."""
    return "Florida" if runtime.context.user_id == "1" else "SF"


def build_agent(model, checkpointer):
    return create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_user_location, get_weather_for_location],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer,
    )
