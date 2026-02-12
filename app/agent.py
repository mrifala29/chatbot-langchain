# app/agent.py
import os
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.structured_output import ToolStrategy

from app.schema import Context, ResponseFormat

BOOKS_DIR = Path("books")

SYSTEM_PROMPT = """
You are a gentle bedtime storyteller for children.

You answer questions strictly based on the selected book.
Your tone must always be:
- calm
- warm
- soothing
- bedtime friendly

If the answer is not found in the book, say it softly and kindly.
"""

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
        system_prompt=SYSTEM_PROMPT,
        tools=[get_book_content],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer,
    )
