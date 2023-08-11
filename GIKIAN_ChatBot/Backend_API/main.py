from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
import sqlite3


#Import GIKIAN...
import os
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

#Scraped data
with open('./cleanScrape.txt') as f:
    documents = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 0,
    length_function = len,  )

texts = text_splitter.create_documents([documents])

len(texts)

# Embeddings
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

#Database storing

llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

chain = load_qa_chain(llm, chain_type="stuff")

def get_similar_documents(query):
    docs = db.similarity_search(query)
    return docs

def get_chatbot_response(question, docs):
    response = chain.run(input_documents=docs, question=question)
    return response

def insert_into_database(query, response):
    cursor.execute('INSERT INTO chatbot_history (query, chatbot_response) VALUES (?, ?)', (query, response))
    conn.commit()


# Connect to the SQLite database on Google Drive
database_path = "database.db"
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

print("Debugging")

from typing import List
from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: str
    content: str

@app.post("/api/chatbot")
async def chat_with_bot(message: ChatMessage):
    query = message.content
    relevant_docs = get_similar_documents(query)
    chatbot_response = get_chatbot_response(query, relevant_docs)
    insert_into_database(query, chatbot_response)

    return {"response": chatbot_response}

