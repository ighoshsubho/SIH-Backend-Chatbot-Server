# SIH-Backend-Chatbot-Server
Backend chatbot server for SIH

### Run locally
`pip install -r requirements.txt`

### Set the env
`OPENAI_API_KEY=`

### Run the server
`uvicorn main:app --reload`

### Endpoint
`http://localhost/8000/api`

1. `/generate/chat` - Will generate you response based on grievance particularly it will be a chat endpoint
2. `/generate/submit` - Will generate you response in JSON format along with solution
3. `/index` - Will re create the index based on given text
4. `/token` - Will return token count for the text
5. `/transcribe` - Will transcribe the audio and pass it to the chatbot to query the index and return the result
