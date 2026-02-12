# app/agent.py
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents.structured_output import ToolStrategy

from app.schema import Context, ResponseFormat

BOOKS_DIR = Path("books")
PROMPT_PATH = Path("prompts/booksnap_prompt.txt")


def load_prompt_template() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError("booksnap_prompt.txt not found.")
    return PROMPT_PATH.read_text(encoding="utf-8")


@tool
def get_book_content(runtime: ToolRuntime[Context]) -> str:
    """
    Load the full content of the selected book based on the current context.
    """
    filename = runtime.context.book_title.lower().replace(" ", "_") + ".txt"
    filepath = BOOKS_DIR / filename

    if not filepath.exists():
        return "Book not found."

    return filepath.read_text(encoding="utf-8")


@dynamic_prompt
def booksnap_dynamic_prompt(request: ModelRequest) -> str:
    template = load_prompt_template()

    return template.format(
        username=request.runtime.context.username,   
        book_title=request.runtime.context.book_title,
        summary=request.runtime.context.summary      
    )


def build_agent(model, checkpointer):
    return create_agent(
        model=model,
        tools=[get_book_content],
        middleware=[booksnap_dynamic_prompt],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer,
    )
