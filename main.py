import io
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException, status, UploadFile
from app import helpers
import os
import os.path
import openai
from mangum import Mangum

from app.helpers import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

app = FastAPI()
handler = Mangum(app)

@app.post("/api/generate/",
          tags=["ChatBot Grievance"],
          description="Generate Response from Grievance Chatbot")
async def generate_response(text:str):
    try:
        res = helpers.chatbotQA(text)
        return {"response":res}
    except:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/api/index/",
          tags=["ChatBot Grievance"],
          description="Create Index with Grievance Chatbot",)
async def create_index(text:str,file:str):
        try:
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "data_grieviance/"+file+".txt")
            with open(file_path, 'a') as file:
                file.write("\n"+text)
            res = helpers.ConstructIndex("./data_grieviance/")
            return {"index updated successfully"}
        except:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@app.get("/api/token/",
        tags=["ChatBot Grievance"],
        description="Count tokens for Chat History",)
async def count_token(text:str):
    try:
        res = helpers.count_tokens(text)
        return {"tokens":res}
    except:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/api/transcribe/",
          tags=["ChatBot Grievance"],
          description="Transcribe Speech to Text and Generate Response")
async def transcribe_and_generate_response(audio_file: UploadFile):
        audio = audio_file.file.read()

        buffer = io.BytesIO(audio)
        buffer.name = audio_file.filename
        
        # Transcribe audio using the OpenAI Whisper API
        response = openai.Audio.translate(
            api_key=OPENAI_API_KEY,
            model="whisper-1",
            file=buffer
        )

        # Get the transcribed text from the API response
        transcribed_text = response["text"]
        
        print(transcribed_text)

        # Now, pass the transcribed text to the "generate_response" endpoint
        # res = await generate_response(transcribed_text)
        return transcribed_text