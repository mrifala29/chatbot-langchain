# app/schema.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Context:
    username: str
    book_title: str
    summary: str

@dataclass
class ResponseFormat:
    answer: str
    book_title: str
    recommendation_questions: Optional[List[str]]
