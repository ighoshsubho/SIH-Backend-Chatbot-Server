from fastapi import FastAPI
from pydantic import BaseModel
from app import helpers
app = FastAPI()

@app.post("/api/")
async def create_item(text:str):
    res = helpers.chatbotQA(text)
    return {"response":res}
