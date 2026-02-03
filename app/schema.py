from dataclasses import dataclass

@dataclass
class Context:
    """Runtime context for agent."""
    user_id: str

@dataclass
class ResponseFormat:
    """Structured response from agent."""
    punny_response: str
    weather_conditions: str | None = None
