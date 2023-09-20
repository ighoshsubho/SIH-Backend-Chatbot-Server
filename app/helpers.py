import tiktoken
from langchain.llms import OpenAI
from llama_index import GPTVectorStoreIndex, PromptHelper, LLMPredictor, SimpleDirectoryReader
from llama_index import load_index_from_storage,StorageContext
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def ConstructIndex(directory_path):
  max_input_size = 4096
  max_outputs = 400
  max_chunk_overlap = 0.7
  max_size_limit = 400

  prompt_helper = PromptHelper(max_input_size,max_outputs,max_chunk_overlap,max_size_limit)
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=0,model_name="gpt-4",max_tokens=max_outputs))
  documents = SimpleDirectoryReader(directory_path).load_data()
  index = GPTVectorStoreIndex(documents,llm_predictor=llm_predictor,prompt_helper=prompt_helper)
  index.storage_context.persist(persist_dir="index.json")
  return index

def chatbotQA(text):
  index_context = StorageContext.from_defaults(persist_dir="app/index.json")
  print(index_context)
  index = load_index_from_storage(index_context).as_query_engine()
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