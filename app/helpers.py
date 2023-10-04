import pinecone
import tiktoken
from llama_index.llms import OpenAI
from llama_index import GPTVectorStoreIndex, PromptHelper, LLMPredictor, SimpleDirectoryReader
from llama_index import load_index_from_storage,StorageContext
from llama_index.vector_stores import PineconeVectorStore
import openai
import os
import mimetypes
from dotenv import load_dotenv

load_dotenv()

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIORNMENT"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def is_valid_audio_file(filename):
  mime_type, _ = mimetypes.guess_type(filename)
  return mime_type in ['audio/mpeg', 'audio/wav']

def ConstructIndex(directory_path):
  max_input_size = 4096
  max_outputs = 400
  max_chunk_overlap = 0.7
  max_size_limit = 400

  pinecone.delete_index('grievance')
  pinecone.create_index("grievance", dimension=1536, metric="euclidean", pod_type="p1")

  prompt_helper = PromptHelper(max_input_size,max_outputs,max_chunk_overlap,max_size_limit)
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=0,model_name="gpt-4",max_tokens=max_outputs))
  documents = SimpleDirectoryReader(directory_path).load_data()

  pinecone_index = pinecone.Index("grievance")
  vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
  storage_context = StorageContext.from_defaults(vector_store=vector_store)

  index = GPTVectorStoreIndex(documents,llm_predictor=llm_predictor,prompt_helper=prompt_helper,storage_context=storage_context)

  return index

def chatbotQASubmit(text):
  # index_context = StorageContext.from_defaults(persist_dir="index.json")
  # print(index_context)
  vector_store = PineconeVectorStore(pinecone.Index("grievance"))
  index_context = GPTVectorStoreIndex.from_vector_store(vector_store=vector_store)
  index = index_context.as_query_engine()
  prompt = "You are a grievance adressing assistant."\
           "Your goal is to help users with their issues and grievances by providing proper solution like which department they should address and other problems."\
           "You can speak in Hindi, English, Bengali"\
           "Return only the department that the user can address in JSON format and the JSON should always contain department and how_can_they_help"\
           "If the user asks issue that is not relevant to a grievance, politely respond that you are unable to answer."
  
  query = prompt + text
  response = index.query(query)
  return response.response

def chatbotQA(text):
  # index_context = StorageContext.from_defaults(persist_dir="index.json")
  # print(index_context)
  vector_store = PineconeVectorStore(pinecone.Index("grievance"))
  index_context = GPTVectorStoreIndex.from_vector_store(vector_store=vector_store)
  index = index_context.as_query_engine()
  prompt = "You are a grievance adressing assistant."\
           "Your goal is to help users with their issues and grievances by providing proper solution like which department they should address and other problems."\
           "You can speak in Hindi, English, Bengali"
  
  query = prompt + text
  response = index.query(query)
  return response.response

MAX_MEMORY_TOKENS = 100
def count_tokens(text):
  encoding = tiktoken.encoding_for_model("gpt-4")
  return len(encoding.encode(text))

# index = ConstructIndex("../data_grieviance/")
# print(index)

# res = chatbotQA("How can I see my grievances?")
# print(res)