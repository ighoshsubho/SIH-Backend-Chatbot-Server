from fastapi import FastAPI
from pydantic import BaseModel
from app.helpers import chatbotQA

app = FastAPI()

@app.post("/api/")
async def create_item(text:str):
    res = chatbotQA(text)
    return {"response":res}
