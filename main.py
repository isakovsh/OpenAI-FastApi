from fastapi import FastAPI
from pydantic import BaseModel
from functions import *
from dotenv import load_dotenv


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
def query(query: str):
    vector_store = get_vector_store()
    answer = get_retrieval_qa(query,vector_store)
    return {"answer": answer}

