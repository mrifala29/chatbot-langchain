# app/agent.py
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.structured_output import ToolStrategy

from app.schema import Context, ResponseFormat

BOOKS_DIR = Path("books")
PROMPT_PATH = Path("prompts/system_prompt.txt")

def load_system_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError("System prompt file not found.")
    return PROMPT_PATH.read_text(encoding="utf-8")

@tool
def get_book_content(runtime: ToolRuntime[Context]) -> str:
    """
    Load the full content of the selected book.
    """
    filename = runtime.context.book_title.lower().replace(" ", "_") + ".txt"
    filepath = BOOKS_DIR / filename

    if not filepath.exists():
        return "Book not found."

    return filepath.read_text(encoding="utf-8")

def build_agent(model, checkpointer):
    return create_agent(
        model=model,
        system_prompt=load_system_prompt(),
        tools=[get_book_content],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer,
    )