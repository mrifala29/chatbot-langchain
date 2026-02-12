# app/schema.py
from dataclasses import dataclass

@dataclass
class Context:
    """Runtime context for Booksnap agent."""
    username: str
    book_title: str
    summary: str   # ✅ TAMBAH

@dataclass
class ResponseFormat:
    """Structured response from agent."""
    answer: str
    book_title: str
