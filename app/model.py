import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_model():
    return ChatOpenAI(
        # model="mistralai/ministral-3b-2512", # use free model
        temperature=0.5,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )
