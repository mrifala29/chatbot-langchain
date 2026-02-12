# app/schema.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Context:
    """Runtime context for Booksnap agent."""
    user_id: str
    book_title: str

@dataclass
class ResponseFormat:
    """Structured response from agent."""
    answer: str
    book_title: str
