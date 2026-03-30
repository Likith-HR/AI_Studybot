import os
import time
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
from langchain_groq import ChatGroq # For LLM Calling
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from datetime import datetime,timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
groq_api_key=os.getenv("Groq_api_key") #stores the api key present in the folder of .env
mongo_url=os.getenv("Mongo_url")

def connect_to_mongo():
    while True:
        try:
            client = MongoClient(
            mongo_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
            )
            client.admin.command('ping')  # force connection check
            print("✅ Connected to MongoDB")
            return client
        except ServerSelectionTimeoutError:
            print("⏳ MongoDB not ready, retrying in 5 seconds...")
            time.sleep(5)
client=connect_to_mongo()
db=client["AI_Chatbot"]
collection=db["users"]
app=FastAPI()

class ChatRequest(BaseModel):
	user_id:str
	question:str
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   
# Here * provided so that all systems could access api

prompt=ChatPromptTemplate.from_messages(
	[
		("system",
   		"""
		You are an AI tutor designed to help students with their academic learning. Always provide accurate, clear, and structured explanations of concepts. 
		- Act as a patient and supportive teacher who explains step by step. 
		- Focus exclusively on education-related queries (subjects, concepts, study strategies). 
		- Format answers using GitHub-flavored Markdown with headings, bullet points, tables, and LaTeX for math. 
		- Maintain a friendly, encouraging, and professional tone. 
		- Provide complete, contextual, and engaging responses that help students truly understand the material.
		"""),
		("placeholder","{history}"),
		("user","{question}")
	]
)
llm=ChatGroq(api_key=groq_api_key, model="openai/gpt-oss-20b")
chain=prompt|llm

user_id="user3445"
def get_history(user_id):
	chats=collection.find({"user_id":user_id}).sort("timestamp",1)
	history=[]
	for chat in chats:
		history.append((chat["role"],chat["message"]))
	return history

@app.get("/")
def home():
	return {"message": "Welcome to the world of curiosity."}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        history = get_history(request.user_id)
        res = chain.invoke({"history": history, "question": request.question})

        collection.insert_one({
            "user_id": request.user_id,
            "role": "user",
            "message": request.question,
            "timestamp": datetime.now(timezone.utc)
        })

        collection.insert_one({
            "user_id": request.user_id,
            "role": "assistant",
            "message": res.content,
            "timestamp": datetime.now(timezone.utc)
        })

        return {"response": res.content}

 except Exception as e:
            print("❌ Error:", e)
            time.sleep(5)
            return {"message": "Server is waking up, please wait a moment."}




