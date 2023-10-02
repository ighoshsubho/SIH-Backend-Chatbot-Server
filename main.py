import io
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException, status, UploadFile
from app import helpers
import os
import os.path
import openai
from pydub import AudioSegment
# from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

from app.helpers import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

app = FastAPI()
# handler = Mangum(app)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate/chat/",
          tags=["ChatBot Grievance"],
          description="Generate Response from Grievance Chatbot")
async def generate_response(text:str):
    try:
        res = helpers.chatbotQA(text)
        return {"response":res}
    except:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/api/generate/submit/",
          tags=["ChatBot Grievance"],
          description="Generate Response from Grievance Chatbot")
async def generate_response(text:str):
    try:
        res = helpers.chatbotQASubmit(text)
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
    # Read the blob data
    audio_blob = await audio_file.read()

    # Convert the blob data to an MP3 file (assuming it's in a compatible audio format)
    audio = AudioSegment.from_file(io.BytesIO(audio_blob), format="blob")

    # Create a buffer to hold the MP3 audio data
    buffer = io.BytesIO()
    audio.export(buffer, format="mp3")
    buffer.seek(0)
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

    return {"text":transcribed_text}