from fastapi import FastAPI
from pydantic import BaseModel

from app.model import get_model
from app.memory import get_checkpointer
from app.agent import build_agent
from app.schema import Context

app = FastAPI()

agent = build_agent(
    model=get_model(),
    checkpointer=get_checkpointer()
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "1"

@app.post("/chat")
def chat(req: ChatRequest):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": req.message}]},
        context=Context(user_id=req.user_id),
        config={"configurable": {"thread_id": req.user_id}},
    )
    return response["structured_response"]
