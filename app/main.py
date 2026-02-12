# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel

from app.model import get_model
from app.memory import get_checkpointer
from app.agent import build_agent
from app.schema import Context

app = FastAPI()

checkpointer = get_checkpointer()

agent = build_agent(
    model=get_model(),
    checkpointer=checkpointer
)

class ChatRequest(BaseModel):
    message: str
    username: str      
    book_title: str
    summary: str       

@app.post("/chat")
def chat(req: ChatRequest):
    thread_id = req.username

    response = agent.invoke(
        {"messages": [{"role": "user", "content": req.message}]},
        context=Context(
            username=req.username,    
            book_title=req.book_title,
            summary=req.summary       
        ),
        config={"configurable": {"thread_id": thread_id}},  
    )

    result = response["structured_response"]


    state = checkpointer.get(
        {"configurable": {"thread_id": thread_id}}
    )

    if state and len(state["channel_values"]["messages"]) <= 2:
        result.recommendation_questions = [
            "Who is the main character in this story?",
            "What happens at the beginning of the story?",
            "How does the character feel in this part of the story?"
        ]
    else:
        result.recommendation_questions = None

    return result
